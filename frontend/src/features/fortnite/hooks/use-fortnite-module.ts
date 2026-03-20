import { useQuery } from "@tanstack/react-query";

import { getFortniteModuleData } from "@/features/fortnite/services/fortnite-service";

export function useFortniteModule() {
  return useQuery({
    queryKey: ["game-module", "fortnite"],
    queryFn: getFortniteModuleData,
  });
}
