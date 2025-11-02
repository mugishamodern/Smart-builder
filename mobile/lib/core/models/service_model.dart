import 'package:freezed_annotation/freezed_annotation.dart';
import 'user_model.dart';

part 'service_model.freezed.dart';
part 'service_model.g.dart';

/// Service model matching Flask Service model
@freezed
class ServiceModel with _$ServiceModel {
  const factory ServiceModel({
    @JsonKey(fromJson: _intFromJson) required int id,
    @JsonKey(fromJson: _stringFromJson) required String title,
    @JsonKey(fromJson: _stringFromJsonNullable) String? description,
    @JsonKey(name: 'service_type', fromJson: _stringFromJson) required String serviceType, // e.g., 'plumbing', 'electrical', 'carpentry'
    @JsonKey(name: 'hourly_rate', fromJson: _hourlyRateFromJson) required double hourlyRate,
    @JsonKey(name: 'years_experience', fromJson: _yearsExperienceFromJson) @Default(0) int yearsExperience,
    @JsonKey(fromJson: _ratingFromJson) @Default(0.0) double rating,
    @JsonKey(name: 'is_available', defaultValue: true) @Default(true) bool isAvailable,
    @JsonKey(name: 'service_area', fromJson: _stringFromJsonNullable) String? serviceArea,
    @JsonKey(fromJson: _stringFromJsonNullable) String? certifications,
    @JsonKey(name: 'portfolio_url', fromJson: _stringFromJsonNullable) String? portfolioUrl,
    @JsonKey(name: 'provider_id', fromJson: _providerIdFromJson) required int providerId,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @JsonKey(name: 'updated_at') DateTime? updatedAt,
    // Nested provider info (when fetched with details)
    @JsonKey(fromJson: _providerFromJson) UserModel? provider,
  }) = _ServiceModel;

  factory ServiceModel.fromJson(Map<String, dynamic> json) =>
      _$ServiceModelFromJson(json);
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

/// Helper function to convert hourly rate from JSON (handles null, string, and number)
double _hourlyRateFromJson(dynamic value) {
  if (value == null) return 0.0;
  if (value is num) {
    return value.toDouble();
  } else if (value is String) {
    return double.parse(value);
  } else {
    throw ArgumentError('Hourly rate must be a number or string, got ${value.runtimeType}');
  }
}

/// Helper function to convert years experience from JSON (handles null, string, and number)
int _yearsExperienceFromJson(dynamic value) {
  if (value == null) return 0;
  if (value is num) {
    return value.toInt();
  } else if (value is String) {
    return int.parse(value);
  } else {
    throw ArgumentError('Years experience must be a number or string, got ${value.runtimeType}');
  }
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

/// Helper function to convert provider_id from JSON (handles null, extracts from provider object)
int _providerIdFromJson(dynamic value) {
  if (value == null) {
    // If provider_id is null, try to extract from provider object
    // This is handled in the repository when parsing
    return 0;
  }
  if (value is num) {
    return value.toInt();
  } else if (value is String) {
    return int.parse(value);
  } else {
    throw ArgumentError('Provider ID must be a number or string, got ${value.runtimeType}');
  }
}

/// Helper function to convert provider from JSON (handles LinkedMap)
UserModel? _providerFromJson(dynamic value) {
  if (value == null) return null;
  if (value is Map) {
    return UserModel.fromJson(Map<String, dynamic>.from(value));
  } else {
    throw ArgumentError('Provider must be a Map, got ${value.runtimeType}');
  }
}

