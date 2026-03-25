import { useState } from "react";
import { useMutation } from "@tanstack/react-query";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { GameModulePage } from "@/features/core/components/game-module-page";
import { useFortniteModule } from "@/features/fortnite/hooks/use-fortnite-module";
import { syncFortniteProfile } from "@/features/fortnite/services/fortnite-service";

export function FortniteOverview() {
  const [name, setName] = useState("Ninja");
  const [accountType, setAccountType] = useState("epic");
  const [activeHandle, setActiveHandle] = useState<string | null>(null);
  const query = useFortniteModule(activeHandle);
  const mutation = useMutation({
    mutationFn: () => syncFortniteProfile(name, accountType),
    onSuccess: (response) => setActiveHandle(response.data.handle),
  });

  if (!activeHandle) {
    return (
      <Card>
        <p className="font-display text-3xl font-bold">Fortnite Sync</p>
        <p className="mt-3 text-sm text-slate-600">Informe nome de conta e tipo para sincronizar stats reais.</p>
        <div className="mt-6 grid gap-3 md:grid-cols-2">
          <input value={name} onChange={(e) => setName(e.target.value)} className="rounded-full border border-border px-4 py-3 text-sm" placeholder="Player name" />
          <input value={accountType} onChange={(e) => setAccountType(e.target.value)} className="rounded-full border border-border px-4 py-3 text-sm" placeholder="epic / xbl / psn" />
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
    return <Card>Carregando modulo Fortnite...</Card>;
  }

  if (query.isError || !query.data) {
    return <Card>Falha ao carregar o modulo Fortnite.</Card>;
  }

  return <GameModulePage data={query.data} />;
}
