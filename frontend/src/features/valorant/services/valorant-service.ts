import { apiFetch } from "@/services/http";
import type { ApiEnvelope, ListEnvelope } from "@/types/api";
import type { GameModulePageData } from "@/types/games";

type OverviewResponse = ApiEnvelope<{
  handle: string;
  region: string;
  rank: string;
  agents: string[];
  weapons: string[];
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
  slug: "valorant",
  title: "Valorant",
  strapline: "Tactical shooter module",
  description:
    "Modulo isolado para perfil, rank, agents, armas, HS%, KDA, winrate, comparacao entre jogadores e historico recente.",
  trackedHandle: "opticnova",
  statCards: [
    { label: "Rank", value: "Ascendant 3", tone: "accent" },
    { label: "HS%", value: "27.8%" },
    { label: "KDA", value: "1.42" },
    { label: "Winrate", value: "54.6%", tone: "warm" },
  ],
  highlights: ["Agents", "Weapons", "Competitive history"],
  comparisonRows: [],
  historyRows: [],
  referenceGroups: [],
};

export async function getValorantModuleData(): Promise<GameModulePageData> {
  try {
    const [overview, referenceData, comparison, history] = await Promise.all([
      apiFetch<OverviewResponse>("/modules/valorant/overview/opticnova"),
      apiFetch<ReferenceResponse>("/modules/valorant/reference-data"),
      apiFetch<ComparisonResponse>("/modules/valorant/compare/opticnova/rivalop"),
      apiFetch<HistoryResponse>("/modules/valorant/history/opticnova"),
    ]);

    return {
      slug: "valorant",
      title: "Valorant",
      strapline: "Tactical shooter module",
      description:
        "Modulo isolado para perfil, rank, agents, armas, HS%, KDA, winrate, comparacao entre jogadores e historico recente.",
      trackedHandle: overview.data.handle,
      statCards: [
        { label: "Rank", value: overview.data.rank, tone: "accent" },
        { label: "Region", value: overview.data.region },
        { label: "HS%", value: `${overview.data.core_stats.hs_percentage}%` },
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
        { label: "Roles / Modes", items: referenceData.data.roles_or_modes },
        { label: "Agents", items: referenceData.data.roster_or_characters },
        { label: "Ranks", items: referenceData.data.ranks },
      ],
    };
  } catch {
    return fallback;
  }
}
