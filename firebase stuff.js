// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAFP5HU9ebgCYi1Pk3SycHzvwAP0GFnVEA",
  authDomain: "dbms-test-c9871.firebaseapp.com",
  projectId: "dbms-test-c9871",
  storageBucket: "dbms-test-c9871.appspot.com",
  messagingSenderId: "890102974902",
  appId: "1:890102974902:web:79ec0ed954c7506e369917",
  measurementId: "G-T7L3CXVST2"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);