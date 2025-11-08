import 'package:freezed_annotation/freezed_annotation.dart';
import 'user_model.dart';
import 'message_model.dart';

part 'conversation_model.freezed.dart';
part 'conversation_model.g.dart';

/// Conversation model matching Flask Conversation model
@freezed
class ConversationModel with _$ConversationModel {
  const factory ConversationModel({
    @JsonKey(fromJson: _intFromJson) required int id,
    @JsonKey(name: 'participant_1_id', fromJson: _intFromJson) required int participant1Id,
    @JsonKey(name: 'participant_2_id', fromJson: _intFromJson) required int participant2Id,
    @JsonKey(name: 'last_message_at') DateTime? lastMessageAt,
    @JsonKey(name: 'last_message_preview', fromJson: _stringFromJsonNullable) String? lastMessagePreview,
    @JsonKey(name: 'unread_count', defaultValue: 0) @Default(0) int unreadCount,
    // Nested participants info (when fetched with details)
    @JsonKey(fromJson: _participant1FromJson) UserModel? participant1,
    @JsonKey(fromJson: _participant2FromJson) UserModel? participant2,
    // Last message details
    @JsonKey(fromJson: _lastMessageFromJson) MessageModel? lastMessage,
  }) = _ConversationModel;

  factory ConversationModel.fromJson(Map<String, dynamic> json) =>
      _$ConversationModelFromJson(json);
}

/// Helper function to convert int from JSON
int _intFromJson(dynamic value) {
  if (value == null) return 0;
  if (value is int) return value;
  if (value is String) return int.tryParse(value) ?? 0;
  return 0;
}

/// Helper function to convert string from JSON (nullable)
String? _stringFromJsonNullable(dynamic value) {
  if (value == null) return null;
  return value.toString();
}

/// Helper function to convert participant1 from JSON
UserModel? _participant1FromJson(dynamic value) {
  if (value == null) return null;
  if (value is Map) {
    try {
      return UserModel.fromJson(Map<String, dynamic>.from(value));
    } catch (e) {
      return null;
    }
  }
  return null;
}

/// Helper function to convert participant2 from JSON
UserModel? _participant2FromJson(dynamic value) {
  if (value == null) return null;
  if (value is Map) {
    try {
      return UserModel.fromJson(Map<String, dynamic>.from(value));
    } catch (e) {
      return null;
    }
  }
  return null;
}

/// Helper function to convert last message from JSON
MessageModel? _lastMessageFromJson(dynamic value) {
  if (value == null) return null;
  if (value is Map) {
    try {
      return MessageModel.fromJson(Map<String, dynamic>.from(value));
    } catch (e) {
      return null;
    }
  }
  return null;
}
