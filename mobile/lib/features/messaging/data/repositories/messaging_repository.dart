import 'package:dio/dio.dart';
import 'package:buildsmart_mobile/core/http/api_client.dart';
import 'package:buildsmart_mobile/core/constants/api_endpoints.dart';
import 'package:buildsmart_mobile/core/models/models.dart';

/// Messaging repository for handling messages and conversations
class MessagingRepository {
  final ApiClient _apiClient;

  MessagingRepository({ApiClient? apiClient})
      : _apiClient = apiClient ?? ApiClient.instance;

  /// Send a message
  Future<MessageModel> sendMessage({
    required int receiverId,
    required String content,
  }) async {
    try {
      final response = await _apiClient.post(
        ApiEndpoints.messagesSend,
        data: {
          'receiver_id': receiverId,
          'content': content,
        },
      );

      if (response.statusCode == 200 && response.data['success'] == true) {
        return MessageModel.fromJson(response.data['message']);
      }
      throw Exception(response.data['message'] ?? 'Failed to send message');
    } on DioException catch (e) {
      throw Exception(e.response?.data['message'] ?? 'Failed to send message');
    }
  }

  /// Get all conversations for current user
  Future<List<ConversationModel>> getConversations() async {
    try {
      final response = await _apiClient.get(
        ApiEndpoints.messagesConversations,
      );

      if (response.statusCode == 200 && response.data['success'] == true) {
        final List<dynamic> conversationsData = response.data['conversations'] ?? [];
        return conversationsData
            .map((json) => ConversationModel.fromJson(json))
            .toList();
      }
      return [];
    } on DioException catch (e) {
      throw Exception(e.response?.data['message'] ?? 'Failed to fetch conversations');
    }
  }

  /// Get messages for a conversation with a specific user
  Future<List<MessageModel>> getConversationMessages(int userId) async {
    try {
      final response = await _apiClient.get(
        '${ApiEndpoints.messagesConversation}/$userId',
      );

      if (response.statusCode == 200 && response.data['success'] == true) {
        final List<dynamic> messagesData = response.data['messages'] ?? [];
        return messagesData
            .map((json) => MessageModel.fromJson(json))
            .toList();
      }
      return [];
    } on DioException catch (e) {
      throw Exception(e.response?.data['message'] ?? 'Failed to fetch messages');
    }
  }

  /// Get unread message count
  Future<int> getUnreadCount() async {
    try {
      final response = await _apiClient.get(
        ApiEndpoints.messagesUnreadCount,
      );

      if (response.statusCode == 200 && response.data['success'] == true) {
        return response.data['unread_count'] ?? 0;
      }
      return 0;
    } on DioException {
      return 0;
    }
  }

  /// Mark a message as read
  Future<void> markAsRead(int messageId) async {
    try {
      await _apiClient.put(
        '${ApiEndpoints.messagesMarkRead}/$messageId/read',
      );
    } on DioException catch (e) {
      throw Exception(e.response?.data['message'] ?? 'Failed to mark message as read');
    }
  }
}
