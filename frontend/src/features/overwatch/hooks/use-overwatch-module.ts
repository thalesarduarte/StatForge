import { useQuery } from "@tanstack/react-query";

import { getOverwatchModuleData } from "@/features/overwatch/services/overwatch-service";

export function useOverwatchModule() {
  return useQuery({
    queryKey: ["game-module", "overwatch"],
    queryFn: getOverwatchModuleData,
  });
}
