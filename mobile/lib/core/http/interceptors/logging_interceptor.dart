import 'package:dio/dio.dart';

/// Logging interceptor for debugging API requests/responses
/// 
/// Logs all API requests and responses in debug mode.
/// Should be disabled or minimized in production.
class LoggingInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    if (const bool.fromEnvironment('dart.vm.product') == false) {
      print('🚀 REQUEST[${options.method}] => PATH: ${options.path}');
      if (options.queryParameters.isNotEmpty) {
        print('   Query: ${options.queryParameters}');
      }
      if (options.data != null) {
        print('   Data: ${options.data}');
      }
    }
    handler.next(options);
  }

  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    if (const bool.fromEnvironment('dart.vm.product') == false) {
      print('✅ RESPONSE[${response.statusCode}] => PATH: ${response.requestOptions.path}');
      if (response.data != null) {
        print('   Data: ${response.data}');
      }
    }
    handler.next(response);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    if (const bool.fromEnvironment('dart.vm.product') == false) {
      print('❌ ERROR[${err.response?.statusCode}] => PATH: ${err.requestOptions.path}');
      print('   Message: ${err.message}');
      if (err.response?.data != null) {
        print('   Data: ${err.response?.data}');
      }
    }
    handler.next(err);
  }
}

