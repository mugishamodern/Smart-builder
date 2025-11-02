// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'user_model.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

UserModel _$UserModelFromJson(Map<String, dynamic> json) {
  return _UserModel.fromJson(json);
}

/// @nodoc
mixin _$UserModel {
  @JsonKey(fromJson: _intFromJson)
  int get id => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _stringFromJson)
  String get username => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _stringFromJson)
  String get email => throw _privateConstructorUsedError;
  @JsonKey(name: 'full_name', fromJson: _stringFromJsonNullable)
  String? get fullName => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _stringFromJsonNullable)
  String? get phone => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _stringFromJsonNullable)
  String? get address => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _coordinateFromJson)
  double? get latitude => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _coordinateFromJson)
  double? get longitude => throw _privateConstructorUsedError;
  @JsonKey(name: 'user_type', defaultValue: 'customer')
  String get userType => throw _privateConstructorUsedError; // customer, shop_owner, service_provider
  @JsonKey(name: 'is_active', defaultValue: true)
  bool get isActive => throw _privateConstructorUsedError;
  @JsonKey(name: 'is_verified', defaultValue: false)
  bool get isVerified => throw _privateConstructorUsedError;
  @JsonKey(name: 'created_at', fromJson: _dateTimeFromJsonNullable)
  DateTime? get createdAt => throw _privateConstructorUsedError;
  @JsonKey(name: 'updated_at', fromJson: _dateTimeFromJsonNullable)
  DateTime? get updatedAt => throw _privateConstructorUsedError;

  /// Serializes this UserModel to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of UserModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $UserModelCopyWith<UserModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $UserModelCopyWith<$Res> {
  factory $UserModelCopyWith(UserModel value, $Res Function(UserModel) then) =
      _$UserModelCopyWithImpl<$Res, UserModel>;
  @useResult
  $Res call({
    @JsonKey(fromJson: _intFromJson) int id,
    @JsonKey(fromJson: _stringFromJson) String username,
    @JsonKey(fromJson: _stringFromJson) String email,
    @JsonKey(name: 'full_name', fromJson: _stringFromJsonNullable)
    String? fullName,
    @JsonKey(fromJson: _stringFromJsonNullable) String? phone,
    @JsonKey(fromJson: _stringFromJsonNullable) String? address,
    @JsonKey(fromJson: _coordinateFromJson) double? latitude,
    @JsonKey(fromJson: _coordinateFromJson) double? longitude,
    @JsonKey(name: 'user_type', defaultValue: 'customer') String userType,
    @JsonKey(name: 'is_active', defaultValue: true) bool isActive,
    @JsonKey(name: 'is_verified', defaultValue: false) bool isVerified,
    @JsonKey(name: 'created_at', fromJson: _dateTimeFromJsonNullable)
    DateTime? createdAt,
    @JsonKey(name: 'updated_at', fromJson: _dateTimeFromJsonNullable)
    DateTime? updatedAt,
  });
}

/// @nodoc
class _$UserModelCopyWithImpl<$Res, $Val extends UserModel>
    implements $UserModelCopyWith<$Res> {
  _$UserModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of UserModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? username = null,
    Object? email = null,
    Object? fullName = freezed,
    Object? phone = freezed,
    Object? address = freezed,
    Object? latitude = freezed,
    Object? longitude = freezed,
    Object? userType = null,
    Object? isActive = null,
    Object? isVerified = null,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as int,
            username: null == username
                ? _value.username
                : username // ignore: cast_nullable_to_non_nullable
                      as String,
            email: null == email
                ? _value.email
                : email // ignore: cast_nullable_to_non_nullable
                      as String,
            fullName: freezed == fullName
                ? _value.fullName
                : fullName // ignore: cast_nullable_to_non_nullable
                      as String?,
            phone: freezed == phone
                ? _value.phone
                : phone // ignore: cast_nullable_to_non_nullable
                      as String?,
            address: freezed == address
                ? _value.address
                : address // ignore: cast_nullable_to_non_nullable
                      as String?,
            latitude: freezed == latitude
                ? _value.latitude
                : latitude // ignore: cast_nullable_to_non_nullable
                      as double?,
            longitude: freezed == longitude
                ? _value.longitude
                : longitude // ignore: cast_nullable_to_non_nullable
                      as double?,
            userType: null == userType
                ? _value.userType
                : userType // ignore: cast_nullable_to_non_nullable
                      as String,
            isActive: null == isActive
                ? _value.isActive
                : isActive // ignore: cast_nullable_to_non_nullable
                      as bool,
            isVerified: null == isVerified
                ? _value.isVerified
                : isVerified // ignore: cast_nullable_to_non_nullable
                      as bool,
            createdAt: freezed == createdAt
                ? _value.createdAt
                : createdAt // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            updatedAt: freezed == updatedAt
                ? _value.updatedAt
                : updatedAt // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$UserModelImplCopyWith<$Res>
    implements $UserModelCopyWith<$Res> {
  factory _$$UserModelImplCopyWith(
    _$UserModelImpl value,
    $Res Function(_$UserModelImpl) then,
  ) = __$$UserModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    @JsonKey(fromJson: _intFromJson) int id,
    @JsonKey(fromJson: _stringFromJson) String username,
    @JsonKey(fromJson: _stringFromJson) String email,
    @JsonKey(name: 'full_name', fromJson: _stringFromJsonNullable)
    String? fullName,
    @JsonKey(fromJson: _stringFromJsonNullable) String? phone,
    @JsonKey(fromJson: _stringFromJsonNullable) String? address,
    @JsonKey(fromJson: _coordinateFromJson) double? latitude,
    @JsonKey(fromJson: _coordinateFromJson) double? longitude,
    @JsonKey(name: 'user_type', defaultValue: 'customer') String userType,
    @JsonKey(name: 'is_active', defaultValue: true) bool isActive,
    @JsonKey(name: 'is_verified', defaultValue: false) bool isVerified,
    @JsonKey(name: 'created_at', fromJson: _dateTimeFromJsonNullable)
    DateTime? createdAt,
    @JsonKey(name: 'updated_at', fromJson: _dateTimeFromJsonNullable)
    DateTime? updatedAt,
  });
}

