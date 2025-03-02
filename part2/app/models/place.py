from app.models.BaseModel import BaseModel
from app.models.user import User
from app.persistence.repository import InMemoryRepository
from app.models.amenity import Amenity


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id, user_repository, amenities=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = None
        self.reviews = []  # Liste pour stocker les avis associés
        self.amenities = amenities if amenities is not None else []

        # Vérification des contraintes de validation
        if not title or len(title) > 100:
            raise ValueError(
                "Le titre doit être compris entre 1 et 100 caractères")
        if price < 0:
            raise ValueError("Le prix doit être positif")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("La latitude doit être entre -90 et 90.")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("La longitude doit être entre -180 et 180.")

        # Vérification que l'utilisateur existe dans le repository
        owner = user_repository.get(owner_id)
        if owner is None:
            raise ValueError(
                "L'utilisateur spécifié comme propriétaire n'existe pas")
        self.owner = owner

    def add_review(self, review):
        """Ajouter un avis à la place."""
        if hasattr(review, 'to_dict'):
            self.reviews.append(review)
        else:
            raise ValueError(
                "L'objet review doit posséder une méthode to_dict()")

    def add_amenity(self, amenity):
        """Ajouter un équipement à la place."""
        if isinstance(amenity, Amenity):  # Vérifier si amenity est bien un objet Amenity
            self.amenities.append(amenity)
        else:
            raise ValueError("L'objet amenity doit être de type Amenity")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner.id if self.owner else None,
            "reviews": [review.to_dict() for review in self.reviews],
            "amenities": [
                {"id": amenity.id, "name": amenity.name} if isinstance(amenity, Amenity)
                # Si 'amenity' est un ID, on met à la fois l'ID et le nom
                else {"id": amenity, "name": amenity}
                for amenity in self.amenities
            ]
        }
