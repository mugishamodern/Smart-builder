import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:buildsmart_mobile/core/models/user_model.dart';
import 'package:buildsmart_mobile/features/auth/data/repositories/auth_repository.dart';
import 'package:buildsmart_mobile/features/auth/data/models/auth_request.dart';

/// SharedPreferences provider
final sharedPreferencesProvider = FutureProvider<SharedPreferences>((ref) async {
  return await SharedPreferences.getInstance();
});

/// AuthRepository provider
final authRepositoryProvider = FutureProvider<AuthRepository>((ref) async {
  final prefs = await ref.watch(sharedPreferencesProvider.future);
  
  return AuthRepository(
    prefs: prefs,
  );
});

/// Current user state provider
final currentUserProvider = StateNotifierProvider<AuthNotifier, AsyncValue<UserModel?>>((ref) {
  return AuthNotifier(ref);
});

/// Auth state notifier
class AuthNotifier extends StateNotifier<AsyncValue<UserModel?>> {
  final Ref _ref;

  AuthNotifier(this._ref) : super(const AsyncValue.loading()) {
    _checkAuthStatus();
  }

  /// Get auth repository
  Future<AuthRepository> _getAuthRepository() async {
    final repoAsync = await _ref.read(authRepositoryProvider.future);
    return repoAsync;
  }

  /// Check if user is authenticated on app start
  Future<void> _checkAuthStatus() async {
    try {
      final authRepo = await _getAuthRepository();
      final user = await authRepo.getCurrentUser();
      state = AsyncValue.data(user);
    } catch (e) {
      state = AsyncValue.data(null);
    }
  }

  /// Login user
  Future<void> login(String email, String password, {bool rememberMe = false}) async {
    state = const AsyncValue.loading();
    try {
      final authRepo = await _getAuthRepository();
      final request = LoginRequest(
        email: email,
        password: password,
        rememberMe: rememberMe,
      );
      final user = await authRepo.login(request);
      state = AsyncValue.data(user);
    } catch (e) {
      state = AsyncValue.error(e, StackTrace.current);
    }
  }

  /// Register new user
  Future<void> register(RegisterRequest request) async {
    state = const AsyncValue.loading();
    try {
      final authRepo = await _getAuthRepository();
      final user = await authRepo.register(request);
      state = AsyncValue.data(user);
    } catch (e) {
      state = AsyncValue.error(e, StackTrace.current);
    }
  }

  /// Logout user
  Future<void> logout() async {
    try {
      final authRepo = await _getAuthRepository();
      await authRepo.logout();
      state = const AsyncValue.data(null);
    } catch (e) {
      state = AsyncValue.error(e, StackTrace.current);
    }
  }

  /// Get current user
  UserModel? get currentUser {
    return state.valueOrNull;
  }

  /// Check if user is authenticated
  bool get isAuthenticated {
    return state.valueOrNull != null;
  }
}

/// Helper provider to check auth status
final isAuthenticatedProvider = Provider<bool>((ref) {
  final authState = ref.watch(currentUserProvider);
  return authState.valueOrNull != null;
});