/// @nodoc
class __$$UserModelImplCopyWithImpl<$Res>
    extends _$UserModelCopyWithImpl<$Res, _$UserModelImpl>
    implements _$$UserModelImplCopyWith<$Res> {
  __$$UserModelImplCopyWithImpl(
    _$UserModelImpl _value,
    $Res Function(_$UserModelImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of UserModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? username = null,
    Object? email = null,
    Object? fullName = freezed,
    Object? phone = freezed,
    Object? address = freezed,
    Object? latitude = freezed,
    Object? longitude = freezed,
    Object? userType = null,
    Object? isActive = null,
    Object? isVerified = null,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(
      _$UserModelImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as int,
        username: null == username
            ? _value.username
            : username // ignore: cast_nullable_to_non_nullable
                  as String,
        email: null == email
            ? _value.email
            : email // ignore: cast_nullable_to_non_nullable
                  as String,
        fullName: freezed == fullName
            ? _value.fullName
            : fullName // ignore: cast_nullable_to_non_nullable
                  as String?,
        phone: freezed == phone
            ? _value.phone
            : phone // ignore: cast_nullable_to_non_nullable
                  as String?,
        address: freezed == address
            ? _value.address
            : address // ignore: cast_nullable_to_non_nullable
                  as String?,
        latitude: freezed == latitude
            ? _value.latitude
            : latitude // ignore: cast_nullable_to_non_nullable
                  as double?,
        longitude: freezed == longitude
            ? _value.longitude
            : longitude // ignore: cast_nullable_to_non_nullable
                  as double?,
        userType: null == userType
            ? _value.userType
            : userType // ignore: cast_nullable_to_non_nullable
                  as String,
        isActive: null == isActive
            ? _value.isActive
            : isActive // ignore: cast_nullable_to_non_nullable
                  as bool,
        isVerified: null == isVerified
            ? _value.isVerified
            : isVerified // ignore: cast_nullable_to_non_nullable
                  as bool,
        createdAt: freezed == createdAt
            ? _value.createdAt
            : createdAt // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        updatedAt: freezed == updatedAt
            ? _value.updatedAt
            : updatedAt // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$UserModelImpl implements _UserModel {
  const _$UserModelImpl({
    @JsonKey(fromJson: _intFromJson) required this.id,
    @JsonKey(fromJson: _stringFromJson) required this.username,
    @JsonKey(fromJson: _stringFromJson) required this.email,
    @JsonKey(name: 'full_name', fromJson: _stringFromJsonNullable)
    this.fullName,
    @JsonKey(fromJson: _stringFromJsonNullable) this.phone,
    @JsonKey(fromJson: _stringFromJsonNullable) this.address,
    @JsonKey(fromJson: _coordinateFromJson) this.latitude,
    @JsonKey(fromJson: _coordinateFromJson) this.longitude,
    @JsonKey(name: 'user_type', defaultValue: 'customer')
    this.userType = 'customer',
    @JsonKey(name: 'is_active', defaultValue: true) this.isActive = true,
    @JsonKey(name: 'is_verified', defaultValue: false) this.isVerified = false,
    @JsonKey(name: 'created_at', fromJson: _dateTimeFromJsonNullable)
    this.createdAt,
    @JsonKey(name: 'updated_at', fromJson: _dateTimeFromJsonNullable)
    this.updatedAt,
  });

  factory _$UserModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$UserModelImplFromJson(json);

  @override
  @JsonKey(fromJson: _intFromJson)
  final int id;
  @override
  @JsonKey(fromJson: _stringFromJson)
  final String username;
  @override
  @JsonKey(fromJson: _stringFromJson)
  final String email;
  @override
  @JsonKey(name: 'full_name', fromJson: _stringFromJsonNullable)
  final String? fullName;
  @override
  @JsonKey(fromJson: _stringFromJsonNullable)
  final String? phone;
  @override
  @JsonKey(fromJson: _stringFromJsonNullable)
  final String? address;
  @override
  @JsonKey(fromJson: _coordinateFromJson)
  final double? latitude;
  @override
  @JsonKey(fromJson: _coordinateFromJson)
  final double? longitude;
  @override
  @JsonKey(name: 'user_type', defaultValue: 'customer')
  final String userType;
  // customer, shop_owner, service_provider
  @override
  @JsonKey(name: 'is_active', defaultValue: true)
  final bool isActive;
  @override
  @JsonKey(name: 'is_verified', defaultValue: false)
  final bool isVerified;
  @override
  @JsonKey(name: 'created_at', fromJson: _dateTimeFromJsonNullable)
  final DateTime? createdAt;
  @override
  @JsonKey(name: 'updated_at', fromJson: _dateTimeFromJsonNullable)
  final DateTime? updatedAt;

  @override
  String toString() {
    return 'UserModel(id: $id, username: $username, email: $email, fullName: $fullName, phone: $phone, address: $address, latitude: $latitude, longitude: $longitude, userType: $userType, isActive: $isActive, isVerified: $isVerified, createdAt: $createdAt, updatedAt: $updatedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$UserModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.username, username) ||
                other.username == username) &&
            (identical(other.email, email) || other.email == email) &&
            (identical(other.fullName, fullName) ||
                other.fullName == fullName) &&
            (identical(other.phone, phone) || other.phone == phone) &&
            (identical(other.address, address) || other.address == address) &&
            (identical(other.latitude, latitude) ||
                other.latitude == latitude) &&
            (identical(other.longitude, longitude) ||
                other.longitude == longitude) &&
            (identical(other.userType, userType) ||
                other.userType == userType) &&
            (identical(other.isActive, isActive) ||
                other.isActive == isActive) &&
            (identical(other.isVerified, isVerified) ||
                other.isVerified == isVerified) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt) &&
            (identical(other.updatedAt, updatedAt) ||
                other.updatedAt == updatedAt));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    username,
    email,
    fullName,
    phone,
    address,
    latitude,
    longitude,
    userType,
    isActive,
    isVerified,
    createdAt,
    updatedAt,
  );

  /// Create a copy of UserModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$UserModelImplCopyWith<_$UserModelImpl> get copyWith =>
      __$$UserModelImplCopyWithImpl<_$UserModelImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$UserModelImplToJson(this);
  }
}

