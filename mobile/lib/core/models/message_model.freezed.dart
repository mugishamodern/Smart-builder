// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'message_model.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

MessageModel _$MessageModelFromJson(Map<String, dynamic> json) {
  return _MessageModel.fromJson(json);
}

/// @nodoc
mixin _$MessageModel {
  @JsonKey(fromJson: _intFromJson)
  int get id => throw _privateConstructorUsedError;
  @JsonKey(name: 'sender_id', fromJson: _intFromJson)
  int get senderId => throw _privateConstructorUsedError;
  @JsonKey(name: 'receiver_id', fromJson: _intFromJson)
  int get receiverId => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _stringFromJson)
  String get content => throw _privateConstructorUsedError;
  @JsonKey(name: 'is_read', defaultValue: false)
  bool get isRead => throw _privateConstructorUsedError;
  @JsonKey(name: 'timestamp')
  DateTime? get timestamp => throw _privateConstructorUsedError; // Nested user info (when fetched with details)
  @JsonKey(fromJson: _senderFromJson)
  UserModel? get sender => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _receiverFromJson)
  UserModel? get receiver => throw _privateConstructorUsedError;

  /// Serializes this MessageModel to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of MessageModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $MessageModelCopyWith<MessageModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $MessageModelCopyWith<$Res> {
  factory $MessageModelCopyWith(
    MessageModel value,
    $Res Function(MessageModel) then,
  ) = _$MessageModelCopyWithImpl<$Res, MessageModel>;
  @useResult
  $Res call({
    @JsonKey(fromJson: _intFromJson) int id,
    @JsonKey(name: 'sender_id', fromJson: _intFromJson) int senderId,
    @JsonKey(name: 'receiver_id', fromJson: _intFromJson) int receiverId,
    @JsonKey(fromJson: _stringFromJson) String content,
    @JsonKey(name: 'is_read', defaultValue: false) bool isRead,
    @JsonKey(name: 'timestamp') DateTime? timestamp,
    @JsonKey(fromJson: _senderFromJson) UserModel? sender,
    @JsonKey(fromJson: _receiverFromJson) UserModel? receiver,
  });

  $UserModelCopyWith<$Res>? get sender;
  $UserModelCopyWith<$Res>? get receiver;
}

/// @nodoc
class _$MessageModelCopyWithImpl<$Res, $Val extends MessageModel>
    implements $MessageModelCopyWith<$Res> {
  _$MessageModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of MessageModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? senderId = null,
    Object? receiverId = null,
    Object? content = null,
    Object? isRead = null,
    Object? timestamp = freezed,
    Object? sender = freezed,
    Object? receiver = freezed,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as int,
            senderId: null == senderId
                ? _value.senderId
                : senderId // ignore: cast_nullable_to_non_nullable
                      as int,
            receiverId: null == receiverId
                ? _value.receiverId
                : receiverId // ignore: cast_nullable_to_non_nullable
                      as int,
            content: null == content
                ? _value.content
                : content // ignore: cast_nullable_to_non_nullable
                      as String,
            isRead: null == isRead
                ? _value.isRead
                : isRead // ignore: cast_nullable_to_non_nullable
                      as bool,
            timestamp: freezed == timestamp
                ? _value.timestamp
                : timestamp // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            sender: freezed == sender
                ? _value.sender
                : sender // ignore: cast_nullable_to_non_nullable
                      as UserModel?,
            receiver: freezed == receiver
                ? _value.receiver
                : receiver // ignore: cast_nullable_to_non_nullable
                      as UserModel?,
          )
          as $Val,
    );
  }

  /// Create a copy of MessageModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $UserModelCopyWith<$Res>? get sender {
    if (_value.sender == null) {
      return null;
    }

    return $UserModelCopyWith<$Res>(_value.sender!, (value) {
      return _then(_value.copyWith(sender: value) as $Val);
    });
  }

  /// Create a copy of MessageModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $UserModelCopyWith<$Res>? get receiver {
    if (_value.receiver == null) {
      return null;
    }

    return $UserModelCopyWith<$Res>(_value.receiver!, (value) {
      return _then(_value.copyWith(receiver: value) as $Val);
    });
  }
}

/// @nodoc
abstract class _$$MessageModelImplCopyWith<$Res>
    implements $MessageModelCopyWith<$Res> {
  factory _$$MessageModelImplCopyWith(
    _$MessageModelImpl value,
    $Res Function(_$MessageModelImpl) then,
  ) = __$$MessageModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    @JsonKey(fromJson: _intFromJson) int id,
    @JsonKey(name: 'sender_id', fromJson: _intFromJson) int senderId,
    @JsonKey(name: 'receiver_id', fromJson: _intFromJson) int receiverId,
    @JsonKey(fromJson: _stringFromJson) String content,
    @JsonKey(name: 'is_read', defaultValue: false) bool isRead,
    @JsonKey(name: 'timestamp') DateTime? timestamp,
    @JsonKey(fromJson: _senderFromJson) UserModel? sender,
    @JsonKey(fromJson: _receiverFromJson) UserModel? receiver,
  });

  @override
  $UserModelCopyWith<$Res>? get sender;
  @override
  $UserModelCopyWith<$Res>? get receiver;
}

