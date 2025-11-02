import 'package:freezed_annotation/freezed_annotation.dart';

part 'recommendation_model.freezed.dart';
part 'recommendation_model.g.dart';

/// Recommendation model matching Flask Recommendation model
@freezed
class RecommendationModel with _$RecommendationModel {
  const factory RecommendationModel({
    required int id,
    required String projectType, // e.g., '2_bedroom_house', 'office_building'
    required String projectDescription,
    double? totalEstimatedCost,
    required Map<String, dynamic> recommendationData, // Full recommendation as JSON
    @Default(false) bool isSaved,
    required int userId,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) = _RecommendationModel;

  factory RecommendationModel.fromJson(Map<String, dynamic> json) =>
      _$RecommendationModelFromJson(json);
}

