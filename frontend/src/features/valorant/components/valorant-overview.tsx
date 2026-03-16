import { Card } from "@/components/ui/card";

export function ValorantOverview() {
  return (
    <Card>
      <p className="font-display text-3xl font-bold">Valorant Module</p>
      <p className="mt-3 text-sm text-slate-600">
        Perfis táticos com agents, mapas, ranks e estatísticas centrais como ACS, KD e HS%.
      </p>
      <div className="mt-6 grid gap-3 sm:grid-cols-3">
        <div className="rounded-3xl bg-red-50 p-4">
          <p className="text-xs uppercase tracking-[0.2em] text-red-500">Main agent</p>
          <p className="mt-2 text-xl font-semibold">Jett</p>
        </div>
        <div className="rounded-3xl bg-slate-100 p-4">
          <p className="text-xs uppercase tracking-[0.2em] text-slate-500">Rank</p>
          <p className="mt-2 text-xl font-semibold">Ascendant</p>
        </div>
        <div className="rounded-3xl bg-emerald-50 p-4">
          <p className="text-xs uppercase tracking-[0.2em] text-emerald-500">ACS</p>
          <p className="mt-2 text-xl font-semibold">243.4</p>
        </div>
      </div>
    </Card>
  );
}
