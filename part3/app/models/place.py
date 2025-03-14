from app.models.BaseModel import BaseModel
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository
from app.models.amenity import Amenity
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

class Place(BaseModel):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relationship placeholders (will be added later)
    reviews = relationship("Review", back_populates="place", lazy='dynamic')
    amenities = relationship("Amenity", secondary='place_amenity', back_populates="places", lazy='dynamic')

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

        # Validation
        if not title or len(title) > 100:
            raise ValueError("Le titre doit être compris entre 1 et 100 caractères.")
        if price < 0:
            raise ValueError("Le prix doit être positif.")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("La latitude doit être entre -90 et 90.")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("La longitude doit être entre -180 et 180.")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "reviews": [review.to_dict() for review in self.reviews],
            "amenities": [{"id": amenity.id, "name": amenity.name} for amenity in self.amenities]
        }