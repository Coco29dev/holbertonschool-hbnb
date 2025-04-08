// Fonctions liées à la vue détaillée d'une place
import { getCookie, getUrlParams, showError } from './utils.js';
import { updateLoginButton } from './auth.js';
import { setupReviewForm } from './reviews.js';

// Initialisation de la page des détails
function initPlaceDetailsPage() {
  const token = getCookie('token');
  const params = getUrlParams();
  const placeId = params.id;

  if (!placeId) {
    showError('Place ID is missing in the URL');
    return;
  }

  // Mise à jour du bouton login/logout
  updateLoginButton(token);

  // Gestion de l'affichage du formulaire d'ajout de revue
  const addReviewSection = document.getElementById('add-review');
  if (addReviewSection) {
    if (!token) {
      addReviewSection.style.display = 'none';
    } else {
      addReviewSection.style.display = 'block';
      setupReviewForm(placeId, token);
    }
  }

  // Récupération des détails de la place
  fetchPlaceDetails(placeId, token);
}

// Récupération des détails d'une place depuis l'API
async function fetchPlaceDetails(placeId, token) {
  try {
    const headers = {
      'Content-Type': 'application/json'
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
      method: 'GET',
      headers: headers
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const placeData = await response.json();
    displayPlaceDetails(placeData);

  } catch (error) {
    console.error('Error fetching place details:', error);
    showError('Failed to load place details. Please try again later.');
  }
}

// Affichage des détails de la place
function displayPlaceDetails(place) {
  // Section des détails de la place
  const placeInfoElement = document.querySelector('.place-info');
  if (placeInfoElement) {
    // Utiliser une image basée sur l'ID de la place pour avoir une consistance
    const imageIndex = (place.id.charCodeAt(0) % 4) + 1;

    placeInfoElement.innerHTML = `
      <img src="images/place${imageIndex}.jpg" alt="${place.title}">
      <h2>${place.title}</h2>
      <p>Hosted by Owner ID: ${place.owner_id}</p>
      <p>$${place.price} per night</p>
      <p>${place.description || 'No description available'}</p>
      
      <h3>Amenities</h3>
      <ul id="amenities-list">
        ${place.amenities && place.amenities.length > 0
        ? place.amenities.map(amenity => `<li>${amenity.name}</li>`).join('')
        : '<li>No amenities listed</li>'}
      </ul>
    `;
  }

  // Section des revues
  const reviewsSection = document.getElementById('reviews');
  if (reviewsSection) {
    // Conserver le titre et le bouton pour ajouter une revue
    const title = reviewsSection.querySelector('h2');
    const addReviewButton = reviewsSection.querySelector('.details-button');

    reviewsSection.innerHTML = '';

    if (title) {
      reviewsSection.appendChild(title);
    }

    if (place.reviews && place.reviews.length > 0) {
      place.reviews.forEach(review => {
        const reviewElement = document.createElement('div');
        reviewElement.className = 'review-card';
        reviewElement.innerHTML = `
          <p><strong>User ID: ${review.user_id}</strong></p>
          <p>${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</p>
          <p>${review.text}</p>
        `;
        reviewsSection.appendChild(reviewElement);
      });
    } else {
      const noReviewsElement = document.createElement('p');
      noReviewsElement.textContent = 'No reviews yet.';
      reviewsSection.appendChild(noReviewsElement);
    }

    if (addReviewButton) {
      // Mettre à jour le lien avec l'ID de la place
      addReviewButton.href = `add_review.html?id=${place.id}`;
      reviewsSection.appendChild(addReviewButton);
    }
  }
}

export { initPlaceDetailsPage, fetchPlaceDetails, displayPlaceDetails };