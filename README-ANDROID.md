# MT Digital Store Android app

Native Android WebView client for the existing Flask marketplace.

- Application ID: `com.metmc.digitalstore`
- Display name: MT Digital Store
- HTTPS-only configurable marketplace URL
- JavaScript and DOM storage for the existing web marketplace
- Offline/network status feedback and WebView caching
- Back navigation, refresh, loading progress, and DownloadManager integration

## Build

The GitHub Actions workflow **Build MT Digital Store APK** builds a debug APK on pushes to this branch and manual dispatch. The APK is uploaded as an Actions artifact.

## Connect the marketplace

On first launch, enter the HTTPS URL of the deployed Flask website. The repository source is not itself a deployed marketplace URL; deploy the Flask service and configure its database and Supabase environment variables before connecting.
