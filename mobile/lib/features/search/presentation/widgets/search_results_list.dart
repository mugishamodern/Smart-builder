import 'package:flutter/material.dart';

/// Reusable list widget with pagination support
class SearchResultsList<T> extends StatelessWidget {
  final List<T> items;
  final bool hasMore;
  final VoidCallback? onLoadMore;
  final Widget Function(BuildContext context, T item) itemBuilder;

  const SearchResultsList({
    super.key,
    required this.items,
    required this.hasMore,
    this.onLoadMore,
    required this.itemBuilder,
  });

  @override
  Widget build(BuildContext context) {
    if (items.isEmpty) {
      return const Center(child: Text('No results found'));
    }

    return NotificationListener<ScrollNotification>(
      onNotification: (notification) {
        if (notification is ScrollEndNotification &&
            notification.metrics.pixels >=
                notification.metrics.maxScrollExtent * 0.9) {
          if (hasMore && onLoadMore != null) {
            onLoadMore!();
          }
        }
        return false;
      },
      child: ListView.builder(
        itemCount: items.length + (hasMore ? 1 : 0),
        itemBuilder: (context, index) {
          if (index == items.length) {
            // Loading indicator at the bottom
            return const Padding(
              padding: EdgeInsets.all(16.0),
              child: Center(child: CircularProgressIndicator()),
            );
          }
          return itemBuilder(context, items[index]);
        },
      ),
    );
  }
}

