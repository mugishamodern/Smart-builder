// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'order_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$OrderModelImpl _$$OrderModelImplFromJson(Map<String, dynamic> json) =>
    _$OrderModelImpl(
      id: (json['id'] as num).toInt(),
      orderNumber: json['orderNumber'] as String,
      status: json['status'] as String? ?? 'pending',
      totalAmount: (json['totalAmount'] as num).toDouble(),
      deliveryAddress: json['deliveryAddress'] as String?,
      deliveryNotes: json['deliveryNotes'] as String?,
      paymentStatus: json['paymentStatus'] as String? ?? 'pending',
      paymentMethod: json['paymentMethod'] as String?,
      customerId: (json['customerId'] as num).toInt(),
      shopId: (json['shopId'] as num).toInt(),
      createdAt: json['createdAt'] == null
          ? null
          : DateTime.parse(json['createdAt'] as String),
      updatedAt: json['updatedAt'] == null
          ? null
          : DateTime.parse(json['updatedAt'] as String),
      items: (json['items'] as List<dynamic>?)
          ?.map((e) => OrderItemModel.fromJson(e as Map<String, dynamic>))
          .toList(),
      shop: json['shop'] == null
          ? null
          : ShopModel.fromJson(json['shop'] as Map<String, dynamic>),
      customer: json['customer'] == null
          ? null
          : UserModel.fromJson(json['customer'] as Map<String, dynamic>),
    );

Map<String, dynamic> _$$OrderModelImplToJson(_$OrderModelImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'orderNumber': instance.orderNumber,
      'status': instance.status,
      'totalAmount': instance.totalAmount,
      'deliveryAddress': instance.deliveryAddress,
      'deliveryNotes': instance.deliveryNotes,
      'paymentStatus': instance.paymentStatus,
      'paymentMethod': instance.paymentMethod,
      'customerId': instance.customerId,
      'shopId': instance.shopId,
      'createdAt': instance.createdAt?.toIso8601String(),
      'updatedAt': instance.updatedAt?.toIso8601String(),
      'items': instance.items,
      'shop': instance.shop,
      'customer': instance.customer,
    };

_$OrderItemModelImpl _$$OrderItemModelImplFromJson(Map<String, dynamic> json) =>
    _$OrderItemModelImpl(
      id: (json['id'] as num).toInt(),
      quantity: (json['quantity'] as num).toInt(),
      unitPrice: (json['unitPrice'] as num).toDouble(),
      totalPrice: (json['totalPrice'] as num).toDouble(),
      orderId: (json['orderId'] as num).toInt(),
      productId: (json['productId'] as num).toInt(),
      product: json['product'] == null
          ? null
          : ProductModel.fromJson(json['product'] as Map<String, dynamic>),
    );

Map<String, dynamic> _$$OrderItemModelImplToJson(
  _$OrderItemModelImpl instance,
) => <String, dynamic>{
  'id': instance.id,
  'quantity': instance.quantity,
  'unitPrice': instance.unitPrice,
  'totalPrice': instance.totalPrice,
  'orderId': instance.orderId,
  'productId': instance.productId,
  'product': instance.product,
};
