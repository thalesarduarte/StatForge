export type StatCard = {
  label: string;
  value: string;
  tone?: "default" | "accent" | "warm";
};

export type ComparisonRow = {
  label: string;
  left: string;
  right: string;
  better: string;
};

export type HistoryRow = {
  id: string;
  result: string;
  mode: string;
  map: string;
  playedAt: string;
  stats: Array<{ label: string; value: string }>;
};

export type ReferenceGroup = {
  label: string;
  items: string[];
};

export type GameModulePageData = {
  slug: string;
  title: string;
  strapline: string;
  description: string;
  trackedHandle: string;
  statCards: StatCard[];
  highlights: string[];
  comparisonRows: ComparisonRow[];
  historyRows: HistoryRow[];
  referenceGroups: ReferenceGroup[];
};
