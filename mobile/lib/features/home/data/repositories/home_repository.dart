import 'package:dio/dio.dart';
import 'package:buildsmart_mobile/core/http/api_client.dart';
import 'package:buildsmart_mobile/core/constants/api_endpoints.dart';
import 'package:buildsmart_mobile/core/models/models.dart';

/// Home repository for fetching featured content
/// 
/// Fetches featured shops, products, and services for the home page
class HomeRepository {
  final ApiClient _apiClient;

  HomeRepository({ApiClient? apiClient})
      : _apiClient = apiClient ?? ApiClient.instance;

  /// Get featured shops
  /// 
  /// Returns list of verified, active shops
  Future<List<ShopModel>> getFeaturedShops({int limit = 6}) async {
    try {
      // Use nearby shops endpoint with default location (Kampala center)
      // This will return verified shops
      final response = await _apiClient.get(
        ApiEndpoints.shopsNearby,
        queryParameters: {
          'lat': 0.3476, // Kampala center
          'lon': 32.5825,
          'radius': 50.0, // Large radius to get featured shops
          'limit': limit,
        },
      );

      if (response.statusCode == 200) {
        final List<dynamic> shopsData = response.data['shops'] ?? [];
        return shopsData
            .map((json) {
              // Add missing fields that nearby endpoint might not return
              final jsonMap = Map<String, dynamic>.from(json);
              // Ensure all required fields are present
              jsonMap['latitude'] ??= 0.0;
              jsonMap['longitude'] ??= 0.0;
              jsonMap['owner_id'] ??= 0;
              jsonMap['rating'] ??= 0.0;
              jsonMap['total_reviews'] ??= 0;
              jsonMap['is_verified'] ??= true;
              jsonMap['is_active'] ??= true;
              return ShopModel.fromJson(jsonMap);
            })
            .take(limit)
            .toList();
      }
      return [];
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// Get featured products
  /// 
  /// Returns list of available products
  Future<List<ProductModel>> getFeaturedProducts({int limit = 8}) async {
    try {
      // Use product search endpoint with empty query to get all products
      final response = await _apiClient.get(
        ApiEndpoints.productsSearch,
        queryParameters: {
          'q': '',
          'page': 1,
          'per_page': limit,
        },
      );

      if (response.statusCode == 200) {
        final List<dynamic> productsData = response.data['products'] ?? [];
        return productsData
            .map((json) {
              // Ensure all required fields are present
              final jsonMap = Map<String, dynamic>.from(json);
              jsonMap['shop_id'] ??= jsonMap['shop']?['id'] ?? 0;
              jsonMap['shopId'] ??= jsonMap['shop_id'];
              return ProductModel.fromJson(jsonMap);
            })
            .take(limit)
            .toList();
      }
      return [];
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// Get featured services
  /// 
  /// Returns list of available services
  Future<List<ServiceModel>> getFeaturedServices({int limit = 6}) async {
    try {
      // Use services search endpoint
      final response = await _apiClient.get(
        ApiEndpoints.servicesSearch,
        queryParameters: {
          'q': '',
          'limit': limit,
        },
      );

      if (response.statusCode == 200) {
        final List<dynamic> servicesData = response.data['services'] ?? 
                                          response.data ?? [];
        return servicesData
            .map((json) {
              // Ensure all required fields are present
              final jsonMap = Map<String, dynamic>.from(json);
              // Extract provider_id from provider object if available
              if (jsonMap['provider'] != null && jsonMap['provider'] is Map) {
                final providerMap = Map<String, dynamic>.from(jsonMap['provider']);
                jsonMap['provider_id'] ??= providerMap['id'];
              }
              jsonMap['provider_id'] ??= 0;
              // Ensure rating and years_experience are numbers or null
              jsonMap['rating'] ??= 0.0;
              jsonMap['years_experience'] ??= 0;
              jsonMap['hourly_rate'] ??= 0.0;
              return ServiceModel.fromJson(jsonMap);
            })
            .take(limit)
            .toList();
      }
      return [];
    } on DioException {
      // If endpoint doesn't exist or fails, return empty list gracefully
      return [];
    }
  }

  /// Get product categories
  /// 
  /// Returns list of available product categories
  Future<List<String>> getCategories() async {
    try {
      final response = await _apiClient.get(ApiEndpoints.categories);

      if (response.statusCode == 200) {
        final List<dynamic> categoriesData = response.data['categories'] ?? [];
        return categoriesData.map((cat) => cat.toString()).toList();
      }
      return [];
    } on DioException {
      // If endpoint fails, return default categories
      return _getDefaultCategories();
    }
  }

  /// Default categories if API fails
  List<String> _getDefaultCategories() {
    return [
      'Cement',
      'Steel',
      'Paint',
      'Tiles',
      'Plumbing',
      'Electrical',
      'Hardware',
      'Tools',
    ];
  }

  /// Handle Dio exceptions
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
