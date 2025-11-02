import 'package:dio/dio.dart';
import 'package:buildsmart_mobile/core/http/api_client.dart';
import 'package:buildsmart_mobile/core/constants/api_endpoints.dart';
import 'package:buildsmart_mobile/core/models/models.dart';

/// Recommendation repository
/// 
/// Handles AI recommendation operations (generate, get, save, delete)
class RecommendationRepository {
  final ApiClient _apiClient;

  RecommendationRepository({ApiClient? apiClient})
      : _apiClient = apiClient ?? ApiClient.instance;

  /// Generate AI recommendation
  Future<RecommendationResponse> generateRecommendation({
    required String projectDescription,
    String projectType = '2_bedroom_house',
    Map<String, dynamic>? customSpecs,
  }) async {
    try {
      final response = await _apiClient.post(
        ApiEndpoints.apiRecommend,
        data: {
          'project_description': projectDescription,
          'project_type': projectType,
          if (customSpecs != null) 'custom_specs': customSpecs,
        },
      );

      if (response.statusCode == 200) {
        return RecommendationResponse.fromJson(response.data);
      }
      throw Exception('Failed to generate recommendation');
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// Save recommendation
  Future<RecommendationModel> saveRecommendation({
    required String projectDescription,
    required String projectType,
    required Map<String, dynamic> recommendationData,
    double? totalEstimatedCost,
  }) async {
    try {
      // The recommendation is automatically saved when generated
      // But we can update the is_saved flag
      final response = await _apiClient.post(
        ApiEndpoints.userRecommendations,
        data: {
          'project_description': projectDescription,
          'project_type': projectType,
          'recommendation_data': recommendationData,
          if (totalEstimatedCost != null) 'total_estimated_cost': totalEstimatedCost,
        },
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        return RecommendationModel.fromJson(response.data['recommendation'] ?? response.data);
      }
      throw Exception('Failed to save recommendation');
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// Delete recommendation
  Future<void> deleteRecommendation(int recommendationId) async {
    try {
      final response = await _apiClient.delete(
        '${ApiEndpoints.userRecommendations}/$recommendationId',
      );

      if (response.statusCode != 200 && response.statusCode != 204) {
        throw Exception('Failed to delete recommendation');
      }
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Exception _handleError(DioException e) {
    if (e.response != null) {
      final message = e.response?.data['message'] ??
          e.response?.data['error'] ??
          'An error occurred';
      return Exception(message);
    } else if (e.type == DioExceptionType.connectionTimeout ||
        e.type == DioExceptionType.receiveTimeout) {
      return Exception('Connection timeout. Please check your internet.');
    } else {
      return Exception('Network error: ${e.message}');
    }
  }
}

/// Recommendation response from API
class RecommendationResponse {
  final String projectType;
  final List<MaterialRecommendation> materials;
  final CostEstimate costEstimate;
  final List<ServiceRecommendation> services;
  final List<ShoppingPlan> shoppingPlan;
  final double confidenceScore;

  RecommendationResponse({
    required this.projectType,
    required this.materials,
    required this.costEstimate,
    required this.services,
    required this.shoppingPlan,
    required this.confidenceScore,
  });

  factory RecommendationResponse.fromJson(Map<String, dynamic> json) {
    return RecommendationResponse(
      projectType: json['project_type'] ?? '2_bedroom_house',
      materials: (json['materials'] as List<dynamic>?)
              ?.map((m) => MaterialRecommendation.fromJson(m))
              .toList() ??
          [],
      costEstimate: CostEstimate.fromJson(
          json['cost_estimate'] ?? {'total': 0.0, 'breakdown': {}}),
      services: (json['services'] as List<dynamic>?)
              ?.map((s) => ServiceRecommendation.fromJson(s))
              .toList() ??
          [],
      shoppingPlan: (json['shopping_plan'] as List<dynamic>?)
              ?.map((s) => ShoppingPlan.fromJson(s))
              .toList() ??
          [],
      confidenceScore: (json['confidence_score'] ?? 0.85).toDouble(),
    );
  }
}

/// Material recommendation
class MaterialRecommendation {
  final String name;
  final String category;
  final double quantity;
  final String unit;
  final String? description;

  MaterialRecommendation({
    required this.name,
    required this.category,
    required this.quantity,
    required this.unit,
    this.description,
  });

  factory MaterialRecommendation.fromJson(Map<String, dynamic> json) {
    return MaterialRecommendation(
      name: json['name'] ?? '',
      category: json['category'] ?? '',
      quantity: (json['quantity'] ?? 0.0).toDouble(),
      unit: json['unit'] ?? 'piece',
      description: json['description'],
    );
  }
}

/// Cost estimate
class CostEstimate {
  final double total;
  final Map<String, double> breakdown;

  CostEstimate({
    required this.total,
    required this.breakdown,
  });

  factory CostEstimate.fromJson(Map<String, dynamic> json) {
    final breakdown = <String, double>{};
    if (json['breakdown'] != null) {
      (json['breakdown'] as Map<String, dynamic>).forEach((key, value) {
        breakdown[key] = (value ?? 0.0).toDouble();
      });
    }
    return CostEstimate(
      total: (json['total'] ?? 0.0).toDouble(),
      breakdown: breakdown,
    );
  }
}

/// Service recommendation
class ServiceRecommendation {
  final String serviceType;
  final String description;
  final double? estimatedCost;

  ServiceRecommendation({
    required this.serviceType,
    required this.description,
    this.estimatedCost,
  });

  factory ServiceRecommendation.fromJson(Map<String, dynamic> json) {
    return ServiceRecommendation(
      serviceType: json['service_type'] ?? '',
      description: json['description'] ?? '',
      estimatedCost: json['estimated_cost'] != null
          ? (json['estimated_cost'] as num).toDouble()
          : null,
    );
  }
}

/// Shopping plan
class ShoppingPlan {
  final int shopId;
  final String shopName;
  final double distance;
  final List<String> materials;
  final double estimatedCost;

  ShoppingPlan({
    required this.shopId,
    required this.shopName,
    required this.distance,
    required this.materials,
    required this.estimatedCost,
  });

  factory ShoppingPlan.fromJson(Map<String, dynamic> json) {
    return ShoppingPlan(
      shopId: json['shop_id'] ?? 0,
      shopName: json['shop_name'] ?? '',
      distance: (json['distance'] ?? 0.0).toDouble(),
      materials: (json['materials'] as List<dynamic>?)
              ?.map((m) => m.toString())
              .toList() ??
          [],
      estimatedCost: (json['estimated_cost'] ?? 0.0).toDouble(),
    );
  }
}

