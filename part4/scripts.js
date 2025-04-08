/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/
document.addEventListener('DOMContentLoaded', () => {
  // Vérifier si nous sommes sur la page de détails d'une place
  if (document.getElementById('place-details')) {
    initPlaceDetailsPage();
  } else {
    // Gérer le formulaire de connexion si présent
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
      loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        try {
          await loginUser(email, password);
        } catch (error) {
          console.error('Login failed:', error);
        }
      });
    }

    // Vérifier l'authentification pour toutes les pages
    checkAuthentication();
  }
});

// Fonction pour extraire les paramètres de l'URL
function getUrlParams() {
  const params = {};
  const queryString = window.location.search.substring(1);
  const pairs = queryString.split('&');

  for (const pair of pairs) {
    const [key, value] = pair.split('=');
    if (key) {
      params[key] = decodeURIComponent(value || '');
    }
  }

  return params;
}

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

// Mise à jour du bouton de connexion/déconnexion
function updateLoginButton(token) {
  const loginButton = document.querySelector('.login-button');
  if (!loginButton) return;

  if (!token) {
    loginButton.textContent = 'Login';
    loginButton.href = 'login.html';
    loginButton.replaceWith(loginButton.cloneNode(true));
  } else {
    loginButton.textContent = 'Logout';
    loginButton.href = '#';

    const newLoginButton = loginButton.cloneNode(true);
    loginButton.parentNode.replaceChild(newLoginButton, loginButton);

    newLoginButton.addEventListener('click', function (e) {
      e.preventDefault();
      document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
      window.location.reload();
    });
  }
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
    placeInfoElement.innerHTML = `
      <img src="place1.jpg" alt="${place.title}">
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
      reviewsSection.appendChild(addReviewButton);
    }
  }
}

// Configuration du formulaire d'ajout de revue
function setupReviewForm(placeId, token) {
  const reviewForm = document.getElementById('review-form');
  if (!reviewForm) return;

  reviewForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const reviewText = document.getElementById('review-text').value;
    const rating = document.getElementById('rating').value;

    if (!reviewText || !rating) {
      alert('Please fill in all fields');
      return;
    }

    try {
      const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          text: reviewText,
          rating: parseInt(rating)
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || errorData.message || 'Failed to submit review');
      }

      alert('Review submitted successfully!');
      window.location.reload(); // Rafraîchir la page pour afficher la nouvelle revue

    } catch (error) {
      console.error('Error submitting review:', error);
      alert(error.message || 'Failed to submit review. Please try again.');
    }
  });
}

// Affichage d'un message d'erreur
function showError(message) {
  const mainElement = document.querySelector('main');
  if (mainElement) {
    mainElement.innerHTML = `<div class="error-message">${message}</div>`;
  } else {
    alert(message);
  }
}

async function loginUser(email, password) {
  const response = await fetch('http://localhost:5000/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, password })
  });

  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
  } else {
    alert('Login failed: ' + response.statusText);
  }
}

function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith(name + '=')) {
      return cookie.substring(name.length + 1);
    }
  }
  return null;
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginButton = document.querySelector('.login-button');

  if (!loginButton) return; // Sortir si le bouton n'existe pas

  if (!token) {
    // Utilisateur non connecté
    loginButton.textContent = 'Login';
    loginButton.href = 'login.html';
    // Supprimer l'écouteur d'événements s'il existe
    loginButton.replaceWith(loginButton.cloneNode(true));

    fetchPlaces();
  } else {
    // Utilisateur connecté
    loginButton.textContent = 'Logout';
    loginButton.href = '#';

    // Recréer le bouton pour éviter les écouteurs d'événements multiples
    const newLoginButton = loginButton.cloneNode(true);
    loginButton.parentNode.replaceChild(newLoginButton, loginButton);

    newLoginButton.addEventListener('click', function (e) {
      e.preventDefault();
      document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
      window.location.reload();
    });

    fetchPlaces(token);
  }
}

async function fetchPlaces(token) {
  try {
    const headers = {
      'Content-Type': 'application/json'
    };
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    const response = await fetch('http://localhost:5000/api/v1/places/', {
      method: 'GET',
      headers: headers
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const placesData = await response.json();
    window.allPlaces = placesData;
    displayPlaces(placesData);
    initializePriceFilter(placesData);
  } catch (error) {
    console.error('Error fetching places:', error);
    const placesListElement = document.getElementById('places-list');
    if (placesListElement) {
      placesListElement.innerHTML = `<p>Unable to load places. Please try again later.</p>`;
    }
  }
}

function displayPlaces(places) {
  const placesListElement = document.getElementById('places-list');
  if (!placesListElement) return; // Sortir si l'élément n'existe pas

  const headerElement = placesListElement.querySelector('h2');
  placesListElement.innerHTML = '';
  if (headerElement) {
    placesListElement.appendChild(headerElement);
  }

  if (!places || places.length === 0) {
    placesListElement.innerHTML += '<p>No places available at the moment.</p>';
    return;
  }

  places.forEach(place => {
    const placeElement = document.createElement('div');
    placeElement.className = 'place-card';
    placeElement.dataset.price = place.price;

    placeElement.innerHTML = `
      <img src="place1.jpg" alt="${place.title}">
      <h3>${place.title}</h3>
      <p>$${place.price} per night</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;

    placesListElement.appendChild(placeElement);
  });
}

function initializePriceFilter(places) {
  const priceFilter = document.getElementById('price-filter');
  if (!priceFilter) return; // Sortir si l'élément n'existe pas

  priceFilter.innerHTML = '';

  const options = [
    { value: 'all', text: 'All Prices' },
    { value: '10', text: 'Up to $10' },
    { value: '50', text: 'Up to $50' },
    { value: '100', text: 'Up to $100' }
  ];

  options.forEach(option => {
    const optionElement = document.createElement('option');
    optionElement.value = option.value;
    optionElement.textContent = option.text;
    priceFilter.appendChild(optionElement);
  });

  priceFilter.addEventListener('change', function () {
    filterPlacesByPrice(this.value);
  });
}

function filterPlacesByPrice(maxPrice) {
  const places = window.allPlaces;
  if (!places) return;

  if (maxPrice === 'all') {
    displayPlaces(places);
    return;
  }

  const maxPriceValue = parseInt(maxPrice);
  const filteredPlaces = places.filter(place => place.price <= maxPriceValue);
  displayPlaces(filteredPlaces);
}