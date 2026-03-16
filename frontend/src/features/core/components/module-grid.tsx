import { Card } from "@/components/ui/card";
import type { GameModuleSummary } from "@/types/platform";

const modules: GameModuleSummary[] = [
  {
    name: "Overwatch",
    description: "Perfis por role, main hero, mapas, modos, ranks e comparativos desacoplados.",
    highlights: ["Heroes e roles", "Comparativos por player", "Integração externa isolada"],
  },
  {
    name: "Valorant",
    description: "Perfis táticos com agents, mapas, elo, ACS/KD e estrutura pronta para match history.",
    highlights: ["Agents e ranks", "Comparativos rápidos", "Serviços próprios do módulo"],
  },
  {
    name: "CS2",
    description: "KPIs competitivos focados em KD, HS%, mapas e perfil modular para expansão futura.",
    highlights: ["KD e HS%", "Ranks por fila", "Modelo independente"],
  },
];

export function ModuleGrid() {
  return (
    <section className="grid gap-4 lg:grid-cols-3">
      {modules.map((module) => (
        <Card key={module.name}>
          <p className="font-display text-2xl font-bold">{module.name}</p>
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
