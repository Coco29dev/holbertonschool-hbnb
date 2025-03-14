from app.models import Place
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)
    
    # Exemple de méthode spécifique pour Place
    def get_places_by_max_price(self, max_price):
        return self.model.query.filter(Place.price <= max_price).all()
