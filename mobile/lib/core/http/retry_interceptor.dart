import 'package:dio/dio.dart';

/// Retry interceptor for Dio
/// 
/// Automatically retries failed requests with exponential backoff
class RetryInterceptor extends Interceptor {
  final int maxRetries;
  final Duration baseDelay;

  RetryInterceptor({
    this.maxRetries = 3,
    this.baseDelay = const Duration(seconds: 1),
  });

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    if (_shouldRetry(err) && err.requestOptions.extra['retryCount'] == null) {
      err.requestOptions.extra['retryCount'] = 0;
    }

    final retryCount = err.requestOptions.extra['retryCount'] as int? ?? 0;

    if (retryCount < maxRetries && _shouldRetry(err)) {
      final delay = Duration(
        milliseconds: (baseDelay.inMilliseconds * (1 << retryCount)),
      );

      await Future.delayed(delay);

      err.requestOptions.extra['retryCount'] = retryCount + 1;

      try {
        final dio = Dio();
        final response = await dio.fetch(err.requestOptions);
        handler.resolve(response);
        return;
      } catch (e) {
        handler.next(err);
        return;
      }
    }

    handler.next(err);
  }

  bool _shouldRetry(DioException err) {
    // Retry on network errors or 5xx server errors
    return err.type == DioExceptionType.connectionTimeout ||
        err.type == DioExceptionType.receiveTimeout ||
        err.type == DioExceptionType.connectionError ||
        (err.response?.statusCode != null &&
            err.response!.statusCode! >= 500 &&
            err.response!.statusCode! < 600);
  }
}

