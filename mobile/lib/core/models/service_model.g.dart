// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'service_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$ServiceModelImpl _$$ServiceModelImplFromJson(Map<String, dynamic> json) =>
    _$ServiceModelImpl(
      id: _intFromJson(json['id']),
      title: _stringFromJson(json['title']),
      description: _stringFromJsonNullable(json['description']),
      serviceType: _stringFromJson(json['service_type']),
      hourlyRate: _hourlyRateFromJson(json['hourly_rate']),
      yearsExperience: json['years_experience'] == null
          ? 0
          : _yearsExperienceFromJson(json['years_experience']),
      rating: json['rating'] == null ? 0.0 : _ratingFromJson(json['rating']),
      isAvailable: json['is_available'] as bool? ?? true,
      serviceArea: _stringFromJsonNullable(json['service_area']),
      certifications: _stringFromJsonNullable(json['certifications']),
      portfolioUrl: _stringFromJsonNullable(json['portfolio_url']),
      providerId: _providerIdFromJson(json['provider_id']),
      createdAt: json['created_at'] == null
          ? null
          : DateTime.parse(json['created_at'] as String),
      updatedAt: json['updated_at'] == null
          ? null
          : DateTime.parse(json['updated_at'] as String),
      provider: _providerFromJson(json['provider']),
    );

Map<String, dynamic> _$$ServiceModelImplToJson(_$ServiceModelImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'title': instance.title,
      'description': instance.description,
      'service_type': instance.serviceType,
      'hourly_rate': instance.hourlyRate,
      'years_experience': instance.yearsExperience,
      'rating': instance.rating,
      'is_available': instance.isAvailable,
      'service_area': instance.serviceArea,
      'certifications': instance.certifications,
      'portfolio_url': instance.portfolioUrl,
      'provider_id': instance.providerId,
      'created_at': instance.createdAt?.toIso8601String(),
      'updated_at': instance.updatedAt?.toIso8601String(),
      'provider': instance.provider,
    };
