import { Card } from "@/components/ui/card";
import { GameModulePage } from "@/features/core/components/game-module-page";
import { useFortniteModule } from "@/features/fortnite/hooks/use-fortnite-module";

export function FortniteOverview() {
  const query = useFortniteModule();

  if (query.isLoading && !query.data) {
    return <Card>Carregando modulo Fortnite...</Card>;
  }

  return <GameModulePage data={query.data!} />;
}
