import { apiFetch } from "@/services/http";
import type { ApiEnvelope, ListEnvelope } from "@/types/api";
import type { GameModulePageData } from "@/types/games";

type OverviewResponse = ApiEnvelope<{
  handle: string;
  region: string;
  rank: string;
  maps: string[];
  kd: number;
  hs_percentage: number;
  adr: number;
  weapons: string[];
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
  slug: "cs2",
  title: "CS2",
  strapline: "Precision shooter module",
  description:
    "Modulo isolado para rank, elo, KD, HS%, ADR, mapas, armas, comparacao e historico recente.",
  trackedHandle: "fragcontrol",
  statCards: [
    { label: "Rank", value: "Level 10", tone: "accent" },
    { label: "KD", value: "1.18" },
    { label: "HS%", value: "46.2%" },
    { label: "ADR", value: "83.5", tone: "warm" },
  ],
  highlights: ["KD tracking", "Weapon view", "Recent match history"],
  comparisonRows: [],
  historyRows: [],
  referenceGroups: [],
};

export async function getCS2ModuleData(): Promise<GameModulePageData> {
  try {
    const [overview, referenceData, comparison, history] = await Promise.all([
      apiFetch<OverviewResponse>("/modules/cs2/overview/fragcontrol"),
      apiFetch<ReferenceResponse>("/modules/cs2/reference-data"),
      apiFetch<ComparisonResponse>("/modules/cs2/compare/fragcontrol/rivalawp"),
      apiFetch<HistoryResponse>("/modules/cs2/history/fragcontrol"),
    ]);

    return {
      slug: "cs2",
      title: "CS2",
      strapline: "Precision shooter module",
      description:
        "Modulo isolado para rank, elo, KD, HS%, ADR, mapas, armas, comparacao e historico recente.",
      trackedHandle: overview.data.handle,
      statCards: [
        { label: "Rank", value: overview.data.rank, tone: "accent" },
        { label: "KD", value: String(overview.data.kd) },
        { label: "HS%", value: `${overview.data.hs_percentage}%` },
        { label: "ADR", value: String(overview.data.adr), tone: "warm" },
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
        { label: "Queues / Modes", items: referenceData.data.roles_or_modes },
        { label: "Weapons", items: referenceData.data.roster_or_characters },
        { label: "Ranks", items: referenceData.data.ranks },
      ],
    };
  } catch {
    return fallback;
  }
}
