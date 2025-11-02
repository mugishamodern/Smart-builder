import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/core/models/models.dart';
import 'package:buildsmart_mobile/features/search/data/repositories/search_repository.dart';
import 'package:buildsmart_mobile/features/search/data/repositories/search_repository.dart' as repo;

/// Search repository provider
final searchRepositoryProvider = Provider<SearchRepository>((ref) {
  return SearchRepository();
});

/// Product search provider
final productSearchProvider = StateNotifierProvider.family<
    ProductSearchNotifier,
    AsyncValue<repo.SearchResult<ProductModel>>,
    ProductSearchParams>(
  (ref, params) {
    final repository = ref.watch(searchRepositoryProvider);
    return ProductSearchNotifier(repository, params);
  },
);

/// Service search provider
final serviceSearchProvider = StateNotifierProvider.family<
    ServiceSearchNotifier,
    AsyncValue<repo.SearchResult<ServiceModel>>,
    ServiceSearchParams>(
  (ref, params) {
    final repository = ref.watch(searchRepositoryProvider);
    return ServiceSearchNotifier(repository, params);
  },
);

/// Shop search provider
final shopSearchProvider = FutureProvider.family<List<ShopModel>, String?>(
  (ref, query) async {
    final repository = ref.watch(searchRepositoryProvider);
    return await repository.searchShops(query: query);
  },
);

/// Product search parameters
class ProductSearchParams {
  final String? query;
  final String? category;
  final double? minPrice;
  final double? maxPrice;
  final int page;
  final int perPage;

  ProductSearchParams({
    this.query,
    this.category,
    this.minPrice,
    this.maxPrice,
    this.page = 1,
    this.perPage = 20,
  });

  ProductSearchParams copyWith({
    String? query,
    String? category,
    double? minPrice,
    double? maxPrice,
    int? page,
    int? perPage,
  }) {
    return ProductSearchParams(
      query: query ?? this.query,
      category: category ?? this.category,
      minPrice: minPrice ?? this.minPrice,
      maxPrice: maxPrice ?? this.maxPrice,
      page: page ?? this.page,
      perPage: perPage ?? this.perPage,
    );
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is ProductSearchParams &&
          runtimeType == other.runtimeType &&
          query == other.query &&
          category == other.category &&
          minPrice == other.minPrice &&
          maxPrice == other.maxPrice &&
          page == other.page &&
          perPage == other.perPage;

  @override
  int get hashCode =>
      query.hashCode ^
      category.hashCode ^
      minPrice.hashCode ^
      maxPrice.hashCode ^
      page.hashCode ^
      perPage.hashCode;
}

/// Service search parameters
class ServiceSearchParams {
  final String? query;
  final String? serviceType;
  final double? minRate;
  final double? maxRate;
  final int page;
  final int perPage;

  ServiceSearchParams({
    this.query,
    this.serviceType,
    this.minRate,
    this.maxRate,
    this.page = 1,
    this.perPage = 20,
  });

  ServiceSearchParams copyWith({
    String? query,
    String? serviceType,
    double? minRate,
    double? maxRate,
    int? page,
    int? perPage,
  }) {
    return ServiceSearchParams(
      query: query ?? this.query,
      serviceType: serviceType ?? this.serviceType,
      minRate: minRate ?? this.minRate,
      maxRate: maxRate ?? this.maxRate,
      page: page ?? this.page,
      perPage: perPage ?? this.perPage,
    );
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is ServiceSearchParams &&
          runtimeType == other.runtimeType &&
          query == other.query &&
          serviceType == other.serviceType &&
          minRate == other.minRate &&
          maxRate == other.maxRate &&
          page == other.page &&
          perPage == other.perPage;

  @override
  int get hashCode =>
      query.hashCode ^
      serviceType.hashCode ^
      minRate.hashCode ^
      maxRate.hashCode ^
      page.hashCode ^
      perPage.hashCode;
}

/// Product search notifier
class ProductSearchNotifier
    extends StateNotifier<AsyncValue<repo.SearchResult<ProductModel>>> {
  final SearchRepository _repository;
  final ProductSearchParams _params;

  ProductSearchNotifier(this._repository, this._params)
      : super(const AsyncValue.loading()) {
    _search();
  }

  Future<void> _search() async {
    state = const AsyncValue.loading();
    try {
      final result = await _repository.searchProducts(
        query: _params.query,
        category: _params.category,
        minPrice: _params.minPrice,
        maxPrice: _params.maxPrice,
        page: _params.page,
        perPage: _params.perPage,
      );
      state = AsyncValue.data(result);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  Future<void> loadMore() async {
    if (state.valueOrNull?.hasMore != true) return;

    try {
      final nextPage = _params.page + 1;
      final nextParams = _params.copyWith(page: nextPage);
      final result = await _repository.searchProducts(
        query: nextParams.query,
        category: nextParams.category,
        minPrice: nextParams.minPrice,
        maxPrice: nextParams.maxPrice,
        page: nextParams.page,
        perPage: nextParams.perPage,
      );

      final currentResult = state.valueOrNull;
      if (currentResult != null) {
        state = AsyncValue.data(repo.SearchResult(
          items: [...currentResult.items, ...result.items],
          total: result.total,
          pages: result.pages,
          currentPage: result.currentPage,
        ));
      }
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }
}

/// Service search notifier
class ServiceSearchNotifier
    extends StateNotifier<AsyncValue<repo.SearchResult<ServiceModel>>> {
  final SearchRepository _repository;
  final ServiceSearchParams _params;

  ServiceSearchNotifier(this._repository, this._params)
      : super(const AsyncValue.loading()) {
    _search();
  }

  Future<void> _search() async {
    state = const AsyncValue.loading();
    try {
      final result = await _repository.searchServices(
        query: _params.query,
        serviceType: _params.serviceType,
        minRate: _params.minRate,
        maxRate: _params.maxRate,
        page: _params.page,
        perPage: _params.perPage,
      );
      state = AsyncValue.data(result);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  Future<void> loadMore() async {
    if (state.valueOrNull?.hasMore != true) return;

    try {
      final nextPage = _params.page + 1;
      final nextParams = _params.copyWith(page: nextPage);
      final result = await _repository.searchServices(
        query: nextParams.query,
        serviceType: nextParams.serviceType,
        minRate: nextParams.minRate,
        maxRate: nextParams.maxRate,
        page: nextParams.page,
        perPage: nextParams.perPage,
      );

      final currentResult = state.valueOrNull;
      if (currentResult != null) {
        state = AsyncValue.data(repo.SearchResult(
          items: [...currentResult.items, ...result.items],
          total: result.total,
          pages: result.pages,
          currentPage: result.currentPage,
        ));
      }
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }
}

