import { Card } from "@/components/ui/card";
import type { GameModulePageData } from "@/types/games";

type GameModulePageProps = {
  data: GameModulePageData;
};

export function GameModulePage({ data }: GameModulePageProps) {
  return (
    <div className="space-y-6">
      <Card className="bg-slate-950 text-white">
        <p className="text-xs font-semibold uppercase tracking-[0.3em] text-cyan-300">{data.strapline}</p>
        <h1 className="mt-3 font-display text-4xl font-bold">{data.title}</h1>
        <p className="mt-4 max-w-3xl text-sm text-slate-300">{data.description}</p>
        <p className="mt-4 text-sm text-slate-400">Tracked handle: {data.trackedHandle}</p>
        <div className="mt-6 grid gap-3 md:grid-cols-4">
          {data.statCards.map((stat) => (
            <div
              key={stat.label}
              className={[
                "rounded-[24px] p-4",
                stat.tone === "accent" ? "bg-cyan-400/15" : "",
                stat.tone === "warm" ? "bg-amber-300/15" : "",
                !stat.tone || stat.tone === "default" ? "bg-white/5" : "",
              ].join(" ")}
            >
              <p className="text-xs uppercase tracking-[0.2em] text-slate-400">{stat.label}</p>
              <p className="mt-2 text-2xl font-semibold text-white">{stat.value}</p>
            </div>
          ))}
        </div>
      </Card>

      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <Card>
          <p className="font-display text-2xl font-bold">Highlights</p>
          <div className="mt-4 flex flex-wrap gap-2">
            {data.highlights.map((highlight) => (
              <span key={highlight} className="rounded-full bg-slate-100 px-3 py-1 text-sm text-slate-700">
                {highlight}
              </span>
            ))}
          </div>
          <p className="mt-6 font-display text-2xl font-bold">Comparison</p>
          <div className="mt-4 space-y-3">
            {data.comparisonRows.map((row) => (
              <div key={row.label} className="rounded-3xl bg-slate-100 p-4">
                <div className="flex items-center justify-between gap-4">
                  <p className="text-sm font-semibold text-slate-600">{row.label}</p>
                  <p className="text-xs uppercase tracking-[0.2em] text-cyan-700">Better: {row.better}</p>
                </div>
                <div className="mt-2 grid grid-cols-2 gap-3 text-sm text-slate-700">
                  <p>{row.left}</p>
                  <p className="text-right">{row.right}</p>
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <p className="font-display text-2xl font-bold">Reference Data</p>
          <div className="mt-4 space-y-4">
            {data.referenceGroups.map((group) => (
              <div key={group.label}>
                <p className="text-xs uppercase tracking-[0.2em] text-slate-500">{group.label}</p>
                <div className="mt-2 flex flex-wrap gap-2">
                  {group.items.map((item) => (
                    <span key={item} className="rounded-full border border-border px-3 py-1 text-sm text-slate-700">
                      {item}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>

      <Card>
        <p className="font-display text-2xl font-bold">Recent History</p>
        <div className="mt-4 grid gap-3">
          {data.historyRows.map((entry) => (
            <div key={entry.id} className="rounded-3xl border border-border bg-white/80 p-4">
              <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
                <div>
                  <p className="font-semibold text-slate-900">
                    {entry.result} • {entry.mode}
                  </p>
                  <p className="text-sm text-slate-500">
                    {entry.map} • {entry.playedAt}
                  </p>
                </div>
                <div className="flex flex-wrap gap-2">
                  {entry.stats.map((stat) => (
                    <span key={`${entry.id}-${stat.label}`} className="rounded-full bg-slate-100 px-3 py-1 text-sm">
                      {stat.label}: {stat.value}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
