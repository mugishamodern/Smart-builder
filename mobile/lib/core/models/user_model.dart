import 'package:freezed_annotation/freezed_annotation.dart';

part 'user_model.freezed.dart';
part 'user_model.g.dart';

/// User model matching Flask User model
@freezed
class UserModel with _$UserModel {
  const factory UserModel({
    @JsonKey(fromJson: _intFromJson) required int id,
    @JsonKey(fromJson: _stringFromJson) required String username,
    @JsonKey(fromJson: _stringFromJson) required String email,
    @JsonKey(name: 'full_name', fromJson: _stringFromJsonNullable) String? fullName,
    @JsonKey(fromJson: _stringFromJsonNullable) String? phone,
    @JsonKey(fromJson: _stringFromJsonNullable) String? address,
    @JsonKey(fromJson: _coordinateFromJson) double? latitude,
    @JsonKey(fromJson: _coordinateFromJson) double? longitude,
    @JsonKey(name: 'user_type', defaultValue: 'customer') @Default('customer') String userType, // customer, shop_owner, service_provider
    @JsonKey(name: 'is_active', defaultValue: true) @Default(true) bool isActive,
    @JsonKey(name: 'is_verified', defaultValue: false) @Default(false) bool isVerified,
    @JsonKey(name: 'created_at', fromJson: _dateTimeFromJsonNullable) DateTime? createdAt,
    @JsonKey(name: 'updated_at', fromJson: _dateTimeFromJsonNullable) DateTime? updatedAt,
  }) = _UserModel;

  factory UserModel.fromJson(Map<String, dynamic> json) =>
      _$UserModelFromJson(json);
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

/// Helper function to convert coordinate from JSON (handles null, string, and number)
double? _coordinateFromJson(dynamic value) {
  if (value == null) return null;
  if (value is num) {
    return value.toDouble();
  } else if (value is String) {
    return double.parse(value);
  } else {
    throw ArgumentError('Coordinate must be a number or string, got ${value.runtimeType}');
  }
}

/// Helper function to convert DateTime from JSON (handles null, string)
DateTime? _dateTimeFromJsonNullable(dynamic value) {
  if (value == null) return null;
  if (value is DateTime) return value;
  if (value is String) {
    if (value.isEmpty) return null;
    try {
      return DateTime.parse(value);
    } catch (e) {
      print('Warning: Failed to parse date: $value');
      return null;
    }
  }
  return null;
}

extension UserModelExtension on UserModel {
  bool get isShopOwner => userType == 'shop_owner';
  bool get isServiceProvider => userType == 'service_provider';
  bool get isCustomer => userType == 'customer';
}

