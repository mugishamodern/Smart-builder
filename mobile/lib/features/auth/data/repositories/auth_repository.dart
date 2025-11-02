import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:buildsmart_mobile/core/http/api_client.dart';
import 'package:buildsmart_mobile/core/constants/api_endpoints.dart';
import 'package:buildsmart_mobile/core/models/user_model.dart';
import 'package:buildsmart_mobile/features/auth/data/models/auth_request.dart';

/// Authentication repository
/// 
/// Handles all authentication operations: login, register, logout, session management
class AuthRepository {
  final ApiClient _apiClient;
  final SharedPreferences _prefs;

  AuthRepository({
    ApiClient? apiClient,
    required SharedPreferences prefs,
  })  : _apiClient = apiClient ?? ApiClient.instance,
        _prefs = prefs;

  /// Login user
  /// 
  /// Returns UserModel on success, throws exception on failure
  Future<UserModel> login(LoginRequest request) async {
    try {
      final response = await _apiClient.post(
        ApiEndpoints.login,
        data: request.toJson(),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        // Debug: Print response structure
        print('Login response: ${response.data}');
        print('Response type: ${response.data.runtimeType}');
        
        // Handle different response formats
        dynamic userData;
        if (response.data is Map<String, dynamic>) {
          final data = response.data as Map<String, dynamic>;
          
          // Check if 'user' key exists and is a Map
          if (data.containsKey('user')) {
            final userField = data['user'];
            if (userField is Map<String, dynamic>) {
              userData = userField;
            } else if (userField is Map) {
              // Convert LinkedMap to Map<String, dynamic>
              userData = Map<String, dynamic>.from(userField);
            } else {
              // Fallback: use entire response if 'user' is not a map
              userData = data;
            }
          } else {
            // No 'user' key, use entire response
            userData = data;
          }
        } else {
          throw Exception('Unexpected response format: ${response.data.runtimeType}');
        }
        
        // Ensure userData is a Map
        if (userData is! Map<String, dynamic>) {
          if (userData is Map) {
            userData = Map<String, dynamic>.from(userData);
          } else {
            throw Exception('User data is not a valid map: ${userData.runtimeType}');
          }
        }
        
        print('Parsed user data: $userData');
        return UserModel.fromJson(userData);
      } else {
        throw Exception('Login failed: ${response.statusCode}');
      }
    } on DioException catch (e) {
      if (e.response != null) {
        print('Login error response: ${e.response?.data}');
      }
      throw _handleDioError(e);
    } catch (e, stackTrace) {
      print('Login parsing error: $e');
      print('Stack trace: $stackTrace');
      rethrow;
    }
  }

  /// Register new user
  /// 
  /// Returns UserModel on success, throws exception on failure
  Future<UserModel> register(RegisterRequest request) async {
    try {
      final response = await _apiClient.post(
        ApiEndpoints.register,
        data: request.toJson(),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        // Handle different response formats
        dynamic userData;
        if (response.data is Map<String, dynamic>) {
          final data = response.data as Map<String, dynamic>;
          
          // Check if 'user' key exists and is a Map
          if (data.containsKey('user')) {
            final userField = data['user'];
            if (userField is Map<String, dynamic>) {
              userData = userField;
            } else if (userField is Map) {
              // Convert LinkedMap to Map<String, dynamic>
              userData = Map<String, dynamic>.from(userField);
            } else {
              // Fallback: use entire response if 'user' is not a map
              userData = data;
            }
          } else {
            // No 'user' key, use entire response
            userData = data;
          }
        } else {
          throw Exception('Unexpected response format: ${response.data.runtimeType}');
        }
        
        // Ensure userData is a Map
        if (userData is! Map<String, dynamic>) {
          if (userData is Map) {
            userData = Map<String, dynamic>.from(userData);
          } else {
            throw Exception('User data is not a valid map: ${userData.runtimeType}');
          }
        }
        
        return UserModel.fromJson(userData);
      } else {
        throw Exception('Registration failed: ${response.statusCode}');
      }
    } on DioException catch (e) {
      throw _handleDioError(e);
    } catch (e, stackTrace) {
      print('Registration parsing error: $e');
      print('Stack trace: $stackTrace');
      rethrow;
    }
  }

  /// Logout user
  Future<void> logout() async {
    try {
      await _apiClient.post(ApiEndpoints.logout);
      
      // Clear stored auth data
      await _prefs.remove('auth_token');
      await _prefs.remove('user_id');
      await _prefs.remove('user_data');
    } on DioException catch (e) {
      // Even if logout fails, clear local data
      await _prefs.remove('auth_token');
      await _prefs.remove('user_id');
      await _prefs.remove('user_data');
      throw _handleDioError(e);
    }
  }

  /// Get current user from session
  Future<UserModel?> getCurrentUser() async {
    try {
      final response = await _apiClient.get(ApiEndpoints.userDashboard);
      
      if (response.statusCode == 200) {
        // Extract user from dashboard response
        // Adjust based on actual Flask response structure
        return UserModel.fromJson(response.data['user'] ?? response.data);
      }
      return null;
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        // Not authenticated
        return null;
      }
      throw _handleDioError(e);
    }
  }

  /// Check if user is authenticated
  Future<bool> isAuthenticated() async {
    try {
      final user = await getCurrentUser();
      return user != null;
    } catch (_) {
      return false;
    }
  }

  /// Handle Dio exceptions and convert to readable errors
  Exception _handleDioError(DioException e) {
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

