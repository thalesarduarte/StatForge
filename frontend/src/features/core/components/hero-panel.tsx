import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { coreMetrics } from "@/features/core/services/platform-service";

export function HeroPanel() {
  return (
    <Card className="overflow-hidden bg-slate-950 text-white">
      <div className="grid gap-8 lg:grid-cols-[1.3fr_0.9fr]">
        <div>
          <p className="mb-3 text-xs font-semibold uppercase tracking-[0.3em] text-cyan-300">Core Platform</p>
          <h1 className="max-w-2xl font-display text-4xl font-bold leading-tight sm:text-5xl">
            StatForge centraliza dados competitivos sem perder o isolamento entre jogos.
          </h1>
          <p className="mt-4 max-w-2xl text-sm text-slate-300 sm:text-base">
            Frontend e backend desacoplados, módulos independentes por jogo e um core compartilhado para identidade,
            comunidade, torneios, atividade e governança.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Button>Explorar módulos</Button>
            <Button variant="ghost">Ver arquitetura</Button>
          </div>
        </div>
        <div className="grid gap-4">
          {coreMetrics.map((metric) => (
            <div key={metric.label} className="rounded-[24px] border border-white/10 bg-white/5 p-4">
              <p className="text-sm text-slate-400">{metric.label}</p>
              <p className="mt-2 font-display text-3xl font-bold">{metric.value}</p>
              <p className="mt-1 text-sm text-slate-300">{metric.hint}</p>
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
}
