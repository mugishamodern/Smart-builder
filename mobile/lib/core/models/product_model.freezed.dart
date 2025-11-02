// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'product_model.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

ProductModel _$ProductModelFromJson(Map<String, dynamic> json) {
  return _ProductModel.fromJson(json);
}

/// @nodoc
mixin _$ProductModel {
  @JsonKey(fromJson: _intFromJson)
  int get id => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _stringFromJson)
  String get name => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _stringFromJsonNullable)
  String? get description => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _stringFromJson)
  String get category => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _priceFromJson)
  double get price => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _stringFromJson)
  String get unit => throw _privateConstructorUsedError; // e.g., 'kg', 'piece', 'bag', 'm2'
  @JsonKey(
    name: 'quantity_available',
    fromJson: _quantityFromJson,
    defaultValue: 0,
  )
  int get quantityAvailable => throw _privateConstructorUsedError;
  @JsonKey(name: 'min_order_quantity', defaultValue: 1)
  int get minOrderQuantity => throw _privateConstructorUsedError;
  @JsonKey(name: 'is_available', defaultValue: true)
  bool get isAvailable => throw _privateConstructorUsedError;
  @JsonKey(name: 'image_url', fromJson: _stringFromJsonNullable)
  String? get imageUrl => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _stringFromJsonNullable)
  String? get brand => throw _privateConstructorUsedError;
  @JsonKey(fromJson: _specificationsFromJson)
  Map<String, dynamic>? get specifications =>
      throw _privateConstructorUsedError; // Additional specs as JSON
  @JsonKey(name: 'shop_id', fromJson: _intFromJson)
  int get shopId => throw _privateConstructorUsedError;
  @JsonKey(name: 'created_at')
  DateTime? get createdAt => throw _privateConstructorUsedError;
  @JsonKey(name: 'updated_at')
  DateTime? get updatedAt => throw _privateConstructorUsedError; // Nested shop info (when fetched with shop details)
  @JsonKey(fromJson: _shopFromJson)
  ShopModel? get shop => throw _privateConstructorUsedError;

  /// Serializes this ProductModel to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of ProductModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $ProductModelCopyWith<ProductModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $ProductModelCopyWith<$Res> {
  factory $ProductModelCopyWith(
    ProductModel value,
    $Res Function(ProductModel) then,
  ) = _$ProductModelCopyWithImpl<$Res, ProductModel>;
  @useResult
  $Res call({
    @JsonKey(fromJson: _intFromJson) int id,
    @JsonKey(fromJson: _stringFromJson) String name,
    @JsonKey(fromJson: _stringFromJsonNullable) String? description,
    @JsonKey(fromJson: _stringFromJson) String category,
    @JsonKey(fromJson: _priceFromJson) double price,
    @JsonKey(fromJson: _stringFromJson) String unit,
    @JsonKey(
      name: 'quantity_available',
      fromJson: _quantityFromJson,
      defaultValue: 0,
    )
    int quantityAvailable,
    @JsonKey(name: 'min_order_quantity', defaultValue: 1) int minOrderQuantity,
    @JsonKey(name: 'is_available', defaultValue: true) bool isAvailable,
    @JsonKey(name: 'image_url', fromJson: _stringFromJsonNullable)
    String? imageUrl,
    @JsonKey(fromJson: _stringFromJsonNullable) String? brand,
    @JsonKey(fromJson: _specificationsFromJson)
    Map<String, dynamic>? specifications,
    @JsonKey(name: 'shop_id', fromJson: _intFromJson) int shopId,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @JsonKey(name: 'updated_at') DateTime? updatedAt,
    @JsonKey(fromJson: _shopFromJson) ShopModel? shop,
  });

  $ShopModelCopyWith<$Res>? get shop;
}

