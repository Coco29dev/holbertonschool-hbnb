// Fonctions liées à l'affichage et gestion des places
import { getCookie } from './utils.js';
import { updateLoginButton } from './auth.js';

// Récupérer la liste des places depuis l'API
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

// Afficher la liste des places
function displayPlaces(places) {
  const placesListElement = document.getElementById('places-list');
  if (!placesListElement) return;

  const headerElement = placesListElement.querySelector('h2');
  placesListElement.innerHTML = '';
  if (headerElement) {
    placesListElement.appendChild(headerElement);
  }

  if (!places || places.length === 0) {
    placesListElement.innerHTML += '<p>No places available at the moment.</p>';
    return;
  }

  places.forEach((place, index) => {
    // Distribuer les images entre les différentes places (1-4)
    const imageIndex = (index % 4) + 1;

    const placeElement = document.createElement('div');
    placeElement.className = 'place-card';
    placeElement.dataset.price = place.price;

    placeElement.innerHTML = `
      <img src="images/place${imageIndex}.jpg" alt="${place.title}">
      <h3>${place.title}</h3>
      <p>$${place.price} per night</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;

    placesListElement.appendChild(placeElement);
  });
}

// Initialiser le filtre de prix
function initializePriceFilter(places) {
  const priceFilter = document.getElementById('price-filter');
  if (!priceFilter) return;

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

// Filtrer les places par prix
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

// Vérifier l'authentification sur la page d'accueil
function checkAuthentication() {
  const token = getCookie('token');
  const loginButton = document.querySelector('.login-button');

  if (!loginButton) return;

  if (!token) {
    // Utilisateur non connecté
    loginButton.textContent = 'Login';
    loginButton.href = 'login.html';
    loginButton.replaceWith(loginButton.cloneNode(true));

    fetchPlaces();
  } else {
    // Utilisateur connecté
    loginButton.textContent = 'Logout';
    loginButton.href = '#';

    const newLoginButton = loginButton.cloneNode(true);
    loginButton.parentNode.replaceChild(newLoginButton, loginButton);

    newLoginButton.addEventListener('click', function (e) {
      e.preventDefault();
      document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
      window.location.href = 'index.html';
    });

    fetchPlaces(token);
  }
}

export { fetchPlaces, displayPlaces, initializePriceFilter, filterPlacesByPrice, checkAuthentication };