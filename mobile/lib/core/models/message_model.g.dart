// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'message_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$MessageModelImpl _$$MessageModelImplFromJson(Map<String, dynamic> json) =>
    _$MessageModelImpl(
      id: _intFromJson(json['id']),
      senderId: _intFromJson(json['sender_id']),
      receiverId: _intFromJson(json['receiver_id']),
      content: _stringFromJson(json['content']),
      isRead: json['is_read'] as bool? ?? false,
      timestamp: json['timestamp'] == null
          ? null
          : DateTime.parse(json['timestamp'] as String),
      sender: _senderFromJson(json['sender']),
      receiver: _receiverFromJson(json['receiver']),
    );

Map<String, dynamic> _$$MessageModelImplToJson(_$MessageModelImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'sender_id': instance.senderId,
      'receiver_id': instance.receiverId,
      'content': instance.content,
      'is_read': instance.isRead,
      'timestamp': instance.timestamp?.toIso8601String(),
      'sender': instance.sender,
      'receiver': instance.receiver,
    };
