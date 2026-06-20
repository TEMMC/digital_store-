from flask import Flask, render_template, request, redirect
from flask import session, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy

from werkzeug.utils import secure_filename
from werkzeug.security import (
generate_password_hash,
check_password_hash
)

from supabase import create_client

from datetime import datetime

import os
import uuid

#=====================

#APP SETUP

#=====================

app = Flask(__name__)

app.secret_key = os.getenv(
"SECRET_KEY",
"change-this-secret-key"
)

#Allow large uploads (up to 10GB)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024 * 1024

#=====================

#SUPABASE STORAGE

#=====================
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = None

def supabase_enabled():
       return supabase is not None


if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(
            SUPABASE_URL,
            SUPABASE_KEY
        )
        print("Supabase connected successfully")

    except Exception as e:
        print(
            "Supabase connection failed:",
            str(e)
        )

BUCKET_NAME = "products"

def supabase_enabled():
       return supabase is not None

#=====================

#DATABASE

#=====================

DATABASE_URL = os.environ.get("DATABASE_URL")

#PostgreSQL URL fix

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
           DATABASE_URL = DATABASE_URL.replace(
                "postgres://",
                "postgresql://",
               1
        )

#Local fallback

if not DATABASE_URL:
      DATABASE_URL = "sqlite:///store.db"

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#=====================

#UPLOAD CONFIG

#=====================

UPLOAD_FOLDER = os.environ.get(
"UPLOAD_FOLDER",
os.path.join(
os.getcwd(),
"uploads"
)
)

os.makedirs(
UPLOAD_FOLDER,
exist_ok=True
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

print("Database:", DATABASE_URL)
print("Upload Folder:", UPLOAD_FOLDER)
print("Supabase Enabled:", supabase_enabled())

#=====================

#MARKETPLACE SETTINGS

#=====================

MARKETPLACE_NAME = (
"METMC Digital Store"
)

SITE_VERSION = "2.0"

DEFAULT_CATEGORIES = [

"Apps",
"Games",
"Documents",
"Music",
"Videos",
"Ebooks",
"Scripts",
"Templates",
"Courses",
"AI Tools",
"Graphics",
"Themes",
"Plugins",
"Source Code",
"Education",
"Business",
"News"

]

#=====================

 #SUPABASE HELPERS

 #=====================

def supabase_enabled():
    return supabase is not None


def generate_filename(filename):
    return (
        f"{uuid.uuid4()}_"
        f"{secure_filename(filename)}"
    )


def public_file_url(filename):
    return (
        f"{SUPABASE_URL}"
        f"/storage/v1/object/public/"
        f"{BUCKET_NAME}/"
        f"{filename}"
    )


def upload_to_supabase(file_object):
    """
    Upload file to Supabase Storage.

    Returns:
    (filename, public_url)
    """

    if not supabase_enabled():
        return None, None

    filename = generate_filename(
        file_object.filename
    )

    try:

        supabase.storage.from_(
            BUCKET_NAME
        ).upload(
            path=filename,
            file=file_object,
            file_options={
                "content-type":
                file_object.content_type
            }
        )

        return (
            filename,
            public_file_url(filename)
        )

    except Exception as e:

        print(
            "Supabase upload error:",
            str(e)
        )

        return None, None
#=====================

#UPLOADS ROUTE

#=====================
@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )
#=====================

#MODELS

#=====================
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


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    content = db.Column(db.Text)
    image = db.Column(db.String(500))
    author = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100))
    receiver = db.Column(db.String(100))
    message = db.Column(db.Text)
    is_read = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    title = db.Column(db.String(300))
    message = db.Column(db.Text)
    is_read = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class DownloadLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    product_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


#=====================

#HOME

#=====================
@app.route("/")
def home():

    category = request.args.get("category")
    search = request.args.get("search")

    products = Product.query.filter_by(approved=1)

    if category:
        products = products.filter_by(category=category)

    if search:
        products = products.filter(
            Product.name.contains(search)
        )

    products = products.all()

    categories = DEFAULT_CATEGORIES

    return render_template(
        "index.html",
        products=products,
        categories=categories
    )

