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

# =====================
# APP SETUP
# =====================

app = Flask(__name__)
app.secret_key = os.getenv(
"SECRET_KEY",
"change-this-secret-key"
)

=====================

SUPABASE STORAGE

=====================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = None

if SUPABASE_URL and SUPABASE_KEY:

try:

    supabase = create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )

except Exception as e:

    print(
        "Supabase connection failed:",
        str(e)
    )

BUCKET_NAME = "products"

=====================

DATABASE

=====================

DATABASE_URL = os.getenv(
"DATABASE_URL",
"sqlite:///store.db"
)

app.config[
"SQLALCHEMY_DATABASE_URI"
] = DATABASE_URL

app.config[
"SQLALCHEMY_TRACK_MODIFICATIONS"
] = False

app.config[
"MAX_CONTENT_LENGTH"
] = 500 * 1024 * 1024

db = SQLAlchemy(app)

=====================

UPLOADS

=====================

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

app.config[
"UPLOAD_FOLDER"
] = UPLOAD_FOLDER

=====================

MARKETPLACE SETTINGS

=====================

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

=====================

SUPABASE HELPERS

=====================

def supabase_enabled():

return (
    supabase is not None
)

def generate_filename(
filename
):

return (
    f"{uuid.uuid4()}_"
    f"{secure_filename(filename)}"
)

def public_file_url(
filename
):

return (
    f"{SUPABASE_URL}"
    f"/storage/v1/object/public/"
    f"{BUCKET_NAME}/"
    f"{filename}"
)

def upload_to_supabase(
file_object
):

if not supabase_enabled():
    return None, None

filename = generate_filename(
    file_object.filename
)

supabase.storage.from_(
    BUCKET_NAME
).upload(
    filename,
    file_object.read(),
    {
        "content-type":
        file_object.content_type
    }
)

return (
    filename,
    public_file_url(filename)
)
# =====================
# MODELS
# =====================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(200),
        unique=True
    )

    phone = db.Column(
        db.String(50)
    )

    profile_image = db.Column(
        db.String(500)
    )

    password = db.Column(
        db.String(300),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="buyer"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Product(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100)
    )

    description = db.Column(
        db.Text
    )

    price = db.Column(
        db.Float,
        default=0
    )

    is_free = db.Column(
        db.Integer,
        default=0
    )

    category = db.Column(
        db.String(50)
    )

    seller = db.Column(
        db.String(100)
    )

    file_path = db.Column(
        db.String(500)
    )

    image_path = db.Column(
        db.String(500)
    )

    views = db.Column(
        db.Integer,
        default=0
    )

    downloads = db.Column(
        db.Integer,
        default=0
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class News(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(300)
    )

    content = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Message(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    sender = db.Column(
        db.String(100)
    )

    receiver = db.Column(
        db.String(100)
    )

    message = db.Column(
        db.Text
    )

    is_read = db.Column(
        db.Integer,
        default=0
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class DownloadLog(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100)
    )

    product_id = db.Column(
        db.Integer
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    # =====================
# HEALTH CHECK
# =====================

@app.route("/health")
def health():

    return {
        "status": "ok",
        "products": Product.query.count()
    }

# =====================
# UPLOADS ROUTE
# =====================

@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )

# =====================
# HOME
# =====================

@app.route("/")
def home():

    category = request.args.get("category")
    search = request.args.get("search")

    products = Product.query

    if category:
        products = products.filter_by(
            category=category
        )

    if search:
        products = products.filter(
            Product.name.contains(search)
        )

    products = products.all()

    categories = [
        "Apps",
        "Games",
        "Documents",
        "Music",
        "Videos",
        "Ebooks",
        "Scripts",
        "Templates",
        "Courses",
        "AI Tools"
    ]

    return render_template(
        "index.html",
        products=products,
        categories=categories
    )
#=====================

#REGISTER (UPGRADED)

#=====================

@app.route("/register", methods=["GET", "POST"])
def register():

if request.method == "POST":

    username = request.form["username"].strip()
    email = request.form["email"].strip()
    phone = request.form["phone"].strip()
    password = request.form["password"]
    role = request.form["role"]

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

    hashed_password = generate_password_hash(
        password
    )

    user = User(
        username=username,
        email=email,
        phone=phone,
        password=hashed_password,
        role=role
    )

    db.session.add(user)
    db.session.commit()

    flash("Account created successfully")

    return redirect("/login")

return render_template("register.html")

#=====================

#LOGIN (UPGRADED)

#=====================

@app.route("/login", methods=["GET", "POST"])
def login():

if request.method == "POST":

    username = request.form["username"]
    password = request.form["password"]

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

    flash("Invalid username or password")

    return redirect("/login")

return render_template("login.html")
    # =====================
# LOGOUT
# =====================

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out")
    return redirect("/")


# =====================
# ADD PRODUCT (SELLER ONLY + SUPABASE UPLOAD)
# =====================

@app.route("/add", methods=["GET", "POST"])
def add():

    if "user" not in session:
        return redirect("/login")

    if session.get("role") != "seller":
        return "Access denied (seller only)"

    if request.method == "POST":

        is_free = request.form.get("is_free") == "on"

        file = request.files["file"]
        image = request.files.get("image")

        # =====================
        # UPLOAD PRODUCT FILE TO SUPABASE
        # =====================

        file_name = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
        file_bytes = file.read()

        supabase.storage.from_(BUCKET_NAME).upload(
            file_name,
            file_bytes,
            {"content-type": file.content_type}
        )

        file_path = supabase.storage.from_(
            BUCKET_NAME
        ).get_public_url(file_name)

        # =====================
        # UPLOAD IMAGE TO SUPABASE
        # =====================

        image_path = None

        if image and image.filename:

            image_name = f"{uuid.uuid4()}_{secure_filename(image.filename)}"
            image_bytes = image.read()

            supabase.storage.from_(BUCKET_NAME).upload(
                image_name,
                image_bytes,
                {"content-type": image.content_type}
            )

            image_path = supabase.storage.from_(
                BUCKET_NAME
            ).get_public_url(image_name)

        # =====================
        # SAVE PRODUCT TO DB
        # =====================

        product = Product(
            name=request.form["name"],
            description=request.form["description"],
            price=0 if is_free else float(request.form["price"] or 0),
            is_free=1 if is_free else 0,
            category=request.form["category"],
            seller=session["user"],
            file_path=file_path,
            image_path=image_path
        )

        db.session.add(product)
        db.session.commit()

        flash("Product uploaded successfully")
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

    return render_template(
        "product.html",
        product=product
    )
    # =====================
# DOWNLOAD PRODUCT
# =====================

@app.route("/download/<int:product_id>")
def download(product_id):

    product = Product.query.get(product_id)

    if not product:
        return "Not found"

    if not product.is_free:
        return "Paid product (coming soon)"

    # =====================
    # SUPABASE FILE DOWNLOAD (REDIRECT)
    # =====================

    return redirect(product.file_path)


# =====================
# DELETE PRODUCT (SELLER ONLY)
# =====================

@app.route("/delete/<int:product_id>")
def delete(product_id):

    if "user" not in session:
        return redirect("/login")

    product = Product.query.get(product_id)

    if not product:
        return "Not found"

    if product.seller != session["user"]:
        return "Not allowed"

    # NOTE:
    # Supabase file deletion can be added later if needed

    db.session.delete(product)
    db.session.commit()

    flash("Product deleted")
    return redirect("/")


# =====================
# INIT DATABASE
# =====================

with app.app_context():
    db.create_all()


# =====================
# RUN APP
# =====================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
    