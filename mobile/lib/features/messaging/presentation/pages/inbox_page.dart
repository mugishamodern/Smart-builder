import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/features/messaging/providers/messaging_provider.dart';
import 'package:buildsmart_mobile/features/messaging/presentation/widgets/conversation_tile.dart';
import 'package:buildsmart_mobile/shared/widgets/common_widgets.dart';
import 'package:go_router/go_router.dart';

/// Inbox page displaying all conversations
class InboxPage extends ConsumerWidget {
  const InboxPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final conversationsAsync = ref.watch(conversationsProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Messages'),
        actions: [
          // Unread count badge
          Consumer(
            builder: (context, ref, child) {
              final unreadAsync = ref.watch(unreadCountProvider);
              return unreadAsync.when(
                data: (count) {
                  if (count > 0) {
                    return Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Badge(
                        label: Text(count.toString()),
                        child: const Icon(Icons.mail),
                      ),
                    );
                  }
                  return const Padding(
                    padding: EdgeInsets.all(16.0),
                    child: Icon(Icons.mail_outline),
                  );
                },
                loading: () => const Padding(
                  padding: EdgeInsets.all(16.0),
                  child: Icon(Icons.mail_outline),
                ),
                error: (_, __) => const Padding(
                  padding: EdgeInsets.all(16.0),
                  child: Icon(Icons.mail_outline),
                ),
              );
            },
          ),
        ],
      ),
      body: conversationsAsync.when(
        data: (conversations) {
          if (conversations.isEmpty) {
            return EmptyState(
              icon: Icons.message_outlined,
              title: 'No conversations yet',
              message: 'Start a conversation by messaging a user',
            );
          }

          return RefreshIndicator(
            onRefresh: () async {
              ref.invalidate(conversationsProvider);
              ref.invalidate(unreadCountProvider);
            },
            child: ListView.builder(
              itemCount: conversations.length,
              itemBuilder: (context, index) {
                final conversation = conversations[index];
                return ConversationTile(
                  conversation: conversation,
                  onTap: () {
                    // Navigate to chat page
                    // Need to determine the other user ID
                    final currentUserId = 0; // TODO: Get from auth provider
                    final otherUserId = conversation.participant1Id == currentUserId
                        ? conversation.participant2Id
                        : conversation.participant1Id;
                    
                    context.push('/messages/$otherUserId');
                  },
                );
              },
            ),
          );
        },
        loading: () => const LoadingState(),
        error: (error, stack) => ErrorState(
          message: error.toString(),
          onRetry: () => ref.invalidate(conversationsProvider),
        ),
      ),
    );
  }
}
