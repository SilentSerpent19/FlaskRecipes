from flask_app.models.recipe import Recipe
from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User

@app.route("/recipes/all")
def get_all_recipes():
    if "user_id" not in session:
        return redirect("/user/login")
    recipes = Recipe.get_all_rec()
    return render_template("recipe.html", data=recipes)

@app.route("/recipe/add", methods=["GET"])
def add_recipe_form():
    if "user_id" not in session:
        return redirect("/user/login")
    return render_template("add_recipe.html")

@app.route("/recipe/add", methods=["POST"])
def add_recipe():
    if "user_id" not in session:
        return redirect("/user/login")

    user_name = User.get_name_by_id({"id": session['user_id']})['first_name']
    data = {
        "name": request.form.get("name"),
        "under": request.form.get("under"),
        "posted_by": user_name,
        "description": request.form.get("description"),
        "instruction": request.form.get("instruction"),
        "date_cooked": request.form.get("date_cooked"),
        "users_id": session['user_id']
    }

    if not Recipe.validate_recipe(data):
        return redirect("/recipe/add")
    
    Recipe.add_recipe(data)
    flash("Recipe added successfully!")
    return redirect("/recipes/all")

@app.route("/recipe/<int:id>")
def show_recipe(id):
    if "user_id" not in session:
        return redirect("/user/login")
    
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash("Recipe not found!")
        return redirect("/recipes/all")
    
    return render_template("show_recipe.html", recipe=recipe)

@app.route("/recipe/edit/<int:id>", methods=["GET"])
def edit_recipe_form(id):
    if "user_id" not in session:
        return redirect("/user/login")
    
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash("Recipe not found!")
        return redirect("/recipes/all")
    
    if not Recipe.is_owner(id, session['user_id']):
        flash("You can only edit your own recipes!")
        return redirect("/recipes/all")
    
    return render_template("edit_recipe.html", recipe=recipe)

@app.route("/recipe/edit/<int:id>", methods=["POST"])
def edit_recipe(id):
    if "user_id" not in session:
        return redirect("/user/login")
    
    if not Recipe.is_owner(id, session['user_id']):
        flash("You can only edit your own recipes!")
        return redirect("/recipes/all")
    
    data = {
        "id": id,
        "name": request.form.get("name"),
        "description": request.form.get("description"),
        "instruction": request.form.get("instruction"),
        "under": request.form.get("under"),
        "date_cooked": request.form.get("date_cooked")
    }
    
    if not Recipe.validate_recipe(data):
        return redirect(f"/recipe/edit/{id}")
    
    Recipe.edit_recipe_by_id(data)
    flash("Recipe updated successfully!")
    return redirect("/recipes/all")

@app.route("/recipe/delete/<int:id>", methods=["POST"])
def delete_recipe(id):
    if "user_id" not in session:
        return redirect("/user/login")
    
    if not Recipe.is_owner(id, session['user_id']):
        flash("You can only delete your own recipes!")
        return redirect("/recipes/all")
    
    Recipe.delete_recipe_by_id(id)
    flash("Recipe deleted successfully!")
    return redirect("/recipes/all")

