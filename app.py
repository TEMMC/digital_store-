from flask import Flask, render_template, request, redirect, session
from flask import send_file, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy

from werkzeug.utils import secure_filename
from supabase import create_client

import os
import uuid

# =====================
# APP SETUP
# =====================

app = Flask(__name__)
app.secret_key = "secret123"

# =====================
# SUPABASE STORAGE
# =====================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = None

if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )

BUCKET_NAME = "products"

# =====================
# DATABASE
# =====================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///store.db"
)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =====================
# UPLOADS
# =====================

UPLOAD_FOLDER = os.environ.get(
    "UPLOAD_FOLDER",
    os.path.join(os.getcwd(), "uploads")
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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

    password = db.Column(
        db.String(100),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="buyer"
    )


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    description = db.Column(db.Text)

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

# =====================
# REGISTER
# =====================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        existing = User.query.filter_by(
            username=request.form["username"]
        ).first()

        if existing:
            flash("Username already exists")
            return redirect("/register")

        user = User(
            username=request.form["username"],
            password=request.form["password"],
            role=request.form["role"]
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully")
        return redirect("/login")

    return render_template("register.html")

# =====================
# LOGIN
# =====================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        user = User.query.filter_by(
            username=request.form["username"],
            password=request.form["password"]
        ).first()

        if user:

            session["user"] = user.username
            session["role"] = user.role

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
    