// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'recommendation_model.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

RecommendationModel _$RecommendationModelFromJson(Map<String, dynamic> json) {
  return _RecommendationModel.fromJson(json);
}

/// @nodoc
mixin _$RecommendationModel {
  int get id => throw _privateConstructorUsedError;
  String get projectType =>
      throw _privateConstructorUsedError; // e.g., '2_bedroom_house', 'office_building'
  String get projectDescription => throw _privateConstructorUsedError;
  double? get totalEstimatedCost => throw _privateConstructorUsedError;
  Map<String, dynamic> get recommendationData =>
      throw _privateConstructorUsedError; // Full recommendation as JSON
  bool get isSaved => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  DateTime? get createdAt => throw _privateConstructorUsedError;
  DateTime? get updatedAt => throw _privateConstructorUsedError;

  /// Serializes this RecommendationModel to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of RecommendationModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $RecommendationModelCopyWith<RecommendationModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $RecommendationModelCopyWith<$Res> {
  factory $RecommendationModelCopyWith(
    RecommendationModel value,
    $Res Function(RecommendationModel) then,
  ) = _$RecommendationModelCopyWithImpl<$Res, RecommendationModel>;
  @useResult
  $Res call({
    int id,
    String projectType,
    String projectDescription,
    double? totalEstimatedCost,
    Map<String, dynamic> recommendationData,
    bool isSaved,
    int userId,
    DateTime? createdAt,
    DateTime? updatedAt,
  });
}

/// @nodoc
class _$RecommendationModelCopyWithImpl<$Res, $Val extends RecommendationModel>
    implements $RecommendationModelCopyWith<$Res> {
  _$RecommendationModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of RecommendationModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? projectType = null,
    Object? projectDescription = null,
    Object? totalEstimatedCost = freezed,
    Object? recommendationData = null,
    Object? isSaved = null,
    Object? userId = null,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as int,
            projectType: null == projectType
                ? _value.projectType
                : projectType // ignore: cast_nullable_to_non_nullable
                      as String,
            projectDescription: null == projectDescription
                ? _value.projectDescription
                : projectDescription // ignore: cast_nullable_to_non_nullable
                      as String,
            totalEstimatedCost: freezed == totalEstimatedCost
                ? _value.totalEstimatedCost
                : totalEstimatedCost // ignore: cast_nullable_to_non_nullable
                      as double?,
            recommendationData: null == recommendationData
                ? _value.recommendationData
                : recommendationData // ignore: cast_nullable_to_non_nullable
                      as Map<String, dynamic>,
            isSaved: null == isSaved
                ? _value.isSaved
                : isSaved // ignore: cast_nullable_to_non_nullable
                      as bool,
            userId: null == userId
                ? _value.userId
                : userId // ignore: cast_nullable_to_non_nullable
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
abstract class _$$RecommendationModelImplCopyWith<$Res>
    implements $RecommendationModelCopyWith<$Res> {
  factory _$$RecommendationModelImplCopyWith(
    _$RecommendationModelImpl value,
    $Res Function(_$RecommendationModelImpl) then,
  ) = __$$RecommendationModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    int id,
    String projectType,
    String projectDescription,
    double? totalEstimatedCost,
    Map<String, dynamic> recommendationData,
    bool isSaved,
    int userId,
    DateTime? createdAt,
    DateTime? updatedAt,
  });
}

