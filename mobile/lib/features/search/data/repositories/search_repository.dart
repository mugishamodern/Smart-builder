import 'package:dio/dio.dart';
import 'package:buildsmart_mobile/core/http/api_client.dart';
import 'package:buildsmart_mobile/core/constants/api_endpoints.dart';
import 'package:buildsmart_mobile/core/models/models.dart';

/// Search repository for searching products, shops, and services
/// 
/// Provides search functionality with filters and pagination
class SearchRepository {
  final ApiClient _apiClient;

  SearchRepository({ApiClient? apiClient})
      : _apiClient = apiClient ?? ApiClient.instance;

  /// Search products
  /// 
  /// Returns paginated list of products matching query and filters
  Future<SearchResult<ProductModel>> searchProducts({
    String? query,
    String? category,
    double? minPrice,
    double? maxPrice,
    int page = 1,
    int perPage = 20,
  }) async {
    try {
      final response = await _apiClient.get(
        ApiEndpoints.productsSearch,
        queryParameters: {
          if (query != null && query.isNotEmpty) 'q': query,
          if (category != null && category.isNotEmpty) 'category': category,
          if (minPrice != null) 'min_price': minPrice,
          if (maxPrice != null) 'max_price': maxPrice,
          'page': page,
          'per_page': perPage,
        },
      );

      if (response.statusCode == 200) {
        final data = response.data;
        final List<dynamic> productsData = data['products'] ?? [];
        final products = productsData
            .map((json) => ProductModel.fromJson(json))
            .toList();

        return SearchResult(
          items: products,
          total: data['total'] ?? products.length,
          pages: data['pages'] ?? 1,
          currentPage: data['current_page'] ?? page,
        );
      }
      return SearchResult.empty();
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// Search shops
  /// 
  /// Returns list of shops matching query
  Future<List<ShopModel>> searchShops({
    String? query,
    int limit = 20,
  }) async {
    try {
      final response = await _apiClient.get(
        ApiEndpoints.shopsSearch,
        queryParameters: {
          if (query != null && query.isNotEmpty) 'q': query,
          'limit': limit,
        },
      );

      if (response.statusCode == 200) {
        final List<dynamic> shopsData = response.data['shops'] ?? [];
        return shopsData
            .map((json) => ShopModel.fromJson(json))
            .toList();
      }
      return [];
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// Search services
  /// 
  /// Returns paginated list of services matching query and filters
  Future<SearchResult<ServiceModel>> searchServices({
    String? query,
    String? serviceType,
    double? minRate,
    double? maxRate,
    int page = 1,
    int perPage = 20,
  }) async {
    try {
      final response = await _apiClient.get(
        ApiEndpoints.servicesSearch,
        queryParameters: {
          if (query != null && query.isNotEmpty) 'q': query,
          if (serviceType != null && serviceType.isNotEmpty)
            'type': serviceType,
          if (minRate != null) 'min_rate': minRate,
          if (maxRate != null) 'max_rate': maxRate,
          'page': page,
          'per_page': perPage,
        },
      );

      if (response.statusCode == 200) {
        final data = response.data;
        final List<dynamic> servicesData = data['services'] ?? [];
        final services = servicesData
            .map((json) => ServiceModel.fromJson(json))
            .toList();

        return SearchResult(
          items: services,
          total: data['total'] ?? services.length,
          pages: data['pages'] ?? 1,
          currentPage: data['current_page'] ?? page,
        );
      }
      return SearchResult.empty();
    } on DioException catch (e) {
      throw _handleError(e);
    }
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

/// Search result model with pagination
class SearchResult<T> {
  final List<T> items;
  final int total;
  final int pages;
  final int currentPage;

  SearchResult({
    required this.items,
    required this.total,
    required this.pages,
    required this.currentPage,
  });

  factory SearchResult.empty() {
    return SearchResult(
      items: [],
      total: 0,
      pages: 0,
      currentPage: 1,
    );
  }

  bool get hasMore => currentPage < pages;
}

