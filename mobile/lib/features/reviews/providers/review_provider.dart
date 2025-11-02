import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/features/reviews/data/repositories/review_repository.dart';

/// Review repository provider
final reviewRepositoryProvider =
    Provider<ReviewRepository>((ref) {
  return ReviewRepository();
});

/// Shop reviews provider
final shopReviewsProvider =
    FutureProvider.family<List<ReviewModel>, int>(
  (ref, shopId) async {
    final repository = ref.watch(reviewRepositoryProvider);
    return await repository.getShopReviews(shopId);
  },
);

