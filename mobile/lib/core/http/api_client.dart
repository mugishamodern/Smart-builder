import 'package:dio/dio.dart';
import 'package:dio/browser.dart';
import 'package:flutter/foundation.dart';
import 'package:buildsmart_mobile/core/config/app_config.dart';
import 'package:buildsmart_mobile/core/http/interceptors/auth_interceptor.dart';
import 'package:buildsmart_mobile/core/http/interceptors/logging_interceptor.dart';
import 'package:buildsmart_mobile/core/http/retry_interceptor.dart';
import 'package:buildsmart_mobile/core/cache/cache_interceptor.dart';

/// API client for BuildSmart backend
/// 
/// Provides a configured Dio instance with interceptors for
/// authentication, logging, and error handling.
class ApiClient {
  ApiClient._();

  static final ApiClient _instance = ApiClient._();
  static ApiClient get instance => _instance;

  late Dio _dio;

  /// Initialize the API client with base configuration
  void initialize() {
    _dio = Dio(
      BaseOptions(
        baseUrl: AppConfig.instance.apiBaseUrl,
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 30),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        // Enable sending credentials (cookies) for web
        validateStatus: (status) => status! < 500,
      ),
    );
    
    // Configure for web to send credentials
    if (kIsWeb) {
      _dio.httpClientAdapter = BrowserHttpClientAdapter(
        withCredentials: true, // Enable sending cookies
      );
    }

    // Add interceptors
    _dio.interceptors.addAll([
      LoggingInterceptor(),
      RetryInterceptor(),
      CacheInterceptor(),
      AuthInterceptor(), // Auth should be last to add tokens to retried requests
    ]);
  }

  Dio get dio => _dio;

  /// GET request
  Future<Response> get(
    String path, {
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    return _dio.get(
      path,
      queryParameters: queryParameters,
      options: options,
    );
  }

  /// POST request
  Future<Response> post(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    return _dio.post(
      path,
      data: data,
      queryParameters: queryParameters,
      options: options,
    );
  }

  /// PUT request
  Future<Response> put(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    return _dio.put(
      path,
      data: data,
      queryParameters: queryParameters,
      options: options,
    );
  }

  /// DELETE request
  Future<Response> delete(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    return _dio.delete(
      path,
      data: data,
      queryParameters: queryParameters,
      options: options,
    );
  }
}

