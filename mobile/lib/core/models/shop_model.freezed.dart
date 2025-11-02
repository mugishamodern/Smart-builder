// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'shop_model.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

ShopModel _$ShopModelFromJson(Map<String, dynamic> json) {
  return _ShopModel.fromJson(json);
}

/// @nodoc
mixin _$ShopModel {
  @JsonKey(fromJson: _intFromJson)
  int get id => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _stringFromJson)
  String get name => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _stringFromJsonNullable)
  String? get description => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _stringFromJson)
  String get address => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _stringFromJsonNullable)
  String? get phone => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _stringFromJsonNullable)
  String? get email => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _coordinateFromJson)
  double get latitude => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _coordinateFromJson)
  double get longitude => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _ratingFromJson)
  double get rating => throw _privateConstructorUsedError;
  @JsonKey(name: 'total_reviews', fromJson: _intFromJson)
  int get totalReviews => throw _privateConstructorUsedError;
  @JsonKey(name: 'is_verified', defaultValue: false)
  bool get isVerified => throw _privateConstructorUsedError;
  @JsonKey(name: 'is_active', defaultValue: true)
  bool get isActive => throw _privateConstructorUsedError;
  @JsonKey(name: 'owner_id', fromJson: _intFromJson)
  int get ownerId => throw _privateConstructorUsedError;
  @JsonKey(name: 'created_at')
  DateTime? get createdAt => throw _privateConstructorUsedError;
  @JsonKey(name: 'updated_at')
  DateTime? get updatedAt => throw _privateConstructorUsedError;

  /// Serializes this ShopModel to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of ShopModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $ShopModelCopyWith<ShopModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $ShopModelCopyWith<$Res> {
  factory $ShopModelCopyWith(ShopModel value, $Res Function(ShopModel) then) =
      _$ShopModelCopyWithImpl<$Res, ShopModel>;
  @useResult
  $Res call({
    @JsonKey(fromJson: _intFromJson) int id,
    @JsonKey(fromJson: _stringFromJson) String name,
    @JsonKey(fromJson: _stringFromJsonNullable) String? description,
    @JsonKey(fromJson: _stringFromJson) String address,
    @JsonKey(fromJson: _stringFromJsonNullable) String? phone,
    @JsonKey(fromJson: _stringFromJsonNullable) String? email,
    @JsonKey(fromJson: _coordinateFromJson) double latitude,
    @JsonKey(fromJson: _coordinateFromJson) double longitude,
    @JsonKey(fromJson: _ratingFromJson) double rating,
    @JsonKey(name: 'total_reviews', fromJson: _intFromJson) int totalReviews,
    @JsonKey(name: 'is_verified', defaultValue: false) bool isVerified,
    @JsonKey(name: 'is_active', defaultValue: true) bool isActive,
    @JsonKey(name: 'owner_id', fromJson: _intFromJson) int ownerId,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @JsonKey(name: 'updated_at') DateTime? updatedAt,
  });
}

