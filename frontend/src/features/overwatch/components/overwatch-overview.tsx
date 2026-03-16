import { Card } from "@/components/ui/card";

const stats = [
  { label: "Main hero", value: "Tracer" },
  { label: "Top role", value: "Damage" },
  { label: "Competitive rank", value: "Diamond" },
];

export function OverwatchOverview() {
  return (
    <Card>
      <p className="font-display text-3xl font-bold">Overwatch Module</p>
      <p className="mt-3 text-sm text-slate-600">
        Estrutura isolada para heroes, mapas, modos, ranks, estatísticas por função e perfil competitivo.
      </p>
      <div className="mt-6 grid gap-3 sm:grid-cols-3">
        {stats.map((stat) => (
          <div key={stat.label} className="rounded-3xl bg-slate-100 p-4">
            <p className="text-xs uppercase tracking-[0.2em] text-slate-500">{stat.label}</p>
            <p className="mt-2 text-xl font-semibold text-slate-900">{stat.value}</p>
          </div>
        ))}
      </div>
    </Card>
  );
}
