import 'package:dio/dio.dart';
import 'package:buildsmart_mobile/core/http/api_client.dart';
import 'package:buildsmart_mobile/core/models/models.dart';

/// Cart repository
/// 
/// Handles cart operations (add, update, remove, clear)
class CartRepository {
  final ApiClient _apiClient;

  CartRepository({ApiClient? apiClient})
      : _apiClient = apiClient ?? ApiClient.instance;

  /// Get user's cart
  Future<CartModel> getCart() async {
    try {
      final response = await _apiClient.get('/api/user/cart');

      if (response.statusCode == 200) {
        return CartModel.fromJson(response.data);
      }
      throw Exception('Failed to load cart');
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// Add product to cart
  Future<CartModel> addToCart({
    required int productId,
    required int quantity,
  }) async {
    try {
      final response = await _apiClient.post(
        '/api/user/cart/add',
        data: {
          'product_id': productId,
          'quantity': quantity,
        },
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        // API returns cart directly, not wrapped in 'cart' key
        return CartModel.fromJson(response.data);
      }
      throw Exception('Failed to add to cart');
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// Update cart item quantity
  Future<CartModel> updateCartItem({
    required int itemId,
    required int quantity,
  }) async {
    try {
      final response = await _apiClient.put(
        '/api/user/cart/item/$itemId/update',
        data: {'quantity': quantity},
      );

      if (response.statusCode == 200) {
        // API returns cart directly
        return CartModel.fromJson(response.data);
      }
      throw Exception('Failed to update cart item');
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// Remove item from cart
  Future<CartModel> removeCartItem(int itemId) async {
    try {
      final response = await _apiClient.delete('/api/user/cart/item/$itemId/remove');

      if (response.statusCode == 200) {
        // API returns cart directly
        return CartModel.fromJson(response.data);
      }
      throw Exception('Failed to remove cart item');
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// Clear cart
  Future<void> clearCart() async {
    try {
      final response = await _apiClient.post('/api/user/cart/clear');

      if (response.statusCode != 200) {
        throw Exception('Failed to clear cart');
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

/// Cart model (simplified - matches Cart API response)
class CartModel {
  final int id;
  final List<CartItemModel> items;
  final double total;

  CartModel({
    required this.id,
    required this.items,
    required this.total,
  });

  factory CartModel.fromJson(Map<String, dynamic> json) {
    final List<dynamic> itemsData = json['items'] ?? [];
    return CartModel(
      id: json['id'] ?? 0,
      items: itemsData.map((item) => CartItemModel.fromJson(item)).toList(),
      total: (json['total'] ?? json['get_total'] ?? 0.0).toDouble(),
    );
  }

  bool get isEmpty => items.isEmpty;
  bool get isNotEmpty => items.isNotEmpty;
  int get itemCount => items.fold(0, (sum, item) => sum + item.quantity);
}

/// Cart item model
class CartItemModel {
  final int id;
  final int productId;
  final int quantity;
  final double unitPrice;
  final double subtotal;
  final ProductModel? product; // Nested product info

  CartItemModel({
    required this.id,
    required this.productId,
    required this.quantity,
    required this.unitPrice,
    required this.subtotal,
    this.product,
  });

  factory CartItemModel.fromJson(Map<String, dynamic> json) {
    return CartItemModel(
      id: json['id'] ?? 0,
      productId: json['product_id'] ?? json['product']?['id'] ?? 0,
      quantity: json['quantity'] ?? 1,
      unitPrice: (json['price_snapshot'] ?? json['unit_price'] ?? json['product']?['price'] ?? 0.0).toDouble(),
      subtotal: (json['subtotal'] ?? json['get_subtotal'] ?? 0.0).toDouble(),
      product: json['product'] != null
          ? ProductModel.fromJson(json['product'])
          : null,
    );
  }
}

