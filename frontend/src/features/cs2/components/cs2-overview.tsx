import { Card } from "@/components/ui/card";

export function CS2Overview() {
  return (
    <Card>
      <p className="font-display text-3xl font-bold">CS2 Module</p>
      <p className="mt-3 text-sm text-slate-600">
        Perfil competitivo isolado com foco em mapas, rank, KD, HS% e comparações entre jogadores.
      </p>
      <div className="mt-6 grid gap-3 sm:grid-cols-3">
        <div className="rounded-3xl bg-amber-50 p-4">
          <p className="text-xs uppercase tracking-[0.2em] text-amber-600">KD</p>
          <p className="mt-2 text-xl font-semibold">1.18</p>
        </div>
        <div className="rounded-3xl bg-slate-100 p-4">
          <p className="text-xs uppercase tracking-[0.2em] text-slate-500">HS%</p>
          <p className="mt-2 text-xl font-semibold">46.2%</p>
        </div>
        <div className="rounded-3xl bg-cyan-50 p-4">
          <p className="text-xs uppercase tracking-[0.2em] text-cyan-600">Map pool</p>
          <p className="mt-2 text-xl font-semibold">Mirage / Inferno</p>
        </div>
      </div>
    </Card>
  );
}
