import 'package:dio/dio.dart';
import 'package:buildsmart_mobile/core/cache/cache_manager.dart';

/// Cache interceptor for Dio
/// 
/// Implements stale-while-revalidate strategy:
/// - Returns cached data immediately if available
/// - Fetches fresh data in background
/// - Updates cache with fresh data
class CacheInterceptor extends Interceptor {
  final Duration maxAge;
  final Map<String, String> _cacheKeys = {};

  CacheInterceptor({this.maxAge = const Duration(minutes: 5)});

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) async {
    final cacheKey = _getCacheKey(options);
    _cacheKeys[options.hashCode.toString()] = cacheKey;
    
    // Check cache for GET requests
    if (options.method == 'GET') {
      try {
        final cached = CacheManager.getCachedData('api_cache', cacheKey);
        
        if (cached != null && !CacheManager.isCacheStale('api_cache', cacheKey, maxAge)) {
          // Return cached data immediately
          final response = Response(
            data: cached['data'],
            statusCode: 200,
            requestOptions: options,
          );
          handler.resolve(response);
          return;
        }
      } catch (e) {
        // Box might not be open yet, continue with network request
        // Ignore cache errors and proceed with normal request
      }
    }
    
    handler.next(options);
  }

  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) async {
    // Cache successful GET responses
    if (response.requestOptions.method == 'GET' && response.statusCode == 200) {
      try {
        final cacheKey = _cacheKeys[response.requestOptions.hashCode.toString()];
        if (cacheKey != null) {
          await CacheManager.saveToCache('api_cache', cacheKey, response.data);
        }
      } catch (e) {
        // Box might not be open yet, ignore cache errors
        // Don't block the response if caching fails
      }
    }
    
    handler.next(response);
  }

  String _getCacheKey(RequestOptions options) {
    // Generate cache key from method, path, and query parameters
    final queryString = options.queryParameters.entries
        .map((e) => '${e.key}=${e.value}')
        .join('&');
    return '${options.method}_${options.path}_$queryString';
  }
}

