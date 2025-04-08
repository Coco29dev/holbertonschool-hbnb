// Fonctions utilitaires communes à toute l'application

// Récupérer un cookie par son nom
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

// Extraire les paramètres de l'URL
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

// Afficher un message d'erreur
function showError(message) {
  const mainElement = document.querySelector('main');
  if (mainElement) {
    mainElement.innerHTML = `<div class="error-message">${message}</div>`;
  } else {
    alert(message);
  }
}

// Exporter les fonctions pour les rendre disponibles aux autres modules
export { getCookie, getUrlParams, showError };