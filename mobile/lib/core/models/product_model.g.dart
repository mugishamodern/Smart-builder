// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'product_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$ProductModelImpl _$$ProductModelImplFromJson(Map<String, dynamic> json) =>
    _$ProductModelImpl(
      id: _intFromJson(json['id']),
      name: _stringFromJson(json['name']),
      description: _stringFromJsonNullable(json['description']),
      category: _stringFromJson(json['category']),
      price: _priceFromJson(json['price']),
      unit: _stringFromJson(json['unit']),
      quantityAvailable: json['quantity_available'] == null
          ? 0
          : _quantityFromJson(json['quantity_available']),
      minOrderQuantity: (json['min_order_quantity'] as num?)?.toInt() ?? 1,
      isAvailable: json['is_available'] as bool? ?? true,
      imageUrl: _stringFromJsonNullable(json['image_url']),
      brand: _stringFromJsonNullable(json['brand']),
      specifications: _specificationsFromJson(json['specifications']),
      shopId: _intFromJson(json['shop_id']),
      createdAt: json['created_at'] == null
          ? null
          : DateTime.parse(json['created_at'] as String),
      updatedAt: json['updated_at'] == null
          ? null
          : DateTime.parse(json['updated_at'] as String),
      shop: _shopFromJson(json['shop']),
    );

Map<String, dynamic> _$$ProductModelImplToJson(_$ProductModelImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'description': instance.description,
      'category': instance.category,
      'price': instance.price,
      'unit': instance.unit,
      'quantity_available': instance.quantityAvailable,
      'min_order_quantity': instance.minOrderQuantity,
      'is_available': instance.isAvailable,
      'image_url': instance.imageUrl,
      'brand': instance.brand,
      'specifications': instance.specifications,
      'shop_id': instance.shopId,
      'created_at': instance.createdAt?.toIso8601String(),
      'updated_at': instance.updatedAt?.toIso8601String(),
      'shop': instance.shop,
    };
