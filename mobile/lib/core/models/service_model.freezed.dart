// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'service_model.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

ServiceModel _$ServiceModelFromJson(Map<String, dynamic> json) {
  return _ServiceModel.fromJson(json);
}

/// @nodoc
mixin _$ServiceModel {
  @JsonKey(fromJson: _intFromJson)
  int get id => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _stringFromJson)
  String get title => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _stringFromJsonNullable)
  String? get description => throw _privateConstructorUsedError;
  @JsonKey(name: 'service_type', fromJson: _stringFromJson)
  String get serviceType => throw _privateConstructorUsedError; // e.g., 'plumbing', 'electrical', 'carpentry'
  @JsonKey(name: 'hourly_rate', fromJson: _hourlyRateFromJson)
  double get hourlyRate => throw _privateConstructorUsedError;
  @JsonKey(name: 'years_experience', fromJson: _yearsExperienceFromJson)
  int get yearsExperience => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _ratingFromJson)
  double get rating => throw _privateConstructorUsedError;
  @JsonKey(name: 'is_available', defaultValue: true)
  bool get isAvailable => throw _privateConstructorUsedError;
  @JsonKey(name: 'service_area', fromJson: _stringFromJsonNullable)
  String? get serviceArea => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _stringFromJsonNullable)
  String? get certifications => throw _privateConstructorUsedError;
  @JsonKey(name: 'portfolio_url', fromJson: _stringFromJsonNullable)
  String? get portfolioUrl => throw _privateConstructorUsedError;
  @JsonKey(name: 'provider_id', fromJson: _providerIdFromJson)
  int get providerId => throw _privateConstructorUsedError;
  @JsonKey(name: 'created_at')
  DateTime? get createdAt => throw _privateConstructorUsedError;
  @JsonKey(name: 'updated_at')
  DateTime? get updatedAt => throw _privateConstructorUsedError; // Nested provider info (when fetched with details)
  @JsonKey(fromJson: _providerFromJson)
  UserModel? get provider => throw _privateConstructorUsedError;

  /// Serializes this ServiceModel to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of ServiceModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $ServiceModelCopyWith<ServiceModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $ServiceModelCopyWith<$Res> {
  factory $ServiceModelCopyWith(
    ServiceModel value,
    $Res Function(ServiceModel) then,
  ) = _$ServiceModelCopyWithImpl<$Res, ServiceModel>;
  @useResult
  $Res call({
    @JsonKey(fromJson: _intFromJson) int id,
    @JsonKey(fromJson: _stringFromJson) String title,
    @JsonKey(fromJson: _stringFromJsonNullable) String? description,
    @JsonKey(name: 'service_type', fromJson: _stringFromJson)
    String serviceType,
    @JsonKey(name: 'hourly_rate', fromJson: _hourlyRateFromJson)
    double hourlyRate,
    @JsonKey(name: 'years_experience', fromJson: _yearsExperienceFromJson)
    int yearsExperience,
    @JsonKey(fromJson: _ratingFromJson) double rating,
    @JsonKey(name: 'is_available', defaultValue: true) bool isAvailable,
    @JsonKey(name: 'service_area', fromJson: _stringFromJsonNullable)
    String? serviceArea,
    @JsonKey(fromJson: _stringFromJsonNullable) String? certifications,
    @JsonKey(name: 'portfolio_url', fromJson: _stringFromJsonNullable)
    String? portfolioUrl,
    @JsonKey(name: 'provider_id', fromJson: _providerIdFromJson) int providerId,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @JsonKey(name: 'updated_at') DateTime? updatedAt,
    @JsonKey(fromJson: _providerFromJson) UserModel? provider,
  });

  $UserModelCopyWith<$Res>? get provider;
}

