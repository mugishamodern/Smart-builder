// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'comparison_model.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

ComparisonModel _$ComparisonModelFromJson(Map<String, dynamic> json) {
  return _ComparisonModel.fromJson(json);
}

/// @nodoc
mixin _$ComparisonModel {
  @JsonKey(fromJson: _intFromJson)
  int get id => throw _privateConstructorUsedError;
  @JsonKey(name: 'user_id', fromJson: _intFromJson)
  int get userId => throw _privateConstructorUsedError;
  @JsonKey(name: 'product_id', fromJson: _intFromJson)
  int get productId => throw _privateConstructorUsedError;
  @JsonKey(name: 'created_at')
  DateTime? get createdAt => throw _privateConstructorUsedError; // Nested product info (when fetched with details)
  @JsonKey(fromJson: _productFromJson)
  ProductModel? get product => throw _privateConstructorUsedError;

  /// Serializes this ComparisonModel to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of ComparisonModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $ComparisonModelCopyWith<ComparisonModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $ComparisonModelCopyWith<$Res> {
  factory $ComparisonModelCopyWith(
    ComparisonModel value,
    $Res Function(ComparisonModel) then,
  ) = _$ComparisonModelCopyWithImpl<$Res, ComparisonModel>;
  @useResult
  $Res call({
    @JsonKey(fromJson: _intFromJson) int id,
    @JsonKey(name: 'user_id', fromJson: _intFromJson) int userId,
    @JsonKey(name: 'product_id', fromJson: _intFromJson) int productId,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @JsonKey(fromJson: _productFromJson) ProductModel? product,
  });

  $ProductModelCopyWith<$Res>? get product;
}

/// @nodoc
class _$ComparisonModelCopyWithImpl<$Res, $Val extends ComparisonModel>
    implements $ComparisonModelCopyWith<$Res> {
  _$ComparisonModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of ComparisonModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? productId = null,
    Object? createdAt = freezed,
    Object? product = freezed,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as int,
            userId: null == userId
                ? _value.userId
                : userId // ignore: cast_nullable_to_non_nullable
                      as int,
            productId: null == productId
                ? _value.productId
                : productId // ignore: cast_nullable_to_non_nullable
                      as int,
            createdAt: freezed == createdAt
                ? _value.createdAt
                : createdAt // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            product: freezed == product
                ? _value.product
                : product // ignore: cast_nullable_to_non_nullable
                      as ProductModel?,
          )
          as $Val,
    );
  }

  /// Create a copy of ComparisonModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $ProductModelCopyWith<$Res>? get product {
    if (_value.product == null) {
      return null;
    }

    return $ProductModelCopyWith<$Res>(_value.product!, (value) {
      return _then(_value.copyWith(product: value) as $Val);
    });
  }
}

/// @nodoc
abstract class _$$ComparisonModelImplCopyWith<$Res>
    implements $ComparisonModelCopyWith<$Res> {
  factory _$$ComparisonModelImplCopyWith(
    _$ComparisonModelImpl value,
    $Res Function(_$ComparisonModelImpl) then,
  ) = __$$ComparisonModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    @JsonKey(fromJson: _intFromJson) int id,
    @JsonKey(name: 'user_id', fromJson: _intFromJson) int userId,
    @JsonKey(name: 'product_id', fromJson: _intFromJson) int productId,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @JsonKey(fromJson: _productFromJson) ProductModel? product,
  });

  @override
  $ProductModelCopyWith<$Res>? get product;
}

/// @nodoc
class __$$ComparisonModelImplCopyWithImpl<$Res>
    extends _$ComparisonModelCopyWithImpl<$Res, _$ComparisonModelImpl>
    implements _$$ComparisonModelImplCopyWith<$Res> {
  __$$ComparisonModelImplCopyWithImpl(
    _$ComparisonModelImpl _value,
    $Res Function(_$ComparisonModelImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of ComparisonModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? productId = null,
    Object? createdAt = freezed,
    Object? product = freezed,
  }) {
    return _then(
      _$ComparisonModelImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as int,
        userId: null == userId
            ? _value.userId
            : userId // ignore: cast_nullable_to_non_nullable
                  as int,
        productId: null == productId
            ? _value.productId
            : productId // ignore: cast_nullable_to_non_nullable
                  as int,
        createdAt: freezed == createdAt
            ? _value.createdAt
            : createdAt // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        product: freezed == product
            ? _value.product
            : product // ignore: cast_nullable_to_non_nullable
                  as ProductModel?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$ComparisonModelImpl implements _ComparisonModel {
  const _$ComparisonModelImpl({
    @JsonKey(fromJson: _intFromJson) required this.id,
    @JsonKey(name: 'user_id', fromJson: _intFromJson) required this.userId,
    @JsonKey(name: 'product_id', fromJson: _intFromJson)
    required this.productId,
    @JsonKey(name: 'created_at') this.createdAt,
    @JsonKey(fromJson: _productFromJson) this.product,
  });

  factory _$ComparisonModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$ComparisonModelImplFromJson(json);

  @override
  @JsonKey(fromJson: _intFromJson)
  final int id;
  @override
  @JsonKey(name: 'user_id', fromJson: _intFromJson)
  final int userId;
  @override
  @JsonKey(name: 'product_id', fromJson: _intFromJson)
  final int productId;
  @override
  @JsonKey(name: 'created_at')
  final DateTime? createdAt;
  // Nested product info (when fetched with details)
  @override
  @JsonKey(fromJson: _productFromJson)
  final ProductModel? product;

  @override
  String toString() {
    return 'ComparisonModel(id: $id, userId: $userId, productId: $productId, createdAt: $createdAt, product: $product)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ComparisonModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.productId, productId) ||
                other.productId == productId) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt) &&
            (identical(other.product, product) || other.product == product));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode =>
      Object.hash(runtimeType, id, userId, productId, createdAt, product);

  /// Create a copy of ComparisonModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$ComparisonModelImplCopyWith<_$ComparisonModelImpl> get copyWith =>
      __$$ComparisonModelImplCopyWithImpl<_$ComparisonModelImpl>(
        this,
        _$identity,
      );

  @override
  Map<String, dynamic> toJson() {
    return _$$ComparisonModelImplToJson(this);
  }
}

abstract class _ComparisonModel implements ComparisonModel {
  const factory _ComparisonModel({
    @JsonKey(fromJson: _intFromJson) required final int id,
    @JsonKey(name: 'user_id', fromJson: _intFromJson) required final int userId,
    @JsonKey(name: 'product_id', fromJson: _intFromJson)
    required final int productId,
    @JsonKey(name: 'created_at') final DateTime? createdAt,
    @JsonKey(fromJson: _productFromJson) final ProductModel? product,
  }) = _$ComparisonModelImpl;

  factory _ComparisonModel.fromJson(Map<String, dynamic> json) =
      _$ComparisonModelImpl.fromJson;

  @override
  @JsonKey(fromJson: _intFromJson)
  int get id;
  @override
  @JsonKey(name: 'user_id', fromJson: _intFromJson)
  int get userId;
  @override
  @JsonKey(name: 'product_id', fromJson: _intFromJson)
  int get productId;
  @override
  @JsonKey(name: 'created_at')
  DateTime? get createdAt; // Nested product info (when fetched with details)
  @override
  @JsonKey(fromJson: _productFromJson)
  ProductModel? get product;

  /// Create a copy of ComparisonModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$ComparisonModelImplCopyWith<_$ComparisonModelImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
