import 'package:dio/dio.dart';
import 'package:buildsmart_mobile/core/http/api_client.dart';
import 'package:buildsmart_mobile/core/constants/api_endpoints.dart';
import 'package:buildsmart_mobile/core/models/models.dart';

/// Nearby shops repository
/// 
/// Handles location-based shop queries
class NearbyShopsRepository {
  final ApiClient _apiClient;

  NearbyShopsRepository({ApiClient? apiClient})
      : _apiClient = apiClient ?? ApiClient.instance;

  /// Get nearby shops based on location
  Future<List<ShopModel>> getNearbyShops({
    required double latitude,
    required double longitude,
    double radius = 10.0, // radius in kilometers
    int limit = 50,
  }) async {
    try {
      final response = await _apiClient.get(
        ApiEndpoints.shopsNearby,
        queryParameters: {
          'lat': latitude,
          'lon': longitude,
          'radius': radius,
          'limit': limit,
        },
      );

      if (response.statusCode == 200) {
        final List<dynamic> shopsData = response.data['shops'] ?? [];
        final shops = shopsData
            .map((json) => ShopModel.fromJson(json))
            .toList();

        // Sort by distance if available
        shops.sort((a, b) {
          final distA = a.distanceTo(latitude, longitude);
          final distB = b.distanceTo(latitude, longitude);
          return distA.compareTo(distB);
        });

        return shops;
      }
      throw Exception('Failed to load nearby shops');
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