/// @nodoc
class _$ProductModelCopyWithImpl<$Res, $Val extends ProductModel>
    implements $ProductModelCopyWith<$Res> {
  _$ProductModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of ProductModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? description = freezed,
    Object? category = null,
    Object? price = null,
    Object? unit = null,
    Object? quantityAvailable = null,
    Object? minOrderQuantity = null,
    Object? isAvailable = null,
    Object? imageUrl = freezed,
    Object? brand = freezed,
    Object? specifications = freezed,
    Object? shopId = null,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
    Object? shop = freezed,
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
            category: null == category
                ? _value.category
                : category // ignore: cast_nullable_to_non_nullable
                      as String,
            price: null == price
                ? _value.price
                : price // ignore: cast_nullable_to_non_nullable
                      as double,
            unit: null == unit
                ? _value.unit
                : unit // ignore: cast_nullable_to_non_nullable
                      as String,
            quantityAvailable: null == quantityAvailable
                ? _value.quantityAvailable
                : quantityAvailable // ignore: cast_nullable_to_non_nullable
                      as int,
            minOrderQuantity: null == minOrderQuantity
                ? _value.minOrderQuantity
                : minOrderQuantity // ignore: cast_nullable_to_non_nullable
                      as int,
            isAvailable: null == isAvailable
                ? _value.isAvailable
                : isAvailable // ignore: cast_nullable_to_non_nullable
                      as bool,
            imageUrl: freezed == imageUrl
                ? _value.imageUrl
                : imageUrl // ignore: cast_nullable_to_non_nullable
                      as String?,
            brand: freezed == brand
                ? _value.brand
                : brand // ignore: cast_nullable_to_non_nullable
                      as String?,
            specifications: freezed == specifications
                ? _value.specifications
                : specifications // ignore: cast_nullable_to_non_nullable
                      as Map<String, dynamic>?,
            shopId: null == shopId
                ? _value.shopId
                : shopId // ignore: cast_nullable_to_non_nullable
                      as int,
            createdAt: freezed == createdAt
                ? _value.createdAt
                : createdAt // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            updatedAt: freezed == updatedAt
                ? _value.updatedAt
                : updatedAt // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            shop: freezed == shop
                ? _value.shop
                : shop // ignore: cast_nullable_to_non_nullable
                      as ShopModel?,
          )
          as $Val,
    );
  }

  /// Create a copy of ProductModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $ShopModelCopyWith<$Res>? get shop {
    if (_value.shop == null) {
      return null;
    }

    return $ShopModelCopyWith<$Res>(_value.shop!, (value) {
      return _then(_value.copyWith(shop: value) as $Val);
    });
  }
}

/// @nodoc
abstract class _$$ProductModelImplCopyWith<$Res>
    implements $ProductModelCopyWith<$Res> {
  factory _$$ProductModelImplCopyWith(
    _$ProductModelImpl value,
    $Res Function(_$ProductModelImpl) then,
  ) = __$$ProductModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    @JsonKey(fromJson: _intFromJson) int id,
    @JsonKey(fromJson: _stringFromJson) String name,
    @JsonKey(fromJson: _stringFromJsonNullable) String? description,
    @JsonKey(fromJson: _stringFromJson) String category,
    @JsonKey(fromJson: _priceFromJson) double price,
    @JsonKey(fromJson: _stringFromJson) String unit,
    @JsonKey(
      name: 'quantity_available',
      fromJson: _quantityFromJson,
      defaultValue: 0,
    )
    int quantityAvailable,
    @JsonKey(name: 'min_order_quantity', defaultValue: 1) int minOrderQuantity,
    @JsonKey(name: 'is_available', defaultValue: true) bool isAvailable,
    @JsonKey(name: 'image_url', fromJson: _stringFromJsonNullable)
    String? imageUrl,
    @JsonKey(fromJson: _stringFromJsonNullable) String? brand,
    @JsonKey(fromJson: _specificationsFromJson)
    Map<String, dynamic>? specifications,
    @JsonKey(name: 'shop_id', fromJson: _intFromJson) int shopId,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @JsonKey(name: 'updated_at') DateTime? updatedAt,
    @JsonKey(fromJson: _shopFromJson) ShopModel? shop,
  });

  @override
  $ShopModelCopyWith<$Res>? get shop;
}

