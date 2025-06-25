from flask import Flask, render_template, redirect, url_for, flash, session, request
from forms import SignupForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '250e0e42a7707063093305e00304544e'

# Sample product data
products = [
    {"id": 1, "name": "Sofa", "price": 12000, "description": "Comfortable 3-seater sofa.", "image": "sofa.jpg"},
    {"id": 2, "name": "Dining Table", "price": 18000, "description": "Elegant 6-seater wooden dining table.", "image": "table.jpg"},
    {"id": 3, "name": "Chair", "price": 2500, "description": "Cushioned wooden chair for home or office.", "image": "chair.jpg"},
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        flash(f"User {form.username.data} signed up successfully!", "success")
        return redirect(url_for("home"))
    return render_template("signup.html", title="Signup", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        pw = form.password.data
        if email == "subhampanigrahy05@gmail.com" and pw == "123456":
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login failed. Please check your credentials.", "danger")
    return render_template("login.html", title="Login", form=form)

@app.route("/store")
def store():
    return render_template("store.html", title="Store", products=products)

@app.route("/product/<int:product_id>")
def product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return "Product not found", 404
    return render_template("product.html", title=product["name"], product=product)

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session["cart"] = cart
    flash("Item added to cart!", "success")
    return redirect(url_for("store"))

@app.route("/cart")
def cart():
    cart = session.get("cart", {})
    cart_items = []
    total = 0
    for pid, quantity in cart.items():
        product = next((p for p in products if p["id"] == int(pid)), None)
        if product:
            product_copy = product.copy()
            product_copy["quantity"] = quantity
            product_copy["subtotal"] = product["price"] * quantity
            cart_items.append(product_copy)
            total += product_copy["subtotal"]
    return render_template("cart.html", title="Your Cart", cart_items=cart_items, total=total)

@app.route("/clear_cart")
def clear_cart():
    session.pop("cart", None)
    flash("Cart cleared!", "danger")
    return redirect(url_for("cart"))

if __name__ == "__main__":
    app.run(debug=True)