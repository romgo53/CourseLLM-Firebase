"use client";

import React from "react";
import { useAuth } from "@/components/AuthProviderClient";
import { useRouter } from "next/navigation";

function LoginContent() {
  const { signInWithGoogle, signInWithGithub, loading, firebaseUser } = useAuth();
  const { refreshProfile, onboardingRequired, profile } = useAuth();
  const router = useRouter();

  const handleGoogle = async () => {
    try {
      await signInWithGoogle();
      // refresh profile and navigate based on returned profile
      const p = await refreshProfile();
      console.log(p);
      if (!p) {
        router.replace('/onboarding');
      } else if (p.role) {
        router.replace(p.role === 'teacher' ? '/teacher' : '/student');
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleGithub = async () => {
    try {
      await signInWithGithub();
      const p = await refreshProfile();
      if (!p) {
        router.replace('/onboarding');
      } else if (p.role) {
        router.replace(p.role === 'teacher' ? '/teacher' : '/student');
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Sign in</h1>
      <div className="space-y-2">
        <button className="btn" onClick={handleGoogle} disabled={loading}>
          Sign in with Google
        </button>
        <button className="btn" onClick={handleGithub} disabled={loading}>
          Sign in with GitHub
        </button>
      </div>
      {firebaseUser && <p className="mt-4">Signed in as {firebaseUser.email}</p>}
    </div>
  );
}

export default function LoginPage() {
  return <LoginContent />;
}
