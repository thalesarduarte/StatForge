import { Card } from "@/components/ui/card";
import { GameModulePage } from "@/features/core/components/game-module-page";
import { useLolModule } from "@/features/lol/hooks/use-lol-module";

export function LolOverview() {
  const query = useLolModule();

  if (query.isLoading && !query.data) {
    return <Card>Carregando modulo LoL...</Card>;
  }

  return <GameModulePage data={query.data!} />;
}
