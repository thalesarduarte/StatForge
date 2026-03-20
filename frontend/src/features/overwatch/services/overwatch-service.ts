import { apiFetch } from "@/services/http";
import type { ApiEnvelope, ListEnvelope } from "@/types/api";
import type { GameModulePageData } from "@/types/games";

type OverwatchOverviewResponse = ApiEnvelope<{
  handle: string;
  platform: string;
  region: string;
  rank: string;
  main_hero: string;
  role_stats: Record<string, Record<string, number>>;
  hero_stats: Record<string, Record<string, number>>;
  recent_highlights: string[];
}>;

type ReferenceResponse = ApiEnvelope<{
  maps: string[];
  roles_or_modes: string[];
  roster_or_characters: string[];
  ranks: string[];
}>;

type ComparisonResponse = ApiEnvelope<{
  left_handle: string;
  right_handle: string;
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
  slug: "overwatch",
  title: "Overwatch",
  strapline: "Hero-based competitive module",
  description:
    "Modulo isolado para perfil, roles, heroes, mapas, modos, ranks, main hero, comparativos e historico recente.",
  trackedHandle: "acepilot",
  statCards: [
    { label: "Rank", value: "Diamond 2", tone: "accent" },
    { label: "Main hero", value: "Tracer" },
    { label: "Top role", value: "Damage" },
    { label: "Trend", value: "+12% WR", tone: "warm" },
  ],
  highlights: ["Role stats", "Hero stats", "Competitive history"],
  comparisonRows: [
    { label: "Win rate", left: "55.4%", right: "52.8%", better: "acepilot" },
    { label: "Eliminations", left: "18.2", right: "16.7", better: "acepilot" },
  ],
  historyRows: [],
  referenceGroups: [],
};

export async function getOverwatchModuleData(): Promise<GameModulePageData> {
  try {
    const [overview, referenceData, comparison, history] = await Promise.all([
      apiFetch<OverwatchOverviewResponse>("/modules/overwatch/overview/acepilot"),
      apiFetch<ReferenceResponse>("/modules/overwatch/reference-data"),
      apiFetch<ComparisonResponse>("/modules/overwatch/compare/acepilot/rivalpulse"),
      apiFetch<HistoryResponse>("/modules/overwatch/history/acepilot"),
    ]);

    return {
      slug: "overwatch",
      title: "Overwatch",
      strapline: "Hero-based competitive module",
      description:
        "Modulo isolado para perfil, roles, heroes, mapas, modos, ranks, main hero, comparativos e historico recente.",
      trackedHandle: overview.data.handle,
      statCards: [
        { label: "Rank", value: overview.data.rank, tone: "accent" },
        { label: "Main hero", value: overview.data.main_hero },
        { label: "Platform", value: overview.data.platform },
        { label: "Region", value: overview.data.region, tone: "warm" },
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
        { label: "Heroes", items: referenceData.data.roster_or_characters },
        { label: "Ranks", items: referenceData.data.ranks },
      ],
    };
  } catch {
    return fallback;
  }
}
