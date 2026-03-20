import type { CoreMetric } from "@/types/platform";
import type { GameModuleSummary } from "@/types/platform";

export const coreMetrics: CoreMetric[] = [
  { label: "Players tracked", value: "125K+", hint: "Perfis multi-game conectados" },
  { label: "Competitive events", value: "320", hint: "Torneios, splits e ligas" },
  { label: "Community actions", value: "2.8M", hint: "Comentários, likes, follows e favoritos" },
];

export const gameModules: GameModuleSummary[] = [
  {
    name: "Overwatch",
    path: "/overwatch",
    description: "Heroes, roles, mapas, modos, ranks, comparativos e histórico recente.",
    highlights: ["Role stats", "Hero stats", "Main hero tracking"],
  },
  {
    name: "Valorant",
    path: "/valorant",
    description: "Agents, armas, HS%, KDA, winrate, comparação e match history competitivo.",
    highlights: ["HS% e KDA", "Agents e weapons", "Comparativos"],
  },
  {
    name: "CS2",
    path: "/cs2",
    description: "KD, HS%, ADR, mapas, armas, elo/rank e histórico recente de partidas.",
    highlights: ["KD / ADR", "Weapon view", "Comparação por player"],
  },
  {
    name: "LoL",
    path: "/lol",
    description: "Perfil do invocador, elo, roles, champions, KDA, winrate e histórico.",
    highlights: ["Champion pool", "Roles", "SoloQ snapshots"],
  },
  {
    name: "Fortnite",
    path: "/fortnite",
    description: "Vitórias, kills, KD, modos, partidas e comparativos entre jogadores.",
    highlights: ["Battle Royale", "Zero Build", "Recent match flow"],
  },
];
