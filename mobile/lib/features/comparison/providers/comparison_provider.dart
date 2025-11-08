import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/core/models/models.dart';
import 'package:buildsmart_mobile/features/comparison/data/repositories/comparison_repository.dart';

/// Comparison repository provider
final comparisonRepositoryProvider = Provider<ComparisonRepository>((ref) {
  return ComparisonRepository();
});

/// Comparisons provider (for authenticated users)
final comparisonsProvider = FutureProvider<List<ComparisonModel>>((ref) async {
  final repository = ref.watch(comparisonRepositoryProvider);
  // TODO: Get isGuest status from auth provider
  final isGuest = false;
  return await repository.getComparisons(isGuest: isGuest);
});

/// Add to comparison notifier
final addToComparisonNotifierProvider = StateNotifierProvider<AddToComparisonNotifier, AsyncValue<void>>((ref) {
  final repository = ref.watch(comparisonRepositoryProvider);
  return AddToComparisonNotifier(repository, ref);
});

class AddToComparisonNotifier extends StateNotifier<AsyncValue<void>> {
  final ComparisonRepository _repository;
  final Ref _ref;

  AddToComparisonNotifier(this._repository, this._ref) : super(const AsyncValue.data(null));

  Future<void> addToComparison(int productId) async {
    state = const AsyncValue.loading();
    try {
      // TODO: Get isGuest status from auth provider
      final isGuest = false;
      await _repository.addToComparison(productId: productId, isGuest: isGuest);
      state = const AsyncValue.data(null);
      
      // Invalidate comparisons to refresh
      _ref.invalidate(comparisonsProvider);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  void reset() {
    state = const AsyncValue.data(null);
  }
}

/// Remove from comparison notifier
final removeFromComparisonNotifierProvider = StateNotifierProvider<RemoveFromComparisonNotifier, AsyncValue<void>>((ref) {
  final repository = ref.watch(comparisonRepositoryProvider);
  return RemoveFromComparisonNotifier(repository, ref);
});

class RemoveFromComparisonNotifier extends StateNotifier<AsyncValue<void>> {
  final ComparisonRepository _repository;
  final Ref _ref;

  RemoveFromComparisonNotifier(this._repository, this._ref) : super(const AsyncValue.data(null));

  Future<void> removeFromComparison(int productId) async {
    state = const AsyncValue.loading();
    try {
      // TODO: Get isGuest status from auth provider
      final isGuest = false;
      await _repository.removeFromComparison(productId: productId, isGuest: isGuest);
      state = const AsyncValue.data(null);
      
      // Invalidate comparisons to refresh
      _ref.invalidate(comparisonsProvider);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  void reset() {
    state = const AsyncValue.data(null);
  }
}

/// Clear comparisons notifier
final clearComparisonsNotifierProvider = StateNotifierProvider<ClearComparisonsNotifier, AsyncValue<void>>((ref) {
  final repository = ref.watch(comparisonRepositoryProvider);
  return ClearComparisonsNotifier(repository, ref);
});

class ClearComparisonsNotifier extends StateNotifier<AsyncValue<void>> {
  final ComparisonRepository _repository;
  final Ref _ref;

  ClearComparisonsNotifier(this._repository, this._ref) : super(const AsyncValue.data(null));

  Future<void> clearComparisons() async {
    state = const AsyncValue.loading();
    try {
      // TODO: Get isGuest status from auth provider
      final isGuest = false;
      await _repository.clearComparisons(isGuest: isGuest);
      state = const AsyncValue.data(null);
      
      // Invalidate comparisons to refresh
      _ref.invalidate(comparisonsProvider);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  void reset() {
    state = const AsyncValue.data(null);
  }
}
