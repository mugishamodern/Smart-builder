import 'package:flutter/material.dart';

/// Rating display widget
class RatingDisplay extends StatelessWidget {
  final double rating;
  final int totalReviews;
  final double? size;
  final Color? color;

  const RatingDisplay({
    super.key,
    required this.rating,
    this.totalReviews = 0,
    this.size = 20,
    this.color = Colors.amber,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        ...List.generate(5, (index) {
          if (index < rating.floor()) {
            // Full star
            return Icon(Icons.star, size: size, color: color);
          } else if (index < rating) {
            // Half star
            return Icon(Icons.star_half, size: size, color: color);
          } else {
            // Empty star
            return Icon(Icons.star_border, size: size, color: color);
          }
        }),
        if (totalReviews > 0) ...[
          const SizedBox(width: 4),
          Text(
            '($totalReviews)',
            style: TextStyle(
              fontSize: (size ?? 20) * 0.7,
              color: Colors.grey[600],
            ),
          ),
        ],
      ],
    );
  }
}

/// Verified badge widget
class VerifiedBadge extends StatelessWidget {
  final bool isVerified;
  final double? size;

  const VerifiedBadge({
    super.key,
    required this.isVerified,
    this.size = 20,
  });

  @override
  Widget build(BuildContext context) {
    if (!isVerified) return const SizedBox.shrink();

    return Container(
      padding: const EdgeInsets.all(4),
      decoration: BoxDecoration(
        color: Colors.blue.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            Icons.verified,
            color: Colors.blue,
            size: size,
          ),
          const SizedBox(width: 4),
          Text(
            'Verified',
            style: TextStyle(
              color: Colors.blue,
              fontSize: (size ?? 20) * 0.7,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }
}

