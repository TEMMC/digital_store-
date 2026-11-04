package com.metmc.digitalstore

import android.app.Activity
import android.app.AlertDialog
import android.app.DownloadManager
import android.content.Context
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
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
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ListView
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import org.json.JSONArray
import org.json.JSONObject

private data class SavedPage(val title: String, val url: String)

class MainActivity : Activity() {
    private lateinit var webView: WebView
    private lateinit var progress: ProgressBar
    private lateinit var status: TextView
    private lateinit var address: EditText
    private val prefs by lazy { getSharedPreferences("mt_store", Context.MODE_PRIVATE) }
    private val storeUrl: String get() = prefs.getString("store_url", "") ?: ""

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.statusBarColor = android.graphics.Color.rgb(10, 16, 14)
        window.navigationBarColor = android.graphics.Color.rgb(10, 16, 14)
        buildInterface()
        configureWebView()
        if (savedInstanceState != null) webView.restoreState(savedInstanceState)
        else if (storeUrl.isNotBlank()) loadStore() else showSetupMessage()
    }

    private fun buildInterface() {
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(android.graphics.Color.rgb(10, 16, 14))
        }
        val header = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding(16, 12, 12, 12)
        }
        val brand = TextView(this).apply {
            text = "MT  DIGITAL STORE"
            textSize = 18f
            setTextColor(android.graphics.Color.rgb(90, 235, 155))
            typeface = android.graphics.Typeface.DEFAULT_BOLD
        }
        val pages = Button(this).apply {
            text = "WEB PAGES"
            setOnClickListener { showPagesDialog() }
        }
        val settings = Button(this).apply {
            text = "SET URL"
            setOnClickListener { showUrlDialog() }
        }
        header.addView(brand, LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f))
        header.addView(pages)
        header.addView(settings)
        progress = ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal).apply {
            max = 100
            visibility = View.GONE
        }
        status = TextView(this).apply {
            text = "Ready"
            textSize = 12f
            setTextColor(android.graphics.Color.LTGRAY)
            setPadding(16, 5, 16, 5)
        }
        address = EditText(this).apply {
            hint = "Website address (https://...)"
            setSingleLine(true)
            setTextColor(android.graphics.Color.WHITE)
            setHintTextColor(android.graphics.Color.GRAY)
            setPadding(14, 8, 14, 8)
        }
        val controls = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            setPadding(8, 2, 8, 8)
        }
        val open = Button(this).apply {
            text = "OPEN"
            setOnClickListener { openAddress(address.text.toString()) }
        }
        val refresh = Button(this).apply {
            text = "REFRESH"
            setOnClickListener { if (webView.url != null) webView.reload() else showUrlDialog() }
        }
        controls.addView(open, LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f))
        controls.addView(refresh, LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f))
        webView = WebView(this)
        root.addView(header)
        root.addView(progress)
        root.addView(status)
        root.addView(address)
        root.addView(controls)
        root.addView(webView, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f))
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
                status.text = if (newProgress == 100) "Page loaded" else "Loading $newProgress%"
            }
        }
        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                val uri = request?.url ?: return false
                return uri.scheme != "https" && uri.scheme != "http"
            }
            override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {
                if (!url.isNullOrBlank()) address.setText(url)
            }
            override fun onReceivedError(view: WebView?, request: WebResourceRequest?, error: WebResourceError?) {
                if (request?.isForMainFrame == true) status.text =
                    if (isOnline()) "Could not load page" else "Offline"
            }
        }
        webView.setDownloadListener(DownloadListener { url, userAgent, _, mimeType, _ ->
            try {
                val request = DownloadManager.Request(Uri.parse(url))
                    .setMimeType(mimeType)
                    .addRequestHeader("User-Agent", userAgent)
                    .addRequestHeader("Cookie", CookieManager.getInstance().getCookie(url) ?: "")
                    .setTitle("MT Digital Store download")
                    .setDescription("Downloading website file")
                    .setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
                    .setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, "MT-Store-" + System.currentTimeMillis())
                (getSystemService(DOWNLOAD_SERVICE) as DownloadManager).enqueue(request)
                Toast.makeText(this, "Download started", Toast.LENGTH_SHORT).show()
            } catch (e: Exception) {
                Toast.makeText(this, "Download failed: ${e.localizedMessage}", Toast.LENGTH_LONG).show()
            }
        })
    }

    private fun normalizeHttpsUrl(raw: String): String? {
        var value = raw.trim()
        if (value.isBlank()) return null
        if (!value.contains("://")) value = "https://$value"
        val uri = Uri.parse(value)
        return if (uri.scheme == "https" && !uri.host.isNullOrBlank()) value else null
    }

    private fun openAddress(raw: String) {
        val url = normalizeHttpsUrl(raw)
        if (url == null) {
            Toast.makeText(this, "Enter a valid HTTPS website address", Toast.LENGTH_LONG).show()
            return
        }
        address.setText(url)
        status.text = "Opening website"
        webView.loadUrl(url)
    }

    private fun saveAndLoad(raw: String) {
        val url = normalizeHttpsUrl(raw)
        if (url == null) {
            Toast.makeText(this, "Enter a valid HTTPS marketplace URL", Toast.LENGTH_LONG).show()
            return
        }
        prefs.edit().putString("store_url", url).apply()
        address.setText(url)
        webView.loadUrl(url)
    }

    private fun loadStore() {
        address.setText(storeUrl)
        if (!isOnline()) status.text = "Offline — showing cached pages where available"
        webView.loadUrl(storeUrl)
    }

    private fun readSavedPages(): MutableList<SavedPage> {
        val pages = mutableListOf<SavedPage>()
        val json = prefs.getString("saved_web_pages", "[]") ?: "[]"
        try {
            val array = JSONArray(json)
            for (i in 0 until array.length()) {
                val item = array.optJSONObject(i) ?: continue
                val title = item.optString("title").trim()
                val url = item.optString("url").trim()
                if (title.isNotBlank() && normalizeHttpsUrl(url) != null) pages.add(SavedPage(title, url))
            }
        } catch (_: Exception) {
            prefs.edit().putString("saved_web_pages", "[]").apply()
        }
        return pages
    }

    private fun savePages(pages: List<SavedPage>) {
        val array = JSONArray()
        pages.forEach { page ->
            array.put(JSONObject().put("title", page.title).put("url", page.url))
        }
        prefs.edit().putString("saved_web_pages", array.toString()).apply()
    }

    private fun showPagesDialog() {
        val pages = readSavedPages()
        val listView = ListView(this)
        val labels = pages.map { "${it.title}\n${it.url}" }
        listView.adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, labels)
        val dialog = AlertDialog.Builder(this)
            .setTitle("Your web pages")
            .setView(listView)
            .setPositiveButton("ADD PAGE", null)
            .setNegativeButton("CLOSE", null)
            .create()
        listView.setOnItemClickListener { _, _, position, _ ->
            openAddress(pages[position].url)
            dialog.dismiss()
        }
        listView.setOnItemLongClickListener { _, _, position, _ ->
            showPageActions(pages[position], position)
            true
        }
        dialog.setOnShowListener {
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
                showPageEditor(null, null) {
                    dialog.dismiss()
                    showPagesDialog()
                }
            }
        }
        dialog.show()
    }

    private fun showPageActions(page: SavedPage, index: Int) {
        AlertDialog.Builder(this)
            .setTitle(page.title)
            .setItems(arrayOf("Open page", "Edit page", "Delete page")) { _, choice ->
                when (choice) {
                    0 -> openAddress(page.url)
                    1 -> showPageEditor(page, index)
                    2 -> AlertDialog.Builder(this)
                        .setMessage("Delete \"${page.title}\" from your saved pages?")
                        .setPositiveButton("DELETE") { _, _ ->
                            val pages = readSavedPages()
                            if (index in pages.indices) {
                                pages.removeAt(index)
                                savePages(pages)
                                Toast.makeText(this, "Page deleted", Toast.LENGTH_SHORT).show()
                            }
                        }
                        .setNegativeButton("CANCEL", null)
                        .show()
                }
            }
            .show()
    }

    private fun showPageEditor(page: SavedPage?, index: Int?, onSaved: () -> Unit = {}) {
        val form = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(24, 8, 24, 0)
        }
        val titleInput = EditText(this).apply {
            hint = "Page name (e.g. Products)"
            setSingleLine(true)
            setText(page?.title ?: "")
        }
        val urlInput = EditText(this).apply {
            hint = "https://example.com/page"
            setSingleLine(true)
            setText(page?.url ?: "")
        }
        form.addView(titleInput)
        form.addView(urlInput)
        AlertDialog.Builder(this)
            .setTitle(if (page == null) "Add web page" else "Edit web page")
            .setView(form)
            .setPositiveButton("SAVE", null)
            .setNegativeButton("CANCEL", null)
            .create().also { dialog ->
                dialog.setOnShowListener {
                    dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
                        val url = normalizeHttpsUrl(urlInput.text.toString())
                        if (url == null) {
                            urlInput.error = "Enter a valid HTTPS address"
                            return@setOnClickListener
                        }
                        val title = titleInput.text.toString().trim().ifBlank {
                            Uri.parse(url).host ?: "Saved page"
                        }
                        val pages = readSavedPages()
                        val saved = SavedPage(title, url)
                        if (index != null && index in pages.indices) pages[index] = saved
                        else pages.add(saved)
                        savePages(pages)
                        Toast.makeText(this, "Web page saved", Toast.LENGTH_SHORT).show()
                        dialog.dismiss()
                        onSaved()
                    }
                }
                dialog.show()
            }
    }

    private fun showSetupMessage() {
        status.text = "Marketplace address required"
        webView.loadDataWithBaseURL(null, """
            <html><meta name="viewport" content="width=device-width,initial-scale=1">
            <body style="background:#0a100e;color:#e8fff0;font-family:sans-serif;padding:28px">
            <h2 style="color:#5aeb9b">Welcome to MT Digital Store</h2>
            <p>Connect this app to your deployed MT Digital Store website.</p>
            <p>Tap <b>SET URL</b> to connect your marketplace, or <b>WEB PAGES</b> to add saved websites.</p></body></html>
        """.trimIndent(), "text/html", "UTF-8", null)
        showUrlDialog()
    }

    private fun showUrlDialog() {
        val input = EditText(this).apply {
            hint = "https://your-marketplace.example"
            setSingleLine(true)
            setText(storeUrl)
        }
        AlertDialog.Builder(this)
            .setTitle("Connect MT Digital Store")
            .setMessage("Enter the HTTPS address where your MT Digital Store website is hosted.")
            .setView(input)
            .setPositiveButton("SAVE & OPEN") { _, _ -> saveAndLoad(input.text.toString()) }
            .setNegativeButton("CANCEL", null)
            .show()
    }

    private fun isOnline(): Boolean {
        val manager = getSystemService(CONNECTIVITY_SERVICE) as ConnectivityManager
        val network = manager.activeNetwork ?: return false
        val capabilities = manager.getNetworkCapabilities(network) ?: return false
        return capabilities.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
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
        super.onDestroy()
    }
}
