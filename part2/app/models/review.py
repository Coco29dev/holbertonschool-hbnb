from models.BaseModel import BaseModel
from models.place import Place
from models.user import User


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

        self.validate()

    def validate(self):
        if not (1 <= self.rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        if not self.text or len(self.text.strip()) == 0:
            raise ValueError("Review text cannot be empty")

        if not isinstance(self.place, Place):
            raise ValueError("Place must be a valid Place instance")
        if not isinstance(self.user, User):
            raise ValueError("User must be a valid User instance")

    def update_review(self, new_text, new_rating):
        """Met à jour la review et sauvegarde les modifications"""
        self.text = new_text
        self.rating = new_rating
        self.validate()
        self.save()  # Met à jour updated_at via BaseModel