abstract class _UserModel implements UserModel {
  const factory _UserModel({
    @JsonKey(fromJson: _intFromJson) required final int id,
    @JsonKey(fromJson: _stringFromJson) required final String username,
    @JsonKey(fromJson: _stringFromJson) required final String email,
    @JsonKey(name: 'full_name', fromJson: _stringFromJsonNullable)
    final String? fullName,
    @JsonKey(fromJson: _stringFromJsonNullable) final String? phone,
    @JsonKey(fromJson: _stringFromJsonNullable) final String? address,
    @JsonKey(fromJson: _coordinateFromJson) final double? latitude,
    @JsonKey(fromJson: _coordinateFromJson) final double? longitude,
    @JsonKey(name: 'user_type', defaultValue: 'customer') final String userType,
    @JsonKey(name: 'is_active', defaultValue: true) final bool isActive,
    @JsonKey(name: 'is_verified', defaultValue: false) final bool isVerified,
    @JsonKey(name: 'created_at', fromJson: _dateTimeFromJsonNullable)
    final DateTime? createdAt,
    @JsonKey(name: 'updated_at', fromJson: _dateTimeFromJsonNullable)
    final DateTime? updatedAt,
  }) = _$UserModelImpl;

  factory _UserModel.fromJson(Map<String, dynamic> json) =
      _$UserModelImpl.fromJson;

  @override
  @JsonKey(fromJson: _intFromJson)
  int get id;
  @override
  @JsonKey(fromJson: _stringFromJson)
  String get username;
  @override
  @JsonKey(fromJson: _stringFromJson)
  String get email;
  @override
  @JsonKey(name: 'full_name', fromJson: _stringFromJsonNullable)
  String? get fullName;
  @override
  @JsonKey(fromJson: _stringFromJsonNullable)
  String? get phone;
  @override
  @JsonKey(fromJson: _stringFromJsonNullable)
  String? get address;
  @override
  @JsonKey(fromJson: _coordinateFromJson)
  double? get latitude;
  @override
  @JsonKey(fromJson: _coordinateFromJson)
  double? get longitude;
  @override
  @JsonKey(name: 'user_type', defaultValue: 'customer')
  String get userType; // customer, shop_owner, service_provider
  @override
  @JsonKey(name: 'is_active', defaultValue: true)
  bool get isActive;
  @override
  @JsonKey(name: 'is_verified', defaultValue: false)
  bool get isVerified;
  @override
  @JsonKey(name: 'created_at', fromJson: _dateTimeFromJsonNullable)
  DateTime? get createdAt;
  @override
  @JsonKey(name: 'updated_at', fromJson: _dateTimeFromJsonNullable)
  DateTime? get updatedAt;

  /// Create a copy of UserModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$UserModelImplCopyWith<_$UserModelImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
