// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'order_model.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

OrderModel _$OrderModelFromJson(Map<String, dynamic> json) {
  return _OrderModel.fromJson(json);
}

/// @nodoc
mixin _$OrderModel {
  int get id => throw _privateConstructorUsedError;
  String get orderNumber => throw _privateConstructorUsedError;
  String get status =>
      throw _privateConstructorUsedError; // pending, confirmed, processing, shipped, delivered, cancelled
  double get totalAmount => throw _privateConstructorUsedError;
  String? get deliveryAddress => throw _privateConstructorUsedError;
  String? get deliveryNotes => throw _privateConstructorUsedError;
  String get paymentStatus =>
      throw _privateConstructorUsedError; // pending, paid, failed, refunded
  String? get paymentMethod => throw _privateConstructorUsedError;
  int get customerId => throw _privateConstructorUsedError;
  int get shopId => throw _privateConstructorUsedError;
  DateTime? get createdAt => throw _privateConstructorUsedError;
  DateTime? get updatedAt =>
      throw _privateConstructorUsedError; // Nested data (when fetched with details)
  List<OrderItemModel>? get items => throw _privateConstructorUsedError;
  ShopModel? get shop => throw _privateConstructorUsedError;
  UserModel? get customer => throw _privateConstructorUsedError;

  /// Serializes this OrderModel to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of OrderModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $OrderModelCopyWith<OrderModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $OrderModelCopyWith<$Res> {
  factory $OrderModelCopyWith(
    OrderModel value,
    $Res Function(OrderModel) then,
  ) = _$OrderModelCopyWithImpl<$Res, OrderModel>;
  @useResult
  $Res call({
    int id,
    String orderNumber,
    String status,
    double totalAmount,
    String? deliveryAddress,
    String? deliveryNotes,
    String paymentStatus,
    String? paymentMethod,
    int customerId,
    int shopId,
    DateTime? createdAt,
    DateTime? updatedAt,
    List<OrderItemModel>? items,
    ShopModel? shop,
    UserModel? customer,
  });

  $ShopModelCopyWith<$Res>? get shop;
  $UserModelCopyWith<$Res>? get customer;
}

/// @nodoc
class _$OrderModelCopyWithImpl<$Res, $Val extends OrderModel>
    implements $OrderModelCopyWith<$Res> {
  _$OrderModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of OrderModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? orderNumber = null,
    Object? status = null,
    Object? totalAmount = null,
    Object? deliveryAddress = freezed,
    Object? deliveryNotes = freezed,
    Object? paymentStatus = null,
    Object? paymentMethod = freezed,
    Object? customerId = null,
    Object? shopId = null,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
    Object? items = freezed,
    Object? shop = freezed,
    Object? customer = freezed,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as int,
            orderNumber: null == orderNumber
                ? _value.orderNumber
                : orderNumber // ignore: cast_nullable_to_non_nullable
                      as String,
            status: null == status
                ? _value.status
                : status // ignore: cast_nullable_to_non_nullable
                      as String,
            totalAmount: null == totalAmount
                ? _value.totalAmount
                : totalAmount // ignore: cast_nullable_to_non_nullable
                      as double,
            deliveryAddress: freezed == deliveryAddress
                ? _value.deliveryAddress
                : deliveryAddress // ignore: cast_nullable_to_non_nullable
                      as String?,
            deliveryNotes: freezed == deliveryNotes
                ? _value.deliveryNotes
                : deliveryNotes // ignore: cast_nullable_to_non_nullable
                      as String?,
            paymentStatus: null == paymentStatus
                ? _value.paymentStatus
                : paymentStatus // ignore: cast_nullable_to_non_nullable
                      as String,
            paymentMethod: freezed == paymentMethod
                ? _value.paymentMethod
                : paymentMethod // ignore: cast_nullable_to_non_nullable
                      as String?,
            customerId: null == customerId
                ? _value.customerId
                : customerId // ignore: cast_nullable_to_non_nullable
                      as int,
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
            items: freezed == items
                ? _value.items
                : items // ignore: cast_nullable_to_non_nullable
                      as List<OrderItemModel>?,
            shop: freezed == shop
                ? _value.shop
                : shop // ignore: cast_nullable_to_non_nullable
                      as ShopModel?,
            customer: freezed == customer
                ? _value.customer
                : customer // ignore: cast_nullable_to_non_nullable
                      as UserModel?,
          )
          as $Val,
    );
  }

  /// Create a copy of OrderModel
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

  /// Create a copy of OrderModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $UserModelCopyWith<$Res>? get customer {
    if (_value.customer == null) {
      return null;
    }

    return $UserModelCopyWith<$Res>(_value.customer!, (value) {
      return _then(_value.copyWith(customer: value) as $Val);
    });
  }
}