/// @nodoc
class __$$RecommendationModelImplCopyWithImpl<$Res>
    extends _$RecommendationModelCopyWithImpl<$Res, _$RecommendationModelImpl>
    implements _$$RecommendationModelImplCopyWith<$Res> {
  __$$RecommendationModelImplCopyWithImpl(
    _$RecommendationModelImpl _value,
    $Res Function(_$RecommendationModelImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of RecommendationModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? projectType = null,
    Object? projectDescription = null,
    Object? totalEstimatedCost = freezed,
    Object? recommendationData = null,
    Object? isSaved = null,
    Object? userId = null,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(
      _$RecommendationModelImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as int,
        projectType: null == projectType
            ? _value.projectType
            : projectType // ignore: cast_nullable_to_non_nullable
                  as String,
        projectDescription: null == projectDescription
            ? _value.projectDescription
            : projectDescription // ignore: cast_nullable_to_non_nullable
                  as String,
        totalEstimatedCost: freezed == totalEstimatedCost
            ? _value.totalEstimatedCost
            : totalEstimatedCost // ignore: cast_nullable_to_non_nullable
                  as double?,
        recommendationData: null == recommendationData
            ? _value._recommendationData
            : recommendationData // ignore: cast_nullable_to_non_nullable
                  as Map<String, dynamic>,
        isSaved: null == isSaved
            ? _value.isSaved
            : isSaved // ignore: cast_nullable_to_non_nullable
                  as bool,
        userId: null == userId
            ? _value.userId
            : userId // ignore: cast_nullable_to_non_nullable
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
class _$RecommendationModelImpl implements _RecommendationModel {
  const _$RecommendationModelImpl({
    required this.id,
    required this.projectType,
    required this.projectDescription,
    this.totalEstimatedCost,
    required final Map<String, dynamic> recommendationData,
    this.isSaved = false,
    required this.userId,
    this.createdAt,
    this.updatedAt,
  }) : _recommendationData = recommendationData;

  factory _$RecommendationModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$RecommendationModelImplFromJson(json);

  @override
  final int id;
  @override
  final String projectType;
  // e.g., '2_bedroom_house', 'office_building'
  @override
  final String projectDescription;
  @override
  final double? totalEstimatedCost;
  final Map<String, dynamic> _recommendationData;
  @override
  Map<String, dynamic> get recommendationData {
    if (_recommendationData is EqualUnmodifiableMapView)
      return _recommendationData;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_recommendationData);
  }

  // Full recommendation as JSON
  @override
  @JsonKey()
  final bool isSaved;
  @override
  final int userId;
  @override
  final DateTime? createdAt;
  @override
  final DateTime? updatedAt;

  @override
  String toString() {
    return 'RecommendationModel(id: $id, projectType: $projectType, projectDescription: $projectDescription, totalEstimatedCost: $totalEstimatedCost, recommendationData: $recommendationData, isSaved: $isSaved, userId: $userId, createdAt: $createdAt, updatedAt: $updatedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$RecommendationModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.projectType, projectType) ||
                other.projectType == projectType) &&
            (identical(other.projectDescription, projectDescription) ||
                other.projectDescription == projectDescription) &&
            (identical(other.totalEstimatedCost, totalEstimatedCost) ||
                other.totalEstimatedCost == totalEstimatedCost) &&
            const DeepCollectionEquality().equals(
              other._recommendationData,
              _recommendationData,
            ) &&
            (identical(other.isSaved, isSaved) || other.isSaved == isSaved) &&
            (identical(other.userId, userId) || other.userId == userId) &&
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
    projectType,
    projectDescription,
    totalEstimatedCost,
    const DeepCollectionEquality().hash(_recommendationData),
    isSaved,
    userId,
    createdAt,
    updatedAt,
  );

  /// Create a copy of RecommendationModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$RecommendationModelImplCopyWith<_$RecommendationModelImpl> get copyWith =>
      __$$RecommendationModelImplCopyWithImpl<_$RecommendationModelImpl>(
        this,
        _$identity,
      );

  @override
  Map<String, dynamic> toJson() {
    return _$$RecommendationModelImplToJson(this);
  }
}

abstract class _RecommendationModel implements RecommendationModel {
  const factory _RecommendationModel({
    required final int id,
    required final String projectType,
    required final String projectDescription,
    final double? totalEstimatedCost,
    required final Map<String, dynamic> recommendationData,
    final bool isSaved,
    required final int userId,
    final DateTime? createdAt,
    final DateTime? updatedAt,
  }) = _$RecommendationModelImpl;

  factory _RecommendationModel.fromJson(Map<String, dynamic> json) =
      _$RecommendationModelImpl.fromJson;

  @override
  int get id;
  @override
  String get projectType; // e.g., '2_bedroom_house', 'office_building'
  @override
  String get projectDescription;
  @override
  double? get totalEstimatedCost;
  @override
  Map<String, dynamic> get recommendationData; // Full recommendation as JSON
  @override
  bool get isSaved;
  @override
  int get userId;
  @override
  DateTime? get createdAt;
  @override
  DateTime? get updatedAt;

  /// Create a copy of RecommendationModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$RecommendationModelImplCopyWith<_$RecommendationModelImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
