/// Route path constants
/// 
/// Centralized route definitions for type-safe navigation.
class AppRoutes {
  AppRoutes._();

  // Public routes
  static const String home = '/';
  static const String login = '/login';
  static const String register = '/register';
  static const String search = '/search';
  static const String projects = '/projects';

  // User routes
  static const String userDashboard = '/user/dashboard';
  static const String userProfile = '/user/profile';
  static const String userOrders = '/user/orders';
  static const String userRecommendations = '/user/recommendations';

  // Shop routes
  static const String shopDashboard = '/shop/dashboard';
  static const String shopRegister = '/shop/register';
  static const String shopDetail = '/shop/:id';
  static const String shopInventory = '/shop/:id/inventory';

  // Product routes
  static const String productDetail = '/product/:id';

  // Service routes
  static const String serviceDetail = '/service/:id';

  // Order routes
  static const String cart = '/cart';
  static const String checkout = '/checkout';
  static const String orderDetail = '/order/:id';

  // Map routes
  static const String nearbyShops = '/nearby-shops';
}

