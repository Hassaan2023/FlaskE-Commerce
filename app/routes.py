# app/routes.py

from flask import render_template, url_for, flash, redirect
from app import app, db
from app.models import User, Product, CartItem
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)

@app.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get(product_id)
    return render_template("product.html", product=product)

@app.route("/add_to_cart/<int:product_id>")
@login_required
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    cart_item = CartItem(product_id=product.id, user_id=current_user.id)
    db.session.add(cart_item)
    db.session.commit()
    flash('Product added to your cart!', 'success')
    return redirect(url_for('index'))

@app.route("/cart")
@login_required
def cart():
    cart_items = current_user.cart
    total_price = sum(item.product.price for item in cart_items)
    return render_template("cart.html", cart_items=cart_items, total_price=total_price)

@app.route("/remove_all_from_cart")
@login_required
def remove_all_from_cart():
    current_user.cart = []
    db.session.commit()
    flash('All items removed from your cart!', 'success')
    return redirect(url_for('cart'))

@app.route("/remove_from_cart/<int:item_id>")
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get(item_id)
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from your cart!', 'success')
    return redirect(url_for('cart'))
