#!/usr/bin/python3
import re
from models.BaseModel import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.validate_email(email)
        self.validate_name(first_name, last_name)

    def validate_email(self, email):
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, email):
            raise ValueError("Email invalide")

    def validate_name(self, first_name, last_name):
        if len(first_name) > 50 or len(last_name) > 50:
            raise ValueError(
                "Le nom ou prénom ne doit pas dépasser 50 caractères.")