/// @nodoc
class _$ShopModelCopyWithImpl<$Res, $Val extends ShopModel>
    implements $ShopModelCopyWith<$Res> {
  _$ShopModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of ShopModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? description = freezed,
    Object? address = null,
    Object? phone = freezed,
    Object? email = freezed,
    Object? latitude = null,
    Object? longitude = null,
    Object? rating = null,
    Object? totalReviews = null,
    Object? isVerified = null,
    Object? isActive = null,
    Object? ownerId = null,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as int,
            name: null == name
                ? _value.name
                : name // ignore: cast_nullable_to_non_nullable
                      as String,
            description: freezed == description
                ? _value.description
                : description // ignore: cast_nullable_to_non_nullable
                      as String?,
            address: null == address
                ? _value.address
                : address // ignore: cast_nullable_to_non_nullable
                      as String,
            phone: freezed == phone
                ? _value.phone
                : phone // ignore: cast_nullable_to_non_nullable
                      as String?,
            email: freezed == email
                ? _value.email
                : email // ignore: cast_nullable_to_non_nullable
                      as String?,
            latitude: null == latitude
                ? _value.latitude
                : latitude // ignore: cast_nullable_to_non_nullable
                      as double,
            longitude: null == longitude
                ? _value.longitude
                : longitude // ignore: cast_nullable_to_non_nullable
                      as double,
            rating: null == rating
                ? _value.rating
                : rating // ignore: cast_nullable_to_non_nullable
                      as double,
            totalReviews: null == totalReviews
                ? _value.totalReviews
                : totalReviews // ignore: cast_nullable_to_non_nullable
                      as int,
            isVerified: null == isVerified
                ? _value.isVerified
                : isVerified // ignore: cast_nullable_to_non_nullable
                      as bool,
            isActive: null == isActive
                ? _value.isActive
                : isActive // ignore: cast_nullable_to_non_nullable
                      as bool,
            ownerId: null == ownerId
                ? _value.ownerId
                : ownerId // ignore: cast_nullable_to_non_nullable
                      as int,
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
abstract class _$$ShopModelImplCopyWith<$Res>
    implements $ShopModelCopyWith<$Res> {
  factory _$$ShopModelImplCopyWith(
    _$ShopModelImpl value,
    $Res Function(_$ShopModelImpl) then,
  ) = __$$ShopModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    @JsonKey(fromJson: _intFromJson) int id,
    @JsonKey(fromJson: _stringFromJson) String name,
    @JsonKey(fromJson: _stringFromJsonNullable) String? description,
    @JsonKey(fromJson: _stringFromJson) String address,
    @JsonKey(fromJson: _stringFromJsonNullable) String? phone,
    @JsonKey(fromJson: _stringFromJsonNullable) String? email,
    @JsonKey(fromJson: _coordinateFromJson) double latitude,
    @JsonKey(fromJson: _coordinateFromJson) double longitude,
    @JsonKey(fromJson: _ratingFromJson) double rating,
    @JsonKey(name: 'total_reviews', fromJson: _intFromJson) int totalReviews,
    @JsonKey(name: 'is_verified', defaultValue: false) bool isVerified,
    @JsonKey(name: 'is_active', defaultValue: true) bool isActive,
    @JsonKey(name: 'owner_id', fromJson: _intFromJson) int ownerId,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @JsonKey(name: 'updated_at') DateTime? updatedAt,
  });
}

