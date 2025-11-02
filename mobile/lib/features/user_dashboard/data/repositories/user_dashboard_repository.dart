import 'dart:convert';
import 'package:dio/dio.dart';
import 'package:buildsmart_mobile/core/http/api_client.dart';
import 'package:buildsmart_mobile/core/constants/api_endpoints.dart';
import 'package:buildsmart_mobile/core/models/models.dart';

/// User dashboard repository
/// 
/// Handles fetching user dashboard data including stats, orders, and recommendations
class UserDashboardRepository {
  final ApiClient _apiClient;

  UserDashboardRepository({ApiClient? apiClient})
      : _apiClient = apiClient ?? ApiClient.instance;

  /// Get dashboard data (stats, recent orders, saved recommendations)
  Future<DashboardData> getDashboardData() async {
    try {
      final response = await _apiClient.get(ApiEndpoints.userDashboard);

      if (response.statusCode == 200) {
        final data = response.data;
        
        // Debug: Print response structure
        print('Dashboard response type: ${data.runtimeType}');
        print('Dashboard response: $data');
        
        // Check if response is HTML (login page redirect)
        if (data is String && data.contains('<!DOCTYPE html>')) {
          throw Exception('Authentication required. Please log in.');
        }
        
        // Ensure data is a Map
        if (data is! Map<String, dynamic>) {
          // Try to convert if it's a Map but not Map<String, dynamic>
          if (data is Map) {
            final convertedData = Map<String, dynamic>.from(data);
            return _parseDashboardData(convertedData);
          }
          print('Invalid response type: ${data.runtimeType}, expected Map<String, dynamic>');
          throw Exception('Invalid response format from server. Expected JSON object.');
        }
        
        return _parseDashboardData(data);
      }
      throw Exception('Failed to load dashboard data');
    } on DioException catch (e) {
      throw _handleError(e);
    } catch (e, stackTrace) {
      print('Dashboard error: $e');
      print('Stack trace: $stackTrace');
      rethrow;
    }
  }
  
