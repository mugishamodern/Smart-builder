// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'user_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$UserModelImpl _$$UserModelImplFromJson(Map<String, dynamic> json) =>
    _$UserModelImpl(
      id: _intFromJson(json['id']),
      username: _stringFromJson(json['username']),
      email: _stringFromJson(json['email']),
      fullName: _stringFromJsonNullable(json['full_name']),
      phone: _stringFromJsonNullable(json['phone']),
      address: _stringFromJsonNullable(json['address']),
      latitude: _coordinateFromJson(json['latitude']),
      longitude: _coordinateFromJson(json['longitude']),
      userType: json['user_type'] as String? ?? 'customer',
      isActive: json['is_active'] as bool? ?? true,
      isVerified: json['is_verified'] as bool? ?? false,
      createdAt: _dateTimeFromJsonNullable(json['created_at']),
      updatedAt: _dateTimeFromJsonNullable(json['updated_at']),
    );

Map<String, dynamic> _$$UserModelImplToJson(_$UserModelImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'username': instance.username,
      'email': instance.email,
      'full_name': instance.fullName,
      'phone': instance.phone,
      'address': instance.address,
      'latitude': instance.latitude,
      'longitude': instance.longitude,
      'user_type': instance.userType,
      'is_active': instance.isActive,
      'is_verified': instance.isVerified,
      'created_at': instance.createdAt?.toIso8601String(),
      'updated_at': instance.updatedAt?.toIso8601String(),
    };
