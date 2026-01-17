import { NextResponse } from "next/server";
import admin from "firebase-admin";
import { setUserRole } from "@/lib/auth-admin";

// Ensure admin is initialized if not already (auth-admin initializes when imported,
// but double-checking here is harmless)

if (process.env.NODE_ENV === "development") {
  process.env.FIREBASE_AUTH_EMULATOR_HOST = "127.0.0.1:9099";
  process.env.FIRESTORE_EMULATOR_HOST = "127.0.0.1:8080";
  process.env.FIREBASE_STORAGE_EMULATOR_HOST = "127.0.0.1:9199";
}
if (!admin.apps.length) {
  const json = process.env.FIREBASE_SERVICE_ACCOUNT_JSON || "{}";
  try {
    admin.initializeApp({
      credential: admin.credential.cert(JSON.parse(json)),
    });
  } catch (e) {
    console.warn("Failed to initialize firebase-admin in onboarding route:", e);
  }
}

export async function POST(req: Request) {
  try {
    const authHeader = String(req.headers.get("authorization") || "");
    const match = authHeader.match(/^Bearer (.+)$/);
    if (!match)
      return NextResponse.json({ error: "Missing token" }, { status: 401 });

    const idToken = match[1];

    // Verify token (throws if invalid). We do not check revocation here by default.
    const decoded = await admin.auth().verifyIdToken(idToken);
    const uid = decoded.uid;

    const body = await req.json().catch(() => ({}));
    const { role, department, courses, displayName, photoURL } = body || {};

    if (!role || (role !== "student" && role !== "teacher")) {
      return NextResponse.json({ error: "Invalid role" }, { status: 400 });
    }

    const userRef = admin.firestore().doc(`users/${uid}`);
    const now = admin.firestore.FieldValue.serverTimestamp();

    await userRef.set(
      {
        uid,
        email: decoded.email || null,
        displayName: displayName || decoded.name || null,
        photoURL: photoURL || null,
        role,
        department: department || null,
        courses: Array.isArray(courses) ? courses : [],
        updatedAt: now,
        createdAt: now,
        profileComplete: true,
      },
      { merge: true }
    );

    // Set/merge custom claim for role
    await setUserRole(uid, role);

    return NextResponse.json({ ok: true });
  } catch (err: any) {
    console.error("onboarding route error", err);
    return NextResponse.json(
      { error: err?.message || "internal" },
      { status: 500 }
    );
  }
}
