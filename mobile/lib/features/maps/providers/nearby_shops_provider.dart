import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:geolocator/geolocator.dart';
import 'package:buildsmart_mobile/features/maps/data/repositories/nearby_shops_repository.dart';
import 'package:buildsmart_mobile/core/models/models.dart';

/// Nearby shops repository provider
final nearbyShopsRepositoryProvider =
    Provider<NearbyShopsRepository>((ref) {
  return NearbyShopsRepository();
});

/// User location provider
final userLocationProvider = FutureProvider<Position?>((ref) async {
  try {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      return null;
    }

    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        return null;
      }
    }

    if (permission == LocationPermission.deniedForever) {
      return null;
    }

    return await Geolocator.getCurrentPosition(
      desiredAccuracy: LocationAccuracy.high,
    );
  } catch (e) {
    return null;
  }
});

/// Nearby shops provider
final nearbyShopsProvider =
    FutureProvider.family<List<ShopModel>, NearbyShopsParams>(
  (ref, params) async {
    final repository = ref.watch(nearbyShopsRepositoryProvider);
    return await repository.getNearbyShops(
      latitude: params.latitude,
      longitude: params.longitude,
      radius: params.radius,
      limit: params.limit,
    );
  },
);

/// Nearby shops parameters
class NearbyShopsParams {
  final double latitude;
  final double longitude;
  final double radius;
  final int limit;

  NearbyShopsParams({
    required this.latitude,
    required this.longitude,
    this.radius = 10.0,
    this.limit = 50,
  });

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is NearbyShopsParams &&
          runtimeType == other.runtimeType &&
          latitude == other.latitude &&
          longitude == other.longitude &&
          radius == other.radius &&
          limit == other.limit;

  @override
  int get hashCode =>
      latitude.hashCode ^
      longitude.hashCode ^
      radius.hashCode ^
      limit.hashCode;
}

