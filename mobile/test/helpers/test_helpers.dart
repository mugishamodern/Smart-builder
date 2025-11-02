import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/core/http/api_client.dart';
import 'package:buildsmart_mobile/core/config/app_config.dart';

/// Test helpers for setting up test environment
class TestHelpers {
  /// Initialize test environment
  static Future<void> setupTestEnvironment() async {
    // Load test environment variables
    await AppConfig.instance.load();
    
    // Initialize API client
    ApiClient.instance.initialize();
    
    // Initialize cache (mock for tests)
    // await CacheManager.initialize();
  }

  /// Create test provider container
  static ProviderContainer createTestContainer({
    List<Override>? overrides,
  }) {
    return ProviderContainer(
      overrides: overrides ?? [],
    );
  }

  /// Wait for async operations
  static Future<void> waitFor(Future<void> Function() callback) async {
    await callback();
    await Future.delayed(const Duration(milliseconds: 100));
  }
}

/// Mock API client for testing
class MockApiClient {
  static Map<String, dynamic> mockData = {};
  
  static void setMockResponse(String endpoint, dynamic response) {
    mockData[endpoint] = response;
  }
  
  static void clearMocks() {
    mockData.clear();
  }
}

