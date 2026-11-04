# MT Digital Store 3.1 — marketplace + social community

MT Digital Store runs its Flask backend directly on Android at `http://127.0.0.1:8765/`. The phone stores the SQLite database, uploaded files and session secret in app-private storage.

## Marketplace
- Product search, categories, sorting and pagination.
- Buyer/creator accounts, profile and password management.
- Creator studio, product uploads, editing and statistics.
- Favourites, ratings, reviews, notifications and admin review console.

## MT social platform
- **MT Feed:** signed-in members can publish community posts.
- **Direct Messages:** member directory, one-to-one text conversations and unread state.
- **MT Group:** members can join, leave and participate in the official group chat.
- **Call options:** phone-number links open Android's dialler; voice/video call requests can be sent as notifications and are recorded.
- **About:** project story and creator credit: **Created by Tinotenda Enock Mapfumo**.

## Important network and calling limits
- This release's Flask server binds to `127.0.0.1`. Its database and social content are on this phone only; different phones do not share accounts or messages yet.
- The current call request is not a live internet voice/video call. Real app-to-app calling needs a network-reachable backend, WebRTC signalling and a STUN/TURN media relay. These are not bundled or falsely simulated.
- Phone calls use Android's normal dialler and carrier service; the user confirms the call in the dialler.
- Paid-product checkout is not enabled. External HTTPS downloads need internet; uploaded files are local.
- Android may stop the server if it terminates the app process in the background.

## Build and verification
GitHub Actions runs Python backend smoke tests before packaging the arm64 debug APK. Chaquopy embeds Python 3.11, Flask and Flask-SQLAlchemy. Minimum Android API 24.
