// Public Firebase Web App identifiers. Inject via Vite/Vercel environment variables.
// Do not add private Firebase service-account keys to the browser.
export const firebaseConfig = {
  apiKey: import.meta.env?.VITE_FIREBASE_API_KEY || '',
  authDomain: import.meta.env?.VITE_FIREBASE_AUTH_DOMAIN || '',
  projectId: import.meta.env?.VITE_FIREBASE_PROJECT_ID || '',
  appId: import.meta.env?.VITE_FIREBASE_APP_ID || '',
  messagingSenderId: import.meta.env?.VITE_FIREBASE_MESSAGING_SENDER_ID || undefined,
  storageBucket: import.meta.env?.VITE_FIREBASE_STORAGE_BUCKET || undefined,
};
