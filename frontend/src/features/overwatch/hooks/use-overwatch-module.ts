import { useQuery } from "@tanstack/react-query";

import { getOverwatchModuleData } from "@/features/overwatch/services/overwatch-service";

export function useOverwatchModule(handle: string | null) {
  return useQuery({
    queryKey: ["game-module", "overwatch", handle],
    queryFn: () => getOverwatchModuleData(handle!),
    enabled: Boolean(handle),
  });
}
