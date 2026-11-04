"""MT Digital Store — local-first Flask marketplace.
Existing User and Product columns are retained for SQLite compatibility.
"""
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
from urllib.parse import urlparse
import os, uuid, hmac

from flask import (Flask, render_template, request, redirect, url_for, session,
                   flash, send_from_directory, abort, jsonify)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(32)
app.config.update(
    MAX_CONTENT_LENGTH=100 * 1024 * 1024,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,  # local HTTP loopback WebView
    PERMANENT_SESSION_LIFETIME=timedelta(days=14),
)
db_url = os.environ.get("DATABASE_URL") or "sqlite:///store.db"
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

MARKETPLACE_NAME = "MT Digital Store"
SITE_VERSION = "3.0"
DEFAULT_CATEGORIES = ["Apps", "Games", "Documents", "Music", "Videos", "Ebooks",
    "Scripts", "Templates", "Courses", "AI Tools", "Graphics", "Themes",
    "Plugins", "Source Code", "Education", "Business", "News", "Utilities",
    "Photography", "Productivity", "Developer Tools"]
UPLOAD_FOLDER = os.path.abspath(os.environ.get("UPLOAD_FOLDER", os.path.join(os.getcwd(), "uploads")))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_FILES = {"zip", "apk", "pdf", "epub", "mp3", "mp4", "png", "jpg", "jpeg",
                 "webp", "gif", "txt", "md", "docx", "xlsx", "pptx", "py", "js",
                 "html", "css", "json", "7z", "tar", "gz"}
ALLOWED_IMAGES = {"png", "jpg", "jpeg", "webp", "gif"}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    phone = db.Column(db.String(50))
    password = db.Column(db.String(300), nullable=False)
    role = db.Column(db.String(20), default="buyer")
    bio = db.Column(db.Text)
    country = db.Column(db.String(100))
    profile_image = db.Column(db.String(500))
    verified = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, default=0)
    is_free = db.Column(db.Integer, default=0)
    category = db.Column(db.String(100))
    seller = db.Column(db.String(100))
    file_path = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.Text)
    supabase_file = db.Column(db.String(500))
    supabase_image = db.Column(db.String(500))
    views = db.Column(db.Integer, default=0)
    downloads = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0)
    rating_count = db.Column(db.Integer, default=0)
    featured = db.Column(db.Integer, default=0)
    approved = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint("user_id", "product_id", name="uq_favorite_user_product"),)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1200), default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint("user_id", "product_id", name="uq_review_user_product"),)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, default="")
    is_read = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def current_user():
    uid = session.get("user_id")
    return db.session.get(User, uid) if uid else None

def login_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if not current_user():
            flash("Please sign in to continue.")
            return redirect(url_for("login", next=request.path))
        return fn(*args, **kwargs)
    return wrapped

def seller_required(fn):
    @wraps(fn)
    @login_required
    def wrapped(*args, **kwargs):
        user = current_user()
        if user.role not in ("seller", "admin"):
            abort(403)
        return fn(*args, **kwargs)
    return wrapped

def admin_required(fn):
    @wraps(fn)
    @login_required
    def wrapped(*args, **kwargs):
        if current_user().role != "admin":
            abort(403)
        return fn(*args, **kwargs)
    return wrapped

def safe_upload(file, image=False):
    if not file or not file.filename:
        return None
    name = secure_filename(file.filename)
    if not name or "." not in name:
        raise ValueError("Choose a file with a valid extension.")
    ext = name.rsplit(".", 1)[1].lower()
    allowed = ALLOWED_IMAGES if image else ALLOWED_FILES
    if ext not in allowed:
        raise ValueError("That file type is not supported.")
    stored = f"{uuid.uuid4().hex}_{name}"
    file.save(os.path.join(UPLOAD_FOLDER, stored))
    return "/uploads/" + stored

def valid_external_url(value):
    if not value:
        return None
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("External product links must use HTTPS.")
    return value

def notify(username, title, message):
    db.session.add(Notification(username=username, title=title, message=message))

