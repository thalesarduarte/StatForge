import { Card } from "@/components/ui/card";

const pillars = [
  "Core compartilhado com auth, usuários, perfis, comentários, likes, follows, favoritos e badges.",
  "Hub multi-game com módulos independentes e prontos para receber novas integrações.",
  "Base preparada para feed de atividade, times/clãs, torneios e expansão de conteúdo.",
];

export function CorePillars() {
  return (
    <section className="grid gap-4 lg:grid-cols-3">
      {pillars.map((pillar) => (
        <Card key={pillar} className="bg-white/70">
          <p className="font-display text-xl font-bold">Core Platform</p>
          <p className="mt-3 text-sm text-slate-600">{pillar}</p>
        </Card>
      ))}
    </section>
  );
}