/// @nodoc
class _$ServiceModelCopyWithImpl<$Res, $Val extends ServiceModel>
    implements $ServiceModelCopyWith<$Res> {
  _$ServiceModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of ServiceModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? title = null,
    Object? description = freezed,
    Object? serviceType = null,
    Object? hourlyRate = null,
    Object? yearsExperience = null,
    Object? rating = null,
    Object? isAvailable = null,
    Object? serviceArea = freezed,
    Object? certifications = freezed,
    Object? portfolioUrl = freezed,
    Object? providerId = null,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
    Object? provider = freezed,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as int,
            title: null == title
                ? _value.title
                : title // ignore: cast_nullable_to_non_nullable
                      as String,
            description: freezed == description
                ? _value.description
                : description // ignore: cast_nullable_to_non_nullable
                      as String?,
            serviceType: null == serviceType
                ? _value.serviceType
                : serviceType // ignore: cast_nullable_to_non_nullable
                      as String,
            hourlyRate: null == hourlyRate
                ? _value.hourlyRate
                : hourlyRate // ignore: cast_nullable_to_non_nullable
                      as double,
            yearsExperience: null == yearsExperience
                ? _value.yearsExperience
                : yearsExperience // ignore: cast_nullable_to_non_nullable
                      as int,
            rating: null == rating
                ? _value.rating
                : rating // ignore: cast_nullable_to_non_nullable
                      as double,
            isAvailable: null == isAvailable
                ? _value.isAvailable
                : isAvailable // ignore: cast_nullable_to_non_nullable
                      as bool,
            serviceArea: freezed == serviceArea
                ? _value.serviceArea
                : serviceArea // ignore: cast_nullable_to_non_nullable
                      as String?,
            certifications: freezed == certifications
                ? _value.certifications
                : certifications // ignore: cast_nullable_to_non_nullable
                      as String?,
            portfolioUrl: freezed == portfolioUrl
                ? _value.portfolioUrl
                : portfolioUrl // ignore: cast_nullable_to_non_nullable
                      as String?,
            providerId: null == providerId
                ? _value.providerId
                : providerId // ignore: cast_nullable_to_non_nullable
                      as int,
            createdAt: freezed == createdAt
                ? _value.createdAt
                : createdAt // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            updatedAt: freezed == updatedAt
                ? _value.updatedAt
                : updatedAt // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            provider: freezed == provider
                ? _value.provider
                : provider // ignore: cast_nullable_to_non_nullable
                      as UserModel?,
          )
          as $Val,
    );
  }

  /// Create a copy of ServiceModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $UserModelCopyWith<$Res>? get provider {
    if (_value.provider == null) {
      return null;
    }

    return $UserModelCopyWith<$Res>(_value.provider!, (value) {
      return _then(_value.copyWith(provider: value) as $Val);
    });
  }
}

/// @nodoc
abstract class _$$ServiceModelImplCopyWith<$Res>
    implements $ServiceModelCopyWith<$Res> {
  factory _$$ServiceModelImplCopyWith(
    _$ServiceModelImpl value,
    $Res Function(_$ServiceModelImpl) then,
  ) = __$$ServiceModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    @JsonKey(fromJson: _intFromJson) int id,
    @JsonKey(fromJson: _stringFromJson) String title,
    @JsonKey(fromJson: _stringFromJsonNullable) String? description,
    @JsonKey(name: 'service_type', fromJson: _stringFromJson)
    String serviceType,
    @JsonKey(name: 'hourly_rate', fromJson: _hourlyRateFromJson)
    double hourlyRate,
    @JsonKey(name: 'years_experience', fromJson: _yearsExperienceFromJson)
    int yearsExperience,
    @JsonKey(fromJson: _ratingFromJson) double rating,
    @JsonKey(name: 'is_available', defaultValue: true) bool isAvailable,
    @JsonKey(name: 'service_area', fromJson: _stringFromJsonNullable)
    String? serviceArea,
    @JsonKey(fromJson: _stringFromJsonNullable) String? certifications,
    @JsonKey(name: 'portfolio_url', fromJson: _stringFromJsonNullable)
    String? portfolioUrl,
    @JsonKey(name: 'provider_id', fromJson: _providerIdFromJson) int providerId,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @JsonKey(name: 'updated_at') DateTime? updatedAt,
    @JsonKey(fromJson: _providerFromJson) UserModel? provider,
  });

  @override
  $UserModelCopyWith<$Res>? get provider;
}

