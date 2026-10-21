import { AlertTriangle } from "lucide-react";

import { AgentsSection } from "../components/site/AgentsSection";
import { SiteFooter, SiteHeader } from "../components/site/Chrome";
import { CraftSection } from "../components/site/CraftSection";
import { HarnessSection } from "../components/site/HarnessSection";
import { Hero } from "../components/site/Hero";
import { LoopSection } from "../components/site/LoopSection";
import { ModelHubSection } from "../components/site/ModelHubSection";
import { ModelsSection } from "../components/site/ModelsSection";
import { CheatsheetSection, CompareSection } from "../components/site/ReferenceSections";
import { ResourcesSection } from "../components/site/ResourcesSection";
import { SecurityLabSection } from "../components/site/SecurityLabSection";
import { CtaSection, WalkthroughsSection } from "../components/site/WalkthroughsSection";
import { useSiteContent } from "../hooks/useSite";

export function Home() {
  const { data, isLoading, error, refetch } = useSiteContent();

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-term-950">
        <div className="shimmer h-10 w-48 rounded-xl" />
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-term-950 px-6 text-center">
        <p className="text-[15px] text-ink-strong">Could not load the site content.</p>
        <p className="max-w-md text-[13px] text-ink-muted">
          {(error as Error)?.message ?? "The API did not respond."}
        </p>
        <button onClick={() => refetch()} className="btn btn-primary">
          Retry
        </button>
      </div>
    );
  }

  const content = data.content;

  return (
    <div className="min-h-screen bg-term-950">
      <SiteHeader />
      {data.offline ? (
        <div className="border-b border-amber-500/30 bg-amber-500/10 px-5 py-2.5">
          <p className="mx-auto flex max-w-7xl items-center gap-2 text-[12.5px] text-amber-200">
            <AlertTriangle size={13} className="shrink-0" />
            Showing the bundled copy - the content API is not responding
            {data.error ? ` (${data.error})` : ""}. Start the backend with{" "}
            <code className="font-mono">start.bat</code> for live content.
          </p>
        </div>
      ) : null}
      <main>
        <Hero />
        <LoopSection stages={content.loop_stages} />
        <HarnessSection
          layers={content.harness_layers}
          projects={content.harness_projects}
          skillFormat={content.skill_format}
          skillPackages={content.skill_packages}
          orchestrators={content.orchestrators}
          protocols={content.protocols}
          playbook={content.context_playbook}
        />
        <AgentsSection agents={content.agents} />
        <ModelHubSection models={content.model_hub} intro={content.hub_intro} />
        <SecurityLabSection lab={content.security_lab} />
        <WalkthroughsSection walkthroughs={content.walkthroughs} agents={content.agents} />
        <CraftSection craft={content.craft} snippets={content.config_snippets} />
        <ModelsSection
          guides={content.model_guide}
          providers={content.providers}
          models={content.models}
        />
        <CheatsheetSection
          rows={content.cheatsheet}
          groups={content.cheatsheet_groups}
          agents={content.agents}
        />
        <ResourcesSection />
        <CompareSection rows={content.comparison} agents={content.agents} />
        <CtaSection />
      </main>
      <SiteFooter />
    </div>
  );
}
