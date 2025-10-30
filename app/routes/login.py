from flask import Blueprint, render_template, request, redirect, session, flash
from app.models.login import authenticate

login_bp = Blueprint('login', __name__)

@login_bp.route("/login", methods=["GET", "POST"])
def login_view():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = authenticate(email, password)
        if user:
            session['user'] = {
                'id': user['id'],
                'email': user['email'],
                'name': user['name'],
                'role': user['role']
            }
            
            return redirect("/products")
        
        else:
            flash("Invalid credentials. Please try again.")
            return redirect("/login")

    return render_template("login.html")

@login_bp.route("/logout")
def logout_view():
    session.clear()
    return redirect("/login")