import { Link } from "react-router-dom";

import { Card } from "@/components/ui/card";
import { gameModules } from "@/features/core/services/platform-service";

export function ModuleGrid() {
  return (
    <section className="grid gap-4 lg:grid-cols-3">
      {gameModules.map((module) => (
        <Card key={module.name}>
          <div className="flex items-start justify-between gap-4">
            <p className="font-display text-2xl font-bold">{module.name}</p>
            <Link to={module.path} className="text-sm font-semibold text-cyan-700">
              Open
            </Link>
          </div>
          <p className="mt-3 text-sm text-slate-600">{module.description}</p>
          <div className="mt-5 flex flex-wrap gap-2">
            {module.highlights.map((highlight) => (
              <span key={highlight} className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
                {highlight}
              </span>
            ))}
          </div>
        </Card>
      ))}
    </section>
  );
}
