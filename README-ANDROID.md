# MT Digital Store 3 — on-device Flask marketplace

MT Digital Store runs its marketplace backend directly on the Android phone. The app starts the bundled Flask server and opens the real marketplace at `http://127.0.0.1:8765/`. No deployed website URL is required.

## Included marketplace capabilities

- Responsive neon-glass marketplace UI designed for phones and desktop screens.
- Product discovery with full-text style name/description/category search, category filters, sorting and pagination.
- Buyer and creator accounts, password hashing, profile editing and password changes.
- Creator studio with product statistics, listing creation, editing and deletion.
- Upload product packages and cover images from the phone (up to 100 MB per file), or use HTTPS-hosted files.
- Saved products / favourites, product ratings and written reviews.
- In-app notifications and an administrator review console.
- SQLite database, uploaded files and session secret are stored in app-private storage and persist across normal app restarts.
- CSRF protection for state-changing forms, role checks, secure filenames, upload type allowlists and security response headers.
- Health endpoint: `/health`; feature/status endpoint: `/api/v1/status`.

## Important limits

- The local server binds to `127.0.0.1` only. Other devices on Wi-Fi cannot access it.
- Paid-product checkout and payment processing are deliberately not simulated. Paid listings show that checkout is not enabled until a real payment provider is configured.
- HTTPS external download links require internet. Files uploaded from the phone are served locally.
- The administrator role is not available through public registration. An existing account can be promoted by setting `MT_ADMIN_USERNAME` before Flask starts; the Android launcher currently does not expose this setting.
- Android may stop the server if it terminates the app process in the background.

## Build and tests

GitHub Actions workflow **Build MT Digital Store APK** runs Python backend smoke tests before building the arm64 debug APK. Chaquopy embeds Python 3.11, Flask and Flask-SQLAlchemy. Minimum Android API is 24.
