from flask_app.config.mysqlconnection import connect_to_mysql
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Recipe:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.under = data["under"]
        self.posted_by = data["posted_by"]
        self.description = data["description"]
        self.instruction = data["instruction"]
        self.date_cooked = data["date_cooked"]
        self.users_id = data["users_id"]

    @classmethod
    def add_recipe(cls, data):
        query = """insert into recipes (name , under, posted_by, users_id, description, instruction, date_cooked) values (%(name)s, %(under)s, %(posted_by)s, %(users_id)s, %(description)s, %(instruction)s, %(date_cooked)s) """
        recipe_id = connect_to_mysql("recipe_db").query_db(query, data)
        return recipe_id
    
    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if len(data["name"]) ==1:
            flash("Name cannot be empty!")
            return False

        if len(data["name"]) >= 100:
            flash("Name cannot be longer than 100 chars!")
            return False
        
        if len(data["instruction"]) >= 160:
            flash("Instruction cannot be longer than 160 chars!")
            return False
        
        if len(data["instruction"]) == 160:
            flash("Instruction cannot be longer than 100 chars")
            return False
        
        return is_valid
    

    @classmethod
    def edit_recipe_by_id(cls,data):
        query = """update recipes set name = %(name)s, description = %(description)s, instruction = %(instruction)s where id= %(id)s """
        connect_to_mysql("recipe_db").query_db(query,data)
        return


    @classmethod
    def delete_recipe_by_id(cls,id):
        query = """delete from recipes where id = %(id)s """
        connect_to_mysql("recipe_db").query_db(query, {"id": id})
        return


    @classmethod
    def get_all_rec(cls):
        query = """SELECT * FROM recipes"""
        results = connect_to_mysql("recipe_db").query_db(query)
        recipes = []
        if results:
            for row in results:
                recipes.append(cls(row))
        return recipes

    @classmethod
    def get_by_id(cls, id):
        query = """SELECT * FROM recipes WHERE id = %(id)s"""
        result = connect_to_mysql("recipe_db").query_db(query, {"id": id})
        if result:
            return cls(result[0])
        return None

    @classmethod
    def is_owner(cls, recipe_id, user_id):
        query = """SELECT * FROM recipes WHERE id = %(id)s AND users_id = %(user_id)s"""
        result = connect_to_mysql("recipe_db").query_db(query, {"id": recipe_id, "user_id": user_id})
        return bool(result)
        
        
