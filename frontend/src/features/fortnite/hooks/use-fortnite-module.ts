import { useQuery } from "@tanstack/react-query";

import { getFortniteModuleData } from "@/features/fortnite/services/fortnite-service";

export function useFortniteModule(handle: string | null) {
  return useQuery({
    queryKey: ["game-module", "fortnite", handle],
    queryFn: () => getFortniteModuleData(handle!),
    enabled: Boolean(handle),
  });
}
