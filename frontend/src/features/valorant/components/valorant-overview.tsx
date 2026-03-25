import { useState } from "react";
import { useMutation } from "@tanstack/react-query";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { GameModulePage } from "@/features/core/components/game-module-page";
import { useValorantModule } from "@/features/valorant/hooks/use-valorant-module";
import { syncValorantProfile } from "@/features/valorant/services/valorant-service";

export function ValorantOverview() {
  const [name, setName] = useState("TenZ");
  const [tag, setTag] = useState("NA1");
  const [region, setRegion] = useState("na");
  const [activeHandle, setActiveHandle] = useState<string | null>(null);
  const query = useValorantModule(activeHandle);
  const mutation = useMutation({
    mutationFn: () => syncValorantProfile(name, tag, region),
    onSuccess: (response) => setActiveHandle(response.data.handle),
  });

  if (!activeHandle) {
    return (
      <Card>
        <p className="font-display text-3xl font-bold">Valorant Sync</p>
        <p className="mt-3 text-sm text-slate-600">Informe nome, tag e região para sincronizar dados reais.</p>
        <div className="mt-6 grid gap-3 md:grid-cols-3">
          <input value={name} onChange={(e) => setName(e.target.value)} className="rounded-full border border-border px-4 py-3 text-sm" placeholder="Name" />
          <input value={tag} onChange={(e) => setTag(e.target.value)} className="rounded-full border border-border px-4 py-3 text-sm" placeholder="Tag" />
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
    return <Card>Carregando modulo Valorant...</Card>;
  }

  if (query.isError || !query.data) {
    return <Card>Falha ao carregar o modulo Valorant.</Card>;
  }

  return <GameModulePage data={query.data} />;
}
