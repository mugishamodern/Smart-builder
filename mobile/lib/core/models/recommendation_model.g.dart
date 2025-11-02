// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'recommendation_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$RecommendationModelImpl _$$RecommendationModelImplFromJson(
  Map<String, dynamic> json,
) => _$RecommendationModelImpl(
  id: (json['id'] as num).toInt(),
  projectType: json['projectType'] as String,
  projectDescription: json['projectDescription'] as String,
  totalEstimatedCost: (json['totalEstimatedCost'] as num?)?.toDouble(),
  recommendationData: json['recommendationData'] as Map<String, dynamic>,
  isSaved: json['isSaved'] as bool? ?? false,
  userId: (json['userId'] as num).toInt(),
  createdAt: json['createdAt'] == null
      ? null
      : DateTime.parse(json['createdAt'] as String),
  updatedAt: json['updatedAt'] == null
      ? null
      : DateTime.parse(json['updatedAt'] as String),
);

Map<String, dynamic> _$$RecommendationModelImplToJson(
  _$RecommendationModelImpl instance,
) => <String, dynamic>{
  'id': instance.id,
  'projectType': instance.projectType,
  'projectDescription': instance.projectDescription,
  'totalEstimatedCost': instance.totalEstimatedCost,
  'recommendationData': instance.recommendationData,
  'isSaved': instance.isSaved,
  'userId': instance.userId,
  'createdAt': instance.createdAt?.toIso8601String(),
  'updatedAt': instance.updatedAt?.toIso8601String(),
};
