// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'shop_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$ShopModelImpl _$$ShopModelImplFromJson(Map<String, dynamic> json) =>
    _$ShopModelImpl(
      id: _intFromJson(json['id']),
      name: _stringFromJson(json['name']),
      description: _stringFromJsonNullable(json['description']),
      address: _stringFromJson(json['address']),
      phone: _stringFromJsonNullable(json['phone']),
      email: _stringFromJsonNullable(json['email']),
      latitude: _coordinateFromJson(json['latitude']),
      longitude: _coordinateFromJson(json['longitude']),
      rating: json['rating'] == null ? 0.0 : _ratingFromJson(json['rating']),
      totalReviews: json['total_reviews'] == null
          ? 0
          : _intFromJson(json['total_reviews']),
      isVerified: json['is_verified'] as bool? ?? false,
      isActive: json['is_active'] as bool? ?? true,
      ownerId: _intFromJson(json['owner_id']),
      createdAt: json['created_at'] == null
          ? null
          : DateTime.parse(json['created_at'] as String),
      updatedAt: json['updated_at'] == null
          ? null
          : DateTime.parse(json['updated_at'] as String),
    );

Map<String, dynamic> _$$ShopModelImplToJson(_$ShopModelImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'description': instance.description,
      'address': instance.address,
      'phone': instance.phone,
      'email': instance.email,
      'latitude': instance.latitude,
      'longitude': instance.longitude,
      'rating': instance.rating,
      'total_reviews': instance.totalReviews,
      'is_verified': instance.isVerified,
      'is_active': instance.isActive,
      'owner_id': instance.ownerId,
      'created_at': instance.createdAt?.toIso8601String(),
      'updated_at': instance.updatedAt?.toIso8601String(),
    };
