// Point d'entrée principal et initialisation
import { getCookie } from './utils.js';
import { initLoginForm } from './auth.js';
import { checkAuthentication } from './places.js';
import { initPlaceDetailsPage } from './placeDetails.js';
import { initAddReviewPage } from './reviews.js';

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
  // Vérifier si nous sommes sur la page d'ajout d'avis
  const reviewForm = document.getElementById('review-form');
  const placeDetailsElement = document.getElementById('place-details');

  if (reviewForm && !placeDetailsElement) {
    // Nous sommes sur la page add_review.html
    initAddReviewPage();
  }
  // Vérifier si nous sommes sur la page de détails d'une place
  else if (placeDetailsElement) {
    initPlaceDetailsPage();
  } else {
    // Gérer le formulaire de connexion si présent
    initLoginForm();

    // Vérifier l'authentification pour toutes les pages
    checkAuthentication();
  }
});