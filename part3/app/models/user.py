#!/usr/bin/python3
import re
from app.models.BaseModel import BaseModel
from app import db, bcrypt
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class User(BaseModel):
    __tablename__ = 'users'  # Nom de la table dans la base de données

    # Définition des colonnes de la table 'users'
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()  # Appel du constructeur de BaseModel

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        self.validate_email(email)
        self.validate_name(first_name, last_name)

        if password:
            self.hash_password(password)  # Hash le mot de passe avant de le stocker

    def hash_password(self, password):
        """Hache le mot de passe avant de le stocker."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Vérifie si le mot de passe fourni correspond au mot de passe haché."""
        return bcrypt.check_password_hash(self.password, password)

    def validate_email(self, email):
        email_regex = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        if not re.match(email_regex, email):
            raise ValueError("Email invalide")

    def validate_name(self, first_name, last_name):
        if not first_name or not last_name:
            raise ValueError("Le nom et le prénom ne doivent pas être vides.")
        if len(first_name) > 50 or len(last_name) > 50:
            raise ValueError(
                "Le nom ou prénom ne doit pas dépasser 50 caractères.")

    def to_dict(self):
        """Convertit l'objet en un dictionnaire."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        }