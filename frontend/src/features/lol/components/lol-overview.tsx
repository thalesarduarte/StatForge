import { useState } from "react";
import { useMutation } from "@tanstack/react-query";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { GameModulePage } from "@/features/core/components/game-module-page";
import { useLolModule } from "@/features/lol/hooks/use-lol-module";
import { syncLolProfile } from "@/features/lol/services/lol-service";

export function LolOverview() {
  const [gameName, setGameName] = useState("Faker");
  const [tagLine, setTagLine] = useState("KR1");
  const [region, setRegion] = useState("kr");
  const [activeHandle, setActiveHandle] = useState<string | null>(null);
  const query = useLolModule(activeHandle);
  const mutation = useMutation({
    mutationFn: () => syncLolProfile(gameName, tagLine, region),
    onSuccess: (response) => setActiveHandle(response.data.handle),
  });

  if (!activeHandle) {
    return (
      <Card>
        <p className="font-display text-3xl font-bold">LoL Sync</p>
        <p className="mt-3 text-sm text-slate-600">Informe Riot ID e região do invocador para sincronizar.</p>
        <div className="mt-6 grid gap-3 md:grid-cols-3">
          <input value={gameName} onChange={(e) => setGameName(e.target.value)} className="rounded-full border border-border px-4 py-3 text-sm" placeholder="Game name" />
          <input value={tagLine} onChange={(e) => setTagLine(e.target.value)} className="rounded-full border border-border px-4 py-3 text-sm" placeholder="Tag line" />
          <input value={region} onChange={(e) => setRegion(e.target.value)} className="rounded-full border border-border px-4 py-3 text-sm" placeholder="Region" />
        </div>
        <div className="mt-4">
          <Button onClick={() => mutation.mutate()} disabled={mutation.isPending}>
            {mutation.isPending ? "Sincronizando..." : "Sincronizar"}
          </Button>
        </div>
      </Card>
    );
  }

  if (query.isLoading && !query.data) {
    return <Card>Carregando modulo LoL...</Card>;
  }

  if (query.isError || !query.data) {
    return <Card>Falha ao carregar o modulo LoL.</Card>;
  }

  return <GameModulePage data={query.data} />;
}
