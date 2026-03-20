import { Card } from "@/components/ui/card";
import { GameModulePage } from "@/features/core/components/game-module-page";
import { useOverwatchModule } from "@/features/overwatch/hooks/use-overwatch-module";

export function OverwatchOverview() {
  const query = useOverwatchModule();

  if (query.isLoading && !query.data) {
    return <Card>Carregando modulo Overwatch...</Card>;
  }

  return <GameModulePage data={query.data!} />;
}
