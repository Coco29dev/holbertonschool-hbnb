/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
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
});

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
    placesListElement.innerHTML = `<p>Unable to load places. Please try again later.</p>`;
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