/// @nodoc
class __$$ServiceModelImplCopyWithImpl<$Res>
    extends _$ServiceModelCopyWithImpl<$Res, _$ServiceModelImpl>
    implements _$$ServiceModelImplCopyWith<$Res> {
  __$$ServiceModelImplCopyWithImpl(
    _$ServiceModelImpl _value,
    $Res Function(_$ServiceModelImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of ServiceModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? title = null,
    Object? description = freezed,
    Object? serviceType = null,
    Object? hourlyRate = null,
    Object? yearsExperience = null,
    Object? rating = null,
    Object? isAvailable = null,
    Object? serviceArea = freezed,
    Object? certifications = freezed,
    Object? portfolioUrl = freezed,
    Object? providerId = null,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
    Object? provider = freezed,
  }) {
    return _then(
      _$ServiceModelImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as int,
        title: null == title
            ? _value.title
            : title // ignore: cast_nullable_to_non_nullable
                  as String,
        description: freezed == description
            ? _value.description
            : description // ignore: cast_nullable_to_non_nullable
                  as String?,
        serviceType: null == serviceType
            ? _value.serviceType
            : serviceType // ignore: cast_nullable_to_non_nullable
                  as String,
        hourlyRate: null == hourlyRate
            ? _value.hourlyRate
            : hourlyRate // ignore: cast_nullable_to_non_nullable
                  as double,
        yearsExperience: null == yearsExperience
            ? _value.yearsExperience
            : yearsExperience // ignore: cast_nullable_to_non_nullable
                  as int,
        rating: null == rating
            ? _value.rating
            : rating // ignore: cast_nullable_to_non_nullable
                  as double,
        isAvailable: null == isAvailable
            ? _value.isAvailable
            : isAvailable // ignore: cast_nullable_to_non_nullable
                  as bool,
        serviceArea: freezed == serviceArea
            ? _value.serviceArea
            : serviceArea // ignore: cast_nullable_to_non_nullable
                  as String?,
        certifications: freezed == certifications
            ? _value.certifications
            : certifications // ignore: cast_nullable_to_non_nullable
                  as String?,
        portfolioUrl: freezed == portfolioUrl
            ? _value.portfolioUrl
            : portfolioUrl // ignore: cast_nullable_to_non_nullable
                  as String?,
        providerId: null == providerId
            ? _value.providerId
            : providerId // ignore: cast_nullable_to_non_nullable
                  as int,
        createdAt: freezed == createdAt
            ? _value.createdAt
            : createdAt // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        updatedAt: freezed == updatedAt
            ? _value.updatedAt
            : updatedAt // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        provider: freezed == provider
            ? _value.provider
            : provider // ignore: cast_nullable_to_non_nullable
                  as UserModel?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$ServiceModelImpl implements _ServiceModel {
  const _$ServiceModelImpl({
    @JsonKey(fromJson: _intFromJson) required this.id,
    @JsonKey(fromJson: _stringFromJson) required this.title,
    @JsonKey(fromJson: _stringFromJsonNullable) this.description,
    @JsonKey(name: 'service_type', fromJson: _stringFromJson)
    required this.serviceType,
    @JsonKey(name: 'hourly_rate', fromJson: _hourlyRateFromJson)
    required this.hourlyRate,
    @JsonKey(name: 'years_experience', fromJson: _yearsExperienceFromJson)
    this.yearsExperience = 0,
    @JsonKey(fromJson: _ratingFromJson) this.rating = 0.0,
    @JsonKey(name: 'is_available', defaultValue: true) this.isAvailable = true,
    @JsonKey(name: 'service_area', fromJson: _stringFromJsonNullable)
    this.serviceArea,
    @JsonKey(fromJson: _stringFromJsonNullable) this.certifications,
    @JsonKey(name: 'portfolio_url', fromJson: _stringFromJsonNullable)
    this.portfolioUrl,
    @JsonKey(name: 'provider_id', fromJson: _providerIdFromJson)
    required this.providerId,
    @JsonKey(name: 'created_at') this.createdAt,
    @JsonKey(name: 'updated_at') this.updatedAt,
    @JsonKey(fromJson: _providerFromJson) this.provider,
  });

  factory _$ServiceModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$ServiceModelImplFromJson(json);

  @override
  @JsonKey(fromJson: _intFromJson)
  final int id;
  @override
  @JsonKey(fromJson: _stringFromJson)
  final String title;
  @override
  @JsonKey(fromJson: _stringFromJsonNullable)
  final String? description;
  @override
  @JsonKey(name: 'service_type', fromJson: _stringFromJson)
  final String serviceType;
  // e.g., 'plumbing', 'electrical', 'carpentry'
  @override
  @JsonKey(name: 'hourly_rate', fromJson: _hourlyRateFromJson)
  final double hourlyRate;
  @override
  @JsonKey(name: 'years_experience', fromJson: _yearsExperienceFromJson)
  final int yearsExperience;
  @override
  @JsonKey(fromJson: _ratingFromJson)
  final double rating;
  @override
  @JsonKey(name: 'is_available', defaultValue: true)
  final bool isAvailable;
  @override
  @JsonKey(name: 'service_area', fromJson: _stringFromJsonNullable)
  final String? serviceArea;
  @override
  @JsonKey(fromJson: _stringFromJsonNullable)
  final String? certifications;
  @override
  @JsonKey(name: 'portfolio_url', fromJson: _stringFromJsonNullable)
  final String? portfolioUrl;
  @override
  @JsonKey(name: 'provider_id', fromJson: _providerIdFromJson)
  final int providerId;
  @override
  @JsonKey(name: 'created_at')
  final DateTime? createdAt;
  @override
  @JsonKey(name: 'updated_at')
  final DateTime? updatedAt;
  // Nested provider info (when fetched with details)
  @override
  @JsonKey(fromJson: _providerFromJson)
  final UserModel? provider;

  @override
  String toString() {
    return 'ServiceModel(id: $id, title: $title, description: $description, serviceType: $serviceType, hourlyRate: $hourlyRate, yearsExperience: $yearsExperience, rating: $rating, isAvailable: $isAvailable, serviceArea: $serviceArea, certifications: $certifications, portfolioUrl: $portfolioUrl, providerId: $providerId, createdAt: $createdAt, updatedAt: $updatedAt, provider: $provider)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ServiceModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.title, title) || other.title == title) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.serviceType, serviceType) ||
                other.serviceType == serviceType) &&
            (identical(other.hourlyRate, hourlyRate) ||
                other.hourlyRate == hourlyRate) &&
            (identical(other.yearsExperience, yearsExperience) ||
                other.yearsExperience == yearsExperience) &&
            (identical(other.rating, rating) || other.rating == rating) &&
            (identical(other.isAvailable, isAvailable) ||
                other.isAvailable == isAvailable) &&
            (identical(other.serviceArea, serviceArea) ||
                other.serviceArea == serviceArea) &&
            (identical(other.certifications, certifications) ||
                other.certifications == certifications) &&
            (identical(other.portfolioUrl, portfolioUrl) ||
                other.portfolioUrl == portfolioUrl) &&
            (identical(other.providerId, providerId) ||
                other.providerId == providerId) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt) &&
            (identical(other.updatedAt, updatedAt) ||
                other.updatedAt == updatedAt) &&
            (identical(other.provider, provider) ||
                other.provider == provider));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    title,
    description,
    serviceType,
    hourlyRate,
    yearsExperience,
    rating,
    isAvailable,
    serviceArea,
    certifications,
    portfolioUrl,
    providerId,
    createdAt,
    updatedAt,
    provider,
  );

  /// Create a copy of ServiceModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$ServiceModelImplCopyWith<_$ServiceModelImpl> get copyWith =>
      __$$ServiceModelImplCopyWithImpl<_$ServiceModelImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$ServiceModelImplToJson(this);
  }
}

