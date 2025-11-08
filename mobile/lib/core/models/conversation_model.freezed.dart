// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'conversation_model.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

ConversationModel _$ConversationModelFromJson(Map<String, dynamic> json) {
  return _ConversationModel.fromJson(json);
}

/// @nodoc
mixin _$ConversationModel {
  @JsonKey(fromJson: _intFromJson)
  int get id => throw _privateConstructorUsedError;
  @JsonKey(name: 'participant_1_id', fromJson: _intFromJson)
  int get participant1Id => throw _privateConstructorUsedError;
  @JsonKey(name: 'participant_2_id', fromJson: _intFromJson)
  int get participant2Id => throw _privateConstructorUsedError;
  @JsonKey(name: 'last_message_at')
  DateTime? get lastMessageAt => throw _privateConstructorUsedError;
  @JsonKey(name: 'last_message_preview', fromJson: _stringFromJsonNullable)
  String? get lastMessagePreview => throw _privateConstructorUsedError;
  @JsonKey(name: 'unread_count', defaultValue: 0)
  int get unreadCount => throw _privateConstructorUsedError; // Nested participants info (when fetched with details)
  @JsonKey(fromJson: _participant1FromJson)
  UserModel? get participant1 => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _participant2FromJson)
  UserModel? get participant2 => throw _privateConstructorUsedError; // Last message details
  @JsonKey(fromJson: _lastMessageFromJson)
  MessageModel? get lastMessage => throw _privateConstructorUsedError;

  /// Serializes this ConversationModel to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of ConversationModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $ConversationModelCopyWith<ConversationModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $ConversationModelCopyWith<$Res> {
  factory $ConversationModelCopyWith(
    ConversationModel value,
    $Res Function(ConversationModel) then,
  ) = _$ConversationModelCopyWithImpl<$Res, ConversationModel>;
  @useResult
  $Res call({
    @JsonKey(fromJson: _intFromJson) int id,
    @JsonKey(name: 'participant_1_id', fromJson: _intFromJson)
    int participant1Id,
    @JsonKey(name: 'participant_2_id', fromJson: _intFromJson)
    int participant2Id,
    @JsonKey(name: 'last_message_at') DateTime? lastMessageAt,
    @JsonKey(name: 'last_message_preview', fromJson: _stringFromJsonNullable)
    String? lastMessagePreview,
    @JsonKey(name: 'unread_count', defaultValue: 0) int unreadCount,
    @JsonKey(fromJson: _participant1FromJson) UserModel? participant1,
    @JsonKey(fromJson: _participant2FromJson) UserModel? participant2,
    @JsonKey(fromJson: _lastMessageFromJson) MessageModel? lastMessage,
  });

  $UserModelCopyWith<$Res>? get participant1;
  $UserModelCopyWith<$Res>? get participant2;
  $MessageModelCopyWith<$Res>? get lastMessage;
}

/// @nodoc
class _$ConversationModelCopyWithImpl<$Res, $Val extends ConversationModel>
    implements $ConversationModelCopyWith<$Res> {
  _$ConversationModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of ConversationModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? participant1Id = null,
    Object? participant2Id = null,
    Object? lastMessageAt = freezed,
    Object? lastMessagePreview = freezed,
    Object? unreadCount = null,
    Object? participant1 = freezed,
    Object? participant2 = freezed,
    Object? lastMessage = freezed,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as int,
            participant1Id: null == participant1Id
                ? _value.participant1Id
                : participant1Id // ignore: cast_nullable_to_non_nullable
                      as int,
            participant2Id: null == participant2Id
                ? _value.participant2Id
                : participant2Id // ignore: cast_nullable_to_non_nullable
                      as int,
            lastMessageAt: freezed == lastMessageAt
                ? _value.lastMessageAt
                : lastMessageAt // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            lastMessagePreview: freezed == lastMessagePreview
                ? _value.lastMessagePreview
                : lastMessagePreview // ignore: cast_nullable_to_non_nullable
                      as String?,
            unreadCount: null == unreadCount
                ? _value.unreadCount
                : unreadCount // ignore: cast_nullable_to_non_nullable
                      as int,
            participant1: freezed == participant1
                ? _value.participant1
                : participant1 // ignore: cast_nullable_to_non_nullable
                      as UserModel?,
            participant2: freezed == participant2
                ? _value.participant2
                : participant2 // ignore: cast_nullable_to_non_nullable
                      as UserModel?,
            lastMessage: freezed == lastMessage
                ? _value.lastMessage
                : lastMessage // ignore: cast_nullable_to_non_nullable
                      as MessageModel?,
          )
          as $Val,
    );
  }

  /// Create a copy of ConversationModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $UserModelCopyWith<$Res>? get participant1 {
    if (_value.participant1 == null) {
      return null;
    }

    return $UserModelCopyWith<$Res>(_value.participant1!, (value) {
      return _then(_value.copyWith(participant1: value) as $Val);
    });
  }

  /// Create a copy of ConversationModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $UserModelCopyWith<$Res>? get participant2 {
    if (_value.participant2 == null) {
      return null;
    }

    return $UserModelCopyWith<$Res>(_value.participant2!, (value) {
      return _then(_value.copyWith(participant2: value) as $Val);
    });
  }

  /// Create a copy of ConversationModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $MessageModelCopyWith<$Res>? get lastMessage {
    if (_value.lastMessage == null) {
      return null;
    }

    return $MessageModelCopyWith<$Res>(_value.lastMessage!, (value) {
      return _then(_value.copyWith(lastMessage: value) as $Val);
    });
  }
}