#=====================
# REGISTER
#=====================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        role = request.form.get(
            "role",
            "buyer"
        )

        # =====================
        # VALIDATION
        # =====================

        if not username or not email or not password:
            flash("Please fill all required fields")
            return redirect("/register")

        if len(password) < 4:
            flash("Password must be at least 4 characters")
            return redirect("/register")

        # =====================
        # CHECK DUPLICATES
        # =====================

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:
            flash("Username already exists")
            return redirect("/register")

        existing_email = User.query.filter_by(
            email=email
        ).first()

        if existing_email:
            flash("Email already exists")
            return redirect("/register")

        # =====================
        # CREATE USER
        # =====================

        try:

            user = User(
                username=username,
                email=email,
                phone=phone,
                password=generate_password_hash(
                    password
                ),
                role=role
            )

            db.session.add(user)
            db.session.commit()

            flash(
                "Account created successfully"
            )

            return redirect("/login")

        except Exception as e:

            db.session.rollback()

            print(
                "Registration error:",
                str(e)
            )

            flash(
                "Registration failed. Please try again."
            )

            return redirect("/register")

    return render_template("register.html")


#=====================
# LOGIN
#=====================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        if not username or not password:

            flash(
                "Please enter username and password"
            )

            return redirect("/login")

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            session["user"] = user.username
            session["role"] = user.role
            session["user_id"] = user.id

            flash("Login successful")

            return redirect("/")

        flash(
            "Invalid username or password"
        )

        return redirect("/login")

    return render_template("login.html")
#=====================

#LOGOUT

#=====================

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out")
    return redirect("/")

# =====================
# ADD PRODUCT
# =====================

@app.route("/add", methods=["GET", "POST"])
def add():

    if "user" not in session:
        return redirect("/login")

    if session.get("role") != "seller":
        return "Access denied (seller only)"

    if request.method == "POST":

        is_free = request.form.get("is_free") == "on"

        file_url = request.form.get("file_url", "").strip()
        image_url = request.form.get("image_url", "").strip()

        if not file_url:
            flash("File URL is required")
            return redirect("/add")

        # =====================
        # PRICE HANDLING (FIXED)
        # =====================
        try:
            price = float(request.form.get("price", 0) or 0)
        except ValueError:
            flash("Invalid price")
            return redirect("/add")

        price = 0 if is_free else price

        # =====================
        # CREATE PRODUCT
        # =====================
        product = Product(
            name=request.form.get("name"),
            description=request.form.get("description"),
            price=price,
            is_free=1 if is_free else 0,
            category=request.form.get("category"),
            seller=session["user"],
            file_path=file_url,
            image_path=image_url
        )

        db.session.add(product)
        db.session.commit()

        flash("Product added successfully")
        return redirect("/")

    return render_template("add.html")
# =====================
# VIEW SINGLE PRODUCT
# =====================

@app.route("/product/<int:product_id>")
def product(product_id):

    product = Product.query.get(product_id)

    if not product:
        return "Product not found"

    product.views = (product.views or 0) + 1
    db.session.commit()

    return render_template("product.html", product=product)

# =====================
# DOWNLOAD PRODUCT
# =====================

@app.route("/download/<int:product_id>")
def download(product_id):

    product = Product.query.get(product_id)

    if not product:
        return "Not found", 404

    if not product.is_free:
        return "Paid product (coming soon)", 403

    # increment downloads safely
    product.downloads = (product.downloads or 0) + 1
    db.session.commit()

    return redirect(product.file_path)
#=====================

#DELETE PRODUCT (SELLER ONLY)

#=====================

from flask import redirect, session, flash

@app.route("/delete/<int:product_id>", methods=["POST"])
def delete(product_id):

    if "user" not in session:
        return redirect("/login")

    product = Product.query.get(product_id)

    if not product:
        return "Not found", 404

    if product.seller != session["user"]:
        return "Not allowed", 403

    # NOTE:
    # Supabase file deletion can be added here later if needed

    db.session.delete(product)
    db.session.commit()

    flash("Product deleted successfully")
    return redirect("/")

#=====================

#INIT DATABASE

#=====================

with app.app_context():
       db.create_all()

# =====================
# DEBUG ROUTES
# =====================

@app.route("/debug")
def debug():
    return f"Products: {Product.query.count()}"


@app.route("/dbinfo")
def dbinfo():
    return app.config["SQLALCHEMY_DATABASE_URI"]
# =====================
# RUN APP
# =====================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
    
    