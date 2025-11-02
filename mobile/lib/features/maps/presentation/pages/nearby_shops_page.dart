import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:geolocator/geolocator.dart';
import 'package:buildsmart_mobile/features/maps/providers/nearby_shops_provider.dart';
import 'package:buildsmart_mobile/core/models/models.dart';
import 'package:buildsmart_mobile/shared/widgets/common_widgets.dart';
import 'package:buildsmart_mobile/shared/theme/app_theme.dart';

/// Nearby shops page
/// 
/// Displays shops on a map and in a list view
class NearbyShopsPage extends ConsumerStatefulWidget {
  const NearbyShopsPage({super.key});

  @override
  ConsumerState<NearbyShopsPage> createState() => _NearbyShopsPageState();
}

class _NearbyShopsPageState extends ConsumerState<NearbyShopsPage> {
  // Default to list view on web since Google Maps has issues on web
  bool _showMap = !kIsWeb;
  GoogleMapController? _mapController;

  @override
  void dispose() {
    _mapController?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final locationState = ref.watch(userLocationProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Nearby Shops'),
        actions: [
          IconButton(
            icon: Icon(_showMap ? Icons.list : Icons.map),
            onPressed: () {
              setState(() => _showMap = !_showMap);
            },
            tooltip: _showMap ? 'Show List' : 'Show Map',
          ),
        ],
      ),
      body: locationState.when(
        data: (position) {
          if (position == null) {
            return ErrorState(
              message: 'Location permission denied or unavailable',
              icon: Icons.location_off,
              onRetry: () {
                ref.invalidate(userLocationProvider);
              },
            );
          }

          final params = NearbyShopsParams(
            latitude: position.latitude,
            longitude: position.longitude,
          );
          final shopsState = ref.watch(nearbyShopsProvider(params));

          return Column(
            children: [
              // Toggle buttons
              Container(
                padding: const EdgeInsets.all(8),
                color: Colors.grey[100],
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    _ViewToggleButton(
                      icon: Icons.map,
                      label: 'Map',
                      selected: _showMap,
                      onTap: () => setState(() => _showMap = true),
                    ),
                    const SizedBox(width: 8),
                    _ViewToggleButton(
                      icon: Icons.list,
                      label: 'List',
                      selected: !_showMap,
                      onTap: () => setState(() => _showMap = false),
                    ),
                  ],
                ),
              ),
              // Map or List view
              Expanded(
                child: _showMap
                    ? _buildMapView(position, shopsState)
                    : _buildListView(shopsState, position),
              ),
            ],
          );
        },
        loading: () => const LoadingState(),
        error: (err, stack) => ErrorState(
          message: err.toString(),
          onRetry: () => ref.invalidate(userLocationProvider),
        ),
      ),
    );
  }

  Widget _buildMapView(Position position, AsyncValue<List<ShopModel>> shopsState) {
    // Show message on web since Google Maps doesn't work well on web
    if (kIsWeb) {
      return shopsState.when(
        data: (shops) => Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.map, size: 64, color: Colors.grey),
              const SizedBox(height: 16),
              const Text(
                'Map view is not available on web',
                style: TextStyle(fontSize: 16, color: Colors.grey),
              ),
              const SizedBox(height: 8),
              const Text(
                'Please use list view instead',
                style: TextStyle(fontSize: 14, color: Colors.grey),
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: () => setState(() => _showMap = false),
                child: const Text('Switch to List View'),
              ),
            ],
          ),
        ),
        loading: () => const LoadingState(message: 'Loading nearby shops...'),
        error: (err, stack) => ErrorState(
          message: err.toString(),
          onRetry: () {
            // Retry logic handled by provider
          },
        ),
      );
    }

    return shopsState.when(
      data: (shops) {
        final markers = shops.map((shop) {
          return Marker(
            markerId: MarkerId(shop.id.toString()),
            position: LatLng(shop.latitude, shop.longitude),
            infoWindow: InfoWindow(
              title: shop.name,
              snippet: shop.address,
            ),
          );
        }).toSet();

        return GoogleMap(
          initialCameraPosition: CameraPosition(
            target: LatLng(position.latitude, position.longitude),
            zoom: 12,
          ),
          markers: markers,
          myLocationEnabled: true,
          myLocationButtonEnabled: true,
          onMapCreated: (controller) {
            _mapController = controller;
          },
        );
      },
      loading: () => const LoadingState(message: 'Loading nearby shops...'),
      error: (err, stack) => ErrorState(
        message: err.toString(),
        onRetry: () {
          // Retry logic handled by provider
        },
      ),
    );
  }

  Widget _buildListView(AsyncValue<List<ShopModel>> shopsState, Position position) {
    return shopsState.when(
      data: (shops) {
        if (shops.isEmpty) {
          return const EmptyState(
            icon: Icons.store_outlined,
            title: 'No shops found nearby',
            message: 'Try increasing the search radius',
          );
        }

        return RefreshIndicator(
          onRefresh: () async {
            ref.invalidate(nearbyShopsProvider(NearbyShopsParams(
              latitude: position.latitude,
              longitude: position.longitude,
            )));
          },
          child: ListView.builder(
            itemCount: shops.length,
            padding: const EdgeInsets.all(16),
            itemBuilder: (context, index) {
              final shop = shops[index];
              final distance = shop.distanceTo(
                position.latitude,
                position.longitude,
              );

              return Card(
                margin: const EdgeInsets.only(bottom: 12),
                child: ListTile(
                  leading: CircleAvatar(
                    backgroundColor: AppTheme.primaryYellow,
                    child: Text(
                      shop.name[0].toUpperCase(),
                      style: const TextStyle(color: Colors.white),
                    ),
                  ),
                  title: Row(
                    children: [
                      Expanded(child: Text(shop.name)),
                      if (shop.isVerified)
                        const Icon(Icons.verified,
                            size: 16, color: Colors.blue),
                    ],
                  ),
                  subtitle: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(shop.address),
                      const SizedBox(height: 4),
                      Row(
                        children: [
                          const Icon(Icons.location_on,
                              size: 14, color: Colors.grey),
                          const SizedBox(width: 4),
                          Text(
                            '${distance.toStringAsFixed(1)} km away',
                            style: TextStyle(
                              fontSize: 12,
                              color: Colors.grey[600],
                            ),
                          ),
                          if (shop.rating > 0) ...[
                            const SizedBox(width: 12),
                            const Icon(Icons.star,
                                size: 14, color: Colors.amber),
                            const SizedBox(width: 4),
                            Text(
                              shop.rating.toStringAsFixed(1),
                              style: TextStyle(
                                fontSize: 12,
                                color: Colors.grey[600],
                              ),
                            ),
                          ],
                        ],
                      ),
                    ],
                  ),
                  onTap: () {
                    // TODO: Navigate to shop detail
                    // context.push('${AppRoutes.shopDetail}/${shop.id}');
                  },
                ),
              );
            },
          ),
        );
      },
      loading: () => const LoadingState(message: 'Loading nearby shops...'),
      error: (err, stack) => ErrorState(
        message: err.toString(),
        onRetry: () {
          // Retry logic handled by provider
        },
      ),
    );
  }
}

class _ViewToggleButton extends StatelessWidget {
  final IconData icon;
  final String label;
  final bool selected;
  final VoidCallback onTap;

  const _ViewToggleButton({
    required this.icon,
    required this.label,
    required this.selected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(8),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          color: selected
              ? AppTheme.primaryYellow
              : Colors.white,
          borderRadius: BorderRadius.circular(8),
          border: Border.all(
            color: selected
                ? AppTheme.primaryYellow
                : Colors.grey[300]!,
          ),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              icon,
              size: 18,
              color: selected ? Colors.white : Colors.grey[600],
            ),
            const SizedBox(width: 8),
            Text(
              label,
              style: TextStyle(
                color: selected ? Colors.white : Colors.grey[600],
                fontWeight: selected ? FontWeight.bold : FontWeight.normal,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