/// @nodoc
abstract class _$$OrderModelImplCopyWith<$Res>
    implements $OrderModelCopyWith<$Res> {
  factory _$$OrderModelImplCopyWith(
    _$OrderModelImpl value,
    $Res Function(_$OrderModelImpl) then,
  ) = __$$OrderModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    int id,
    String orderNumber,
    String status,
    double totalAmount,
    String? deliveryAddress,
    String? deliveryNotes,
    String paymentStatus,
    String? paymentMethod,
    int customerId,
    int shopId,
    DateTime? createdAt,
    DateTime? updatedAt,
    List<OrderItemModel>? items,
    ShopModel? shop,
    UserModel? customer,
  });

  @override
  $ShopModelCopyWith<$Res>? get shop;
  @override
  $UserModelCopyWith<$Res>? get customer;
}

/// @nodoc
class __$$OrderModelImplCopyWithImpl<$Res>
    extends _$OrderModelCopyWithImpl<$Res, _$OrderModelImpl>
    implements _$$OrderModelImplCopyWith<$Res> {
  __$$OrderModelImplCopyWithImpl(
    _$OrderModelImpl _value,
    $Res Function(_$OrderModelImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of OrderModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? orderNumber = null,
    Object? status = null,
    Object? totalAmount = null,
    Object? deliveryAddress = freezed,
    Object? deliveryNotes = freezed,
    Object? paymentStatus = null,
    Object? paymentMethod = freezed,
    Object? customerId = null,
    Object? shopId = null,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
    Object? items = freezed,
    Object? shop = freezed,
    Object? customer = freezed,
  }) {
    return _then(
      _$OrderModelImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as int,
        orderNumber: null == orderNumber
            ? _value.orderNumber
            : orderNumber // ignore: cast_nullable_to_non_nullable
                  as String,
        status: null == status
            ? _value.status
            : status // ignore: cast_nullable_to_non_nullable
                  as String,
        totalAmount: null == totalAmount
            ? _value.totalAmount
            : totalAmount // ignore: cast_nullable_to_non_nullable
                  as double,
        deliveryAddress: freezed == deliveryAddress
            ? _value.deliveryAddress
            : deliveryAddress // ignore: cast_nullable_to_non_nullable
                  as String?,
        deliveryNotes: freezed == deliveryNotes
            ? _value.deliveryNotes
            : deliveryNotes // ignore: cast_nullable_to_non_nullable
                  as String?,
        paymentStatus: null == paymentStatus
            ? _value.paymentStatus
            : paymentStatus // ignore: cast_nullable_to_non_nullable
                  as String,
        paymentMethod: freezed == paymentMethod
            ? _value.paymentMethod
            : paymentMethod // ignore: cast_nullable_to_non_nullable
                  as String?,
        customerId: null == customerId
            ? _value.customerId
            : customerId // ignore: cast_nullable_to_non_nullable
                  as int,
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
        items: freezed == items
            ? _value._items
            : items // ignore: cast_nullable_to_non_nullable
                  as List<OrderItemModel>?,
        shop: freezed == shop
            ? _value.shop
            : shop // ignore: cast_nullable_to_non_nullable
                  as ShopModel?,
        customer: freezed == customer
            ? _value.customer
            : customer // ignore: cast_nullable_to_non_nullable
                  as UserModel?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$OrderModelImpl implements _OrderModel {
  const _$OrderModelImpl({
    required this.id,
    required this.orderNumber,
    this.status = 'pending',
    required this.totalAmount,
    this.deliveryAddress,
    this.deliveryNotes,
    this.paymentStatus = 'pending',
    this.paymentMethod,
    required this.customerId,
    required this.shopId,
    this.createdAt,
    this.updatedAt,
    final List<OrderItemModel>? items,
    this.shop,
    this.customer,
  }) : _items = items;

  factory _$OrderModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$OrderModelImplFromJson(json);

  @override
  final int id;
  @override
  final String orderNumber;
  @override
  @JsonKey()
  final String status;
  // pending, confirmed, processing, shipped, delivered, cancelled
  @override
  final double totalAmount;
  @override
  final String? deliveryAddress;
  @override
  final String? deliveryNotes;
  @override
  @JsonKey()
  final String paymentStatus;
  // pending, paid, failed, refunded
  @override
  final String? paymentMethod;
  @override
  final int customerId;
  @override
  final int shopId;
  @override
  final DateTime? createdAt;
  @override
  final DateTime? updatedAt;
  // Nested data (when fetched with details)
  final List<OrderItemModel>? _items;
  // Nested data (when fetched with details)
  @override
  List<OrderItemModel>? get items {
    final value = _items;
    if (value == null) return null;
    if (_items is EqualUnmodifiableListView) return _items;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(value);
  }

  @override
  final ShopModel? shop;
  @override
  final UserModel? customer;

  @override
  String toString() {
    return 'OrderModel(id: $id, orderNumber: $orderNumber, status: $status, totalAmount: $totalAmount, deliveryAddress: $deliveryAddress, deliveryNotes: $deliveryNotes, paymentStatus: $paymentStatus, paymentMethod: $paymentMethod, customerId: $customerId, shopId: $shopId, createdAt: $createdAt, updatedAt: $updatedAt, items: $items, shop: $shop, customer: $customer)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$OrderModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.orderNumber, orderNumber) ||
                other.orderNumber == orderNumber) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.totalAmount, totalAmount) ||
                other.totalAmount == totalAmount) &&
            (identical(other.deliveryAddress, deliveryAddress) ||
                other.deliveryAddress == deliveryAddress) &&
            (identical(other.deliveryNotes, deliveryNotes) ||
                other.deliveryNotes == deliveryNotes) &&
            (identical(other.paymentStatus, paymentStatus) ||
                other.paymentStatus == paymentStatus) &&
            (identical(other.paymentMethod, paymentMethod) ||
                other.paymentMethod == paymentMethod) &&
            (identical(other.customerId, customerId) ||
                other.customerId == customerId) &&
            (identical(other.shopId, shopId) || other.shopId == shopId) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt) &&
            (identical(other.updatedAt, updatedAt) ||
                other.updatedAt == updatedAt) &&
            const DeepCollectionEquality().equals(other._items, _items) &&
            (identical(other.shop, shop) || other.shop == shop) &&
            (identical(other.customer, customer) ||
                other.customer == customer));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    orderNumber,
    status,
    totalAmount,
    deliveryAddress,
    deliveryNotes,
    paymentStatus,
    paymentMethod,
    customerId,
    shopId,
    createdAt,
    updatedAt,
    const DeepCollectionEquality().hash(_items),
    shop,
    customer,
  );

  /// Create a copy of OrderModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$OrderModelImplCopyWith<_$OrderModelImpl> get copyWith =>
      __$$OrderModelImplCopyWithImpl<_$OrderModelImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$OrderModelImplToJson(this);
  }
}

