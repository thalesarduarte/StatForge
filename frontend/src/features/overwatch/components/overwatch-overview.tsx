import { useState } from "react";
import { useMutation } from "@tanstack/react-query";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { GameModulePage } from "@/features/core/components/game-module-page";
import { useOverwatchModule } from "@/features/overwatch/hooks/use-overwatch-module";
import { syncOverwatchProfile } from "@/features/overwatch/services/overwatch-service";

export function OverwatchOverview() {
  const [handleInput, setHandleInput] = useState("SpaceRanger-1234");
  const [activeHandle, setActiveHandle] = useState<string | null>(null);
  const query = useOverwatchModule(activeHandle);
  const mutation = useMutation({
    mutationFn: syncOverwatchProfile,
    onSuccess: (response) => {
      setActiveHandle(response.data.handle);
    },
  });

  if (!activeHandle) {
    return (
      <Card>
        <p className="font-display text-3xl font-bold">Overwatch Sync</p>
        <p className="mt-3 text-sm text-slate-600">Informe a BattleTag ou handle aceito pelo provider OverFast.</p>
        <div className="mt-6 flex flex-col gap-3 sm:flex-row">
          <input
            value={handleInput}
            onChange={(event) => setHandleInput(event.target.value)}
            className="w-full rounded-full border border-border bg-white px-4 py-3 text-sm outline-none"
            placeholder="Ex.: SpaceRanger-1234"
          />
          <Button onClick={() => mutation.mutate(handleInput)} disabled={mutation.isPending}>
            {mutation.isPending ? "Sincronizando..." : "Sincronizar"}
          </Button>
        </div>
        {mutation.isError ? <p className="mt-4 text-sm text-red-600">Falha ao sincronizar o perfil.</p> : null}
      </Card>
    );
  }

  if (query.isLoading && !query.data) {
    return <Card>Carregando modulo Overwatch...</Card>;
  }

  if (query.isError || !query.data) {
    return (
      <Card>
        <p className="font-display text-2xl font-bold">Erro ao carregar Overwatch</p>
        <p className="mt-3 text-sm text-slate-600">O perfil foi sincronizado, mas a leitura do snapshot falhou.</p>
      </Card>
    );
  }

  return <GameModulePage data={query.data} />;
}
