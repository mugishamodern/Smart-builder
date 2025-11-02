import 'package:hive_flutter/hive_flutter.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Cache manager for offline data persistence
/// 
/// Manages Hive boxes for cached data and handles cache invalidation
class CacheManager {
  static const String _cacheVersionKey = 'cache_version';
  static const int _currentCacheVersion = 1;

  /// Initialize cache (Hive boxes)
  static Future<void> initialize() async {
    await Hive.initFlutter();
    
    // Register adapters if needed
    // TODO: Register Hive adapters for models
    
    // Open boxes
    await Hive.openBox('shops');
    await Hive.openBox('products');
    await Hive.openBox('services');
    await Hive.openBox('orders');
    await Hive.openBox('recommendations');
    await Hive.openBox('api_cache');
    
    // Check and migrate cache if needed
    await _checkCacheVersion();
  }

  /// Check cache version and migrate if needed
  static Future<void> _checkCacheVersion() async {
    final prefs = await SharedPreferences.getInstance();
    final storedVersion = prefs.getInt(_cacheVersionKey) ?? 0;
    
    if (storedVersion < _currentCacheVersion) {
      // Clear old cache
      await clearCache();
      await prefs.setInt(_cacheVersionKey, _currentCacheVersion);
    }
  }

  /// Clear all cached data
  static Future<void> clearCache() async {
    final boxes = ['shops', 'products', 'services', 'orders', 'recommendations', 'api_cache'];
    for (final boxName in boxes) {
      try {
        final box = Hive.box(boxName);
        await box.clear();
      } catch (e) {
        // Box might not be opened yet, ignore
      }
    }
  }

  /// Get cache box
  static Box getBox(String boxName) {
    return Hive.box(boxName);
  }

  /// Check if data exists in cache
  static bool hasData(String boxName, String key) {
    final box = Hive.box(boxName);
    return box.containsKey(key);
  }

  /// Get cached data
  static dynamic getCachedData(String boxName, String key) {
    final box = Hive.box(boxName);
    return box.get(key);
  }

  /// Save data to cache
  static Future<void> saveToCache(String boxName, String key, dynamic data) async {
    try {
      final box = Hive.box(boxName);
      await box.put(key, {
        'data': data,
        'timestamp': DateTime.now().toIso8601String(),
      });
    } catch (e) {
      // Box not open yet, ignore cache save errors
    }
  }

  /// Check if cache is stale
  static bool isCacheStale(String boxName, String key, Duration maxAge) {
    try {
      final box = Hive.box(boxName);
      final cached = box.get(key);
      
      if (cached == null) return true;
      
      final timestamp = DateTime.parse(cached['timestamp']);
      final age = DateTime.now().difference(timestamp);
      
      return age > maxAge;
    } catch (e) {
      // Box not open yet, consider cache stale
      return true;
    }
  }

  /// Close all boxes
  static Future<void> closeCache() async {
    await Hive.close();
  }
}

