import 'package:flutter/material.dart';
import 'package:buildsmart_mobile/features/reviews/data/repositories/review_repository.dart';
import 'package:buildsmart_mobile/features/reviews/presentation/widgets/rating_display.dart';
import 'package:intl/intl.dart';

/// Reviews list widget
class ReviewsList extends StatelessWidget {
  final List<ReviewModel> reviews;

  const ReviewsList({
    super.key,
    required this.reviews,
  });

  @override
  Widget build(BuildContext context) {
    if (reviews.isEmpty) {
      return const Center(
        child: Padding(
          padding: EdgeInsets.all(32),
          child: Text(
            'No reviews yet',
            style: TextStyle(color: Colors.grey),
          ),
        ),
      );
    }

    return ListView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: reviews.length,
      itemBuilder: (context, index) {
        final review = reviews[index];
        return Card(
          margin: const EdgeInsets.only(bottom: 12),
          child: Padding(
            padding: const EdgeInsets.all(12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      children: [
                        // User avatar
                        CircleAvatar(
                          radius: 20,
                          backgroundColor: Colors.grey[300],
                          child: Text(
                            (review.user?.fullName?.isNotEmpty == true
                                    ? review.user!.fullName![0]
                                    : review.user?.username[0] ?? 'U')
                                .toUpperCase(),
                            style: const TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                review.user?.fullName ??
                                    review.user?.username ??
                                    'Anonymous',
                                style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              if (review.user?.isVerified == true)
                                const Row(
                                  children: [
                                    Icon(Icons.verified,
                                        size: 14, color: Colors.blue),
                                    SizedBox(width: 4),
                                    Text(
                                      'Verified',
                                      style: TextStyle(
                                        fontSize: 12,
                                        color: Colors.blue,
                                      ),
                                    ),
                                  ],
                                ),
                            ],
                          ),
                        ),
                      ],
                    ),
                    // Rating
                    RatingDisplay(
                      rating: review.rating.toDouble(),
                      size: 16,
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                Text(review.comment),
                const SizedBox(height: 8),
                Text(
                  DateFormat('MMMM dd, yyyy').format(review.createdAt),
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey[600],
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}