abstract class _ServiceModel implements ServiceModel {
  const factory _ServiceModel({
    @JsonKey(fromJson: _intFromJson) required final int id,
    @JsonKey(fromJson: _stringFromJson) required final String title,
    @JsonKey(fromJson: _stringFromJsonNullable) final String? description,
    @JsonKey(name: 'service_type', fromJson: _stringFromJson)
    required final String serviceType,
    @JsonKey(name: 'hourly_rate', fromJson: _hourlyRateFromJson)
    required final double hourlyRate,
    @JsonKey(name: 'years_experience', fromJson: _yearsExperienceFromJson)
    final int yearsExperience,
    @JsonKey(fromJson: _ratingFromJson) final double rating,
    @JsonKey(name: 'is_available', defaultValue: true) final bool isAvailable,
    @JsonKey(name: 'service_area', fromJson: _stringFromJsonNullable)
    final String? serviceArea,
    @JsonKey(fromJson: _stringFromJsonNullable) final String? certifications,
    @JsonKey(name: 'portfolio_url', fromJson: _stringFromJsonNullable)
    final String? portfolioUrl,
    @JsonKey(name: 'provider_id', fromJson: _providerIdFromJson)
    required final int providerId,
    @JsonKey(name: 'created_at') final DateTime? createdAt,
    @JsonKey(name: 'updated_at') final DateTime? updatedAt,
    @JsonKey(fromJson: _providerFromJson) final UserModel? provider,
  }) = _$ServiceModelImpl;

