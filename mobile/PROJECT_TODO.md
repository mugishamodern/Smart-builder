# BuildSmart Mobile TODOs

## ✅ Completed

- [x] Initialize Flutter project and repository structure
- [x] Add core packages (dio, go_router, riverpod, flutter_dotenv, shared_preferences, hive, google_maps_flutter, geolocator, url_launcher, intl, etc.)
- [x] Configure environments and API base URL (AppConfig with .env)
- [x] Implement global theming (brand colors, typography, dark mode scaffold)
- [x] App shell: routing (go_router), guarded routes with auth
- [x] Auth: register, login, logout, session persistence, guards
- [x] Home: hero banner, categories grid, featured shops/products/services
- [x] Search: products/shops/services, filters, pagination with debounced input
- [x] User Dashboard: stats, recent orders, saved recommendations
- [x] Shop Dashboard: shops list, stats, recent orders
- [x] Inventory: list/add/edit products (owner)
- [x] Orders: cart, checkout, order details, status tracking
- [x] AI Recommendations: form submit, results view, save/delete
- [x] Services: list, provider profile details, contact actions
- [x] Reviews & Verified Badges: display ratings, verified badges
- [x] Nearby Shops: geolocation, map display, list view with distance
- [x] UI State Components: loading, empty, error states (reusable widgets)

## 🚧 In Progress

_(None currently)_

## 📋 Pending / Optional

- [ ] Offline cache adapters (Hive adapters for models - basic cache manager ready)
- [ ] Push notifications (optional): Firebase setup, FCM integration
- [ ] Complete test implementation (test scaffold ready, need actual test cases)
- [ ] CI/CD deployment (workflow configured, needs repository connection)
- [ ] Custom app icons and splash screens (documentation ready)
- [ ] Privacy policy creation
- [ ] Additional localization languages (structure ready for expansion)
- [ ] Accessibility enhancements (semantics labels, contrast testing)

## 📝 Notes

### Features with TODOs in code:
- Navigation to product/service/shop detail pages (routes exist, need detail pages)
- Navigation to full orders/recommendations lists (routes exist, need list pages)
- Forgot password functionality
- Token secure storage (currently using SharedPreferences - can upgrade to flutter_secure_storage)
- Dark theme implementation (scaffold ready)
- Submit review functionality (repository exists, need UI form)

### Architecture & Best Practices:
- ✅ Clean architecture with feature-based structure
- ✅ Riverpod for state management
- ✅ Repository pattern for data access
- ✅ Reusable UI components
- ✅ Error handling and loading states
- ✅ Type-safe routing with go_router
