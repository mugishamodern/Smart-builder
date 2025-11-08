// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'comparison_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$ComparisonModelImpl _$$ComparisonModelImplFromJson(
  Map<String, dynamic> json,
) => _$ComparisonModelImpl(
  id: _intFromJson(json['id']),
  userId: _intFromJson(json['user_id']),
  productId: _intFromJson(json['product_id']),
  createdAt: json['created_at'] == null
      ? null
      : DateTime.parse(json['created_at'] as String),
  product: _productFromJson(json['product']),
);

Map<String, dynamic> _$$ComparisonModelImplToJson(
  _$ComparisonModelImpl instance,
) => <String, dynamic>{
  'id': instance.id,
  'user_id': instance.userId,
  'product_id': instance.productId,
  'created_at': instance.createdAt?.toIso8601String(),
  'product': instance.product,
};
