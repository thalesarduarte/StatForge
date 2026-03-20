import { Card } from "@/components/ui/card";
import { GameModulePage } from "@/features/core/components/game-module-page";
import { useCS2Module } from "@/features/cs2/hooks/use-cs2-module";

export function CS2Overview() {
  const query = useCS2Module();

  if (query.isLoading && !query.data) {
    return <Card>Carregando modulo CS2...</Card>;
  }

  return <GameModulePage data={query.data!} />;
}
