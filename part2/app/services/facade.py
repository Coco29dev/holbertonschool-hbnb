from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review 

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Récupère la liste de tous les utilisateurs."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Met à jour les informations d'un utilisateur."""
        user = self.user_repo.get(user_id)
        if not user:
            return None  # Si l'utilisateur n'existe pas
        for key, value in user_data.items():
            setattr(user, key, value)
        self.user_repo.update(user)
        return user
    
    def create_place(self, place_data, user_repository):
        # verifier que owner_id est présent et valide
        owner_id = place_data.get("owner_id")
        if not owner_id or not isinstance(owner_id, str) or not owner_id.strip():
            raise ValueError("L'ID du propriétaire est invalide")
        # verifier que l'utilisateur existe
        owner = user_repository.get(owner_id)
        if owner is None:
            raise ValueError("L'utilisateur spécifié comme propriétaire existe pas")
        # créer nouvelle instance de Place
        place = Place(
        title=place_data["title"],
        description=place_data["description"],
        price_per_night=place_data["price_per_night"],
        latitude=place_data["latitude"],
        longitude=place_data["longitude"],
        number_rooms=place_data["number_rooms"],
        owner_id=owner_id,
        user_repository=user_repository
    )
        # ajouter l'annonce à la BDD
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)
    
    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None # si la place existe pas
        for key, value in place_data.items():
            if hasattr(place, key): # verification si l'attribut existe avant modification
                setattr(place, key, value)
        self.place_repo.update(place_id, place_data) # sauvegarde la mise à jour
        return place # retourn le lieu mis à jour
    
    def search_places(self, criteria):
        places = self.place_repo.get_all() #recuperer toutes les places

        # filtrage en fonction des critères
        if "max_price" in criteria:
            places = [p for p in places if p.price_per_night <= criteria["max_price"]]
        if "min_rooms" in criteria:
            places = [p for p in places if p.number_rooms >= criteria["min_rooms"]]
        if "latitude" in criteria and "longitude" in criteria:
            tolerance = criteria.get("tolerance", 0.1)
            places =[p for p in places if abs(p.latitude - criteria["latitude"]) <= tolerance
                                              and abs(p.longitude - criteria["longitude"]) <= tolerance]
        return places
    
    def delete_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        self.place_repo.delete(place_id)
        return True # suppression réussie
    
    def add_review_to_place(self, place_id, review_data):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Lieu introuvable")
        user_id = review_data.get("user_id")
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("Utilisateur introuvable.")
        if "rating" not in review_data or not (1 <= review_data["rating"] <= 5):
            raise ValueError("La note doit être comprise entre 1 et 5.")
        
        review = Review(
            text=review_data["test"],
            rating=review_data["rating"],
            user_id=user_id
        )
        
        place.add_review(review)
        self.place_repo.update(place_id, place)
        return review


    def get_all_places(self):
        return self.place_repo.get_all()
    
    def create_amenity(self, amenity_data):
        if 'name' not in amenity_data:
            raise ValueError("Missing 'name' field")

        # Create a new amenity and save it
        amenity = amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all() or []

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        for key, value in amenity_data.items():
            setattr(amenity, key, value)
        self.amenity_repo.update(amenity)
        return amenity