/// @nodoc
class __$$ProductModelImplCopyWithImpl<$Res>
    extends _$ProductModelCopyWithImpl<$Res, _$ProductModelImpl>
    implements _$$ProductModelImplCopyWith<$Res> {
  __$$ProductModelImplCopyWithImpl(
    _$ProductModelImpl _value,
    $Res Function(_$ProductModelImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of ProductModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? description = freezed,
    Object? category = null,
    Object? price = null,
    Object? unit = null,
    Object? quantityAvailable = null,
    Object? minOrderQuantity = null,
    Object? isAvailable = null,
    Object? imageUrl = freezed,
    Object? brand = freezed,
    Object? specifications = freezed,
    Object? shopId = null,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
    Object? shop = freezed,
  }) {
    return _then(
      _$ProductModelImpl(
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
        category: null == category
            ? _value.category
            : category // ignore: cast_nullable_to_non_nullable
                  as String,
        price: null == price
            ? _value.price
            : price // ignore: cast_nullable_to_non_nullable
                  as double,
        unit: null == unit
            ? _value.unit
            : unit // ignore: cast_nullable_to_non_nullable
                  as String,
        quantityAvailable: null == quantityAvailable
            ? _value.quantityAvailable
            : quantityAvailable // ignore: cast_nullable_to_non_nullable
                  as int,
        minOrderQuantity: null == minOrderQuantity
            ? _value.minOrderQuantity
            : minOrderQuantity // ignore: cast_nullable_to_non_nullable
                  as int,
        isAvailable: null == isAvailable
            ? _value.isAvailable
            : isAvailable // ignore: cast_nullable_to_non_nullable
                  as bool,
        imageUrl: freezed == imageUrl
            ? _value.imageUrl
            : imageUrl // ignore: cast_nullable_to_non_nullable
                  as String?,
        brand: freezed == brand
            ? _value.brand
            : brand // ignore: cast_nullable_to_non_nullable
                  as String?,
        specifications: freezed == specifications
            ? _value._specifications
            : specifications // ignore: cast_nullable_to_non_nullable
                  as Map<String, dynamic>?,
        shopId: null == shopId
            ? _value.shopId
            : shopId // ignore: cast_nullable_to_non_nullable
                  as int,
        createdAt: freezed == createdAt
            ? _value.createdAt
            : createdAt // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        updatedAt: freezed == updatedAt
            ? _value.updatedAt
            : updatedAt // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        shop: freezed == shop
            ? _value.shop
            : shop // ignore: cast_nullable_to_non_nullable
                  as ShopModel?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$ProductModelImpl implements _ProductModel {
  const _$ProductModelImpl({
    @JsonKey(fromJson: _intFromJson) required this.id,
    @JsonKey(fromJson: _stringFromJson) required this.name,
    @JsonKey(fromJson: _stringFromJsonNullable) this.description,
    @JsonKey(fromJson: _stringFromJson) required this.category,
    @JsonKey(fromJson: _priceFromJson) required this.price,
    @JsonKey(fromJson: _stringFromJson) required this.unit,
    @JsonKey(
      name: 'quantity_available',
      fromJson: _quantityFromJson,
      defaultValue: 0,
    )
    this.quantityAvailable = 0,
    @JsonKey(name: 'min_order_quantity', defaultValue: 1)
    this.minOrderQuantity = 1,
    @JsonKey(name: 'is_available', defaultValue: true) this.isAvailable = true,
    @JsonKey(name: 'image_url', fromJson: _stringFromJsonNullable)
    this.imageUrl,
    @JsonKey(fromJson: _stringFromJsonNullable) this.brand,
    @JsonKey(fromJson: _specificationsFromJson)
    final Map<String, dynamic>? specifications,
    @JsonKey(name: 'shop_id', fromJson: _intFromJson) required this.shopId,
    @JsonKey(name: 'created_at') this.createdAt,
    @JsonKey(name: 'updated_at') this.updatedAt,
    @JsonKey(fromJson: _shopFromJson) this.shop,
  }) : _specifications = specifications;

  factory _$ProductModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$ProductModelImplFromJson(json);

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
  final String category;
  @override
  @JsonKey(fromJson: _priceFromJson)
  final double price;
  @override
  @JsonKey(fromJson: _stringFromJson)
  final String unit;
  // e.g., 'kg', 'piece', 'bag', 'm2'
  @override
  @JsonKey(
    name: 'quantity_available',
    fromJson: _quantityFromJson,
    defaultValue: 0,
  )
  final int quantityAvailable;
  @override
  @JsonKey(name: 'min_order_quantity', defaultValue: 1)
  final int minOrderQuantity;
  @override
  @JsonKey(name: 'is_available', defaultValue: true)
  final bool isAvailable;
  @override
  @JsonKey(name: 'image_url', fromJson: _stringFromJsonNullable)
  final String? imageUrl;
  @override
  @JsonKey(fromJson: _stringFromJsonNullable)
  final String? brand;
  final Map<String, dynamic>? _specifications;
  @override
  @JsonKey(fromJson: _specificationsFromJson)
  Map<String, dynamic>? get specifications {
    final value = _specifications;
    if (value == null) return null;
    if (_specifications is EqualUnmodifiableMapView) return _specifications;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(value);
  }

  // Additional specs as JSON
  @override
  @JsonKey(name: 'shop_id', fromJson: _intFromJson)
  final int shopId;
  @override
  @JsonKey(name: 'created_at')
  final DateTime? createdAt;
  @override
  @JsonKey(name: 'updated_at')
  final DateTime? updatedAt;
  // Nested shop info (when fetched with shop details)
  @override
  @JsonKey(fromJson: _shopFromJson)
  final ShopModel? shop;

  @override
  String toString() {
    return 'ProductModel(id: $id, name: $name, description: $description, category: $category, price: $price, unit: $unit, quantityAvailable: $quantityAvailable, minOrderQuantity: $minOrderQuantity, isAvailable: $isAvailable, imageUrl: $imageUrl, brand: $brand, specifications: $specifications, shopId: $shopId, createdAt: $createdAt, updatedAt: $updatedAt, shop: $shop)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ProductModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.category, category) ||
                other.category == category) &&
            (identical(other.price, price) || other.price == price) &&
            (identical(other.unit, unit) || other.unit == unit) &&
            (identical(other.quantityAvailable, quantityAvailable) ||
                other.quantityAvailable == quantityAvailable) &&
            (identical(other.minOrderQuantity, minOrderQuantity) ||
                other.minOrderQuantity == minOrderQuantity) &&
            (identical(other.isAvailable, isAvailable) ||
                other.isAvailable == isAvailable) &&
            (identical(other.imageUrl, imageUrl) ||
                other.imageUrl == imageUrl) &&
            (identical(other.brand, brand) || other.brand == brand) &&
            const DeepCollectionEquality().equals(
              other._specifications,
              _specifications,
            ) &&
            (identical(other.shopId, shopId) || other.shopId == shopId) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt) &&
            (identical(other.updatedAt, updatedAt) ||
                other.updatedAt == updatedAt) &&
            (identical(other.shop, shop) || other.shop == shop));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    name,
    description,
    category,
    price,
    unit,
    quantityAvailable,
    minOrderQuantity,
    isAvailable,
    imageUrl,
    brand,
    const DeepCollectionEquality().hash(_specifications),
    shopId,
    createdAt,
    updatedAt,
    shop,
  );

  /// Create a copy of ProductModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$ProductModelImplCopyWith<_$ProductModelImpl> get copyWith =>
      __$$ProductModelImplCopyWithImpl<_$ProductModelImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$ProductModelImplToJson(this);
  }
}

