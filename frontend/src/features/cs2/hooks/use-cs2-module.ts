import { useQuery } from "@tanstack/react-query";

import { getCS2ModuleData } from "@/features/cs2/services/cs2-service";

export function useCS2Module(handle: string | null) {
  return useQuery({
    queryKey: ["game-module", "cs2", handle],
    queryFn: () => getCS2ModuleData(handle!),
    enabled: Boolean(handle),
  });
}
