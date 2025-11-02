import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/core/models/models.dart';
import 'package:buildsmart_mobile/features/inventory/data/repositories/inventory_repository.dart';

/// Inventory repository provider
final inventoryRepositoryProvider =
    Provider<InventoryRepository>((ref) {
  return InventoryRepository();
});

/// Shop inventory provider
final shopInventoryProvider =
    FutureProvider.family<List<ProductModel>, int>(
  (ref, shopId) async {
    final repository = ref.watch(inventoryRepositoryProvider);
    return await repository.getShopInventory(shopId);
  },
);

