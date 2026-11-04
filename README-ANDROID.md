# MT Digital Store — on-device Flask marketplace

The Android app bundles and runs the existing Flask marketplace on the phone itself.

- Launching the app starts Flask locally and opens its real homepage at `http://127.0.0.1:8765/`.
- Marketplace templates, static assets, routes and Flask backend are bundled from the repository at build time.
- SQLite database and uploads are stored in the app's private data directory and survive app restarts.
- No public hosting URL is needed for local use.
- The local server listens on loopback only; it is not exposed to Wi-Fi or the public internet.
- Internet is still needed for external product-file links and any optional cloud storage integration.
- The server runs while the app process is alive. Android may stop it if it kills the app in the background.

## Build

GitHub Actions workflow **Build MT Digital Store APK** builds the arm64 APK. Chaquopy embeds Python 3.11, Flask and Flask-SQLAlchemy. The app requires Android API 24 or later.
