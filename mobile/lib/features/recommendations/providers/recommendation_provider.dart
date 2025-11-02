import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/features/recommendations/data/repositories/recommendation_repository.dart';

/// Recommendation repository provider
final recommendationRepositoryProvider =
    Provider<RecommendationRepository>((ref) {
  return RecommendationRepository();
});

/// Recommendation generation provider
final recommendationGenerationProvider =
    StateNotifierProvider<RecommendationNotifier, AsyncValue<RecommendationResponse?>>(
  (ref) {
    final repository = ref.watch(recommendationRepositoryProvider);
    return RecommendationNotifier(repository);
  },
);

class RecommendationNotifier
    extends StateNotifier<AsyncValue<RecommendationResponse?>> {
  final RecommendationRepository _repository;

  RecommendationNotifier(this._repository)
      : super(const AsyncValue.data(null));

  Future<void> generateRecommendation({
    required String projectDescription,
    String projectType = '2_bedroom_house',
    Map<String, dynamic>? customSpecs,
  }) async {
    state = const AsyncValue.loading();
    try {
      final response = await _repository.generateRecommendation(
        projectDescription: projectDescription,
        projectType: projectType,
        customSpecs: customSpecs,
      );
      state = AsyncValue.data(response);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  void clear() {
    state = const AsyncValue.data(null);
  }
}

