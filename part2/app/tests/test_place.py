import unittest
from models.place import Place
from models.user import User
from persistence.repository import InMemoryRepository


class TestPlace(unittest.TestCase):

    def setUp(self):
        """Initialisation avant chaque test"""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()

        # Création d'un utilisateur de test
        self.user = User(first_name="Alice", last_name= "Dupont", email="alice@example.com")
        self.user_repo.add(self.user)

        # Données valides pour un lieu
        self.valid_place_data = {
            "title": "Jolie maison",
            "description": "Une belle maison en bord de mer",
            "price_per_night": 100,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "number_rooms": 2,
            "owner_id": self.user.id,
            "user_repository": self.user_repo
        }

    def test_create_valid_place(self):
        """Test de la création d'un lieu valide"""
        place = Place(**self.valid_place_data)
        self.place_repo.add(place)

        self.assertEqual(place.title, "Jolie maison")
        self.assertEqual(place.price_per_night, 100)
        self.assertEqual(place.owner.id, self.user.id)
        self.assertEqual(len(self.place_repo.get_all()), 1)

    def test_create_place_without_owner(self):
        """Test de création d'un lieu sans propriétaire valide"""
        invalid_data = self.valid_place_data.copy()
        invalid_data["owner_id"] = "invalid_user"

        with self.assertRaises(ValueError) as context:
            Place(**invalid_data)

        self.assertIn("L'utilisateur spécifié comme propriétaire existe pas", str(context.exception))

    def test_update_place(self):
        """Test de mise à jour d'un lieu"""
        place = Place(**self.valid_place_data)
        self.place_repo.add(place)

        updated_data = {"title": "Nouvelle maison", "price_per_night": 120}
        self.place_repo.update(place.id, updated_data)

        updated_place = self.place_repo.get(place.id)
        self.assertEqual(updated_place.title, "Nouvelle maison")
        self.assertEqual(updated_place.price_per_night, 120)

    def test_add_review_to_place(self):
        """Test d'ajout d'un avis à un lieu"""
        place = Place(**self.valid_place_data)
        self.place_repo.add(place)

        review = "Super séjour !"
        place.add_review(review)

        self.assertEqual(len(place.reviews), 1)
        self.assertEqual(place.reviews[0], "Super séjour !")

    def test_add_amenity_to_place(self):
        """Test d'ajout d'un équipement à un lieu"""
        place = Place(**self.valid_place_data)
        self.place_repo.add(place)

        amenity = "Piscine"
        place.add_amenity(amenity)

        self.assertEqual(len(place.amenity), 1)
        self.assertIn("Piscine", place.amenity)


if __name__ == '__main__':
    unittest.main()
