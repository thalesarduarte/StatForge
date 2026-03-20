import { apiFetch } from "@/services/http";
import type { ApiEnvelope, ListEnvelope } from "@/types/api";
import type { GameModulePageData } from "@/types/games";

type OverviewResponse = ApiEnvelope<{
  summoner_name: string;
  server: string;
  elo: string;
  primary_role: string;
  preferred_champions: string[];
  core_stats: Record<string, number>;
  recent_highlights: string[];
}>;

type ReferenceResponse = ApiEnvelope<{
  maps: string[];
  roles_or_modes: string[];
  roster_or_characters: string[];
  ranks: string[];
}>;

type ComparisonResponse = ApiEnvelope<{
  metrics: Record<string, { left: number; right: number; better: string }>;
}>;

type HistoryResponse = ListEnvelope<{
  match_id: string;
  result: string;
  mode: string;
  map_name: string;
  played_at: string;
  stats: Record<string, string | number>;
}>;

const fallback: GameModulePageData = {
  slug: "lol",
  title: "League of Legends",
  strapline: "MOBA module",
  description:
    "Modulo isolado para invocador, elo, champions, roles, KDA, winrate, comparacao e historico recente.",
  trackedHandle: "midcontrol",
  statCards: [
    { label: "Elo", value: "Emerald II", tone: "accent" },
    { label: "Role", value: "Mid" },
    { label: "KDA", value: "3.9" },
    { label: "Winrate", value: "56.1%", tone: "warm" },
  ],
  highlights: ["Champion pool", "Role tracking", "SoloQ history"],
  comparisonRows: [],
  historyRows: [],
  referenceGroups: [],
};

export async function getLolModuleData(): Promise<GameModulePageData> {
  try {
    const [overview, referenceData, comparison, history] = await Promise.all([
      apiFetch<OverviewResponse>("/modules/lol/overview/midcontrol"),
      apiFetch<ReferenceResponse>("/modules/lol/reference-data"),
      apiFetch<ComparisonResponse>("/modules/lol/compare/midcontrol/rivalmid"),
      apiFetch<HistoryResponse>("/modules/lol/history/midcontrol"),
    ]);

    return {
      slug: "lol",
      title: "League of Legends",
      strapline: "MOBA module",
      description:
        "Modulo isolado para invocador, elo, champions, roles, KDA, winrate, comparacao e historico recente.",
      trackedHandle: overview.data.summoner_name,
      statCards: [
        { label: "Elo", value: overview.data.elo, tone: "accent" },
        { label: "Server", value: overview.data.server },
        { label: "Role", value: overview.data.primary_role },
        { label: "Winrate", value: `${overview.data.core_stats.winrate}%`, tone: "warm" },
      ],
      highlights: overview.data.recent_highlights,
      comparisonRows: Object.entries(comparison.data.metrics).map(([label, metric]) => ({
        label,
        left: String(metric.left),
        right: String(metric.right),
        better: metric.better,
      })),
      historyRows: history.items.map((entry) => ({
        id: entry.match_id,
        result: entry.result,
        mode: entry.mode,
        map: entry.map_name,
        playedAt: new Date(entry.played_at).toLocaleString("pt-BR"),
        stats: Object.entries(entry.stats).map(([label, value]) => ({ label, value: String(value) })),
      })),
      referenceGroups: [
        { label: "Maps", items: referenceData.data.maps },
        { label: "Roles", items: referenceData.data.roles_or_modes },
        { label: "Champions", items: referenceData.data.roster_or_characters },
        { label: "Elo bands", items: referenceData.data.ranks },
      ],
    };
  } catch {
    return fallback;
  }
}
