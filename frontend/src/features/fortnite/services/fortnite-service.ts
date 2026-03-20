import { apiFetch } from "@/services/http";
import type { ApiEnvelope, ListEnvelope } from "@/types/api";
import type { GameModulePageData } from "@/types/games";

type OverviewResponse = ApiEnvelope<{
  handle: string;
  platform: string;
  victories: number;
  kills: number;
  kd: number;
  preferred_modes: string[];
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
  slug: "fortnite",
  title: "Fortnite",
  strapline: "Battle royale module",
  description:
    "Modulo isolado para perfil, partidas, vitorias, kills, KD, modos, historico e comparacao entre jogadores.",
  trackedHandle: "stormrider",
  statCards: [
    { label: "Victories", value: "112", tone: "accent" },
    { label: "Kills", value: "1843" },
    { label: "KD", value: "3.14" },
    { label: "Platform", value: "Epic", tone: "warm" },
  ],
  highlights: ["Battle Royale", "Zero Build", "Session history"],
  comparisonRows: [],
  historyRows: [],
  referenceGroups: [],
};

export async function getFortniteModuleData(): Promise<GameModulePageData> {
  try {
    const [overview, referenceData, comparison, history] = await Promise.all([
      apiFetch<OverviewResponse>("/modules/fortnite/overview/stormrider"),
      apiFetch<ReferenceResponse>("/modules/fortnite/reference-data"),
      apiFetch<ComparisonResponse>("/modules/fortnite/compare/stormrider/rivaldrop"),
      apiFetch<HistoryResponse>("/modules/fortnite/history/stormrider"),
    ]);

    return {
      slug: "fortnite",
      title: "Fortnite",
      strapline: "Battle royale module",
      description:
        "Modulo isolado para perfil, partidas, vitorias, kills, KD, modos, historico e comparacao entre jogadores.",
      trackedHandle: overview.data.handle,
      statCards: [
        { label: "Victories", value: String(overview.data.victories), tone: "accent" },
        { label: "Kills", value: String(overview.data.kills) },
        { label: "KD", value: String(overview.data.kd) },
        { label: "Platform", value: overview.data.platform, tone: "warm" },
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
        { label: "Modes", items: referenceData.data.roles_or_modes },
        { label: "Key loadout", items: referenceData.data.roster_or_characters },
        { label: "Rank bands", items: referenceData.data.ranks },
      ],
    };
  } catch {
    return fallback;
  }
}