/// @nodoc
abstract class _$$ConversationModelImplCopyWith<$Res>
    implements $ConversationModelCopyWith<$Res> {
  factory _$$ConversationModelImplCopyWith(
    _$ConversationModelImpl value,
    $Res Function(_$ConversationModelImpl) then,
  ) = __$$ConversationModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    @JsonKey(fromJson: _intFromJson) int id,
    @JsonKey(name: 'participant_1_id', fromJson: _intFromJson)
    int participant1Id,
    @JsonKey(name: 'participant_2_id', fromJson: _intFromJson)
    int participant2Id,
    @JsonKey(name: 'last_message_at') DateTime? lastMessageAt,
    @JsonKey(name: 'last_message_preview', fromJson: _stringFromJsonNullable)
    String? lastMessagePreview,
    @JsonKey(name: 'unread_count', defaultValue: 0) int unreadCount,
    @JsonKey(fromJson: _participant1FromJson) UserModel? participant1,
    @JsonKey(fromJson: _participant2FromJson) UserModel? participant2,
    @JsonKey(fromJson: _lastMessageFromJson) MessageModel? lastMessage,
  });

  @override
  $UserModelCopyWith<$Res>? get participant1;
  @override
  $UserModelCopyWith<$Res>? get participant2;
  @override
  $MessageModelCopyWith<$Res>? get lastMessage;
}

