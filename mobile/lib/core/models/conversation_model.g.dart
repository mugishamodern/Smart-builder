// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'conversation_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$ConversationModelImpl _$$ConversationModelImplFromJson(
  Map<String, dynamic> json,
) => _$ConversationModelImpl(
  id: _intFromJson(json['id']),
  participant1Id: _intFromJson(json['participant_1_id']),
  participant2Id: _intFromJson(json['participant_2_id']),
  lastMessageAt: json['last_message_at'] == null
      ? null
      : DateTime.parse(json['last_message_at'] as String),
  lastMessagePreview: _stringFromJsonNullable(json['last_message_preview']),
  unreadCount: (json['unread_count'] as num?)?.toInt() ?? 0,
  participant1: _participant1FromJson(json['participant1']),
  participant2: _participant2FromJson(json['participant2']),
  lastMessage: _lastMessageFromJson(json['lastMessage']),
);

Map<String, dynamic> _$$ConversationModelImplToJson(
  _$ConversationModelImpl instance,
) => <String, dynamic>{
  'id': instance.id,
  'participant_1_id': instance.participant1Id,
  'participant_2_id': instance.participant2Id,
  'last_message_at': instance.lastMessageAt?.toIso8601String(),
  'last_message_preview': instance.lastMessagePreview,
  'unread_count': instance.unreadCount,
  'participant1': instance.participant1,
  'participant2': instance.participant2,
  'lastMessage': instance.lastMessage,
};
