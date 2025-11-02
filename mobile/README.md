# BuildSmart Mobile (Flutter)

Mirrors the Flask web app features for a construction marketplace: materials, services, shops, orders, and AI recommendations.

## Tech Stack
- Flutter (Stable)
- State: Riverpod or Bloc
- HTTP: dio
- Routing: go_router
- Storage: hive or shared_preferences
- Maps: google_maps_flutter
- Notifications: firebase_messaging (optional)
- Env: flutter_dotenv

## Structure (proposed)
- lib/
  - core/ (env, http, errors, constants)
  - features/ (auth, home, search, user_dashboard, shop_dashboard, inventory, orders, recommendations, services, reviews, maps)
  - shared/ (widgets, theme, utils)

## API
Configure base URL via `.env`:
```
API_BASE_URL=https://your-api.example.com
GOOGLE_MAPS_API_KEY=YOUR_KEY
```

## Feature Parity Checklist
- Auth (login/register/logout)
- Home (hero, categories, featured)
- Search (products/shops/services)
- User dashboard (stats, orders, recommendations)
- Shop dashboard (shops, stats, recent orders)
- Inventory (list/add/edit products)
- Orders (cart/checkout/detail/status)
- AI recommendations (form + results)
- Services (browse/provider profile)
- Reviews & verified badges
- Nearby shops (maps/geolocation)
- Offline cache + retry
- Notifications (optional)
- Theming (brand colors + dark mode)

## Development
- flutter create buildsmart_mobile
- Add packages (see docs)
- flutter run

## Quality
- flutter analyze
- dart test
- CI (GitHub Actions)

## License
TBD
