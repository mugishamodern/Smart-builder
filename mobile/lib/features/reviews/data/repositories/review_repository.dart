import 'package:dio/dio.dart';
import 'package:buildsmart_mobile/core/http/api_client.dart';
import 'package:buildsmart_mobile/core/models/user_model.dart';

/// Review repository
/// 
/// Handles review operations (get, submit)
class ReviewRepository {
  final ApiClient _apiClient;

  ReviewRepository({ApiClient? apiClient})
      : _apiClient = apiClient ?? ApiClient.instance;

  /// Get reviews for a shop
  Future<List<ReviewModel>> getShopReviews(int shopId) async {
    try {
      final response = await _apiClient.get('/api/shop/$shopId/reviews');

      if (response.statusCode == 200) {
        final List<dynamic> reviewsData = response.data['reviews'] ?? [];
        return reviewsData
            .map((json) => ReviewModel.fromJson(json))
            .toList();
      }
      return [];
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// Submit a review
  Future<ReviewModel> submitReview({
    required int shopId,
    required int rating,
    required String comment,
  }) async {
    try {
      final response = await _apiClient.post(
        '/api/reviews/submit',
        data: {
          'shop_id': shopId,
          'rating': rating,
          'comment': comment,
        },
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        return ReviewModel.fromJson(response.data['review'] ?? response.data);
      }
      throw Exception('Failed to submit review');
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

/// Review model (simplified - matches Review API response)
class ReviewModel {
  final int id;
  final int shopId;
  final int userId;
  final int rating;
  final String comment;
  final DateTime createdAt;
  final UserModel? user; // Nested user info

  ReviewModel({
    required this.id,
    required this.shopId,
    required this.userId,
    required this.rating,
    required this.comment,
    required this.createdAt,
    this.user,
  });

  factory ReviewModel.fromJson(Map<String, dynamic> json) {
    return ReviewModel(
      id: json['id'] ?? 0,
      shopId: json['shop_id'] ?? 0,
      userId: json['user_id'] ?? 0,
      rating: json['rating'] ?? 0,
      comment: json['comment'] ?? '',
      createdAt: json['created_at'] != null
          ? DateTime.parse(json['created_at'])
          : DateTime.now(),
      user: json['user'] != null
          ? UserModel.fromJson(json['user'])
          : null,
    );
  }
}

