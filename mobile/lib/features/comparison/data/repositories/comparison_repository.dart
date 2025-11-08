import 'package:dio/dio.dart';
import 'package:buildsmart_mobile/core/http/api_client.dart';
import 'package:buildsmart_mobile/core/constants/api_endpoints.dart';
import 'package:buildsmart_mobile/core/models/models.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';

/// Comparison repository for managing product comparisons
class ComparisonRepository {
  final ApiClient _apiClient;
  static const String _guestComparisonsKey = 'guest_comparisons';

  ComparisonRepository({ApiClient? apiClient})
      : _apiClient = apiClient ?? ApiClient.instance;

  /// Get all comparisons for current user (or guest)
  Future<List<ComparisonModel>> getComparisons({bool isGuest = false}) async {
    if (isGuest) {
      return _getGuestComparisons();
    }

    try {
      final response = await _apiClient.get(
        ApiEndpoints.comparisons,
      );

      if (response.statusCode == 200 && response.data['success'] == true) {
        final List<dynamic> comparisonsData = response.data['products'] ?? [];
        return comparisonsData
            .map((json) => ComparisonModel.fromJson(json))
            .toList();
      }
      return [];
    } on DioException catch (e) {
      throw Exception(e.response?.data['message'] ?? 'Failed to fetch comparisons');
    }
  }

  /// Add product to comparison
  Future<void> addToComparison({
    required int productId,
    bool isGuest = false,
  }) async {
    if (isGuest) {
      await _addGuestComparison(productId);
      return;
    }

    try {
      await _apiClient.post(
        ApiEndpoints.comparisonsAdd,
        data: {'product_id': productId},
      );
    } on DioException catch (e) {
      throw Exception(e.response?.data['message'] ?? 'Failed to add to comparison');
    }
  }

  /// Remove product from comparison
  Future<void> removeFromComparison({
    required int productId,
    bool isGuest = false,
  }) async {
    if (isGuest) {
      await _removeGuestComparison(productId);
      return;
    }

    try {
      await _apiClient.delete(
        '${ApiEndpoints.comparisonsRemove}/$productId/remove',
      );
    } on DioException catch (e) {
      throw Exception(e.response?.data['message'] ?? 'Failed to remove from comparison');
    }
  }

  /// Clear all comparisons
  Future<void> clearComparisons({bool isGuest = false}) async {
    if (isGuest) {
      await _clearGuestComparisons();
      return;
    }

    try {
      await _apiClient.delete(ApiEndpoints.comparisonsClear);
    } on DioException catch (e) {
      throw Exception(e.response?.data['message'] ?? 'Failed to clear comparisons');
    }
  }

  // Guest comparison methods using SharedPreferences

  Future<List<ComparisonModel>> _getGuestComparisons() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final String? jsonString = prefs.getString(_guestComparisonsKey);
      if (jsonString == null) return [];

      final List<dynamic> jsonList = json.decode(jsonString);
      return jsonList
          .map((json) => ComparisonModel.fromJson(json))
          .toList();
    } catch (e) {
      return [];
    }
  }

  Future<void> _addGuestComparison(int productId) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final comparisons = await _getGuestComparisons();

      // Check if already exists
      if (comparisons.any((c) => c.productId == productId)) {
        return;
      }

      final newComparison = ComparisonModel(
        id: DateTime.now().millisecondsSinceEpoch,
        userId: 0, // Guest user
        productId: productId,
        createdAt: DateTime.now(),
      );

      comparisons.add(newComparison);
      final jsonString = json.encode(
        comparisons.map((c) => c.toJson()).toList(),
      );
      await prefs.setString(_guestComparisonsKey, jsonString);
    } catch (e) {
      throw Exception('Failed to save guest comparison: $e');
    }
  }

  Future<void> _removeGuestComparison(int productId) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final comparisons = await _getGuestComparisons();
      comparisons.removeWhere((c) => c.productId == productId);

      final jsonString = json.encode(
        comparisons.map((c) => c.toJson()).toList(),
      );
      await prefs.setString(_guestComparisonsKey, jsonString);
    } catch (e) {
      throw Exception('Failed to remove guest comparison: $e');
    }
  }

  Future<void> _clearGuestComparisons() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove(_guestComparisonsKey);
    } catch (e) {
      throw Exception('Failed to clear guest comparisons: $e');
    }
  }

  /// Sync guest comparisons to server after login
  Future<void> syncGuestComparisons() async {
    try {
      final guestComparisons = await _getGuestComparisons();
      if (guestComparisons.isEmpty) return;

      // Add each guest comparison to server
      for (final comparison in guestComparisons) {
        try {
          await _apiClient.post(
            ApiEndpoints.comparisonsAdd,
            data: {'product_id': comparison.productId},
          );
        } catch (e) {
          // Continue with other comparisons even if one fails
          continue;
        }
      }

      // Clear guest comparisons after syncing
      await _clearGuestComparisons();
    } catch (e) {
      // If sync fails, guest comparisons remain in SharedPreferences
      // They can be synced later
      throw Exception('Failed to sync guest comparisons: $e');
    }
  }
}
