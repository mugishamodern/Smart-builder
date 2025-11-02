import 'package:dio/dio.dart';

/// Interceptor for adding authentication tokens to requests
/// 
/// Automatically adds session token or auth headers to API requests.
/// For Flask session-based auth, we'll use cookies; for token-based,
/// we'll add Authorization header.
class AuthInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) async {
    // TODO: Implement token retrieval from secure storage
    // For now, using session cookies (Flask default)
    // If backend switches to JWT tokens, uncomment:
    
    // final prefs = await SharedPreferences.getInstance();
    // final token = prefs.getString('auth_token');
    // if (token != null) {
    //   options.headers['Authorization'] = 'Bearer $token';
    // }

    // For Flask session-based auth, cookies are handled automatically
    // by Dio if using a CookieManager interceptor
    
    handler.next(options);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    // Handle 401 unauthorized - redirect to login
    if (err.response?.statusCode == 401) {
      // TODO: Navigate to login screen or refresh token
    }
    handler.next(err);
  }
}

