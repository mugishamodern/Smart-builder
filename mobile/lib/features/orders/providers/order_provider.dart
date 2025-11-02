import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/core/models/models.dart';
import 'package:buildsmart_mobile/features/orders/data/repositories/order_repository.dart';

/// Order repository provider
final orderRepositoryProvider = Provider<OrderRepository>((ref) {
  return OrderRepository();
});

/// Order provider
final orderProvider = FutureProvider.family<OrderModel, int>(
  (ref, orderId) async {
    final repository = ref.watch(orderRepositoryProvider);
    return await repository.getOrder(orderId);
  },
);

/// User orders provider
final userOrdersProvider =
    FutureProvider.family<PaginatedOrders, UserOrdersParams>(
  (ref, params) async {
    final repository = ref.watch(orderRepositoryProvider);
    return await repository.getUserOrders(
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

