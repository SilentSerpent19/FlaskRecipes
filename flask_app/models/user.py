from flask_app.config.mysqlconnection import connect_to_mysql
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.confirm_password = data.get("confirm_password")
        self.gender = data["gender"]
        self.birthday = data["birthday"]


    @classmethod
    def register_user(cls,data):
        query = """insert into users (first_name, last_name, email, password, gender, birthday) values (%(first_name)s,%(last_name)s,%(email)s,%(password)s,%(gender)s,%(birthday)s) """
        users_id = connect_to_mysql("recipe_db").query_db(query,data)
        return users_id

    @staticmethod
    def validate_data(data):
        is_valid = True

        if not EMAIL_REGEX.match(data["email"]):
            flash("Invalid Email!")
            return False
        
        if len(data["password"]) < 5:
            flash("Password should be longer than 5 chars!")
            return False
        
        if len(data["first_name"]) < 2 or len(data["last_name"]) < 2:
            flash("First and last name should be longer than 2 chars!")
            return False
        
        return is_valid
    

    @classmethod
    def get_by_email(cls, data):
        query = """select * from users where email = %(email)s """
        result = connect_to_mysql("recipe_db").query_db(query, data)
        if result:
            return cls(result[0])

    @classmethod
    def get_name_by_id(cls, data):
        query = """select first_name from users where id = %(id)s """
        result = connect_to_mysql("recipe_db").query_db(query, data)
        if result:
            return result[0]
        
    @staticmethod
    def validate_login_data(data):
        is_valid = True

        if not EMAIL_REGEX.match(data["email"]):
            flash("Invalid Email!")
            return False
        if len(data["password"]) < 5:
            flash("Password too short")
            return False
        
        return is_valid
    
    