import { ArrowLeft, ArrowRight, BookOpen, Terminal } from "lucide-react";
import { Link, useParams } from "react-router-dom";

import { SiteFooter, SiteHeader } from "../components/site/Chrome";
import { WalkthroughPlayer } from "../components/site/WalkthroughPlayer";
import { useSiteContent } from "../hooks/useSite";

export function WalkthroughPage() {
  const { walkthroughId } = useParams();
  const { data, isLoading } = useSiteContent();

  if (isLoading || !data) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-term-950">
        <div className="shimmer h-10 w-48 rounded-xl" />
      </div>
    );
  }

  const content = data.content;
  const walkthrough = content.walkthroughs.find((item) => item.id === walkthroughId);
  const agent = content.agents.find((item) => item.id === walkthrough?.agent);

  if (!walkthrough) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-term-950 px-6 text-center">
        <p className="text-[15px] text-ink-strong">That walkthrough does not exist.</p>
        <Link to="/#walkthroughs" className="btn btn-primary">
          Back to the walkthroughs
        </Link>
      </div>
    );
  }

  const index = content.walkthroughs.findIndex((item) => item.id === walkthrough.id);
  const previous = content.walkthroughs[index - 1];
  const next = content.walkthroughs[index + 1];

  return (
    <div className="min-h-screen bg-term-950">
      <SiteHeader />
      <main className="mx-auto max-w-7xl px-5 py-10">
        <Link
          to="/#walkthroughs"
          className="inline-flex items-center gap-1.5 text-[12px] text-ink-muted transition hover:text-ink"
        >
          <ArrowLeft size={13} /> All walkthroughs
        </Link>

        <header className="mt-5">
          <div className="flex flex-wrap items-center gap-2">
            <span className="chip chip-phos">
              <Terminal size={11} /> {agent?.name ?? walkthrough.agent}
            </span>
            <span className="chip">{walkthrough.level}</span>
            <span className="chip">{walkthrough.duration_min} min</span>
          </div>
          <h1 className="mt-4 text-3xl font-semibold tracking-tight text-ink-strong sm:text-4xl">
            {walkthrough.title}
          </h1>
          <p className="mt-3 max-w-3xl text-[15px] leading-relaxed text-ink-muted">
            {walkthrough.summary}
          </p>

          <div className="mt-5 rounded-xl border border-line bg-term-900 p-4">
            <p className="flex items-center gap-2 text-[11px] uppercase tracking-[0.14em] text-ink-muted">
              <BookOpen size={12} /> by the end of this you will have
            </p>
            <ul className="mt-3 grid gap-2 sm:grid-cols-2">
              {walkthrough.outcome.map((item) => (
                <li key={item} className="flex gap-2 text-[13px] leading-relaxed text-ink-muted">
                  <span className="mt-[7px] h-1 w-1 shrink-0 rounded-full bg-phos-500" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </header>

        <div className="mt-8">
          <WalkthroughPlayer walkthrough={walkthrough} />
        </div>

        <nav className="mt-12 grid gap-3 border-t border-line pt-8 sm:grid-cols-2">
          {previous ? (
            <Link
              to={`/walkthrough/${previous.id}`}
              className="card group rounded-2xl p-4"
            >
              <span className="text-[11px] uppercase tracking-[0.14em] text-ink-muted">previous</span>
              <p className="mt-1.5 flex items-center gap-1.5 text-[14px] text-ink-strong">
                <ArrowLeft size={13} className="text-phos-400" /> {previous.title}
              </p>
            </Link>
          ) : (
            <span />
          )}
          {next ? (
            <Link to={`/walkthrough/${next.id}`} className="card group rounded-2xl p-4 sm:text-right">
              <span className="text-[11px] uppercase tracking-[0.14em] text-ink-muted">next</span>
              <p className="mt-1.5 flex items-center gap-1.5 text-[14px] text-ink-strong sm:justify-end">
                {next.title} <ArrowRight size={13} className="text-phos-400" />
              </p>
            </Link>
          ) : (
            <span />
          )}
        </nav>
      </main>
      <SiteFooter />
    </div>
  );
}