/// @nodoc
class __$$ConversationModelImplCopyWithImpl<$Res>
    extends _$ConversationModelCopyWithImpl<$Res, _$ConversationModelImpl>
    implements _$$ConversationModelImplCopyWith<$Res> {
  __$$ConversationModelImplCopyWithImpl(
    _$ConversationModelImpl _value,
    $Res Function(_$ConversationModelImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of ConversationModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? participant1Id = null,
    Object? participant2Id = null,
    Object? lastMessageAt = freezed,
    Object? lastMessagePreview = freezed,
    Object? unreadCount = null,
    Object? participant1 = freezed,
    Object? participant2 = freezed,
    Object? lastMessage = freezed,
  }) {
    return _then(
      _$ConversationModelImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as int,
        participant1Id: null == participant1Id
            ? _value.participant1Id
            : participant1Id // ignore: cast_nullable_to_non_nullable
                  as int,
        participant2Id: null == participant2Id
            ? _value.participant2Id
            : participant2Id // ignore: cast_nullable_to_non_nullable
                  as int,
        lastMessageAt: freezed == lastMessageAt
            ? _value.lastMessageAt
            : lastMessageAt // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        lastMessagePreview: freezed == lastMessagePreview
            ? _value.lastMessagePreview
            : lastMessagePreview // ignore: cast_nullable_to_non_nullable
                  as String?,
        unreadCount: null == unreadCount
            ? _value.unreadCount
            : unreadCount // ignore: cast_nullable_to_non_nullable
                  as int,
        participant1: freezed == participant1
            ? _value.participant1
            : participant1 // ignore: cast_nullable_to_non_nullable
                  as UserModel?,
        participant2: freezed == participant2
            ? _value.participant2
            : participant2 // ignore: cast_nullable_to_non_nullable
                  as UserModel?,
        lastMessage: freezed == lastMessage
            ? _value.lastMessage
            : lastMessage // ignore: cast_nullable_to_non_nullable
                  as MessageModel?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$ConversationModelImpl implements _ConversationModel {
  const _$ConversationModelImpl({
    @JsonKey(fromJson: _intFromJson) required this.id,
    @JsonKey(name: 'participant_1_id', fromJson: _intFromJson)
    required this.participant1Id,
    @JsonKey(name: 'participant_2_id', fromJson: _intFromJson)
    required this.participant2Id,
    @JsonKey(name: 'last_message_at') this.lastMessageAt,
    @JsonKey(name: 'last_message_preview', fromJson: _stringFromJsonNullable)
    this.lastMessagePreview,
    @JsonKey(name: 'unread_count', defaultValue: 0) this.unreadCount = 0,
    @JsonKey(fromJson: _participant1FromJson) this.participant1,
    @JsonKey(fromJson: _participant2FromJson) this.participant2,
    @JsonKey(fromJson: _lastMessageFromJson) this.lastMessage,
  });

  factory _$ConversationModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$ConversationModelImplFromJson(json);

  @override
  @JsonKey(fromJson: _intFromJson)
  final int id;
  @override
  @JsonKey(name: 'participant_1_id', fromJson: _intFromJson)
  final int participant1Id;
  @override
  @JsonKey(name: 'participant_2_id', fromJson: _intFromJson)
  final int participant2Id;
  @override
  @JsonKey(name: 'last_message_at')
  final DateTime? lastMessageAt;
  @override
  @JsonKey(name: 'last_message_preview', fromJson: _stringFromJsonNullable)
  final String? lastMessagePreview;
  @override
  @JsonKey(name: 'unread_count', defaultValue: 0)
  final int unreadCount;
  // Nested participants info (when fetched with details)
  @override
  @JsonKey(fromJson: _participant1FromJson)
  final UserModel? participant1;
  @override
  @JsonKey(fromJson: _participant2FromJson)
  final UserModel? participant2;
  // Last message details
  @override
  @JsonKey(fromJson: _lastMessageFromJson)
  final MessageModel? lastMessage;

  @override
  String toString() {
    return 'ConversationModel(id: $id, participant1Id: $participant1Id, participant2Id: $participant2Id, lastMessageAt: $lastMessageAt, lastMessagePreview: $lastMessagePreview, unreadCount: $unreadCount, participant1: $participant1, participant2: $participant2, lastMessage: $lastMessage)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ConversationModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.participant1Id, participant1Id) ||
                other.participant1Id == participant1Id) &&
            (identical(other.participant2Id, participant2Id) ||
                other.participant2Id == participant2Id) &&
            (identical(other.lastMessageAt, lastMessageAt) ||
                other.lastMessageAt == lastMessageAt) &&
            (identical(other.lastMessagePreview, lastMessagePreview) ||
                other.lastMessagePreview == lastMessagePreview) &&
            (identical(other.unreadCount, unreadCount) ||
                other.unreadCount == unreadCount) &&
            (identical(other.participant1, participant1) ||
                other.participant1 == participant1) &&
            (identical(other.participant2, participant2) ||
                other.participant2 == participant2) &&
            (identical(other.lastMessage, lastMessage) ||
                other.lastMessage == lastMessage));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    participant1Id,
    participant2Id,
    lastMessageAt,
    lastMessagePreview,
    unreadCount,
    participant1,
    participant2,
    lastMessage,
  );

  /// Create a copy of ConversationModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$ConversationModelImplCopyWith<_$ConversationModelImpl> get copyWith =>
      __$$ConversationModelImplCopyWithImpl<_$ConversationModelImpl>(
        this,
        _$identity,
      );

  @override
  Map<String, dynamic> toJson() {
    return _$$ConversationModelImplToJson(this);
  }
}

abstract class _ConversationModel implements ConversationModel {
  const factory _ConversationModel({
    @JsonKey(fromJson: _intFromJson) required final int id,
    @JsonKey(name: 'participant_1_id', fromJson: _intFromJson)
    required final int participant1Id,
    @JsonKey(name: 'participant_2_id', fromJson: _intFromJson)
    required final int participant2Id,
    @JsonKey(name: 'last_message_at') final DateTime? lastMessageAt,
    @JsonKey(name: 'last_message_preview', fromJson: _stringFromJsonNullable)
    final String? lastMessagePreview,
    @JsonKey(name: 'unread_count', defaultValue: 0) final int unreadCount,
    @JsonKey(fromJson: _participant1FromJson) final UserModel? participant1,
    @JsonKey(fromJson: _participant2FromJson) final UserModel? participant2,
    @JsonKey(fromJson: _lastMessageFromJson) final MessageModel? lastMessage,
  }) = _$ConversationModelImpl;

  factory _ConversationModel.fromJson(Map<String, dynamic> json) =
      _$ConversationModelImpl.fromJson;

  @override
  @JsonKey(fromJson: _intFromJson)
  int get id;
  @override
  @JsonKey(name: 'participant_1_id', fromJson: _intFromJson)
  int get participant1Id;
  @override
  @JsonKey(name: 'participant_2_id', fromJson: _intFromJson)
  int get participant2Id;
  @override
  @JsonKey(name: 'last_message_at')
  DateTime? get lastMessageAt;
  @override
  @JsonKey(name: 'last_message_preview', fromJson: _stringFromJsonNullable)
  String? get lastMessagePreview;
  @override
  @JsonKey(name: 'unread_count', defaultValue: 0)
  int get unreadCount; // Nested participants info (when fetched with details)
  @override
  @JsonKey(fromJson: _participant1FromJson)
  UserModel? get participant1;
  @override
  @JsonKey(fromJson: _participant2FromJson)
  UserModel? get participant2; // Last message details
  @override
  @JsonKey(fromJson: _lastMessageFromJson)
  MessageModel? get lastMessage;

  /// Create a copy of ConversationModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$ConversationModelImplCopyWith<_$ConversationModelImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
