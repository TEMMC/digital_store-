# MT Digital Store 3.3 — marketplace and MT community

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
The APK remains local-first by default. For shared accounts and cross-device messaging, deploy the included Docker/Render server and build the APK with MT_REMOTE_SERVER_URL set to its HTTPS origin. The direct-message and MT Group APIs are available for authenticated clients. Use persistent PostgreSQL and upload storage in production. Voice/video call requests still notify members but do not establish a live WebRTC call; this requires a separate signalling/media service and TURN infrastructure.

## Build and checks
GitHub Actions runs backend smoke tests and then builds the arm64 debug APK. Chaquopy embeds Python 3.11, Flask and Flask-SQLAlchemy. Minimum Android API is 24.


## Shared server deployment

- A production Docker image and Render blueprint are included (`Dockerfile`, `render.yaml`).
- Set `DATABASE_URL` to PostgreSQL, `SECRET_KEY` to a long random secret, `MT_HTTPS=1`, and `UPLOAD_FOLDER` to persistent storage.
- Set the GitHub Actions repository variable `MT_REMOTE_SERVER_URL` to the deployed HTTPS origin before building the APK. Leave it unset for on-device mode.
- Do not expose Flask's development server publicly. Use HTTPS, backups, persistent uploads and a production database.
