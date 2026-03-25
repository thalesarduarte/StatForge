import { useQuery } from "@tanstack/react-query";

import { getLolModuleData } from "@/features/lol/services/lol-service";

export function useLolModule(handle: string | null) {
  return useQuery({
    queryKey: ["game-module", "lol", handle],
    queryFn: () => getLolModuleData(handle!),
    enabled: Boolean(handle),
  });
}
