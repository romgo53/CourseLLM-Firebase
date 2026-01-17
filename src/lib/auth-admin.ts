// server/admin-auth.ts
import admin from "firebase-admin";

if (!admin.apps.length) {
  admin.initializeApp({
    credential: admin.credential.cert(
      JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT_JSON || "{}")
    ),
  });
}

export async function setUserRole(uid: string, role: string) {
  const user = await admin.auth().getUser(uid);
  const existing = user.customClaims || {};
  const newClaims = { ...existing, role };

  await admin.auth().setCustomUserClaims(uid, newClaims);
}
