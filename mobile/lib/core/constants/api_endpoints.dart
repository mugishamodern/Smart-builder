/// API endpoint constants for BuildSmart backend
/// 
/// Centralized location for all API endpoint paths.
/// All endpoints are relative to the base URL configured in AppConfig.
class ApiEndpoints {
  ApiEndpoints._();

  // Auth endpoints
  static const String login = '/api/auth/login';
  static const String register = '/api/auth/register';
  static const String logout = '/api/auth/logout';

  // User endpoints
  static const String userDashboard = '/api/user/dashboard';
  static const String userProfile = '/user/profile';
  static const String userOrders = '/api/user/orders';
  static const String userRecommendations = '/api/user/recommendations';
  static const String getRecommendation = '/user/get-recommendation';

  // Shop endpoints
  static const String shopsNearby = '/api/shops/nearby';
  static const String shopsSearch = '/api/shops/search';
  static const String shopDetail = '/shop';
  static const String shopProducts = '/api/shop';
  static const String shopDashboard = '/shop/dashboard';
  static const String shopRegister = '/shop/register';
  static const String shopInventory = '/shop';
  static const String shopAddProduct = '/shop';
  static const String shopOrders = '/shop';

  // Product endpoints
  static const String productsSearch = '/api/products/search';
  static const String categories = '/api/categories';

  // Service endpoints
  static const String servicesSearch = '/api/services/search';

  // Cart endpoints
  static const String userCart = '/api/user/cart';
  static const String addToCart = '/api/user/cart/add';
  static const String updateCartItem = '/api/user/cart/item'; // Append /{id}/update
  static const String removeCartItem = '/api/user/cart/item'; // Append /{id}/remove
  static const String clearCart = '/api/user/cart/clear';

  // Checkout endpoints
  static const String placeOrder = '/api/user/checkout/place-order';

  // Order endpoints (inferred - may need adjustment based on Flask routes)
  static const String orders = '/orders';

  // API recommendation endpoint
  static const String apiRecommend = '/api/recommend';
}

