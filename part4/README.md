# HBnB PART4

Ce dossier contient la partie frontend (partie 4) de l'application HBnB, qui est une application web de type Airbnb permettant de consulter des logements, de les évaluer et de les gérer.

## Structure du projet

Le frontend est structuré comme suit:

- `index.html` : Page d'accueil qui affiche la liste des logements
- `place.html` : Page de détail d'un logement
- `login.html` : Page de connexion
- `add_review.html` : Page d'ajout d'une critique
- `js/` : Dossier contenant les scripts JavaScript
  - `main.js` : Point d'entrée principal
  - `auth.js` : Gestion de l'authentification
  - `places.js` : Gestion des logements
  - `placeDetails.js` : Gestion des détails d'un logement
  - `reviews.js` : Gestion des critiques
  - `utils.js` : Fonctions utilitaires
- `styles.css` : Feuille de style CSS
- `images/` : Dossier contenant les images (à ajouter)


## Installation

1. Assurez-vous d'avoir les dépendances installées :

```bash
pip install -r ../part3/requirements.txt
pip install flask-jwt-extended flask-cors
```

2. Créez un dossier `images` dans le dossier `part4` s'il n'existe pas déjà :

```bash
mkdir -p images
```

3. Ajoutez des images pour les logements dans ce dossier (au minimum):
   - `logo.png` : Logo de l'application
   - `icon.png` : Icône de favicon 
   - `place1.jpg`, `place2.jpg`, `place3.jpg`, `place4.jpg` : Images pour les logements

## Lancement de l'application

### Démarrage manuel

Pour lancer le backend (API) et le frontend séparément :

1. Lancez le backend depuis le dossier `part3` :

```bash
cd ../part3
python3 run.py
```

2. Dans un autre terminal, lancez le serveur frontend depuis le dossier racine :

```bash
python3 static_server.py
```

### Démarrage automatique

Pour lancer les deux serveurs en même temps, utilisez le script `start.sh` depuis le dossier racine :

```bash
bash ../start.sh
```

ou rendez-le exécutable et lancez-le :

```bash
chmod +x ../start.sh
../start.sh
```

## Accès à l'application

- Frontend : http://localhost:8080
- Backend API : http://localhost:5000/api/v1
- Documentation API : http://localhost:5000/api/v1/

## Authentification

Utilisez les identifiants suivants pour vous connecter en tant qu'administrateur :
- Email : admin@example.com
- Mot de passe : adminpassword

## Fonctionnalités

- Affichage de la liste des logements
- Filtrage des logements par prix
- Consultation des détails d'un logement
- Ajout de critiques sur un logement (nécessite une connexion)
- Connexion/déconnexion

## Arrêt de l'application

Si vous utilisez le script `start.sh`, appuyez sur `Ctrl+C` pour arrêter les deux serveurs.

Si vous avez lancé les serveurs séparément, arrêtez chaque serveur avec `Ctrl+C` dans le terminal correspondant.
