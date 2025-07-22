// Import Firebase modules
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-auth.js";

// Firebase configuration (replace with your Firebase project config)
const firebaseConfig = {
    apiKey: "AIzaSyA85atwL6vPc7oOHZedxN6FgkBagcfYq4I",
    authDomain: "caplab-81737.firebaseapp.com",
    projectId: "caplab-81737",
    storageBucket: "caplab-81737.firebasestorage.app",
    messagingSenderId: "533257203237",
    appId: "1:533257203237:web:b5b1079750e5aa5ce759cc"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Function to update the UI based on login status
function updateUI(cookie) {
    var token = parseCookieToken(cookie);

    // If the user is logged in, hide the login box and show the sign-out button
    if (token.length > 0) {
        document.getElementById("login-box").hidden = true;
        document.getElementById("sign-out").hidden = false;
    } else {
        // If the user is not logged in, show the login box and hide the sign-out button
        document.getElementById("login-box").hidden = false;
        document.getElementById("sign-out").hidden = true;
    }
}

// Function to parse the token from the cookie
function parseCookieToken(cookie) {
    var strings = cookie.split(';');
    for (let i = 0; i < strings.length; i++) {
        var temp = strings[i].split('=');
        if (temp[0] == "token") {
            return temp[1];
        }
    }
    return "";
}

// Event listener for page load
window.addEventListener("load", function () {
    updateUI(document.cookie);

    // Sign-up functionality
    document.getElementById("sign-up").addEventListener("click", function () {
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        createUserWithEmailAndPassword(auth, email, password)
            .then((userCredential) => {
                const user = userCredential.user;

                // Get the ID token and set it as a cookie
                user.getIdToken().then((token) => {
                    document.cookie = "token=" + token + ";path=/;SameSite=Strict";
                    window.location = "/";
                });
            })
            .catch((error) => {
                console.log(error.code + error.message);
            });
    });

    // Login functionality
    document.getElementById("login").addEventListener("click", function () {
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        signInWithEmailAndPassword(auth, email, password)
            .then((userCredential) => {
                const user = userCredential.user;

                // Get the ID token and set it as a cookie
                user.getIdToken().then((token) => {
                    document.cookie = "token=" + token + ";path=/;SameSite=Strict";
                    window.location = "/";
                });
            })
            .catch((error) => {
                console.log(error.code + error.message);
            });
    });

    // Sign-out functionality
    document.getElementById("sign-out").addEventListener("click", function () {
        signOut(auth)
            .then(() => {
                // Remove the token cookie and redirect to the home page
                document.cookie = "token=;path=/;SameSite=Strict";
                window.location = "/";
            });
    });
});