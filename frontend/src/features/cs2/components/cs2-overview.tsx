import { useState } from "react";
import { useMutation } from "@tanstack/react-query";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { GameModulePage } from "@/features/core/components/game-module-page";
import { useCS2Module } from "@/features/cs2/hooks/use-cs2-module";
import { syncCS2Profile } from "@/features/cs2/services/cs2-service";

export function CS2Overview() {
  const [nickname, setNickname] = useState("s1mple");
  const [activeHandle, setActiveHandle] = useState<string | null>(null);
  const query = useCS2Module(activeHandle);
  const mutation = useMutation({
    mutationFn: () => syncCS2Profile(nickname),
    onSuccess: (response) => setActiveHandle(response.data.handle),
  });

  if (!activeHandle) {
    return (
      <Card>
        <p className="font-display text-3xl font-bold">CS2 Sync</p>
        <p className="mt-3 text-sm text-slate-600">Informe o nickname FACEIT do jogador para sincronizar os dados.</p>
        <div className="mt-6 flex flex-col gap-3 sm:flex-row">
          <input value={nickname} onChange={(e) => setNickname(e.target.value)} className="w-full rounded-full border border-border px-4 py-3 text-sm" placeholder="Nickname FACEIT" />
          <Button onClick={() => mutation.mutate()} disabled={mutation.isPending}>
            {mutation.isPending ? "Sincronizando..." : "Sincronizar"}
          </Button>
        </div>
      </Card>
    );
  }

  if (query.isLoading && !query.data) {
    return <Card>Carregando modulo CS2...</Card>;
  }

  if (query.isError || !query.data) {
    return <Card>Falha ao carregar o modulo CS2.</Card>;
  }

  return <GameModulePage data={query.data} />;
}
