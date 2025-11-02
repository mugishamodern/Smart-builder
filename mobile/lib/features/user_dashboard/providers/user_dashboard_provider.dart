import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/features/user_dashboard/data/repositories/user_dashboard_repository.dart';

/// User dashboard repository provider
final userDashboardRepositoryProvider =
    Provider<UserDashboardRepository>((ref) {
  return UserDashboardRepository();
});

/// Dashboard data provider
final dashboardDataProvider = FutureProvider<DashboardData>((ref) async {
  final repository = ref.watch(userDashboardRepositoryProvider);
  return await repository.getDashboardData();
});

/// User orders provider
final userOrdersProvider =
    FutureProvider.family<PaginatedOrders, UserOrdersParams>(
  (ref, params) async {
    final repository = ref.watch(userDashboardRepositoryProvider);
    return await repository.getUserOrders(
      page: params.page,
      perPage: params.perPage,
    );
  },
);

/// User recommendations provider
final userRecommendationsProvider =
    FutureProvider.family<PaginatedRecommendations, UserRecommendationsParams>(
  (ref, params) async {
    final repository = ref.watch(userDashboardRepositoryProvider);
    return await repository.getUserRecommendations(
      savedOnly: params.savedOnly,
      page: params.page,
      perPage: params.perPage,
    );
  },
);

/// User orders parameters
class UserOrdersParams {
  final int page;
  final int perPage;

  UserOrdersParams({
    this.page = 1,
    this.perPage = 20,
  });

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is UserOrdersParams &&
          runtimeType == other.runtimeType &&
          page == other.page &&
          perPage == other.perPage;

  @override
  int get hashCode => page.hashCode ^ perPage.hashCode;
}

/// User recommendations parameters
class UserRecommendationsParams {
  final bool savedOnly;
  final int page;
  final int perPage;

  UserRecommendationsParams({
    this.savedOnly = false,
    this.page = 1,
    this.perPage = 20,
  });

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is UserRecommendationsParams &&
          runtimeType == other.runtimeType &&
          savedOnly == other.savedOnly &&
          page == other.page &&
          perPage == other.perPage;

  @override
  int get hashCode => savedOnly.hashCode ^ page.hashCode ^ perPage.hashCode;
}

