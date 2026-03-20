import { ActivityPreview } from "@/features/core/components/activity-preview";
import { CorePillars } from "@/features/core/components/core-pillars";
import { HeroPanel } from "@/features/core/components/hero-panel";
import { ModuleGrid } from "@/features/core/components/module-grid";

export function HomePage() {
  return (
    <div className="space-y-6">
      <HeroPanel />
      <CorePillars />
      <ModuleGrid />
      <ActivityPreview />
    </div>
  );
}
