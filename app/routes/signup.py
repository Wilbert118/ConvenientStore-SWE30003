import re
from flask import Blueprint, render_template, request, redirect, flash
from app.models.signup import signup

signup_bp = Blueprint('signup', __name__)

def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

def is_valid_phone(phone):
    return re.match(r"^\+?\d{8,15}$", phone)

def is_valid_address(address):
    return len(address.strip()) >= 5  

@signup_bp.route("/signup", methods=["GET", "POST"])
def signup_view():
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["name"]
        address = request.form["address"]
        phone = request.form["phone"]
        password = request.form["password"]
        role = request.form["role"]
        print(f"Signup role selected: {role}")

        if not is_valid_email(email):
            flash("Invalid email format.")
            return redirect("/signup")
        if not is_valid_phone(phone):
            flash("Invalid phone number.")
            return redirect("/signup")
        if not is_valid_address(address):
            flash("Address is too short.")
            return redirect("/signup")

        
        result = signup(email, name, password, phone, address, role)
        if result:
            return redirect("/login")
        else:
            flash("Signup failed. Try again.")
            return redirect("/signup")

    return render_template("signup.html")
