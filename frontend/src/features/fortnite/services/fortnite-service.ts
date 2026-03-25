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

type SyncResponse = ApiEnvelope<{ handle: string }>;

export async function syncFortniteProfile(name: string, accountType: string) {
  return apiFetch<SyncResponse>("/modules/fortnite/sync", {
    method: "POST",
    body: JSON.stringify({ name, account_type: accountType }),
  });
}

export async function getFortniteModuleData(handle: string): Promise<GameModulePageData> {
  const [overview, referenceData, comparison, history] = await Promise.all([
    apiFetch<OverviewResponse>(`/modules/fortnite/overview/${encodeURIComponent(handle)}`),
    apiFetch<ReferenceResponse>("/modules/fortnite/reference-data"),
    apiFetch<ComparisonResponse>(`/modules/fortnite/compare/${encodeURIComponent(handle)}/${encodeURIComponent(handle)}`),
    apiFetch<HistoryResponse>(`/modules/fortnite/history/${encodeURIComponent(handle)}`),
  ]);

  return {
    slug: "fortnite",
    title: "Fortnite",
    strapline: "Battle royale module",
    description: "Sincronizacao real via Fortnite-API com stats lifetime e playlists como referencia.",
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
      { label: "Loadout", items: referenceData.data.roster_or_characters },
      { label: "Ranks", items: referenceData.data.ranks },
    ],
  };
}
