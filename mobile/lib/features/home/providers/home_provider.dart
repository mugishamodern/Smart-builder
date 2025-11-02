import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/core/models/models.dart';
import 'package:buildsmart_mobile/features/home/data/repositories/home_repository.dart';

/// Home repository provider
final homeRepositoryProvider = Provider<HomeRepository>((ref) {
  return HomeRepository();
});

/// Featured shops provider
final featuredShopsProvider = FutureProvider<List<ShopModel>>((ref) async {
  final repository = ref.watch(homeRepositoryProvider);
  return await repository.getFeaturedShops();
});

/// Featured products provider
final featuredProductsProvider =
    FutureProvider<List<ProductModel>>((ref) async {
  final repository = ref.watch(homeRepositoryProvider);
  return await repository.getFeaturedProducts();
});

/// Featured services provider
final featuredServicesProvider =
    FutureProvider<List<ServiceModel>>((ref) async {
  final repository = ref.watch(homeRepositoryProvider);
  return await repository.getFeaturedServices();
});

/// Categories provider
final categoriesProvider = FutureProvider<List<String>>((ref) async {
  final repository = ref.watch(homeRepositoryProvider);
  return await repository.getCategories();
});
