import 'package:dio/dio.dart';
import 'package:buildsmart_mobile/core/http/api_client.dart';
import 'package:buildsmart_mobile/core/constants/api_endpoints.dart';
import 'package:buildsmart_mobile/core/models/models.dart';

/// Inventory repository
/// 
/// Handles product inventory operations for shop owners
class InventoryRepository {
  final ApiClient _apiClient;

  InventoryRepository({ApiClient? apiClient})
      : _apiClient = apiClient ?? ApiClient.instance;

  /// Get shop inventory (list of products)
  Future<List<ProductModel>> getShopInventory(int shopId) async {
    try {
      final response = await _apiClient.get(
        '${ApiEndpoints.shopInventory}/$shopId/inventory',
      );

      if (response.statusCode == 200) {
        final List<dynamic> productsData = response.data['products'] ??
            response.data ??
            [];
        return productsData
            .map((json) => ProductModel.fromJson(json))
            .toList();
      }
      throw Exception('Failed to load inventory');
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// Add product to shop inventory
  Future<ProductModel> addProduct({
    required int shopId,
    required String name,
    String? description,
    required String category,
    required double price,
    required String unit,
    int quantityAvailable = 0,
    int minOrderQuantity = 1,
    bool isAvailable = true,
    String? imageUrl,
    String? brand,
    Map<String, dynamic>? specifications,
  }) async {
    try {
      final response = await _apiClient.post(
        '${ApiEndpoints.shopAddProduct}/$shopId/add-product',
        data: {
          'name': name,
          if (description != null) 'description': description,
          'category': category,
          'price': price,
          'unit': unit,
          'quantity_available': quantityAvailable,
          'min_order_quantity': minOrderQuantity,
          'is_available': isAvailable,
          if (imageUrl != null) 'image_url': imageUrl,
          if (brand != null) 'brand': brand,
          if (specifications != null) 'specifications': specifications,
        },
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        if (response.data['product'] != null) {
          return ProductModel.fromJson(response.data['product']);
        }
        throw Exception('Product data not found in response');
      }
      throw Exception('Failed to add product');
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// Update product in inventory
  Future<ProductModel> updateProduct({
    required int shopId,
    required int productId,
    String? name,
    String? description,
    String? category,
    double? price,
    String? unit,
    int? quantityAvailable,
    int? minOrderQuantity,
    bool? isAvailable,
    String? imageUrl,
    String? brand,
    Map<String, dynamic>? specifications,
  }) async {
    try {
      final response = await _apiClient.put(
        '${ApiEndpoints.shopInventory}/$shopId/products/$productId',
        data: {
          if (name != null) 'name': name,
          if (description != null) 'description': description,
          if (category != null) 'category': category,
          if (price != null) 'price': price,
          if (unit != null) 'unit': unit,
          if (quantityAvailable != null) 'quantity_available': quantityAvailable,
          if (minOrderQuantity != null) 'min_order_quantity': minOrderQuantity,
          if (isAvailable != null) 'is_available': isAvailable,
          if (imageUrl != null) 'image_url': imageUrl,
          if (brand != null) 'brand': brand,
          if (specifications != null) 'specifications': specifications,
        },
      );

      if (response.statusCode == 200) {
        return ProductModel.fromJson(response.data['product'] ??
            response.data);
      }
      throw Exception('Failed to update product');
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// Delete product from inventory
  Future<void> deleteProduct({
    required int shopId,
    required int productId,
  }) async {
    try {
      final response = await _apiClient.delete(
        '${ApiEndpoints.shopInventory}/$shopId/products/$productId',
      );

      if (response.statusCode != 200 && response.statusCode != 204) {
        throw Exception('Failed to delete product');
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

