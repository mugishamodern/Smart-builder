import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/features/shop_dashboard/data/repositories/shop_dashboard_repository.dart';

/// Shop dashboard repository provider
final shopDashboardRepositoryProvider =
    Provider<ShopDashboardRepository>((ref) {
  return ShopDashboardRepository();
});

/// Shop dashboard data provider
final shopDashboardDataProvider =
    FutureProvider<ShopDashboardData>((ref) async {
  final repository = ref.watch(shopDashboardRepositoryProvider);
  return await repository.getDashboardData();
});

