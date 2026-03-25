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

type SyncResponse = ApiEnvelope<{ handle: string }>;

export async function syncCS2Profile(nickname: string) {
  return apiFetch<SyncResponse>("/modules/cs2/sync", {
    method: "POST",
    body: JSON.stringify({ nickname }),
  });
}

export async function getCS2ModuleData(handle: string): Promise<GameModulePageData> {
  const [overview, referenceData, comparison, history] = await Promise.all([
    apiFetch<OverviewResponse>(`/modules/cs2/overview/${encodeURIComponent(handle)}`),
    apiFetch<ReferenceResponse>("/modules/cs2/reference-data"),
    apiFetch<ComparisonResponse>(`/modules/cs2/compare/${encodeURIComponent(handle)}/${encodeURIComponent(handle)}`),
    apiFetch<HistoryResponse>(`/modules/cs2/history/${encodeURIComponent(handle)}`),
  ]);

  return {
    slug: "cs2",
    title: "CS2",
    strapline: "Precision shooter module",
    description: "Sincronizacao real via FACEIT Data API com persistencia local de overview e historico recente.",
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
      { label: "Queues", items: referenceData.data.roles_or_modes },
      { label: "Weapons", items: referenceData.data.roster_or_characters },
      { label: "Ranks", items: referenceData.data.ranks },
    ],
  };
}
