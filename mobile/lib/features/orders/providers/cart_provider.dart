import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/features/orders/data/repositories/cart_repository.dart';

/// Cart repository provider
final cartRepositoryProvider = Provider<CartRepository>((ref) {
  return CartRepository();
});

/// Cart provider
final cartProvider = FutureProvider<CartModel>((ref) async {
  final repository = ref.watch(cartRepositoryProvider);
  return await repository.getCart();
});

/// Cart notifier for managing cart state
final cartNotifierProvider =
    StateNotifierProvider<CartNotifier, AsyncValue<CartModel>>((ref) {
  final repository = ref.watch(cartRepositoryProvider);
  return CartNotifier(repository, ref);
});

class CartNotifier extends StateNotifier<AsyncValue<CartModel>> {
  final CartRepository _repository;
  final Ref _ref;

  CartNotifier(this._repository, this._ref)
      : super(const AsyncValue.loading()) {
    _loadCart();
  }

  Future<void> _loadCart() async {
    state = const AsyncValue.loading();
    try {
      final cart = await _repository.getCart();
      state = AsyncValue.data(cart);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  Future<void> addToCart(int productId, int quantity) async {
    try {
      final cart = await _repository.addToCart(
        productId: productId,
        quantity: quantity,
      );
      state = AsyncValue.data(cart);
      // Refresh cart provider
      _ref.invalidate(cartProvider);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  Future<void> updateQuantity(int itemId, int quantity) async {
    try {
      final cart = await _repository.updateCartItem(
        itemId: itemId,
        quantity: quantity,
      );
      state = AsyncValue.data(cart);
      _ref.invalidate(cartProvider);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  Future<void> removeItem(int itemId) async {
    try {
      final cart = await _repository.removeCartItem(itemId);
      state = AsyncValue.data(cart);
      _ref.invalidate(cartProvider);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  Future<void> clear() async {
    try {
      await _repository.clearCart();
      await _loadCart();
      _ref.invalidate(cartProvider);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  Future<void> refresh() async {
    await _loadCart();
    _ref.invalidate(cartProvider);
  }
}

