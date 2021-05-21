from django.db import models
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re

# Create your models here.
class UserManager(models.Manager):
    def register_validator(self, session_data, post_data, emails_list):
        errors = {}
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        if len(post_data["first_name"]) < 2:
            errors["first_name_length"] = "First name should be at least 2 characters"
        elif not post_data["first_name"].isalpha():
            errors["first_name_letters"] = "First name should only contain letters"
        else:
            session_data["first_name"] = post_data["first_name"]
        if len(post_data["last_name"]) < 2:
            errors["last_name_length"] = "Last name should be at least 2 characters"
        elif not post_data["last_name"].isalpha():
            errors["last_name_length"] = "Last name should only contain letters"
        else:
            session_data["last_name"] = post_data["last_name"]
        if datetime.strptime(post_data["birth_date"], "%Y-%m-%d") > datetime.now():
            errors["birthday_in_the_future"] = "Your birth date should be in the past"
        elif relativedelta(datetime.today(), datetime.strptime(post_data["birth_date"], "%Y-%m-%d")).years < 13:
            errors["too_young"] = "You should be at least 13 years old"
        else:
            session_data["birth_date"] = post_data["birth_date"]
        if not EMAIL_REGEX.match(post_data["email"]):
            errors["invalid_email"] = "Invalid email address!"
        elif post_data["email"] in emails_list:
            errors["existing_email"] = "This email already exists!"
        else:
            session_data["email"] = post_data["email"]
        if len(post_data["password"]) < 8:
            errors["password_length"] = "Password should be at least 8 characters"
        if post_data["password"] != post_data["confirm_password"]:
            errors["password_confirmation"] = "Password confirmation doesn't match the password"
        return errors

    def login_validator(self, session_data, post_data, emails_list):
        errors = {}
        if post_data["email_login"] not in emails_list:
            errors["non_existing_email"] = "Unknown email"
        else:
            session_data["email_login"] = post_data["email_login"]
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=100)
    birth_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
