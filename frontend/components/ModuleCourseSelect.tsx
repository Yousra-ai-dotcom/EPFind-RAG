/**
 * Double sélecteur Module -> Cours, utilisé dans Chat et Révision.
 * S'appuie sur GET /courses qui renvoie maintenant { courses, modules }.
 */

"use client";

import { useEffect, useState } from "react";
import { getCourses } from "@/lib/api";

type Props = {
  module: string;
  course: string;
  onModuleChange: (module: string) => void;
  onCourseChange: (course: string) => void;
};

export default function ModuleCourseSelect({
  module,
  course,
  onModuleChange,
  onCourseChange,
}: Props) {
  const [modules, setModules] = useState<Record<string, string[]>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getCourses()
      .then((data) => setModules(data.modules || {}))
      .catch(() => setModules({}))
      .finally(() => setLoading(false));
  }, []);

  const moduleNames = Object.keys(modules);
  const coursesForModule = module ? modules[module] || [] : [];

  return (
    <div className="flex w-fit max-w-full gap-2">
      <select
        className="w-48 min-w-0 rounded-xl border border-epf-pink-light bg-white px-3 py-2 text-sm text-epf-dark focus:border-epf-pink focus:outline-none"
        value={module}
        disabled={loading}
        onChange={(e) => {
          onModuleChange(e.target.value);
          onCourseChange(""); // on réinitialise le cours quand le module change
        }}
      >
        <option value="">Module...</option>
        {moduleNames.map((m) => (
          <option key={m} value={m}>
            {m}
          </option>
        ))}
      </select>

      <select
        className="w-48 min-w-0 rounded-xl border border-epf-pink-light bg-white px-3 py-2 text-sm text-epf-dark focus:border-epf-pink focus:outline-none"
        value={course}
        disabled={loading || !module}
        onChange={(e) => onCourseChange(e.target.value)}
      >
        <option value="">Cours...</option>
        {coursesForModule.map((c) => (
          <option key={c} value={c}>
            {c}
          </option>
        ))}
      </select>
    </div>
  );
}