abstract class _OrderModel implements OrderModel {
  const factory _OrderModel({
    required final int id,
    required final String orderNumber,
    final String status,
    required final double totalAmount,
    final String? deliveryAddress,
    final String? deliveryNotes,
    final String paymentStatus,
    final String? paymentMethod,
    required final int customerId,
    required final int shopId,
    final DateTime? createdAt,
    final DateTime? updatedAt,
    final List<OrderItemModel>? items,
    final ShopModel? shop,
    final UserModel? customer,
  }) = _$OrderModelImpl;

  factory _OrderModel.fromJson(Map<String, dynamic> json) =
      _$OrderModelImpl.fromJson;

  @override
  int get id;
  @override
  String get orderNumber;
  @override
  String get status; // pending, confirmed, processing, shipped, delivered, cancelled
  @override
  double get totalAmount;
  @override
  String? get deliveryAddress;
  @override
  String? get deliveryNotes;
  @override
  String get paymentStatus; // pending, paid, failed, refunded
  @override
  String? get paymentMethod;
  @override
  int get customerId;
  @override
  int get shopId;
  @override
  DateTime? get createdAt;
  @override
  DateTime? get updatedAt; // Nested data (when fetched with details)
  @override
  List<OrderItemModel>? get items;
  @override
  ShopModel? get shop;
  @override
  UserModel? get customer;

