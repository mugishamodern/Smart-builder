import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/core/models/models.dart';
import 'package:buildsmart_mobile/core/sockets/socket_service.dart';
import 'package:buildsmart_mobile/features/messaging/providers/messaging_provider.dart';
import 'package:buildsmart_mobile/features/messaging/presentation/widgets/message_bubble.dart';
import 'package:buildsmart_mobile/shared/widgets/common_widgets.dart';
import 'dart:async';

/// Chat page for conversation with a specific user
class ChatPage extends ConsumerStatefulWidget {
  final int userId;

  const ChatPage({
    super.key,
    required this.userId,
  });

  @override
  ConsumerState<ChatPage> createState() => _ChatPageState();
}

class _ChatPageState extends ConsumerState<ChatPage> {
  final TextEditingController _messageController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final SocketService _socketService = SocketService.instance;
  StreamSubscription? _messageSubscription;
  List<MessageModel> _messages = [];
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _setupSocket();
  }

  void _setupSocket() {
    // Connect socket if not already connected
    // TODO: Get current user ID from auth provider
    final currentUserId = 0;
    _socketService.connect(userId: currentUserId);

    // Join conversation room
    _socketService.joinConversation(
      userId: currentUserId,
      otherUserId: widget.userId,
    );

    // Listen for new messages
    _messageSubscription = _socketService.messageStream.listen((data) {
      if (data['sender_id'] == widget.userId || data['receiver_id'] == widget.userId) {
        setState(() {
          _messages.add(MessageModel.fromJson(data));
        });
        _scrollToBottom();
      }
    });
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  Future<void> _sendMessage() async {
    final content = _messageController.text.trim();
    if (content.isEmpty) return;

    setState(() {
      _isLoading = true;
    });

    try {
      final notifier = ref.read(sendMessageNotifierProvider.notifier);
      await notifier.sendMessage(
        receiverId: widget.userId,
        content: content,
      );

      _messageController.clear();

      // Refresh messages
      ref.invalidate(conversationMessagesProvider(widget.userId));
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to send message: $e')),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  void dispose() {
    _messageController.dispose();
    _scrollController.dispose();
    _messageSubscription?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // TODO: Get user info for app bar
    final messagesAsync = ref.watch(conversationMessagesProvider(widget.userId));

    return Scaffold(
      appBar: AppBar(
        title: const Text('Chat'), // TODO: Show user name
      ),
      body: Column(
        children: [
          // Messages list
          Expanded(
            child: messagesAsync.when(
              data: (messages) {
                _messages = messages;
                _scrollToBottom();

                if (messages.isEmpty) {
                  return const Center(
                    child: Text('No messages yet. Start the conversation!'),
                  );
                }

                return ListView.builder(
                  controller: _scrollController,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  itemCount: messages.length,
                  itemBuilder: (context, index) {
                    final message = messages[index];
                    // TODO: Get current user ID from auth provider
                    final currentUserId = 0;
                    final isCurrentUser = message.senderId == currentUserId;

                    return MessageBubble(
                      message: message,
                      isCurrentUser: isCurrentUser,
                    );
                  },
                );
              },
              loading: () => const LoadingState(),
              error: (error, stack) => ErrorState(
                message: error.toString(),
                onRetry: () => ref.invalidate(conversationMessagesProvider(widget.userId)),
              ),
            ),
          ),

          // Message input
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            decoration: BoxDecoration(
              color: Theme.of(context).scaffoldBackgroundColor,
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.1),
                  blurRadius: 4,
                  offset: const Offset(0, -2),
                ),
              ],
            ),
            child: SafeArea(
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _messageController,
                      decoration: InputDecoration(
                        hintText: 'Type a message...',
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(24),
                        ),
                        contentPadding: const EdgeInsets.symmetric(
                          horizontal: 16,
                          vertical: 10,
                        ),
                      ),
                      maxLines: null,
                      textCapitalization: TextCapitalization.sentences,
                      onSubmitted: (_) => _sendMessage(),
                    ),
                  ),
                  const SizedBox(width: 8),
                  IconButton(
                    onPressed: _isLoading ? null : _sendMessage,
                    icon: _isLoading
                        ? const SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          )
                        : const Icon(Icons.send),
                    color: Theme.of(context).colorScheme.primary,
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