/// @nodoc
class __$$ShopModelImplCopyWithImpl<$Res>
    extends _$ShopModelCopyWithImpl<$Res, _$ShopModelImpl>
    implements _$$ShopModelImplCopyWith<$Res> {
  __$$ShopModelImplCopyWithImpl(
    _$ShopModelImpl _value,
    $Res Function(_$ShopModelImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of ShopModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? description = freezed,
    Object? address = null,
    Object? phone = freezed,
    Object? email = freezed,
    Object? latitude = null,
    Object? longitude = null,
    Object? rating = null,
    Object? totalReviews = null,
    Object? isVerified = null,
    Object? isActive = null,
    Object? ownerId = null,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(
      _$ShopModelImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as int,
        name: null == name
            ? _value.name
            : name // ignore: cast_nullable_to_non_nullable
                  as String,
        description: freezed == description
            ? _value.description
            : description // ignore: cast_nullable_to_non_nullable
                  as String?,
        address: null == address
            ? _value.address
            : address // ignore: cast_nullable_to_non_nullable
                  as String,
        phone: freezed == phone
            ? _value.phone
            : phone // ignore: cast_nullable_to_non_nullable
                  as String?,
        email: freezed == email
            ? _value.email
            : email // ignore: cast_nullable_to_non_nullable
                  as String?,
        latitude: null == latitude
            ? _value.latitude
            : latitude // ignore: cast_nullable_to_non_nullable
                  as double,
        longitude: null == longitude
            ? _value.longitude
            : longitude // ignore: cast_nullable_to_non_nullable
                  as double,
        rating: null == rating
            ? _value.rating
            : rating // ignore: cast_nullable_to_non_nullable
                  as double,
        totalReviews: null == totalReviews
            ? _value.totalReviews
            : totalReviews // ignore: cast_nullable_to_non_nullable
                  as int,
        isVerified: null == isVerified
            ? _value.isVerified
            : isVerified // ignore: cast_nullable_to_non_nullable
                  as bool,
        isActive: null == isActive
            ? _value.isActive
            : isActive // ignore: cast_nullable_to_non_nullable
                  as bool,
        ownerId: null == ownerId
            ? _value.ownerId
            : ownerId // ignore: cast_nullable_to_non_nullable
                  as int,
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
class _$ShopModelImpl implements _ShopModel {
  const _$ShopModelImpl({
    @JsonKey(fromJson: _intFromJson) required this.id,
    @JsonKey(fromJson: _stringFromJson) required this.name,
    @JsonKey(fromJson: _stringFromJsonNullable) this.description,
    @JsonKey(fromJson: _stringFromJson) required this.address,
    @JsonKey(fromJson: _stringFromJsonNullable) this.phone,
    @JsonKey(fromJson: _stringFromJsonNullable) this.email,
    @JsonKey(fromJson: _coordinateFromJson) required this.latitude,
    @JsonKey(fromJson: _coordinateFromJson) required this.longitude,
    @JsonKey(fromJson: _ratingFromJson) this.rating = 0.0,
    @JsonKey(name: 'total_reviews', fromJson: _intFromJson)
    this.totalReviews = 0,
    @JsonKey(name: 'is_verified', defaultValue: false) this.isVerified = false,
    @JsonKey(name: 'is_active', defaultValue: true) this.isActive = true,
    @JsonKey(name: 'owner_id', fromJson: _intFromJson) required this.ownerId,
    @JsonKey(name: 'created_at') this.createdAt,
    @JsonKey(name: 'updated_at') this.updatedAt,
  });

  factory _$ShopModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$ShopModelImplFromJson(json);

  @override
  @JsonKey(fromJson: _intFromJson)
  final int id;
  @override
  @JsonKey(fromJson: _stringFromJson)
  final String name;
  @override
  @JsonKey(fromJson: _stringFromJsonNullable)
  final String? description;
  @override
  @JsonKey(fromJson: _stringFromJson)
  final String address;
  @override
  @JsonKey(fromJson: _stringFromJsonNullable)
  final String? phone;
  @override
  @JsonKey(fromJson: _stringFromJsonNullable)
  final String? email;
  @override
  @JsonKey(fromJson: _coordinateFromJson)
  final double latitude;
  @override
  @JsonKey(fromJson: _coordinateFromJson)
  final double longitude;
  @override
  @JsonKey(fromJson: _ratingFromJson)
  final double rating;
  @override
  @JsonKey(name: 'total_reviews', fromJson: _intFromJson)
  final int totalReviews;
  @override
  @JsonKey(name: 'is_verified', defaultValue: false)
  final bool isVerified;
  @override
  @JsonKey(name: 'is_active', defaultValue: true)
  final bool isActive;
  @override
  @JsonKey(name: 'owner_id', fromJson: _intFromJson)
  final int ownerId;
  @override
  @JsonKey(name: 'created_at')
  final DateTime? createdAt;
  @override
  @JsonKey(name: 'updated_at')
  final DateTime? updatedAt;

  @override
  String toString() {
    return 'ShopModel(id: $id, name: $name, description: $description, address: $address, phone: $phone, email: $email, latitude: $latitude, longitude: $longitude, rating: $rating, totalReviews: $totalReviews, isVerified: $isVerified, isActive: $isActive, ownerId: $ownerId, createdAt: $createdAt, updatedAt: $updatedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ShopModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.address, address) || other.address == address) &&
            (identical(other.phone, phone) || other.phone == phone) &&
            (identical(other.email, email) || other.email == email) &&
            (identical(other.latitude, latitude) ||
                other.latitude == latitude) &&
            (identical(other.longitude, longitude) ||
                other.longitude == longitude) &&
            (identical(other.rating, rating) || other.rating == rating) &&
            (identical(other.totalReviews, totalReviews) ||
                other.totalReviews == totalReviews) &&
            (identical(other.isVerified, isVerified) ||
                other.isVerified == isVerified) &&
            (identical(other.isActive, isActive) ||
                other.isActive == isActive) &&
            (identical(other.ownerId, ownerId) || other.ownerId == ownerId) &&
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
    name,
    description,
    address,
    phone,
    email,
    latitude,
    longitude,
    rating,
    totalReviews,
    isVerified,
    isActive,
    ownerId,
    createdAt,
    updatedAt,
  );

  /// Create a copy of ShopModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$ShopModelImplCopyWith<_$ShopModelImpl> get copyWith =>
      __$$ShopModelImplCopyWithImpl<_$ShopModelImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$ShopModelImplToJson(this);
  }
}

abstract class _ShopModel implements ShopModel {
  const factory _ShopModel({
    @JsonKey(fromJson: _intFromJson) required final int id,
    @JsonKey(fromJson: _stringFromJson) required final String name,
    @JsonKey(fromJson: _stringFromJsonNullable) final String? description,
    @JsonKey(fromJson: _stringFromJson) required final String address,
    @JsonKey(fromJson: _stringFromJsonNullable) final String? phone,
    @JsonKey(fromJson: _stringFromJsonNullable) final String? email,
    @JsonKey(fromJson: _coordinateFromJson) required final double latitude,
    @JsonKey(fromJson: _coordinateFromJson) required final double longitude,
    @JsonKey(fromJson: _ratingFromJson) final double rating,
    @JsonKey(name: 'total_reviews', fromJson: _intFromJson)
    final int totalReviews,
    @JsonKey(name: 'is_verified', defaultValue: false) final bool isVerified,
    @JsonKey(name: 'is_active', defaultValue: true) final bool isActive,
    @JsonKey(name: 'owner_id', fromJson: _intFromJson)
    required final int ownerId,
    @JsonKey(name: 'created_at') final DateTime? createdAt,
    @JsonKey(name: 'updated_at') final DateTime? updatedAt,
  }) = _$ShopModelImpl;

  factory _ShopModel.fromJson(Map<String, dynamic> json) =
      _$ShopModelImpl.fromJson;

  @override
  @JsonKey(fromJson: _intFromJson)
  int get id;
  @override
  @JsonKey(fromJson: _stringFromJson)
  String get name;
  @override
  @JsonKey(fromJson: _stringFromJsonNullable)
  String? get description;
  @override
  @JsonKey(fromJson: _stringFromJson)
  String get address;
  @override
  @JsonKey(fromJson: _stringFromJsonNullable)
  String? get phone;
  @override
  @JsonKey(fromJson: _stringFromJsonNullable)
  String? get email;
  @override
  @JsonKey(fromJson: _coordinateFromJson)
  double get latitude;
  @override
  @JsonKey(fromJson: _coordinateFromJson)
  double get longitude;
  @override
  @JsonKey(fromJson: _ratingFromJson)
  double get rating;
  @override
  @JsonKey(name: 'total_reviews', fromJson: _intFromJson)
  int get totalReviews;
  @override
  @JsonKey(name: 'is_verified', defaultValue: false)
  bool get isVerified;
  @override
  @JsonKey(name: 'is_active', defaultValue: true)
  bool get isActive;
  @override
  @JsonKey(name: 'owner_id', fromJson: _intFromJson)
  int get ownerId;
  @override
  @JsonKey(name: 'created_at')
  DateTime? get createdAt;
  @override
  @JsonKey(name: 'updated_at')
  DateTime? get updatedAt;

  /// Create a copy of ShopModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$ShopModelImplCopyWith<_$ShopModelImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
