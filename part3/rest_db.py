from app import create_app
from app.extensions import db
from app.services import get_facade
import uuid

app = create_app()

with app.app_context():
    facade = get_facade()
    
    # Données de l'utilisateur non-admin
    user_data = {
        "first_name": "Pierre",
        "last_name": "Martin",
        "email": "pierre.martin@example.com",
        "password": "motdepasse123",
        "is_admin": False
    }
    
    try:
        # Vérifier si l'utilisateur existe déjà
        existing_user = facade.user_facade.get_user_by_email(user_data["email"])
        
        if existing_user:
            print(f"Un utilisateur avec l'email {user_data['email']} existe déjà.")
            print(f"ID: {existing_user.id}")
            print(f"Nom: {existing_user.first_name} {existing_user.last_name}")
            print(f"Admin: {existing_user.is_admin}")
        else:
            # Créer l'utilisateur
            new_user = facade.user_facade.create_user(user_data)
            print(f"Utilisateur créé avec succès!")
            print(f"ID: {new_user.id}")
            print(f"Nom: {new_user.first_name} {new_user.last_name}")
            print(f"Email: {new_user.email}")
            print(f"Admin: {new_user.is_admin}")
            
            # Informations de connexion pour l'API
            print("\nUtilisez ces informations pour vous connecter à l'API:")
            print(f"Email: {new_user.email}")
            print(f"Mot de passe: {user_data['password']}")
        
        # Afficher la liste de tous les utilisateurs
        print("\nListe de tous les utilisateurs:")
        all_users = facade.user_facade.get_all_users()
        for user in all_users:
            print(f"- {user.first_name} {user.last_name} ({user.email}) {'[Admin]' if user.is_admin else ''}")
            
    except Exception as e:
        print(f"Erreur lors de la création de l'utilisateur: {e}")