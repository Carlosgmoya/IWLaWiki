// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: "lawiki-iweb.firebaseapp.com",
  projectId: "lawiki-iweb",
  storageBucket: "lawiki-iweb.firebasestorage.app",
  messagingSenderId: "691029766224",
  appId: process.env.REACT_APP_FIREBASE_APP_ID,
  measurementId: "G-K0HL3P5HKC"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const analytics = getAnalytics(app);

export { auth, onAuthStateChanged };