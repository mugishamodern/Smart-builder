import 'package:dio/dio.dart';
import 'package:buildsmart_mobile/core/http/api_client.dart';
import 'package:buildsmart_mobile/core/constants/api_endpoints.dart';
import 'package:buildsmart_mobile/core/models/models.dart';

/// Shop dashboard repository
/// 
/// Handles fetching shop dashboard data including shops, stats, and orders
class ShopDashboardRepository {
  final ApiClient _apiClient;

  ShopDashboardRepository({ApiClient? apiClient})
      : _apiClient = apiClient ?? ApiClient.instance;

  /// Get shop dashboard data (shops, recent orders)
  Future<ShopDashboardData> getDashboardData() async {
    try {
      final response = await _apiClient.get(ApiEndpoints.shopDashboard);

      if (response.statusCode == 200) {
        final data = response.data;

        // Parse shops
        final List<dynamic> shopsData = data['shops'] ?? [];
        final shops = shopsData
            .map((json) => ShopModel.fromJson(json))
            .toList();

        // Parse recent orders
        final List<dynamic> ordersData = data['recent_orders'] ?? [];
        final recentOrders = ordersData
            .map((json) => OrderModel.fromJson(json))
            .toList();

        // Calculate stats
        final stats = _calculateStats(shops, recentOrders);

        return ShopDashboardData(
          shops: shops,
          recentOrders: recentOrders,
          stats: stats,
        );
      }
      throw Exception('Failed to load dashboard data');
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// Calculate statistics from shops and orders
  ShopDashboardStats _calculateStats(
    List<ShopModel> shops,
    List<OrderModel> orders,
  ) {
    // Total products (sum of products count from shops)
    // Note: If shop model doesn't have products count, we'd need to fetch it
    int totalProducts = 0; // Will be calculated if products are included

    // Total sales
    double totalSales = orders.fold(0.0, (sum, order) => sum + order.totalAmount);

    // Average shop rating
    double avgRating = 0.0;
    if (shops.isNotEmpty) {
      final totalRating = shops.fold(0.0, (sum, shop) => sum + shop.rating);
      avgRating = totalRating / shops.length;
    }

    // Total unique customers
    final uniqueCustomers = orders.map((o) => o.customerId).toSet().length;

    return ShopDashboardStats(
      totalProducts: totalProducts,
      totalSales: totalSales,
      avgRating: avgRating,
      totalCustomers: uniqueCustomers,
    );
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

/// Shop dashboard data model
class ShopDashboardData {
  final List<ShopModel> shops;
  final List<OrderModel> recentOrders;
  final ShopDashboardStats stats;

  ShopDashboardData({
    required this.shops,
    required this.recentOrders,
    required this.stats,
  });
}

/// Shop dashboard statistics
class ShopDashboardStats {
  final int totalProducts;
  final double totalSales;
  final double avgRating;
  final int totalCustomers;

  ShopDashboardStats({
    required this.totalProducts,
    required this.totalSales,
    required this.avgRating,
    required this.totalCustomers,
  });
}

