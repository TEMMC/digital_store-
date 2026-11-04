plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("com.chaquo.python")
}

android {
    namespace = "com.metmc.digitalstore"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.metmc.digitalstore"
        minSdk = 24
        targetSdk = 35
        versionCode = 4
        versionName = "3.1.0"
        ndk { abiFilters += listOf("arm64-v8a") }
    }

    buildFeatures { buildConfig = true }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }

    sourceSets.getByName("main").assets.srcDir(layout.buildDirectory.dir("generated/marketplaceAssets"))
}

chaquopy {
    defaultConfig {
        buildPython(System.getenv("CHAQUOPY_BUILD_PYTHON") ?: "python3.11")
        version = "3.11"
        pip {
            install("Flask==3.1.3")
            install("Flask-SQLAlchemy==3.1.1")
        }
    }
}

val bundleMarketplace by tasks.registering(Copy::class) {
    from(rootProject.file("app.py")) { into("marketplace") }
    from(rootProject.file("templates")) { into("marketplace/templates") }
    from(rootProject.file("static")) { into("marketplace/static") }
    into(layout.buildDirectory.dir("generated/marketplaceAssets"))
}
tasks.named("preBuild").configure { dependsOn(bundleMarketplace) }