  /// Parse dashboard data from JSON
  DashboardData _parseDashboardData(Map<String, dynamic> data) {
        
        // Parse stats - handle case where stats might be a string or map
        dynamic statsData = data['stats'];
        if (statsData is String) {
          // If stats is a string, try to parse it as JSON
          try {
            statsData = jsonDecode(statsData);
          } catch (e) {
            print('Warning: Could not parse stats string: $statsData');
            statsData = {};
          }
        }
        if (statsData is! Map) {
          statsData = {};
        }
        final stats = DashboardStats.fromJson(Map<String, dynamic>.from(statsData));

        // Parse recent orders - handle minimal order data from dashboard
        final List<dynamic> ordersData = data['recent_orders'] ?? [];
        final recentOrders = ordersData
            .map((json) {
              // Convert backend format to OrderModel format
              final orderJson = Map<String, dynamic>.from(json);
              
              // Ensure required fields have defaults
              orderJson['orderNumber'] ??= 'ORD-${orderJson['id'] ?? DateTime.now().millisecondsSinceEpoch}';
              // Note: customerId and shopId will be 0 for dashboard summary (not full order details)
              orderJson['customerId'] ??= 0;
              orderJson['shopId'] ??= 0;
              
              // Handle totalAmount conversion
              if (orderJson.containsKey('total_amount')) {
                final totalAmount = orderJson['total_amount'];
                if (totalAmount is num) {
                  orderJson['totalAmount'] = totalAmount.toDouble();
                } else if (totalAmount is String) {
                  orderJson['totalAmount'] = double.tryParse(totalAmount) ?? 0.0;
                } else {
                  orderJson['totalAmount'] = 0.0;
                }
              } else {
                orderJson['totalAmount'] = 0.0;
              }
              
              // Convert snake_case to camelCase (totalAmount already handled above)
              if (orderJson.containsKey('total_amount')) {
                orderJson.remove('total_amount');
              }
              if (orderJson.containsKey('created_at')) {
                orderJson['createdAt'] = orderJson['created_at'];
                orderJson.remove('created_at');
              }
              if (orderJson.containsKey('updated_at')) {
                orderJson['updatedAt'] = orderJson['updated_at'];
                orderJson.remove('updated_at');
              }
              if (orderJson.containsKey('customer_id')) {
                orderJson['customerId'] = orderJson['customer_id'];
                orderJson.remove('customer_id');
              }
              if (orderJson.containsKey('shop_id')) {
                orderJson['shopId'] = orderJson['shop_id'];
                orderJson.remove('shop_id');
              }
              if (orderJson.containsKey('order_number')) {
                orderJson['orderNumber'] = orderJson['order_number'];
                orderJson.remove('order_number');
              }
              
              return OrderModel.fromJson(orderJson);
            })
            .toList();

        // Parse saved recommendations - handle minimal recommendation data
        final List<dynamic> recommendationsData =
            data['saved_recommendations'] ?? [];
        final savedRecommendations = recommendationsData
            .map((json) {
              final recJson = Map<String, dynamic>.from(json);
              
              // Ensure required fields
              recJson['projectType'] ??= 'general';
              recJson['projectDescription'] ??= recJson['project_description'] ?? '';
              recJson['recommendationData'] ??= {};
              recJson['userId'] ??= recJson['user_id'] ?? 0;
              recJson['isSaved'] ??= true;
              
              // Convert snake_case to camelCase
              if (recJson.containsKey('project_description')) {
                recJson['projectDescription'] = recJson['project_description'];
                recJson.remove('project_description');
              }
              if (recJson.containsKey('total_estimated_cost')) {
                recJson['totalEstimatedCost'] = recJson['total_estimated_cost'];
                recJson.remove('total_estimated_cost');
              }
              if (recJson.containsKey('recommendation_data')) {
                recJson['recommendationData'] = recJson['recommendation_data'];
                recJson.remove('recommendation_data');
              }
              if (recJson.containsKey('is_saved')) {
                recJson['isSaved'] = recJson['is_saved'];
                recJson.remove('is_saved');
              }
              if (recJson.containsKey('user_id')) {
                recJson['userId'] = recJson['user_id'];
                recJson.remove('user_id');
              }
              if (recJson.containsKey('project_type')) {
                recJson['projectType'] = recJson['project_type'];
                recJson.remove('project_type');
              }
              if (recJson.containsKey('created_at')) {
                recJson['createdAt'] = recJson['created_at'];
                recJson.remove('created_at');
              }
              if (recJson.containsKey('updated_at')) {
                recJson['updatedAt'] = recJson['updated_at'];
                recJson.remove('updated_at');
              }
              
              return RecommendationModel.fromJson(recJson);
            })
            .toList();

        return DashboardData(
          stats: stats,
          recentOrders: recentOrders,
          savedRecommendations: savedRecommendations,
        );
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
            .map((json) {
              // Convert backend format to OrderModel format
              final orderJson = Map<String, dynamic>.from(json);
              
              // Ensure required fields have defaults
              final orderId = orderJson['id'] ?? DateTime.now().millisecondsSinceEpoch;
              orderJson['orderNumber'] ??= orderJson['order_number'] ?? 'ORD-$orderId';
              orderJson['customerId'] ??= orderJson['customer_id'] ?? 0;
              orderJson['shopId'] ??= orderJson['shop_id'] ?? 0;
              orderJson['status'] ??= 'pending';
              orderJson['paymentStatus'] ??= orderJson['payment_status'] ?? 'pending';
              
              // Handle totalAmount conversion
              if (orderJson.containsKey('total_amount')) {
                final totalAmount = orderJson['total_amount'];
                if (totalAmount is num) {
                  orderJson['totalAmount'] = totalAmount.toDouble();
                } else if (totalAmount is String) {
                  orderJson['totalAmount'] = double.tryParse(totalAmount) ?? 0.0;
                } else {
                  orderJson['totalAmount'] = 0.0;
                }
              } else {
                orderJson['totalAmount'] = 0.0;
              }
              
              // Convert snake_case to camelCase
              if (orderJson.containsKey('order_number')) {
                orderJson['orderNumber'] = orderJson['order_number'];
                orderJson.remove('order_number');
              }
              if (orderJson.containsKey('created_at')) {
                orderJson['createdAt'] = orderJson['created_at'];
                orderJson.remove('created_at');
              }
              if (orderJson.containsKey('updated_at')) {
                orderJson['updatedAt'] = orderJson['updated_at'];
                orderJson.remove('updated_at');
              }
              if (orderJson.containsKey('customer_id')) {
                orderJson['customerId'] = orderJson['customer_id'];
                orderJson.remove('customer_id');
              }
              if (orderJson.containsKey('shop_id')) {
                orderJson['shopId'] = orderJson['shop_id'];
                orderJson.remove('shop_id');
              }
              if (orderJson.containsKey('payment_status')) {
                orderJson['paymentStatus'] = orderJson['payment_status'];
                orderJson.remove('payment_status');
              }
              if (orderJson.containsKey('payment_method')) {
                orderJson['paymentMethod'] = orderJson['payment_method'];
                orderJson.remove('payment_method');
              }
              if (orderJson.containsKey('delivery_address')) {
                orderJson['deliveryAddress'] = orderJson['delivery_address'];
                orderJson.remove('delivery_address');
              }
              if (orderJson.containsKey('delivery_notes')) {
                orderJson['deliveryNotes'] = orderJson['delivery_notes'];
                orderJson.remove('delivery_notes');
              }
              
              return OrderModel.fromJson(orderJson);
            })
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

  /// Get user's recommendations with pagination
  Future<PaginatedRecommendations> getUserRecommendations({
    bool savedOnly = false,
    int page = 1,
    int perPage = 20,
  }) async {
    try {
      final response = await _apiClient.get(
        ApiEndpoints.userRecommendations,
        queryParameters: {
          if (savedOnly) 'saved': true,
          'page': page,
          'per_page': perPage,
        },
      );

      if (response.statusCode == 200) {
        final data = response.data;
        final List<dynamic> recommendationsData =
            data['recommendations'] ?? [];
        final recommendations = recommendationsData
            .map((json) {
              final recJson = Map<String, dynamic>.from(json);
              
              // Ensure required fields have defaults
              recJson['projectType'] ??= recJson['project_type'] ?? 'general';
              recJson['projectDescription'] ??= recJson['project_description'] ?? '';
              recJson['recommendationData'] ??= recJson['recommendation_data'] ?? {};
              recJson['userId'] ??= recJson['user_id'] ?? 0;
              recJson['isSaved'] ??= recJson['is_saved'] ?? false;
              
              // Handle totalEstimatedCost conversion
              if (recJson.containsKey('total_estimated_cost')) {
                final cost = recJson['total_estimated_cost'];
                if (cost == null) {
                  recJson['totalEstimatedCost'] = null;
                } else if (cost is num) {
                  recJson['totalEstimatedCost'] = cost.toDouble();
                } else if (cost is String) {
                  recJson['totalEstimatedCost'] = double.tryParse(cost);
                } else {
                  recJson['totalEstimatedCost'] = null;
                }
              }
              
              // Convert snake_case to camelCase
              if (recJson.containsKey('project_type')) {
                recJson['projectType'] = recJson['project_type'] ?? 'general';
                recJson.remove('project_type');
              }
              if (recJson.containsKey('project_description')) {
                recJson['projectDescription'] = recJson['project_description'] ?? '';
                recJson.remove('project_description');
              }
              if (recJson.containsKey('total_estimated_cost')) {
                if (!recJson.containsKey('totalEstimatedCost')) {
                  final cost = recJson['total_estimated_cost'];
                  recJson['totalEstimatedCost'] = cost == null ? null : (cost is num ? cost.toDouble() : (cost is String ? double.tryParse(cost) : null));
                }
                recJson.remove('total_estimated_cost');
              }
              if (recJson.containsKey('recommendation_data')) {
                recJson['recommendationData'] = recJson['recommendation_data'] ?? {};
                recJson.remove('recommendation_data');
              }
              if (recJson.containsKey('is_saved')) {
                recJson['isSaved'] = recJson['is_saved'] ?? false;
                recJson.remove('is_saved');
              }
              if (recJson.containsKey('user_id')) {
                recJson['userId'] = recJson['user_id'] ?? 0;
                recJson.remove('user_id');
              }
              if (recJson.containsKey('created_at')) {
                recJson['createdAt'] = recJson['created_at'];
                recJson.remove('created_at');
              }
              if (recJson.containsKey('updated_at')) {
                recJson['updatedAt'] = recJson['updated_at'];
                recJson.remove('updated_at');
              }
              
              return RecommendationModel.fromJson(recJson);
            })
            .toList();

        return PaginatedRecommendations(
          recommendations: recommendations,
          total: data['total'] ?? recommendations.length,
          pages: data['pages'] ?? 1,
          currentPage: data['current_page'] ?? page,
        );
      }
      throw Exception('Failed to load recommendations');
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

/// Dashboard data model
class DashboardData {
  final DashboardStats stats;
  final List<OrderModel> recentOrders;
  final List<RecommendationModel> savedRecommendations;

  DashboardData({
    required this.stats,
    required this.recentOrders,
    required this.savedRecommendations,
  });
}

/// Dashboard statistics
class DashboardStats {
  final int totalOrders;
  final int totalRecommendations;
  final int totalBookings;
  final double totalSpent;

  DashboardStats({
    required this.totalOrders,
    required this.totalRecommendations,
    required this.totalBookings,
    required this.totalSpent,
  });

  factory DashboardStats.fromJson(Map<String, dynamic> json) {
    return DashboardStats(
      totalOrders: _intFromJson(json['total_orders']),
      totalRecommendations: _intFromJson(json['total_recommendations']),
      totalBookings: _intFromJson(json['total_bookings']),
      totalSpent: _doubleFromJson(json['total_spent']),
    );
  }
}

/// Helper function to convert int from JSON (handles null, string, and number)
int _intFromJson(dynamic value) {
  if (value == null) return 0;
  if (value is num) return value.toInt();
  if (value is String) {
    try {
      return int.parse(value);
    } catch (e) {
      print('Warning: Could not parse int from string: $value');
      return 0;
    }
  }
  throw ArgumentError('Int must be a number or string, got ${value.runtimeType}');
}

/// Helper function to convert double from JSON (handles null, string, and number)
double _doubleFromJson(dynamic value) {
  if (value == null) return 0.0;
  if (value is num) return value.toDouble();
  if (value is String) {
    try {
      return double.parse(value);
    } catch (e) {
      print('Warning: Could not parse double from string: $value');
      return 0.0;
    }
  }
  throw ArgumentError('Double must be a number or string, got ${value.runtimeType}');
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

/// Paginated recommendations
class PaginatedRecommendations {
  final List<RecommendationModel> recommendations;
  final int total;
  final int pages;
  final int currentPage;

  PaginatedRecommendations({
    required this.recommendations,
    required this.total,
    required this.pages,
    required this.currentPage,
  });

  bool get hasMore => currentPage < pages;
}

