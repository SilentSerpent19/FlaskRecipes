from flask_app.models.user import User
from flask_app import app
from flask  import render_template, request, session, redirect
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/user/signup")
def sign_up_form():
    if "user_id" not in session:
        return render_template("sign_up.html")
    return redirect("/recipes/all")

@app.route("/user/signup", methods = ["post"])
def sign_up():

    data = {
        "first_name" : request.form.get("first_name"),
        "last_name" : request.form.get("last_name"),
        "email" : request.form.get("email"),
        "password" : request.form.get("password"),
        "confirm_password" : request.form.get("confirm_password"),
        "gender" : request.form.get("gender"),
        "birthday" : request.form.get("birthday")}
    
    if not User.validate_data(data):
        return redirect("/user/signup")
    
    hashed_password = bcrypt.generate_password_hash(data["password"])
    data["password"] = hashed_password

    user_id = User.register_user(data)
    session["user_id"] = user_id

    return redirect("/recipes/all")


@app.route("/")
def user_login_form():
    if "user_id" in session:
        return redirect("/recipe/add")
    return render_template("login.html")

@app.route("/user/login", methods = ["post"])
def user_login():

    email = request.form["email"]
    password = request.form["password"]

    data = {
        "email" : email,
        "password" : password
    }

    if not User.validate_login_data(data):
        return redirect("/")
    
    my_user = User.get_by_email({"email": email})

    if my_user:
        if not bcrypt.check_password_hash(my_user.password, request.form["password"]):
            flash("Invalid Password")
            return redirect("/")
        
        else:
            session["user_id"] = my_user.id
            return redirect("/recipes/all")
    
    else:
        flash("Incorrect password/email!")
        return redirect("/")
        

@app.route("/user/logout", methods=["POST"])
def logout():
    if "user_id" in session:
        del session["user_id"]
    
    return redirect("/")
