#!/usr/bin/python3
from app import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True  # Empêche SQLAlchemy de créer une table pour cette classe

    # Définition des attributs comme des colonnes SQLAlchemy
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Méthode pour mettre à jour l'attribut updated_at lors de chaque modification
    def save(self):
        """Met à jour l'attribut updated_at chaque fois que l'objet est modifié."""
        self.updated_at = datetime.utcnow()
        db.session.commit()  # Assurer que les modifications sont persistées

    def update(self, data):
        """Met à jour les attributs de l'objet à partir d'un dictionnaire de données"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Sauvegarder l'objet et mettre à jour la date