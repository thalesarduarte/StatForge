import { Card } from "@/components/ui/card";

const entries = [
  "Sincronização de perfil ranqueado finalizada para Overwatch.",
  "Novo comparativo competitivo gerado para Valorant.",
  "Time favorito recebeu atualização de roster no hub.",
];

export function ActivityPreview() {
  return (
    <Card>
      <p className="font-display text-2xl font-bold">Activity Feed Preview</p>
      <div className="mt-4 space-y-3">
        {entries.map((entry) => (
          <div key={entry} className="rounded-2xl bg-slate-100 px-4 py-3 text-sm text-slate-700">
            {entry}
          </div>
        ))}
      </div>
    </Card>
  );
}
