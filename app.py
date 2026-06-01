from flask import Flask, render_template, request, redirect, session, send_file, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os

# =====================
# APP SETUP
# =====================
app = Flask(__name__)
app.secret_key = "secret123"

# =====================
# DATABASE
# =====================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =====================
# MODELS
# =====================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))  # buyer / seller

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    description = db.Column(db.Text)

    price = db.Column(db.Float)
    is_free = db.Column(db.Integer, default=0)

    category = db.Column(db.String(50))
    seller = db.Column(db.String(100))

    file_path = db.Column(db.String(255))
    image_path = db.Column(db.String(255))

# =====================
# 🔥 MISSING PART ADDED (UPLOADS ROUTE)
# =====================

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# =====================
# HOME (SEARCH + CATEGORY FILTER ADDED)
# =====================

@app.route("/")
def home():
    category = request.args.get("category")
    search = request.args.get("search")

    products = Product.query

    if category:
        products = products.filter_by(category=category)

    if search:
        products = products.filter(Product.name.contains(search))

    products = products.all()

    return render_template("index.html", products=products)

# =====================
# REGISTER
# =====================

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=request.form["password"],
            role=request.form["role"]
        )
        db.session.add(user)
        db.session.commit()
        flash("Account created!")
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
            flash("Login successful!")
            return redirect("/")
        else:
            flash("Invalid login")
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
# ADD PRODUCT (SELLER ONLY)
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

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        image_path = None
        if image and image.filename:
            image_path = os.path.join(UPLOAD_FOLDER, image.filename)
            image.save(image_path)

        product = Product(
            name=request.form["name"],
            description=request.form["description"],
            price=0 if is_free else float(request.form["price"]),
            is_free=1 if is_free else 0,
            category=request.form["category"],
            seller=session["user"],
            file_path=file_path,
            image_path=image_path
        )

        db.session.add(product)
        db.session.commit()

        flash("Product uploaded successfully!")
        return redirect("/")

    return render_template("add.html")

# =====================
# DOWNLOAD SYSTEM (FIXED ROUTE)
# =====================

@app.route("/download/<int:id>")
def download(id):
    product = Product.query.get(id)

    if not product:
        return "Not found"

    if not product.is_free:
        return "Paid product (payment system coming soon)"

    return send_file(product.file_path, as_attachment=True)

# =====================
# INIT DB
# =====================

with app.app_context():
    db.create_all()

# =====================
# RUN SERVER
# =====================

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")