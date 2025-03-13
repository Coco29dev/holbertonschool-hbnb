from app.persistence.repository import UserRepository
from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Récupère un utilisateur par ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Récupère un utilisateur par son email."""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Récupère tous les utilisateurs."""
        return [user.to_dict() for user in self.user_repo.get_all()]

    def update_user(self, user_id, user_data):
        """Met à jour les informations d'un utilisateur."""
        user = self.user_repo.get(user_id)
        if not user:
            return None

        self.user_repo.update(user_id, user_data)
        return self.user_repo.get(user_id)

    def create_place(self, place_data):
        """Crée un lieu et retourne l'objet du lieu créé."""
        owner_id = place_data.get('owner_id')
        amenities_ids = place_data.get('amenities', [])

        # Vérifier si l'utilisateur existe
        owner = self.get_user(owner_id)
        if not owner:
            return {"error": "Owner not found"}, 404

        # Créer un objet Place
        new_place = Place(user_repository=self.user_repo,
                          amenity_repository=self.amenity_repo, **place_data)

        # Ajouter les amenities au lieu
        for amenity_id in amenities_ids:
            amenity = self.get_amenity(amenity_id)  # Récupérer l'objet Amenity
            if amenity:
                new_place.add_amenity(amenity)

        self.place_repo.add(new_place)
        return new_place.to_dict()  # Retourner un dict pour une API

    def get_place(self, place_id):
        """Récupère un lieu par ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Récupère tous les lieux."""
        return [place.to_dict() for place in self.place_repo.get_all()]

    def update_place(self, place_id, place_data):
        """Met à jour un lieu par ID."""
        place = self.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        # Vérification des amenities
        for amenity_id in place_data.get('amenities', []):
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                return {"error": f"Amenity {amenity_id} not found"}, 404

        # Mise à jour du lieu
        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id).to_dict()

    def create_amenity(self, amenity_data):
        """Crée un amenity."""
        if 'name' not in amenity_data:
            raise ValueError("Missing 'name' field")

        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity.to_dict()

    def get_amenity(self, amenity_id):
        """Récupère un amenity par ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Récupère tous les amenities."""
        return [amenity.to_dict() for amenity in self.amenity_repo.get_all()]

    def update_amenity(self, amenity_id, amenity_data):
        """Met à jour un amenity."""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        for key, value in amenity_data.items():
            setattr(amenity, key, value)
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity.to_dict()

    def create_review(self, review_data):
        """Crée un avis."""
        user = self.user_repo.get(review_data['user_id'])
        place = self.place_repo.get(review_data['place_id'])

        if not user or not place:
            return None

        rating = review_data.get('rating')
        if not rating or rating < 1 or rating > 5:
            return None

        # Crée l'objet Review
        review = Review(
            text=review_data["text"],
            rating=review_data["rating"],
            place=place,
            user=user
        )

        self.review_repo.add(review)
        return review.to_dict()  # Retourne l'objet Review sous forme de dict

    def get_review(self, review_id):
        """Récupère un avis par ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Récupère tous les avis."""
        return [review.to_dict() for review in self.review_repo.get_all()]

    def get_reviews_by_place(self, place_id):
        """Récupère tous les avis pour un lieu spécifique."""
        reviews = self.review_repo.get_all()
        return [review.to_dict() for review in reviews if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        """Met à jour un avis."""
        review = self.review_repo.get(review_id)
        if not review:
            return None

        for key, value in review_data.items():
            setattr(review, key, value)
        self.review_repo.update(review.id, review_data)
        return review.to_dict()

    def delete_review(self, review_id):
        """Supprime un avis."""
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.delete(review.id)
        return review.to_dict()
