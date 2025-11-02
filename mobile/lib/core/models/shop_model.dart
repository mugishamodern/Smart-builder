import 'dart:math' as math;
import 'package:freezed_annotation/freezed_annotation.dart';

part 'shop_model.freezed.dart';
part 'shop_model.g.dart';

/// Shop model matching Flask Shop model
@freezed
class ShopModel with _$ShopModel {
  const factory ShopModel({
    @JsonKey(fromJson: _intFromJson) required int id,
    @JsonKey(fromJson: _stringFromJson) required String name,
    @JsonKey(fromJson: _stringFromJsonNullable) String? description,
    @JsonKey(fromJson: _stringFromJson) required String address,
    @JsonKey(fromJson: _stringFromJsonNullable) String? phone,
    @JsonKey(fromJson: _stringFromJsonNullable) String? email,
    @JsonKey(fromJson: _coordinateFromJson) required double latitude,
    @JsonKey(fromJson: _coordinateFromJson) required double longitude,
    @JsonKey(fromJson: _ratingFromJson) @Default(0.0) double rating,
    @JsonKey(name: 'total_reviews', fromJson: _intFromJson) @Default(0) int totalReviews,
    @JsonKey(name: 'is_verified', defaultValue: false) @Default(false) bool isVerified,
    @JsonKey(name: 'is_active', defaultValue: true) @Default(true) bool isActive,
    @JsonKey(name: 'owner_id', fromJson: _intFromJson) required int ownerId,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @JsonKey(name: 'updated_at') DateTime? updatedAt,
  }) = _ShopModel;

  factory ShopModel.fromJson(Map<String, dynamic> json) =>
      _$ShopModelFromJson(json);
}

/// Helper function to convert int from JSON (handles null, string, and number)
int _intFromJson(dynamic value) {
  if (value == null) {
    return 0;
  }
  if (value is num) {
    return value.toInt();
  } else if (value is String) {
    try {
      return int.parse(value);
    } catch (e) {
      return 0;
    }
  } else {
    return 0;
  }
}

/// Helper function to convert string from JSON (handles null)
String _stringFromJson(dynamic value) {
  if (value == null) return '';
  if (value is String) return value;
  return value.toString();
}

/// Helper function to convert nullable string from JSON
String? _stringFromJsonNullable(dynamic value) {
  if (value == null) return null;
  if (value is String) return value.isEmpty ? null : value;
  return value.toString();
}

/// Helper function to convert rating from JSON (handles null, string, and number)
double _ratingFromJson(dynamic value) {
  if (value == null) return 0.0;
  if (value is num) {
    return value.toDouble();
  } else if (value is String) {
    return double.parse(value);
  } else {
    throw ArgumentError('Rating must be a number or string, got ${value.runtimeType}');
  }
}

/// Helper function to convert coordinate from JSON (handles null, string, and number)
double _coordinateFromJson(dynamic value) {
  if (value == null) return 0.0; // Default to 0.0 if null
  if (value is num) {
    return value.toDouble();
  } else if (value is String) {
    return double.parse(value);
  } else {
    throw ArgumentError('Coordinate must be a number or string, got ${value.runtimeType}');
  }
}

extension ShopModelExtension on ShopModel {
  /// Calculate distance to given coordinates in kilometers
  double distanceTo(double lat, double lon) {
    // Haversine formula
    const double R = 6371; // Earth's radius in kilometers
    
    double dLat = _toRadians(lat - latitude);
    double dLon = _toRadians(lon - longitude);
    
    double a = math.sin(dLat / 2) * math.sin(dLat / 2) +
        math.cos(_toRadians(latitude)) *
            math.cos(_toRadians(lat)) *
            math.sin(dLon / 2) *
            math.sin(dLon / 2);
    
    double c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a));
    
    return R * c;
  }
  
  double _toRadians(double degrees) => degrees * (math.pi / 180);
}

