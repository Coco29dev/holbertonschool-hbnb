from models.BaseModel import BaseModel
from datetime import datetime

class Review(BaseModel):
    def __init__(self, text, rating, place, user, id=None):
        super().__init__(id)  # Appel du constructeur de BaseModel pour initialiser 'id', 'created_at' et 'updated_at'
        
        # Initialisation des attributs spécifiques à Review
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        # Validation des attributs
        self.validate()

    def validate(self):
        # Validation de la note
        if not (1 <= self.rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        
        # Vérification que le texte n'est pas vide
        if not self.text or len(self.text.strip()) == 0:
            raise ValueError("Review text cannot be empty")
        
        # Validation de l'existence du place et du user
        if not self.place:
            raise ValueError("Place must exist")
        if not self.user:
            raise ValueError("User must exist")

    def update_review(self, new_text, new_rating):
        self.text = new_text
        self.rating = new_rating
        self.updated_at = datetime.now()
        self.validate()  # Revalider après mise à jour