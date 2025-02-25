from models.BaseModel import BaseModel
from models.user import User
from persistence.repository import InMemoryRepository


class Place(BaseModel):
    def __init__(self, title, description, price_per_night, latitude, longitude, number_rooms, owner_id, user_repository):
        super().__init__()
        self.title = title
        self.description = description
        self.price_per_night = price_per_night
        self.latitude = latitude
        self.longitude = longitude
        self.number_rooms = number_rooms
        self.owner = None
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

        if not isinstance(title, str) or not (1 <= len(title) <= 100):
            raise ValueError(
                "Le titre doit être compris entre 1 et 100 caractères")
        if not isinstance(description, str) or len(description) > 500:
            raise ValueError("La description ne doit pas dépasser 500 caractères")
        if not isinstance(price_per_night,(float, int)) or price_per_night < 0:
            raise ValueError("Le prix doit être positif")
        if not isinstance (number_rooms, int) or number_rooms < 0:
            raise ValueError("Le nombre de chambres doit être un entier positif.")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("La latitude doit être entre -90 et 90.")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("La longitude doit être entre -180 et 180.")
        
         # Vérification de l'ID du propriétaire
        if not isinstance(owner_id, str) or not owner_id.strip():
            raise ValueError("L'ID du propriétaire est invalide.")

        # vérification que l'utilisateur existe dans le repository
        owner = user_repository.get(owner_id)
        if owner is None:
            raise ValueError(
                "L'utilisateur spécifié comme propriétaire existe pas")
        self.owner = owner

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
