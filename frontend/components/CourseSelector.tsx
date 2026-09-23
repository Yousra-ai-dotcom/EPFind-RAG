/**
 * Sélecteur de cours (utilisé dans Chat, Révision, QCM).
 * Récupère la liste via GET /courses (lib/api.ts).
 */

"use client";

import { useEffect, useState } from "react";
import { getCourses } from "@/lib/api";

type Props = {
  value: string;
  onChange: (course: string) => void;
  allowAll?: boolean; // affiche l'option "Tous les cours"
};

export default function CourseSelector({ value, onChange, allowAll = false }: Props) {
  const [courses, setCourses] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getCourses()
      .then((data) => setCourses(data.courses))
      .catch(() => setCourses([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <select
      className="w-full rounded-xl border border-epf-pink-light bg-white px-4 py-2.5 text-sm text-epf-dark focus:border-epf-pink focus:outline-none"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      disabled={loading}
    >
      {allowAll && <option value="">Tous les cours</option>}
      {!allowAll && <option value="">Choisir un cours...</option>}
      {courses.map((course) => (
        <option key={course} value={course}>
          {course}
        </option>
      ))}
    </select>
  );
}
