# Next Steps for BuildSmart Mobile

## Immediate Next Steps (Recommended Order)

### 1. Complete Authentication System ⚡ (HIGH PRIORITY)

**Files to Create/Update:**
- `lib/features/auth/providers/auth_provider.dart` - Riverpod providers
- `lib/features/auth/presentation/pages/login_page.dart` - Login form
- `lib/features/auth/presentation/pages/register_page.dart` - Register form
- `lib/core/routing/app_router.dart` - Add route guards

**What to Do:**
1. Create Riverpod providers for auth state management
2. Build login/register UI forms with validation
3. Connect UI to auth repository
4. Add route guards (redirect to login if not authenticated)
5. Test login/logout flow

### 2. Build Home Screen 🏠

**Files to Create/Update:**
- `lib/features/home/presentation/pages/home_page.dart` - Complete home screen
- `lib/features/home/data/repositories/home_repository.dart` - Fetch featured data
- `lib/features/home/providers/home_provider.dart` - Riverpod providers

**What to Do:**
1. Hero section with CTAs
2. Featured shops grid
3. Featured products grid
4. Featured services grid
5. Categories grid

### 3. Implement Search 🔍

**Files to Create:**
- `lib/features/search/presentation/pages/search_page.dart`
- `lib/features/search/data/repositories/search_repository.dart`
- `lib/features/search/providers/search_provider.dart`

**What to Do:**
1. Search bar with debouncing
2. Filter options (category, price, etc.)
3. Results list with pagination
4. Product/Shop/Service cards

## Development Tips

### Running Code Generation
After adding/updating freezed models:
```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

### Running the App
```bash
flutter run -d windows
```

### Testing API Connection
1. Start Flask backend: `python run.py`
2. Test endpoints in app
3. Check logs for API calls

### File Organization
```
lib/
├── core/ (shared infrastructure)
├── features/ (feature modules)
│   └── auth/
│       ├── data/ (repositories, models)
│       ├── presentation/ (UI, pages)
│       └── providers/ (Riverpod providers)
└── shared/ (shared widgets, theme)
```

## Current State

✅ **Ready to Use:**
- All models (User, Shop, Product, Order, Service, Recommendation)
- API client with interceptors
- Routing structure
- Theme configuration
- Auth repository (needs providers)

🚧 **In Progress:**
- Auth UI and state management

📝 **Need to Create:**
- Auth providers
- Complete auth UI
- Home screen
- Search functionality
- All other features

## Recommended Approach

1. **Start with Auth** - Complete login/register flow first
2. **Build Home** - Show data from backend
3. **Add Search** - Enable discovery
4. **User Dashboard** - Personalization
5. **Shop Features** - For shop owners
6. **Advanced Features** - Maps, offline, etc.

This systematic approach ensures each feature builds on the previous ones!

