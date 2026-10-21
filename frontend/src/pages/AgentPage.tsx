import { ArrowLeft, ArrowUpRight, Boxes, KeyRound, Terminal } from "lucide-react";
import { Link, useParams } from "react-router-dom";

import { SiteFooter, SiteHeader } from "../components/site/Chrome";
import { useSiteContent } from "../hooks/useSite";

export function AgentPage() {
  const { agentId } = useParams();
  const { data, isLoading } = useSiteContent();

  if (isLoading || !data) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-term-950">
        <div className="shimmer h-10 w-48 rounded-xl" />
      </div>
    );
  }

  const content = data.content;
  const agent = content.agents.find((item) => item.id === agentId);
  if (!agent) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-term-950 px-6 text-center">
        <p className="text-[15px] text-ink-strong">Unknown agent.</p>
        <Link to="/#agents" className="btn btn-primary">
          Back to the directory
        </Link>
      </div>
    );
  }

  const walkthroughs = content.walkthroughs.filter((item) =>
    agent.walkthroughs.includes(item.id),
  );

  return (
    <div className="min-h-screen bg-term-950">
      <SiteHeader />
      <main className="mx-auto max-w-5xl px-5 py-10">
        <Link
          to="/#agents"
          className="inline-flex items-center gap-1.5 text-[12px] text-ink-muted transition hover:text-ink"
        >
          <ArrowLeft size={13} /> Agent directory
        </Link>

        <header className="mt-5">
          <div className="flex flex-wrap items-center gap-2">
            <span className="chip chip-phos">{agent.kind}</span>
            <span className="chip">{agent.license}</span>
          </div>
          <h1 className="mt-3 font-mono text-3xl font-semibold tracking-tight text-ink-strong sm:text-4xl">
            {agent.name}
          </h1>
          <p className="mt-3 max-w-3xl text-[15px] leading-relaxed text-ink-muted">{agent.tagline}</p>
          <p className="mt-4 max-w-3xl text-[14px] leading-relaxed text-ink">{agent.best_for}</p>

          <div className="mt-6 flex flex-wrap gap-3">
            <a
              href={agent.docs}
              target="_blank"
              rel="noreferrer"
              className="btn btn-primary"
            >
              Official docs <ArrowUpRight size={14} />
            </a>
            <a
              href={agent.repo}
              target="_blank"
              rel="noreferrer"
              className="btn btn-ghost"
            >
              Source <ArrowUpRight size={14} />
            </a>
          </div>
        </header>

        <section className="mt-10 grid gap-4 lg:grid-cols-2">
          <div className="panel rounded-2xl p-5">
            <p className="flex items-center gap-2 text-[11px] uppercase tracking-[0.14em] text-ink-muted">
              <Terminal size={12} className="text-phos-500" /> install
            </p>
            <div className="mt-3 space-y-3">
              {[
                ["macOS / Linux", agent.install],
                ["alternative", agent.install_alt],
                ["Windows", agent.install_windows],
              ].map(([label, command]) => (
                <div key={label} className="rounded-lg border border-line bg-term-950 p-3">
                  <p className="text-[10px] uppercase tracking-wide text-ink-muted">{label}</p>
                  <code className="mt-1.5 block overflow-x-auto font-mono text-[12px] text-phos-300">
                    {command}
                  </code>
                </div>
              ))}
            </div>
          </div>

          <div className="panel rounded-2xl p-5">
            <p className="flex items-center gap-2 text-[11px] uppercase tracking-[0.14em] text-ink-muted">
              <Boxes size={12} className="text-phos-500" /> what it does
            </p>
            <ul className="mt-3 space-y-2">
              {agent.highlights.map((highlight) => (
                <li key={highlight} className="flex gap-2 text-[13px] leading-relaxed text-ink-muted">
                  <span className="mt-[7px] h-1 w-1 shrink-0 rounded-full bg-phos-500" />
                  {highlight}
                </li>
              ))}
            </ul>
          </div>
        </section>

        <section className="mt-10">
          <h2 className="text-lg font-semibold text-ink-strong">Commands worth memorising</h2>
          <div className="panel mt-4 overflow-hidden rounded-2xl">
            <ul className="divide-y divide-line/60">
              {agent.commands.map(([command, description]) => (
                <li key={command} className="flex flex-wrap items-baseline gap-3 px-4 py-2.5">
                  <code className="font-mono text-[12.5px] text-phos-300">{command}</code>
                  <span className="text-[12.5px] text-ink-muted">{description}</span>
                </li>
              ))}
            </ul>
          </div>
        </section>

        {walkthroughs.length ? (
          <section className="mt-10">
            <h2 className="text-lg font-semibold text-ink-strong">Walkthroughs</h2>
            <div className="mt-4 grid gap-3 sm:grid-cols-2">
              {walkthroughs.map((walkthrough) => (
                <Link
                  key={walkthrough.id}
                  to={`/walkthrough/${walkthrough.id}`}
                  className="card rounded-2xl p-4"
                >
                  <p className="text-[14px] font-medium text-ink-strong">{walkthrough.title}</p>
                  <p className="mt-1.5 text-[12.5px] leading-relaxed text-ink-muted">
                    {walkthrough.summary}
                  </p>
                  <p className="mt-3 inline-flex items-center gap-1.5 text-[12px] text-phos-300">
                    <KeyRound size={12} /> {walkthrough.steps.length} steps | {walkthrough.duration_min} min
                  </p>
                </Link>
              ))}
            </div>
          </section>
        ) : null}
      </main>
      <SiteFooter />
    </div>
  );
}
