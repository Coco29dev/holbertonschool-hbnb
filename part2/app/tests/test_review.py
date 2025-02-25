import unittest
from datetime import datetime
from models.user import User
from models.place import Place
from models.review import Review

class TestReview(unittest.TestCase):
    
    def test_review_creation_valid(self):
        # Créer des objets fictifs pour Place et User (en fonction de ta structure)
        place = Place(id="place_1", name="Test Place")
        user = User(id="user_1", name="Test User")

        # Créer une Review valide
        review = Review(text="Super endroit", rating=4, place=place, user=user)

        # Vérifier que l'objet Review a bien été créé avec les bons attributs
        self.assertEqual(review.text, "Super endroit")
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.place.id, "place_1")
        self.assertEqual(review.user.id, "user_1")
        self.assertTrue(isinstance(review.created_at, datetime))
        self.assertTrue(isinstance(review.updated_at, datetime))

    def test_invalid_rating(self):
        # Créer des objets fictifs pour Place et User
        place = Place(id="place_1", name="Test Place")
        user = User(id="user_1", name="Test User")

        # Tester une review avec un rating invalide (en dehors de la plage [1, 5])
        with self.assertRaises(ValueError) as context:
            review = Review(text="Mauvais endroit", rating=6, place=place, user=user)
        
        self.assertEqual(str(context.exception), "Rating must be between 1 and 5")
