import 'package:go_router/go_router.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/features/auth/presentation/pages/login_page.dart';
import 'package:buildsmart_mobile/features/auth/presentation/pages/register_page.dart';
import 'package:buildsmart_mobile/features/home/presentation/pages/home_page.dart';
import 'package:buildsmart_mobile/features/search/presentation/pages/search_page.dart';
import 'package:buildsmart_mobile/features/user_dashboard/presentation/pages/user_dashboard_page.dart';
import 'package:buildsmart_mobile/features/shop_dashboard/presentation/pages/shop_dashboard_page.dart';
import 'package:buildsmart_mobile/features/orders/presentation/pages/cart_page.dart';
import 'package:buildsmart_mobile/features/orders/presentation/pages/checkout_page.dart';
import 'package:buildsmart_mobile/features/orders/presentation/pages/order_detail_page.dart';
import 'package:buildsmart_mobile/features/recommendations/presentation/pages/recommendation_form_page.dart';
import 'package:buildsmart_mobile/features/recommendations/presentation/pages/recommendations_list_page.dart';
import 'package:buildsmart_mobile/features/services/presentation/pages/services_list_page.dart';
import 'package:buildsmart_mobile/features/maps/presentation/pages/nearby_shops_page.dart';
import 'package:buildsmart_mobile/features/orders/presentation/pages/orders_list_page.dart';
import 'package:buildsmart_mobile/core/routing/routes.dart';
import 'package:buildsmart_mobile/features/auth/providers/auth_provider.dart';

/// Application router configuration using go_router
/// 
/// Defines all routes and navigation paths for the app.
/// Includes route guards for authentication.
final appRouterProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    initialLocation: AppRoutes.home,
    routes: [
      // Public routes
      GoRoute(
        path: AppRoutes.home,
        name: AppRoutes.home,
        builder: (context, state) => const HomePage(),
      ),
      GoRoute(
        path: AppRoutes.login,
        name: AppRoutes.login,
        builder: (context, state) => const LoginPage(),
      ),
      GoRoute(
        path: AppRoutes.register,
        name: AppRoutes.register,
        builder: (context, state) => const RegisterPage(),
      ),
      GoRoute(
        path: AppRoutes.search,
        name: AppRoutes.search,
        builder: (context, state) => const SearchPage(),
      ),
      GoRoute(
        path: AppRoutes.userDashboard,
        name: AppRoutes.userDashboard,
        builder: (context, state) => const UserDashboardPage(),
      ),
      GoRoute(
        path: AppRoutes.userOrders,
        name: AppRoutes.userOrders,
        builder: (context, state) => const OrdersListPage(),
      ),
      GoRoute(
        path: AppRoutes.shopDashboard,
        name: AppRoutes.shopDashboard,
        builder: (context, state) => const ShopDashboardPage(),
      ),
      GoRoute(
        path: AppRoutes.cart,
        name: AppRoutes.cart,
        builder: (context, state) => const CartPage(),
      ),
      GoRoute(
        path: AppRoutes.checkout,
        name: AppRoutes.checkout,
        builder: (context, state) => const CheckoutPage(),
      ),
      GoRoute(
        path: AppRoutes.orderDetail,
        name: AppRoutes.orderDetail,
        builder: (context, state) {
          final orderId = int.parse(state.pathParameters['id']!);
          return OrderDetailPage(orderId: orderId);
        },
      ),
      GoRoute(
        path: AppRoutes.userRecommendations,
        name: AppRoutes.userRecommendations,
        builder: (context, state) => const RecommendationsListPage(),
        routes: [
          GoRoute(
            path: 'new',
            builder: (context, state) => const RecommendationFormPage(),
          ),
        ],
      ),
      GoRoute(
        path: '/services',
        name: 'services',
        builder: (context, state) => const ServicesListPage(),
      ),
      GoRoute(
        path: AppRoutes.nearbyShops,
        name: AppRoutes.nearbyShops,
        builder: (context, state) => const NearbyShopsPage(),
      ),
      
      // TODO: Add more routes as features are implemented
      // - Product detail routes
      // - Service detail routes
    ],
    redirect: (context, state) {
      final isAuth = ref.watch(isAuthenticatedProvider);
      final isLoginRoute = state.matchedLocation == AppRoutes.login;
      final isRegisterRoute = state.matchedLocation == AppRoutes.register;
      final isHomeRoute = state.matchedLocation == AppRoutes.home;
      final isSearchRoute = state.matchedLocation == AppRoutes.search;
      final isUserDashboardRoute =
          state.matchedLocation == AppRoutes.userDashboard;
      final isUserOrdersRoute =
          state.matchedLocation == AppRoutes.userOrders;
      final isShopDashboardRoute =
          state.matchedLocation == AppRoutes.shopDashboard;

      // Allow public routes (home, login, register, search)
      if (isHomeRoute || isLoginRoute || isRegisterRoute || isSearchRoute) {
        return null;
      }

      // Protected routes require authentication
      if ((isUserDashboardRoute || isUserOrdersRoute || isShopDashboardRoute) && !isAuth) {
        return AppRoutes.login;
      }
      
      return null;
    },
    // Note: Router refresh handled by watching isAuthenticatedProvider in the router provider
  );
});

