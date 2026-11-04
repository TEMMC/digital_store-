# MT Digital Store 3.2 — local-first marketplace and community

MT Digital Store runs a bundled Flask application on the Android phone and opens it in the app's WebView at `http://127.0.0.1:8765/`. The SQLite database, uploads and Flask secret are stored in app-private storage.

## Marketplace
- Product discovery, search, categories, sorting and pagination.
- Buyer and creator accounts, profiles, password changes and notifications.
- Creator studio, product uploads, listing edits and statistics.
- Favourites, ratings and reviews.

## MT Community
- Public member feed for short posts and announcements.
- One-to-one text messaging with unread state and notifications.
- MT Group membership and group chat.
- About page and project attribution: **Created by Tinotenda Enock Mapfumo**.
- Call request records for voice/video and a phone-dialler link when a member has provided a phone number.

## Communication limitations — important
This build stores messages and group posts locally on the device. It does not yet synchronize accounts across different phones. The server binds to loopback only. Voice/video call request buttons send a notification/request record; they do **not** establish a live call. Real app-to-app calling needs a reachable signalling service and WebRTC media transport, plus camera/microphone permissions and secure deployment. The phone dialler link can start a normal carrier call after the user confirms in Android's dialler.

## Build and checks
GitHub Actions runs backend smoke tests and then builds the arm64 debug APK. Chaquopy embeds Python 3.11, Flask and Flask-SQLAlchemy. Minimum Android API is 24.