/// @nodoc
class __$$MessageModelImplCopyWithImpl<$Res>
    extends _$MessageModelCopyWithImpl<$Res, _$MessageModelImpl>
    implements _$$MessageModelImplCopyWith<$Res> {
  __$$MessageModelImplCopyWithImpl(
    _$MessageModelImpl _value,
    $Res Function(_$MessageModelImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of MessageModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? senderId = null,
    Object? receiverId = null,
    Object? content = null,
    Object? isRead = null,
    Object? timestamp = freezed,
    Object? sender = freezed,
    Object? receiver = freezed,
  }) {
    return _then(
      _$MessageModelImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as int,
        senderId: null == senderId
            ? _value.senderId
            : senderId // ignore: cast_nullable_to_non_nullable
                  as int,
        receiverId: null == receiverId
            ? _value.receiverId
            : receiverId // ignore: cast_nullable_to_non_nullable
                  as int,
        content: null == content
            ? _value.content
            : content // ignore: cast_nullable_to_non_nullable
                  as String,
        isRead: null == isRead
            ? _value.isRead
            : isRead // ignore: cast_nullable_to_non_nullable
                  as bool,
        timestamp: freezed == timestamp
            ? _value.timestamp
            : timestamp // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        sender: freezed == sender
            ? _value.sender
            : sender // ignore: cast_nullable_to_non_nullable
                  as UserModel?,
        receiver: freezed == receiver
            ? _value.receiver
            : receiver // ignore: cast_nullable_to_non_nullable
                  as UserModel?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$MessageModelImpl implements _MessageModel {
  const _$MessageModelImpl({
    @JsonKey(fromJson: _intFromJson) required this.id,
    @JsonKey(name: 'sender_id', fromJson: _intFromJson) required this.senderId,
    @JsonKey(name: 'receiver_id', fromJson: _intFromJson)
    required this.receiverId,
    @JsonKey(fromJson: _stringFromJson) required this.content,
    @JsonKey(name: 'is_read', defaultValue: false) this.isRead = false,
    @JsonKey(name: 'timestamp') this.timestamp,
    @JsonKey(fromJson: _senderFromJson) this.sender,
    @JsonKey(fromJson: _receiverFromJson) this.receiver,
  });

  factory _$MessageModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$MessageModelImplFromJson(json);

  @override
  @JsonKey(fromJson: _intFromJson)
  final int id;
  @override
  @JsonKey(name: 'sender_id', fromJson: _intFromJson)
  final int senderId;
  @override
  @JsonKey(name: 'receiver_id', fromJson: _intFromJson)
  final int receiverId;
  @override
  @JsonKey(fromJson: _stringFromJson)
  final String content;
  @override
  @JsonKey(name: 'is_read', defaultValue: false)
  final bool isRead;
  @override
  @JsonKey(name: 'timestamp')
  final DateTime? timestamp;
  // Nested user info (when fetched with details)
  @override
  @JsonKey(fromJson: _senderFromJson)
  final UserModel? sender;
  @override
  @JsonKey(fromJson: _receiverFromJson)
  final UserModel? receiver;

  @override
  String toString() {
    return 'MessageModel(id: $id, senderId: $senderId, receiverId: $receiverId, content: $content, isRead: $isRead, timestamp: $timestamp, sender: $sender, receiver: $receiver)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$MessageModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.senderId, senderId) ||
                other.senderId == senderId) &&
            (identical(other.receiverId, receiverId) ||
                other.receiverId == receiverId) &&
            (identical(other.content, content) || other.content == content) &&
            (identical(other.isRead, isRead) || other.isRead == isRead) &&
            (identical(other.timestamp, timestamp) ||
                other.timestamp == timestamp) &&
            (identical(other.sender, sender) || other.sender == sender) &&
            (identical(other.receiver, receiver) ||
                other.receiver == receiver));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    senderId,
    receiverId,
    content,
    isRead,
    timestamp,
    sender,
    receiver,
  );

  /// Create a copy of MessageModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$MessageModelImplCopyWith<_$MessageModelImpl> get copyWith =>
      __$$MessageModelImplCopyWithImpl<_$MessageModelImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$MessageModelImplToJson(this);
  }
}

abstract class _MessageModel implements MessageModel {
  const factory _MessageModel({
    @JsonKey(fromJson: _intFromJson) required final int id,
    @JsonKey(name: 'sender_id', fromJson: _intFromJson)
    required final int senderId,
    @JsonKey(name: 'receiver_id', fromJson: _intFromJson)
    required final int receiverId,
    @JsonKey(fromJson: _stringFromJson) required final String content,
    @JsonKey(name: 'is_read', defaultValue: false) final bool isRead,
    @JsonKey(name: 'timestamp') final DateTime? timestamp,
    @JsonKey(fromJson: _senderFromJson) final UserModel? sender,
    @JsonKey(fromJson: _receiverFromJson) final UserModel? receiver,
  }) = _$MessageModelImpl;

  factory _MessageModel.fromJson(Map<String, dynamic> json) =
      _$MessageModelImpl.fromJson;

  @override
  @JsonKey(fromJson: _intFromJson)
  int get id;
  @override
  @JsonKey(name: 'sender_id', fromJson: _intFromJson)
  int get senderId;
  @override
  @JsonKey(name: 'receiver_id', fromJson: _intFromJson)
  int get receiverId;
  @override
  @JsonKey(fromJson: _stringFromJson)
  String get content;
  @override
  @JsonKey(name: 'is_read', defaultValue: false)
  bool get isRead;
  @override
  @JsonKey(name: 'timestamp')
  DateTime? get timestamp; // Nested user info (when fetched with details)
  @override
  @JsonKey(fromJson: _senderFromJson)
  UserModel? get sender;
  @override
  @JsonKey(fromJson: _receiverFromJson)
  UserModel? get receiver;

  /// Create a copy of MessageModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$MessageModelImplCopyWith<_$MessageModelImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