@app.after_request
def security_headers(response):
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
    return response

@app.context_processor
def inject_globals():
    session.setdefault("_csrf_token", uuid.uuid4().hex)
    user = current_user()
    unread = Notification.query.filter_by(username=user.username, is_read=0).count() if user else 0
    return {"MARKETPLACE_NAME": MARKETPLACE_NAME, "SITE_VERSION": SITE_VERSION,
            "current_user": user, "unread_notifications": unread, "csrf_token": session.get("_csrf_token") }

@app.before_request
def protect_post_requests():
    if request.method == "POST":
        expected = session.get("_csrf_token", "")
        supplied = request.form.get("_csrf_token", "") or request.headers.get("X-CSRF-Token", "")
        if not expected or not supplied or not hmac.compare_digest(expected, supplied):
            abort(400, description="Security token missing or expired. Reload the page and try again.")

@app.errorhandler(413)
def too_large(_error):
    flash("That upload is too large. The maximum file size is 100 MB.")
    return redirect(request.referrer or url_for("home"))

@app.route("/")
def home():
    query = Product.query.filter_by(approved=1)
    search = request.args.get("search", "").strip()[:100]
    category = request.args.get("category", "").strip()
    sort = request.args.get("sort", "newest")
    if search:
        like = f"%{search}%"
        query = query.filter(db.or_(Product.name.ilike(like), Product.description.ilike(like), Product.category.ilike(like)))
    if category in DEFAULT_CATEGORIES:
        query = query.filter_by(category=category)
    if sort == "popular":
        query = query.order_by(Product.downloads.desc(), Product.views.desc())
    elif sort == "top":
        query = query.order_by(Product.rating.desc(), Product.rating_count.desc())
    elif sort == "price_low":
        query = query.order_by(Product.price.asc())
    elif sort == "price_high":
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.created_at.desc())
    page = max(1, request.args.get("page", 1, type=int))
    pagination = query.paginate(page=page, per_page=12, error_out=False)
    favorites = set()
    user = current_user()
    if user:
        favorites = {x.product_id for x in Favorite.query.filter_by(user_id=user.id).all()}
    trending = Product.query.filter_by(approved=1).order_by(Product.downloads.desc()).limit(4).all()
    return render_template("index.html", products=pagination.items, pagination=pagination,
        categories=DEFAULT_CATEGORIES, search=search, selected_category=category,
        sort=sort, favorites=favorites, trending=trending)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "buyer")
        if not username or len(username) < 3 or len(username) > 40:
            flash("Username must be 3–40 characters.")
            return redirect(url_for("register"))
        if not email or len(password) < 8:
            flash("Enter a valid email and a password of at least 8 characters.")
            return redirect(url_for("register"))
        if role not in ("buyer", "seller"):
            role = "buyer"  # public registration can never create an administrator
        if User.query.filter(db.or_(User.username.ilike(username), User.email.ilike(email))).first():
            flash("That username or email is already registered.")
            return redirect(url_for("register"))
        user = User(username=username, email=email, phone=request.form.get("phone", "").strip(),
                    password=generate_password_hash(password), role=role)
        db.session.add(user)
        db.session.commit()
        flash("Account created. You can now sign in.")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter(db.or_(User.username.ilike(username), User.email.ilike(username.lower()))).first()
        if user and check_password_hash(user.password, password):
            session.clear()
            session.permanent = True
            session["user_id"] = user.id
            session["user"] = user.username
            session["role"] = user.role
            target = request.args.get("next", "")
            if not target.startswith("/") or target.startswith("//"):
                target = url_for("home")
            return redirect(target)
        flash("Invalid sign-in details.")
    return render_template("login.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("You have signed out.")
    return redirect(url_for("home"))

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = current_user()
    if request.method == "POST":
        user.bio = request.form.get("bio", "")[:500]
        user.phone = request.form.get("phone", "")[:50]
        user.country = request.form.get("country", "")[:100]
        new_password = request.form.get("new_password", "")
        if new_password:
            if len(new_password) < 8:
                flash("New password must be at least 8 characters.")
                return redirect(url_for("profile"))
            if not check_password_hash(user.password, request.form.get("current_password", "")):
                flash("Current password did not match.")
                return redirect(url_for("profile"))
            user.password = generate_password_hash(new_password)
        db.session.commit()
        flash("Profile updated.")
        return redirect(url_for("profile"))
    return render_template("profile.html", user=user)

@app.route("/add", methods=["GET", "POST"])
@seller_required
def add():
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            if not name or len(name) > 200:
                raise ValueError("Product name is required (maximum 200 characters).")
            is_free = request.form.get("is_free") == "on"
            price = float(request.form.get("price", "0") or 0)
            if price < 0:
                raise ValueError("Price cannot be negative.")
            file_path = safe_upload(request.files.get("file")) or valid_external_url(request.form.get("file_url", "").strip())
            if not file_path:
                raise ValueError("Choose a product file or provide an HTTPS download link.")
            image_path = safe_upload(request.files.get("image"), image=True) or valid_external_url(request.form.get("image_url", "").strip())
            category = request.form.get("category", "Apps")
            if category not in DEFAULT_CATEGORIES:
                category = "Apps"
            product = Product(name=name, description=request.form.get("description", "")[:10000],
                price=0 if is_free else price, is_free=int(is_free), category=category,
                seller=current_user().username, file_path=file_path, image_path=image_path)
            db.session.add(product)
            db.session.commit()
            flash("Your product is now listed.")
            return redirect(url_for("dashboard"))
        except (ValueError, OSError) as exc:
            db.session.rollback()
            flash(str(exc))
    return render_template("add.html", categories=DEFAULT_CATEGORIES)

@app.route("/product/<int:product_id>")
def product(product_id):
    item = db.get_or_404(Product, product_id)
    if not item.approved and (not current_user() or current_user().role != "admin"):
        abort(404)
    item.views = (item.views or 0) + 1
    db.session.commit()
    reviews = Review.query.filter_by(product_id=item.id).order_by(Review.created_at.desc()).limit(30).all()
    favorite = bool(current_user() and Favorite.query.filter_by(user_id=current_user().id, product_id=item.id).first())
    return render_template("product.html", product=item, reviews=reviews, favorite=favorite)

@app.route("/favorite/<int:product_id>", methods=["POST"])
@login_required
def favorite(product_id):
    item = db.get_or_404(Product, product_id)
    user = current_user()
    existing = Favorite.query.filter_by(user_id=user.id, product_id=item.id).first()
    if existing:
        db.session.delete(existing)
        flash("Removed from your saved items.")
    else:
        db.session.add(Favorite(user_id=user.id, product_id=item.id))
        flash("Saved to your favourites.")
    db.session.commit()
    return redirect(request.referrer or url_for("home"))

@app.route("/favorites")
@login_required
def favorites():
    items = Product.query.join(Favorite, Favorite.product_id == Product.id).filter(
        Favorite.user_id == current_user().id).order_by(Favorite.created_at.desc()).all()
    return render_template("favorites.html", products=items)

@app.route("/review/<int:product_id>", methods=["POST"])
@login_required
def review(product_id):
    item = db.get_or_404(Product, product_id)
    rating = request.form.get("rating", type=int)
    comment = request.form.get("comment", "").strip()[:1200]
    if rating not in range(1, 6):
        flash("Choose a rating from 1 to 5.")
        return redirect(url_for("product", product_id=item.id))
    review_item = Review.query.filter_by(user_id=current_user().id, product_id=item.id).first()
    if review_item is None:
        review_item = Review(user_id=current_user().id, product_id=item.id, rating=rating)
        db.session.add(review_item)
    review_item.rating, review_item.comment = rating, comment
    db.session.flush()
    stats = db.session.query(db.func.avg(Review.rating), db.func.count(Review.id)).filter_by(product_id=item.id).first()
    item.rating = round(float(stats[0] or 0), 2)
    item.rating_count = int(stats[1] or 0)
    db.session.commit()
    flash("Thanks — your review has been saved.")
    return redirect(url_for("product", product_id=item.id))

@app.route("/download/<int:product_id>")
def download(product_id):
    item = db.get_or_404(Product, product_id)
    if not item.approved:
        abort(404)
    if not item.is_free:
        flash("This item is paid. Secure checkout has not been enabled yet.")
        return redirect(url_for("product", product_id=item.id))
    item.downloads = (item.downloads or 0) + 1
    db.session.commit()
    if item.file_path.startswith("/uploads/"):
        filename = item.file_path.rsplit("/", 1)[-1]
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    return redirect(item.file_path)

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/dashboard")
@seller_required
def dashboard():
    items = Product.query.filter_by(seller=current_user().username).order_by(Product.created_at.desc()).all()
    return render_template("dashboard.html", products=items)

@app.route("/edit/<int:product_id>", methods=["GET", "POST"])
@seller_required
def edit(product_id):
    item = db.get_or_404(Product, product_id)
    if item.seller != current_user().username and current_user().role != "admin":
        abort(403)
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            price = float(request.form.get("price", "0") or 0)
            if not name or price < 0:
                raise ValueError("Enter a product name and a non-negative price.")
            item.name = name[:200]
            item.description = request.form.get("description", "")[:10000]
            item.is_free = int(request.form.get("is_free") == "on")
            item.price = 0 if item.is_free else price
            category = request.form.get("category", item.category)
            if category in DEFAULT_CATEGORIES:
                item.category = category
            db.session.commit()
            flash("Product updated.")
            return redirect(url_for("dashboard"))
        except ValueError as exc:
            db.session.rollback()
            flash(str(exc))
    return render_template("edit.html", product=item, categories=DEFAULT_CATEGORIES)

@app.route("/delete/<int:product_id>", methods=["POST"])
@seller_required
def delete(product_id):
    item = db.get_or_404(Product, product_id)
    if item.seller != current_user().username and current_user().role != "admin":
        abort(403)
    Favorite.query.filter_by(product_id=item.id).delete(synchronize_session=False)
    Review.query.filter_by(product_id=item.id).delete(synchronize_session=False)
    db.session.delete(item)
    db.session.commit()
    flash("Product removed.")
    return redirect(url_for("dashboard"))

@app.route("/admin")
@admin_required
def admin():
    items = Product.query.order_by(Product.created_at.desc()).all()
    users = User.query.order_by(User.created_at.desc()).limit(100).all()
    return render_template("admin.html", products=items, users=users)

@app.route("/approve/<int:product_id>", methods=["POST"])
@admin_required
def approve(product_id):
    item = db.get_or_404(Product, product_id)
    item.approved = 1
    notify(item.seller, "Product approved", f"{item.name} is now visible in the marketplace.")
    db.session.commit()
    flash("Product approved.")
    return redirect(url_for("admin"))

@app.route("/notifications")
@login_required
def notifications():
    items = Notification.query.filter_by(username=current_user().username).order_by(Notification.created_at.desc()).limit(100).all()
    for item in items:
        item.is_read = 1
    db.session.commit()
    return render_template("notifications.html", notifications=items)

@app.route("/api/v1/status")
def api_status():
    return jsonify({"name": MARKETPLACE_NAME, "version": SITE_VERSION, "status": "online",
                    "mode": "local-first", "features": ["catalog-search", "seller-dashboard",
                    "favorites", "reviews", "notifications", "local-uploads"]})

@app.route("/health")
def health():
    try:
        db.session.execute(db.text("SELECT 1"))
        return jsonify({"status": "ok", "database": "connected"}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"status": "degraded", "database": "unavailable"}), 503

with app.app_context():
    db.create_all()
    # Optional administrator bootstrap: set MT_ADMIN_USERNAME to an existing account.
    admin_name = os.environ.get("MT_ADMIN_USERNAME", "").strip()
    if admin_name:
        account = User.query.filter_by(username=admin_name).first()
        if account and account.role != "admin":
            account.role = "admin"
            db.session.commit()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "8765")), debug=False)
