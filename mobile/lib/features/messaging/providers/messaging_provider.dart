import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/core/models/models.dart';
import 'package:buildsmart_mobile/features/messaging/data/repositories/messaging_repository.dart';

/// Messaging repository provider
final messagingRepositoryProvider = Provider<MessagingRepository>((ref) {
  return MessagingRepository();
});

/// Conversations provider
final conversationsProvider = FutureProvider<List<ConversationModel>>((ref) async {
  final repository = ref.watch(messagingRepositoryProvider);
  return await repository.getConversations();
});

/// Conversation messages provider
final conversationMessagesProvider = FutureProvider.family<List<MessageModel>, int>((ref, userId) async {
  final repository = ref.watch(messagingRepositoryProvider);
  return await repository.getConversationMessages(userId);
});

/// Unread count provider
final unreadCountProvider = FutureProvider<int>((ref) async {
  final repository = ref.watch(messagingRepositoryProvider);
  return await repository.getUnreadCount();
});

/// Send message notifier
final sendMessageNotifierProvider = StateNotifierProvider<SendMessageNotifier, AsyncValue<MessageModel?>>((ref) {
  final repository = ref.watch(messagingRepositoryProvider);
  return SendMessageNotifier(repository, ref);
});

class SendMessageNotifier extends StateNotifier<AsyncValue<MessageModel?>> {
  final MessagingRepository _repository;
  final Ref _ref;

  SendMessageNotifier(this._repository, this._ref) : super(const AsyncValue.data(null));

  Future<void> sendMessage({required int receiverId, required String content}) async {
    state = const AsyncValue.loading();
    try {
      final message = await _repository.sendMessage(
        receiverId: receiverId,
        content: content,
      );
      state = AsyncValue.data(message);
      
      // Invalidate conversations and messages to refresh
      _ref.invalidate(conversationsProvider);
      _ref.invalidate(conversationMessagesProvider(receiverId));
      _ref.invalidate(unreadCountProvider);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  void reset() {
    state = const AsyncValue.data(null);
  }
}

/// Mark message as read notifier
final markAsReadNotifierProvider = StateNotifierProvider<MarkAsReadNotifier, AsyncValue<void>>((ref) {
  final repository = ref.watch(messagingRepositoryProvider);
  return MarkAsReadNotifier(repository, ref);
});

class MarkAsReadNotifier extends StateNotifier<AsyncValue<void>> {
  final MessagingRepository _repository;
  final Ref _ref;

  MarkAsReadNotifier(this._repository, this._ref) : super(const AsyncValue.data(null));

  Future<void> markAsRead(int messageId) async {
    state = const AsyncValue.loading();
    try {
      await _repository.markAsRead(messageId);
      state = const AsyncValue.data(null);
      
      // Invalidate conversations and unread count to refresh
      _ref.invalidate(conversationsProvider);
      _ref.invalidate(unreadCountProvider);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }
}