  /// Create a copy of OrderModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$OrderModelImplCopyWith<_$OrderModelImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

OrderItemModel _$OrderItemModelFromJson(Map<String, dynamic> json) {
  return _OrderItemModel.fromJson(json);
}

/// @nodoc
mixin _$OrderItemModel {
  int get id => throw _privateConstructorUsedError;
  int get quantity => throw _privateConstructorUsedError;
  double get unitPrice => throw _privateConstructorUsedError;
  double get totalPrice => throw _privateConstructorUsedError;
  int get orderId => throw _privateConstructorUsedError;
  int get productId =>
      throw _privateConstructorUsedError; // Nested product info (when fetched with details)
  ProductModel? get product => throw _privateConstructorUsedError;

  /// Serializes this OrderItemModel to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of OrderItemModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $OrderItemModelCopyWith<OrderItemModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $OrderItemModelCopyWith<$Res> {
  factory $OrderItemModelCopyWith(
    OrderItemModel value,
    $Res Function(OrderItemModel) then,
  ) = _$OrderItemModelCopyWithImpl<$Res, OrderItemModel>;
  @useResult
  $Res call({
    int id,
    int quantity,
    double unitPrice,
    double totalPrice,
    int orderId,
    int productId,
    ProductModel? product,
  });

  $ProductModelCopyWith<$Res>? get product;
}

/// @nodoc
class _$OrderItemModelCopyWithImpl<$Res, $Val extends OrderItemModel>
    implements $OrderItemModelCopyWith<$Res> {
  _$OrderItemModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of OrderItemModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? quantity = null,
    Object? unitPrice = null,
    Object? totalPrice = null,
    Object? orderId = null,
    Object? productId = null,
    Object? product = freezed,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as int,
            quantity: null == quantity
                ? _value.quantity
                : quantity // ignore: cast_nullable_to_non_nullable
                      as int,
            unitPrice: null == unitPrice
                ? _value.unitPrice
                : unitPrice // ignore: cast_nullable_to_non_nullable
                      as double,
            totalPrice: null == totalPrice
                ? _value.totalPrice
                : totalPrice // ignore: cast_nullable_to_non_nullable
                      as double,
            orderId: null == orderId
                ? _value.orderId
                : orderId // ignore: cast_nullable_to_non_nullable
                      as int,
            productId: null == productId
                ? _value.productId
                : productId // ignore: cast_nullable_to_non_nullable
                      as int,
            product: freezed == product
                ? _value.product
                : product // ignore: cast_nullable_to_non_nullable
                      as ProductModel?,
          )
          as $Val,
    );
  }

  /// Create a copy of OrderItemModel
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
abstract class _$$OrderItemModelImplCopyWith<$Res>
    implements $OrderItemModelCopyWith<$Res> {
  factory _$$OrderItemModelImplCopyWith(
    _$OrderItemModelImpl value,
    $Res Function(_$OrderItemModelImpl) then,
  ) = __$$OrderItemModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    int id,
    int quantity,
    double unitPrice,
    double totalPrice,
    int orderId,
    int productId,
    ProductModel? product,
  });

  @override
  $ProductModelCopyWith<$Res>? get product;
}

