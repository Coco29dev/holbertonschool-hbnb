// Fonctions liées à l'authentification
import { getCookie } from './utils.js';

// Fonction d'authentification
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
      window.location.href = 'index.html';
    });
  }
}

// Initialisation du formulaire de connexion
function initLoginForm() {
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
}

export { loginUser, updateLoginButton, initLoginForm };