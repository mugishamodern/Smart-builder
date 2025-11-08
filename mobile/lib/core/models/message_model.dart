import 'package:freezed_annotation/freezed_annotation.dart';
import 'user_model.dart';

part 'message_model.freezed.dart';
part 'message_model.g.dart';

/// Message model matching Flask Message model
@freezed
class MessageModel with _$MessageModel {
  const factory MessageModel({
    @JsonKey(fromJson: _intFromJson) required int id,
    @JsonKey(name: 'sender_id', fromJson: _intFromJson) required int senderId,
    @JsonKey(name: 'receiver_id', fromJson: _intFromJson) required int receiverId,
    @JsonKey(fromJson: _stringFromJson) required String content,
    @JsonKey(name: 'is_read', defaultValue: false) @Default(false) bool isRead,
    @JsonKey(name: 'timestamp') DateTime? timestamp,
    // Nested user info (when fetched with details)
    @JsonKey(fromJson: _senderFromJson) UserModel? sender,
    @JsonKey(fromJson: _receiverFromJson) UserModel? receiver,
  }) = _MessageModel;

  factory MessageModel.fromJson(Map<String, dynamic> json) =>
      _$MessageModelFromJson(json);
}

/// Helper function to convert int from JSON
int _intFromJson(dynamic value) {
  if (value == null) return 0;
  if (value is int) return value;
  if (value is String) return int.tryParse(value) ?? 0;
  return 0;
}

/// Helper function to convert string from JSON
String _stringFromJson(dynamic value) {
  if (value == null) return '';
  return value.toString();
}

/// Helper function to convert sender from JSON
UserModel? _senderFromJson(dynamic value) {
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

/// Helper function to convert receiver from JSON
UserModel? _receiverFromJson(dynamic value) {
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
