import { useQuery } from "@tanstack/react-query";

import { getLolModuleData } from "@/features/lol/services/lol-service";

export function useLolModule() {
  return useQuery({
    queryKey: ["game-module", "lol"],
    queryFn: getLolModuleData,
  });
}