  factory _ServiceModel.fromJson(Map<String, dynamic> json) =
      _$ServiceModelImpl.fromJson;

  @override
  @JsonKey(fromJson: _intFromJson)
  int get id;
  @override
  @JsonKey(fromJson: _stringFromJson)
  String get title;
  @override
  @JsonKey(fromJson: _stringFromJsonNullable)
  String? get description;
  @override
  @JsonKey(name: 'service_type', fromJson: _stringFromJson)
  String get serviceType; // e.g., 'plumbing', 'electrical', 'carpentry'
  @override
  @JsonKey(name: 'hourly_rate', fromJson: _hourlyRateFromJson)
  double get hourlyRate;
  @override
  @JsonKey(name: 'years_experience', fromJson: _yearsExperienceFromJson)
  int get yearsExperience;
  @override
  @JsonKey(fromJson: _ratingFromJson)
  double get rating;
  @override
  @JsonKey(name: 'is_available', defaultValue: true)
  bool get isAvailable;
  @override
  @JsonKey(name: 'service_area', fromJson: _stringFromJsonNullable)
  String? get serviceArea;
  @override
  @JsonKey(fromJson: _stringFromJsonNullable)
  String? get certifications;
  @override
  @JsonKey(name: 'portfolio_url', fromJson: _stringFromJsonNullable)
  String? get portfolioUrl;
  @override
  @JsonKey(name: 'provider_id', fromJson: _providerIdFromJson)
  int get providerId;
  @override
  @JsonKey(name: 'created_at')
  DateTime? get createdAt;
  @override
  @JsonKey(name: 'updated_at')
  DateTime? get updatedAt; // Nested provider info (when fetched with details)
  @override
  @JsonKey(fromJson: _providerFromJson)
  UserModel? get provider;

  /// Create a copy of ServiceModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$ServiceModelImplCopyWith<_$ServiceModelImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