/// @nodoc
class __$$OrderItemModelImplCopyWithImpl<$Res>
    extends _$OrderItemModelCopyWithImpl<$Res, _$OrderItemModelImpl>
    implements _$$OrderItemModelImplCopyWith<$Res> {
  __$$OrderItemModelImplCopyWithImpl(
    _$OrderItemModelImpl _value,
    $Res Function(_$OrderItemModelImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of OrderItemModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? quantity = null,
    Object? unitPrice = null,
    Object? totalPrice = null,
    Object? orderId = null,
    Object? productId = null,
    Object? product = freezed,
  }) {
    return _then(
      _$OrderItemModelImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as int,
        quantity: null == quantity
            ? _value.quantity
            : quantity // ignore: cast_nullable_to_non_nullable
                  as int,
        unitPrice: null == unitPrice
            ? _value.unitPrice
            : unitPrice // ignore: cast_nullable_to_non_nullable
                  as double,
        totalPrice: null == totalPrice
            ? _value.totalPrice
            : totalPrice // ignore: cast_nullable_to_non_nullable
                  as double,
        orderId: null == orderId
            ? _value.orderId
            : orderId // ignore: cast_nullable_to_non_nullable
                  as int,
        productId: null == productId
            ? _value.productId
            : productId // ignore: cast_nullable_to_non_nullable
                  as int,
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
class _$OrderItemModelImpl implements _OrderItemModel {
  const _$OrderItemModelImpl({
    required this.id,
    required this.quantity,
    required this.unitPrice,
    required this.totalPrice,
    required this.orderId,
    required this.productId,
    this.product,
  });

  factory _$OrderItemModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$OrderItemModelImplFromJson(json);

  @override
  final int id;
  @override
  final int quantity;
  @override
  final double unitPrice;
  @override
  final double totalPrice;
  @override
  final int orderId;
  @override
  final int productId;
  // Nested product info (when fetched with details)
  @override
  final ProductModel? product;

  @override
  String toString() {
    return 'OrderItemModel(id: $id, quantity: $quantity, unitPrice: $unitPrice, totalPrice: $totalPrice, orderId: $orderId, productId: $productId, product: $product)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$OrderItemModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.quantity, quantity) ||
                other.quantity == quantity) &&
            (identical(other.unitPrice, unitPrice) ||
                other.unitPrice == unitPrice) &&
            (identical(other.totalPrice, totalPrice) ||
                other.totalPrice == totalPrice) &&
            (identical(other.orderId, orderId) || other.orderId == orderId) &&
            (identical(other.productId, productId) ||
                other.productId == productId) &&
            (identical(other.product, product) || other.product == product));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    quantity,
    unitPrice,
    totalPrice,
    orderId,
    productId,
    product,
  );

  /// Create a copy of OrderItemModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$OrderItemModelImplCopyWith<_$OrderItemModelImpl> get copyWith =>
      __$$OrderItemModelImplCopyWithImpl<_$OrderItemModelImpl>(
        this,
        _$identity,
      );

  @override
  Map<String, dynamic> toJson() {
    return _$$OrderItemModelImplToJson(this);
  }
}

abstract class _OrderItemModel implements OrderItemModel {
  const factory _OrderItemModel({
    required final int id,
    required final int quantity,
    required final double unitPrice,
    required final double totalPrice,
    required final int orderId,
    required final int productId,
    final ProductModel? product,
  }) = _$OrderItemModelImpl;

  factory _OrderItemModel.fromJson(Map<String, dynamic> json) =
      _$OrderItemModelImpl.fromJson;

  @override
  int get id;
  @override
  int get quantity;
  @override
  double get unitPrice;
  @override
  double get totalPrice;
  @override
  int get orderId;
  @override
  int get productId; // Nested product info (when fetched with details)
  @override
  ProductModel? get product;

  /// Create a copy of OrderItemModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$OrderItemModelImplCopyWith<_$OrderItemModelImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
