import 'package:dio/dio.dart';
import 'package:buildsmart_mobile/core/http/api_client.dart';
import 'package:buildsmart_mobile/core/constants/api_endpoints.dart';
import 'package:buildsmart_mobile/core/models/models.dart';

/// Order repository
/// 
/// Handles order operations (create, get, list, update status)
class OrderRepository {
  final ApiClient _apiClient;

  OrderRepository({ApiClient? apiClient})
      : _apiClient = apiClient ?? ApiClient.instance;

  /// Place order (checkout)
  Future<OrderModel> placeOrder({
    required String deliveryAddress,
    String? deliveryNotes,
    String? paymentMethod,
  }) async {
    try {
      final response = await _apiClient.post(
        ApiEndpoints.placeOrder,
        data: {
          'delivery_address': deliveryAddress,
          if (deliveryNotes != null) 'delivery_notes': deliveryNotes,
          if (paymentMethod != null) 'payment_method': paymentMethod,
        },
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        // API returns {message: '...', orders: [...]} - get first order
        final data = response.data;
        if (data['orders'] != null && (data['orders'] as List).isNotEmpty) {
          // Return first order (or handle multiple orders if needed)
          final orderData = (data['orders'] as List)[0];
          return OrderModel.fromJson(orderData);
        } else if (data['order'] != null) {
          return OrderModel.fromJson(data['order']);
        } else {
          // Try parsing as single order
          return OrderModel.fromJson(data);
        }
      }
      throw Exception('Failed to place order');
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// Get order by ID
  Future<OrderModel> getOrder(int orderId) async {
    try {
      final response = await _apiClient.get('${ApiEndpoints.orders}/$orderId');

      if (response.statusCode == 200) {
        return OrderModel.fromJson(response.data['order'] ?? response.data);
      }
      throw Exception('Failed to load order');
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// Get user's orders with pagination
  Future<PaginatedOrders> getUserOrders({
    int page = 1,
    int perPage = 20,
  }) async {
    try {
      final response = await _apiClient.get(
        ApiEndpoints.userOrders,
        queryParameters: {
          'page': page,
          'per_page': perPage,
        },
      );

      if (response.statusCode == 200) {
        final data = response.data;
        final List<dynamic> ordersData = data['orders'] ?? [];
        final orders = ordersData
            .map((json) => OrderModel.fromJson(json))
            .toList();

        return PaginatedOrders(
          orders: orders,
          total: data['total'] ?? orders.length,
          pages: data['pages'] ?? 1,
          currentPage: data['current_page'] ?? page,
        );
      }
      throw Exception('Failed to load orders');
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// Update order status (for shop owners)
  Future<OrderModel> updateOrderStatus({
    required int orderId,
    required String status,
  }) async {
    try {
      final response = await _apiClient.put(
        '${ApiEndpoints.orders}/$orderId',
        data: {'status': status},
      );

      if (response.statusCode == 200) {
        return OrderModel.fromJson(response.data['order'] ?? response.data);
      }
      throw Exception('Failed to update order status');
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

/// Paginated orders
class PaginatedOrders {
  final List<OrderModel> orders;
  final int total;
  final int pages;
  final int currentPage;

  PaginatedOrders({
    required this.orders,
    required this.total,
    required this.pages,
    required this.currentPage,
  });

  bool get hasMore => currentPage < pages;
}