abstract class _ProductModel implements ProductModel {
  const factory _ProductModel({
    @JsonKey(fromJson: _intFromJson) required final int id,
    @JsonKey(fromJson: _stringFromJson) required final String name,
    @JsonKey(fromJson: _stringFromJsonNullable) final String? description,
    @JsonKey(fromJson: _stringFromJson) required final String category,
    @JsonKey(fromJson: _priceFromJson) required final double price,
    @JsonKey(fromJson: _stringFromJson) required final String unit,
    @JsonKey(
      name: 'quantity_available',
      fromJson: _quantityFromJson,
      defaultValue: 0,
    )
    final int quantityAvailable,
    @JsonKey(name: 'min_order_quantity', defaultValue: 1)
    final int minOrderQuantity,
    @JsonKey(name: 'is_available', defaultValue: true) final bool isAvailable,
    @JsonKey(name: 'image_url', fromJson: _stringFromJsonNullable)
    final String? imageUrl,
    @JsonKey(fromJson: _stringFromJsonNullable) final String? brand,
    @JsonKey(fromJson: _specificationsFromJson)
    final Map<String, dynamic>? specifications,
    @JsonKey(name: 'shop_id', fromJson: _intFromJson) required final int shopId,
    @JsonKey(name: 'created_at') final DateTime? createdAt,
    @JsonKey(name: 'updated_at') final DateTime? updatedAt,
    @JsonKey(fromJson: _shopFromJson) final ShopModel? shop,
  }) = _$ProductModelImpl;

  factory _ProductModel.fromJson(Map<String, dynamic> json) =
      _$ProductModelImpl.fromJson;

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
  String get category;
  @override
  @JsonKey(fromJson: _priceFromJson)
  double get price;
  @override
  @JsonKey(fromJson: _stringFromJson)
  String get unit; // e.g., 'kg', 'piece', 'bag', 'm2'
  @override
  @JsonKey(
    name: 'quantity_available',
    fromJson: _quantityFromJson,
    defaultValue: 0,
  )
  int get quantityAvailable;
  @override
  @JsonKey(name: 'min_order_quantity', defaultValue: 1)
  int get minOrderQuantity;
  @override
  @JsonKey(name: 'is_available', defaultValue: true)
  bool get isAvailable;
  @override
  @JsonKey(name: 'image_url', fromJson: _stringFromJsonNullable)
  String? get imageUrl;
  @override
  @JsonKey(fromJson: _stringFromJsonNullable)
  String? get brand;
  @override
  @JsonKey(fromJson: _specificationsFromJson)
  Map<String, dynamic>? get specifications; // Additional specs as JSON
  @override
  @JsonKey(name: 'shop_id', fromJson: _intFromJson)
  int get shopId;
  @override
  @JsonKey(name: 'created_at')
  DateTime? get createdAt;
  @override
  @JsonKey(name: 'updated_at')
  DateTime? get updatedAt; // Nested shop info (when fetched with shop details)
  @override
  @JsonKey(fromJson: _shopFromJson)
  ShopModel? get shop;

  /// Create a copy of ProductModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$ProductModelImplCopyWith<_$ProductModelImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
