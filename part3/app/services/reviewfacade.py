from app.services.repositories.review_repository import ReviewRepository
from app.models.review import Review


class ReviewFacade:
    def __init__(self, user_facade, place_facade):
        self.review_repo = ReviewRepository()
        self.user_facade = user_facade
        self.place_facade = place_facade

    def create_review(self, review_data):
        user = self.user_facade.get_user(review_data['user_id'])
        # Utiliser load_reviews=False pour éviter la récursion
        place = self.place_facade.get_place(
            review_data['place_id'], load_reviews=False)

        if not user or not place:
            return None

        rating = review_data.get('rating')
        if not rating or rating < 1 or rating > 5:
            return None

        # Créer la review avec les objets complets
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user
        )
        self.review_repo.add(review)

        # Ajouter la review à la place (non persisté en DB car pas de relation)
        place.add_review(review)

        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_reviews_by_place(self, place_id):
        """
        Récupère les reviews associées à un lieu - cette méthode vérifie d'abord 
        que le lieu existe, ce qui peut causer une récursion si utilisée dans get_place()
        """
        # Utiliser load_reviews=False pour éviter la récursion
        place = self.place_facade.get_place(place_id, load_reviews=False)
        if not place:
            return None

        # Récupérer les reviews directement
        return self.get_reviews_by_place_direct(place_id)

    def get_reviews_by_place_direct(self, place_id):
        """
        Récupère les reviews directement depuis le repository sans vérifier l'existence du lieu
        """
        # Rechercher les avis pour ce lieu directement sans passer par get_place
        return [review for review in self.review_repo.get_all()
                if review.place_id == place_id]

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        # Mettre à jour uniquement le texte et la note
        if 'text' in review_data and 'rating' in review_data:
            review.update_review(review_data['text'], review_data['rating'])

        return review

    def delete_review(self, review_id):
        if not self.review_repo.get(review_id):
            return None
        self.review_repo.delete(review_id)
        return {"message": "Review deleted successfully"}, 200
