"use client";

import React, { useState } from "react";
import AuthProviderClient, { useAuth } from "@/components/AuthProviderClient";
import { doc, setDoc, serverTimestamp } from "firebase/firestore";
import { db } from "@/lib/firebase";
import { useRouter } from "next/navigation";

function OnboardingContent() {
  const { firebaseUser, profile, refreshProfile } = useAuth();
  const [department, setDepartment] = useState(profile?.department || "");
  const [coursesInput, setCoursesInput] = useState("");
  const [courses, setCourses] = useState<string[]>(profile?.courses || []);
  const [role, setRole] = useState<"student" | "teacher">((profile?.role as any) || "student");
  const [saving, setSaving] = useState(false);
  const router = useRouter();

  React.useEffect(() => {
    if (!firebaseUser) {
      // redirect to login if not authenticated
      router.replace("/login");
    }
  }, [firebaseUser, router]);

  if (!firebaseUser) {
    // while redirecting, render nothing (avoid router.replace in render)
    return null;
  }

  const addCourseFromInput = () => {
    const v = coursesInput.trim();
    if (v && !courses.includes(v)) {
      setCourses((c) => [...c, v]);
      setCoursesInput("");
    }
  };

  const removeCourse = (c: string) => setCourses((list) => list.filter((x) => x !== c));

  const handleSave = async () => {
    if (!firebaseUser) return;
    if (!role || !department) {
      alert("Please choose a role and department.");
      return;
    }
    setSaving(true);
    try {
      const userDoc = doc(db, "users", firebaseUser.uid);
      await setDoc(
        userDoc,
        {
          uid: firebaseUser.uid,
          email: firebaseUser.email,
          displayName: firebaseUser.displayName,
          photoURL: firebaseUser.photoURL,
          role,
          department,
          courses,
          authProviders: firebaseUser.providerData?.map((p) => p.providerId.replace(/\.com$/, "")) || [],
          createdAt: serverTimestamp(),
          updatedAt: serverTimestamp(),
          profileComplete: true,
        },
        { merge: true }
      );

      // Refresh the in-memory profile so role/flags update before navigating.
      try {
        await refreshProfile();
      } catch (e) {
        console.warn("refreshProfile failed after onboarding save:", e);
      }

      router.replace(role === "student" ? "/student" : "/teacher");
    } catch (err) {
      console.error("Failed saving profile:", err);
      alert("Failed to save profile. Try again.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Complete your profile</h1>

      <div className="mb-4">
        <label className="block mb-1">Role</label>
        <div className="flex gap-4">
          <label>
            <input type="radio" name="role" value="student" checked={role === "student"} onChange={() => setRole("student")} /> Student
          </label>
          <label>
            <input type="radio" name="role" value="teacher" checked={role === "teacher"} onChange={() => setRole("teacher")} /> Teacher
          </label>
        </div>
      </div>

      <div className="mb-4">
        <label className="block mb-1">Department</label>
        <input value={department} onChange={(e) => setDepartment(e.target.value)} placeholder="e.g. Computer Science" className="input" />
        <p className="text-sm text-muted-foreground">Enter your department (free-text). You can later link to canonical departments if desired.</p>
      </div>

      <div className="mb-4">
        <label className="block mb-1">Courses</label>
        <div className="flex gap-2">
          <input value={coursesInput} onChange={(e) => setCoursesInput(e.target.value)} onKeyDown={(e) => e.key === "Enter" && addCourseFromInput()} className="input" placeholder="Add a course and press Enter" />
          <button className="btn" onClick={addCourseFromInput}>Add</button>
        </div>
        <div className="mt-2">
          {courses.map((c) => (
            <span key={c} className="inline-flex items-center gap-2 px-2 py-1 mr-2 mb-2 bg-gray-100 rounded">
              {c} <button onClick={() => removeCourse(c)} className="text-sm">x</button>
            </span>
          ))}
        </div>
      </div>

      <div>
        <button className="btn" onClick={handleSave} disabled={saving}>{saving ? 'Saving...' : 'Save and Continue'}</button>
      </div>
    </div>
  );
}

export default function OnboardingPage() {
  return <OnboardingContent />;
}
