import { Card } from "@/components/ui/card";
import { GameModulePage } from "@/features/core/components/game-module-page";
import { useValorantModule } from "@/features/valorant/hooks/use-valorant-module";

export function ValorantOverview() {
  const query = useValorantModule();

  if (query.isLoading && !query.data) {
    return <Card>Carregando modulo Valorant...</Card>;
  }

  return <GameModulePage data={query.data!} />;
}
