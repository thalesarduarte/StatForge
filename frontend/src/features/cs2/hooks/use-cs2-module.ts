import { useQuery } from "@tanstack/react-query";

import { getCS2ModuleData } from "@/features/cs2/services/cs2-service";

export function useCS2Module() {
  return useQuery({
    queryKey: ["game-module", "cs2"],
    queryFn: getCS2ModuleData,
  });
}
