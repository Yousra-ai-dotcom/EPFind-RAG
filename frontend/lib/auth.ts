/**
 * Connexion Microsoft Entra ID (compte EPF) côté frontend, avec MSAL.
 *
 * On ne stocke jamais de mot de passe : Microsoft gère tout (login, MFA).
 * On récupère seulement un "access token" qu'on envoie ensuite au backend
 * pour prouver qui est l'utilisateur.
 */

"use client";

import {
  PublicClientApplication,
  Configuration,
  AccountInfo,
} from "@azure/msal-browser";

const TENANT_ID = process.env.NEXT_PUBLIC_ENTRA_TENANT_ID || "";
const CLIENT_ID = process.env.NEXT_PUBLIC_ENTRA_CLIENT_ID || "";

const msalConfig: Configuration = {
  auth: {
    clientId: CLIENT_ID,
    authority: `https://login.microsoftonline.com/${TENANT_ID}`,
    redirectUri: typeof window !== "undefined" ? window.location.origin : "/",
  },
  cache: {
    cacheLocation: "localStorage",
  },
};

let msalInstance: PublicClientApplication | null = null;

function getMsalInstance(): PublicClientApplication {
  if (!msalInstance) {
    msalInstance = new PublicClientApplication(msalConfig);
  }
  return msalInstance;
}

const loginScopes = [
  `api://${CLIENT_ID}/access_as_user`,
];
/** Ouvre la popup de connexion Microsoft et retourne le compte connecté. */
export async function loginWithMicrosoft(): Promise<AccountInfo | null> {
  const instance = getMsalInstance();
  await instance.initialize();
  const result = await instance.loginPopup({ scopes: loginScopes });
  return result.account;
}

/** Déconnecte l'utilisateur (supprime la session locale). */
export async function logout(): Promise<void> {
  const instance = getMsalInstance();
  await instance.initialize();
  const account = instance.getAllAccounts()[0];
  if (account) {
    await instance.logoutPopup({ account });
  }
}

/** Retourne le compte actuellement connecté, ou null. */
export function getCurrentAccount(): AccountInfo | null {
  if (typeof window === "undefined") return null;
  const instance = getMsalInstance();
  const accounts = instance.getAllAccounts();
  return accounts[0] || null;
}

/**
 * Récupère un token d'accès valide pour appeler le backend.
 * Retourne null si l'utilisateur n'est pas connecté (mode démo/invité).
 */
export async function getAccessToken(): Promise<string | null> {
  if (typeof window === "undefined") return null;

  const instance = getMsalInstance();
  await instance.initialize();
  const account = instance.getAllAccounts()[0];
  if (!account) return null;

  try {
    const result = await instance.acquireTokenSilent({
      scopes: loginScopes,
      account,
    });
    return result.accessToken;
  } catch {
    // Le token silencieux a échoué -> on redemande une connexion interactive
    try {
      const result = await instance.acquireTokenPopup({ scopes: loginScopes });
      return result.accessToken;
    } catch {
      return null;
    }
  }
}
