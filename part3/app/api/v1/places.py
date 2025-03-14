from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import get_facade

api = Namespace('places', description='Place operations')

# Définir les modèles pour les entités associées
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Définir le modèle de place pour la validation des entrées et la documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),
    'reviews': fields.List(fields.String, description="List of reviews on the place")
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place (authenticated users only)"""
        place_data = api.payload
        current_user_id = get_jwt_identity()  # Récupère l'ID de l'utilisateur connecté
        # Associe l'utilisateur comme propriétaire
        place_data['owner_id'] = current_user_id

        if place_data.get('price', 0) <= 0:
            return {"error": "Le prix doit être positif"}, 400

        # Appel à la méthode pour créer un lieu
        new_place = facade.place_facade.create_place(place_data)

        if isinstance(new_place, tuple):  # Si create_place() a retourné une erreur
            return new_place

        return new_place.to_dict(), 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.place_facade.get_all_places()

        # Utilisation de to_dict() pour retourner chaque place sous forme de dictionnaire
        return [place.to_dict() for place in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.place_facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    def put(self, place_id):
        """Update a place's information"""
        # Récupérer l'utilisateur actuel via le JWT
        current_user_id = get_jwt_identity()

        # Récupérer les données envoyées dans la requête
        place_data = api.payload

        # Vérifier si le lieu existe
        place = facade.place_facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        # Récupérer les informations du JWT (is_admin)
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        # Si l'utilisateur est un admin ou si l'utilisateur est le propriétaire de la place
        if not is_admin and place.owner_id != current_user_id:
            return {"error": "Unauthorized action"}, 403

        if place_data.get('price', 0) <= 0:
            return {"error": "Le prix doit être positif"}, 400

        # Mettre à jour le lieu avec les nouvelles données
        updated_place = facade.place_facade.update_place(place_id, place_data)

        return updated_place.to_dict(), 200

    @jwt_required()
    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    def delete(self, place_id):
        """Delete a place (admins only)"""
        # Récupérer les informations du JWT (is_admin)
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        if not is_admin:
            return {"error": "Unauthorized action, admins only"}, 403

        # Vérifier si la place existe
        place = facade.place_facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        # Appel à la méthode pour supprimer la place
        facade.place_facade.delete_place(place_id)

        return {"message": "Place successfully deleted"}, 200
