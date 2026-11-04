package com.metmc.digitalstore

import android.app.Activity
import android.app.DownloadManager
import android.content.Context
import android.net.Uri
import android.os.Bundle
import android.os.Environment
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.webkit.CookieManager
import android.webkit.DownloadListener
import android.webkit.WebChromeClient
import android.webkit.WebResourceError
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.LinearLayout
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import java.io.File
import java.util.concurrent.Executors

class MainActivity : Activity() {
    private lateinit var webView: WebView
    private lateinit var progress: ProgressBar
    private lateinit var status: TextView
    private val worker = Executors.newSingleThreadExecutor()
    private val localUrl = "http://127.0.0.1:8765/"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.statusBarColor = android.graphics.Color.rgb(10, 16, 14)
        window.navigationBarColor = android.graphics.Color.rgb(10, 16, 14)
        buildInterface()
        configureWebView()
        if (savedInstanceState != null && webView.restoreState(savedInstanceState) != null) {
            return
        }
        startLocalMarketplace()
    }

    private fun buildInterface() {
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(android.graphics.Color.rgb(10, 16, 14))
        }
        val header = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding(16, 12, 16, 12)
        }
        val brand = TextView(this).apply {
            text = "MT  DIGITAL STORE"
            textSize = 18f
            setTextColor(android.graphics.Color.rgb(90, 235, 155))
            typeface = android.graphics.Typeface.DEFAULT_BOLD
        }
        status = TextView(this).apply {
            text = "Starting on-device marketplace…"
            textSize = 12f
            setTextColor(android.graphics.Color.LTGRAY)
            setPadding(16, 5, 16, 8)
        }
        header.addView(brand, LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f))
        progress = ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal).apply {
            max = 100
            visibility = View.GONE
        }
        webView = WebView(this)
        root.addView(header)
        root.addView(progress)
        root.addView(status)
        root.addView(webView, LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f
        ))
        setContentView(root)
    }

    @Suppress("SetJavaScriptEnabled")
    private fun configureWebView() {
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.settings.databaseEnabled = true
        webView.settings.loadsImagesAutomatically = true
        webView.settings.javaScriptCanOpenWindowsAutomatically = false
        webView.settings.allowFileAccess = false
        webView.settings.cacheMode = android.webkit.WebSettings.LOAD_DEFAULT
        CookieManager.getInstance().setAcceptCookie(true)
        webView.webChromeClient = object : WebChromeClient() {
            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                progress.progress = newProgress
                progress.visibility = if (newProgress in 1..99) View.VISIBLE else View.GONE
                if (newProgress == 100) status.text = "Marketplace ready · hosted on this phone"
            }
        }
        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                val uri = request?.url ?: return false
                return uri.scheme != "http" && uri.scheme != "https"
            }
            override fun onReceivedError(view: WebView?, request: WebResourceRequest?, error: WebResourceError?) {
                if (request?.isForMainFrame == true) {
                    status.text = "Marketplace server error — tap refresh"
                }
            }
        }
        webView.setDownloadListener(DownloadListener { url, userAgent, _, mimeType, _ ->
            try {
                val request = DownloadManager.Request(Uri.parse(url))
                    .setMimeType(mimeType)
                    .addRequestHeader("User-Agent", userAgent)
                    .addRequestHeader("Cookie", CookieManager.getInstance().getCookie(url) ?: "")
                    .setTitle("MT Digital Store download")
                    .setDescription("Downloading marketplace file")
                    .setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
                    .setDestinationInExternalPublicDir(
                        Environment.DIRECTORY_DOWNLOADS,
                        "MT-Store-" + System.currentTimeMillis()
                    )
                (getSystemService(DOWNLOAD_SERVICE) as DownloadManager).enqueue(request)
                Toast.makeText(this, "Download started", Toast.LENGTH_SHORT).show()
            } catch (e: Exception) {
                Toast.makeText(this, "Download failed: ${e.localizedMessage}", Toast.LENGTH_LONG).show()
            }
        })
    }

    private fun startLocalMarketplace() {
        status.text = "Preparing the marketplace files…"
        worker.execute {
            try {
                val root = File(filesDir, "marketplace")
                val uploads = File(filesDir, "marketplace-uploads")
                root.mkdirs()
                uploads.mkdirs()
                copyAssetFolder("marketplace", root)

                if (!Python.isStarted()) Python.start(AndroidPlatform(applicationContext))
                val secretPrefs = getSharedPreferences("mt_store_server", Context.MODE_PRIVATE)
                var secret = secretPrefs.getString("flask_secret", null)
                if (secret.isNullOrBlank()) {
                    secret = java.util.UUID.randomUUID().toString() + java.util.UUID.randomUUID()
                    secretPrefs.edit().putString("flask_secret", secret).apply()
                }
                val database = File(filesDir, "mt-digital-store.db")
                Python.getInstance().getModule("mt_server").callAttr(
                    "start",
                    root.absolutePath,
                    database.absolutePath,
                    uploads.absolutePath,
                    secret
                )
                runOnUiThread {
                    if (!isFinishing) {
                        status.text = "Local server running · opening your marketplace…"
                        webView.loadUrl(localUrl)
                    }
                }
            } catch (e: Exception) {
                runOnUiThread {
                    status.text = "Could not start marketplace: ${e.localizedMessage}"
                    Toast.makeText(
                        this,
                        "Local server failed to start: ${e.localizedMessage}",
                        Toast.LENGTH_LONG
                    ).show()
                }
            }
        }
    }

    private fun copyAssetFolder(assetPath: String, destination: File) {
        destination.mkdirs()
        val children = assets.list(assetPath) ?: return
        if (children.isEmpty()) {
            assets.open(assetPath).use { input ->
                destination.outputStream().use { output -> input.copyTo(output) }
            }
            return
        }
        for (child in children) {
            val childAsset = "$assetPath/$child"
            val childFile = File(destination, child)
            val nested = assets.list(childAsset)
            if (nested != null && nested.isNotEmpty()) {
                copyAssetFolder(childAsset, childFile)
            } else {
                assets.open(childAsset).use { input ->
                    childFile.parentFile?.mkdirs()
                    childFile.outputStream().use { output -> input.copyTo(output) }
                }
            }
        }
    }

    override fun onSaveInstanceState(outState: Bundle) {
        webView.saveState(outState)
        super.onSaveInstanceState(outState)
    }

    @Deprecated("Deprecated in Android")
    override fun onBackPressed() {
        if (::webView.isInitialized && webView.canGoBack()) webView.goBack()
        else super.onBackPressed()
    }

    override fun onDestroy() {
        if (::webView.isInitialized) {
            webView.stopLoading()
            webView.destroy()
        }
        worker.shutdown()
        super.onDestroy()
    }
}
