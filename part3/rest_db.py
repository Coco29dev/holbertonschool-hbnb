#!/usr/bin/env python3
# init_db.py
# Script pour initialiser la base de données avec les données essentielles

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.amenity import Amenity
import uuid

def init_database():
    """Initialise la base de données avec des données essentielles."""
    app = create_app()
    
    with app.app_context():
        # Création des tables
        db.create_all()
        
        # Ajout de l'administrateur si non existant
        admin_email = "admin@hbnb.io"
        admin = User.query.filter_by(email=admin_email).first()
        
        if not admin:
            print("Création de l'utilisateur admin...")
            admin = User(
                first_name="Admin",
                last_name="HBnB",
                email=admin_email,
                password="admin1234",  # Sera hashé par la méthode __init__
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print(f"Admin créé avec ID: {admin.id}")
        else:
            print(f"Admin existant avec ID: {admin.id}")
        
        # Ajout des équipements de base s'ils n'existent pas
        basic_amenities = [
            {"id": "550e8400-e29b-41d4-a716-446655440000", "name": "WiFi", "description": "Connexion internet sans fil"},
            {"id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8", "name": "Swimming Pool", "description": "Piscine privée ou commune"},
            {"id": "6ba7b811-9dad-11d1-80b4-00c04fd430c8", "name": "Air Conditioning", "description": "Climatisation dans toutes les pièces"}
        ]
        
        for amenity_data in basic_amenities:
            amenity = Amenity.query.filter_by(name=amenity_data["name"]).first()
            if not amenity:
                print(f"Création de l'équipement {amenity_data['name']}...")
                amenity = Amenity(
                    name=amenity_data["name"],
                    description=amenity_data.get("description", "")
                )
                # Ajuste l'ID pour correspondre à celui du script SQL
                setattr(amenity, 'id', amenity_data["id"])
                db.session.add(amenity)
        
        db.session.commit()
        print("Base de données initialisée avec succès!")

if __name__ == "__main__":
    init_database()