import { useQuery } from "@tanstack/react-query";

import { getValorantModuleData } from "@/features/valorant/services/valorant-service";

export function useValorantModule() {
  return useQuery({
    queryKey: ["game-module", "valorant"],
    queryFn: getValorantModuleData,
  });
}
