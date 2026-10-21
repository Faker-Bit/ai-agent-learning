import { motion } from "framer-motion";
import { ArrowUpRight, Boxes, Filter } from "lucide-react";
import { useMemo, useState } from "react";
import { Link } from "react-router-dom";

import { SectionHeading } from "./Chrome";
import { CopyButton } from "../terminal/Terminal";
import type { Agent } from "../../types";

const KINDS_FALLBACK = ["All", "CLI", "IDE", "Models", "Platform"];

export function AgentsSection({ agents }: { agents: Agent[] }) {
  const [kind, setKind] = useState("All");

  const kinds = useMemo(() => {
    const found = new Set<string>();
    for (const agent of agents) {
      for (const part of agent.kind.split("/").map((item) => item.trim())) {
        found.add(part);
      }
    }
    const list = KINDS_FALLBACK.filter((item) => item === "All" || found.has(item));
    for (const item of [...found].sort()) {
      if (!list.includes(item)) list.push(item);
    }
    return list;
  }, [agents]);

  const filtered = useMemo(
    () =>
      kind === "All"
        ? agents
        : agents.filter((agent) => agent.kind.split("/").some((item) => item.trim() === kind)),
    [agents, kind],
  );

  return (
    <section id="agents" className="border-b border-line py-20">
      <div className="mx-auto max-w-7xl px-5">
        <div className="flex flex-wrap items-end justify-between gap-6">
          <SectionHeading
            eyebrow="The directory"
            title={
              <>
                The agents, <span className="text-phos-400">mapped</span>
              </>
            }
            body="Twelve tools that people actually use to code with models. What each one is for, how to install it, and the commands worth memorising."
          />

          <div className="flex items-center gap-1.5 rounded-xl border border-line bg-term-900 p-1">
            <Filter size={13} className="ml-2 text-ink-muted" />
            {kinds.map((option) => (
              <button
                key={option}
                onClick={() => setKind(option)}
                className={`rounded-lg px-3 py-1.5 text-[12px] transition ${
                  kind === option
                    ? "bg-phos-500/15 text-phos-300"
                    : "text-ink-muted hover:text-ink"
                }`}
              >
                {option}
              </button>
            ))}
          </div>
        </div>

        <div className="mt-10 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {filtered.map((agent, index) => (
            <motion.article
              key={agent.id}
              initial={{ opacity: 0, y: 14 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-60px" }}
              transition={{ duration: 0.4, delay: Math.min(index * 0.03, 0.25) }}
              className="card flex flex-col rounded-2xl p-5"
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <h3 className="font-mono text-[15px] font-semibold text-ink-strong">
                    {agent.name}
                    {agent.stars ? (
                      <span className="ml-2 font-sans text-[11.5px] font-normal text-phos-300">
                        {agent.stars}
                      </span>
                    ) : null}
                  </h3>
                  <p className="mt-1.5 text-[13px] leading-relaxed text-ink-muted">{agent.tagline}</p>
                </div>
                <span className="chip shrink-0">{agent.kind}</span>
              </div>

              <p className="mt-4 text-[13px] leading-relaxed text-ink">{agent.best_for}</p>

              <ul className="mt-4 space-y-1.5">
                {agent.highlights.slice(0, 4).map((highlight) => (
                  <li key={highlight} className="flex gap-2 text-[12.5px] leading-relaxed text-ink-muted">
                    <span className="mt-[7px] h-1 w-1 shrink-0 rounded-full bg-phos-500" />
                    {highlight}
                  </li>
                ))}
              </ul>

              <div className="mt-5 rounded-lg border border-line bg-term-950 p-3">
                <div className="flex items-center justify-between gap-2">
                  <span className="font-mono text-[10px] uppercase tracking-wide text-ink-muted">
                    install
                  </span>
                  <CopyButton value={agent.install} />
                </div>
                <code className="mt-1.5 block overflow-x-auto font-mono text-[11.5px] text-phos-300">
                  {agent.install}
                </code>
              </div>

              <div className="mt-4 flex items-center justify-between gap-3 border-t border-line pt-4">
                <span className="text-[11px] text-ink-muted">{agent.license}</span>
                <div className="flex items-center gap-2">
                  {agent.walkthroughs.length ? (
                    <Link
                      to={`/walkthrough/${agent.walkthroughs[0]}`}
                      className="text-[12px] text-phos-300 hover:text-phos-200"
                    >
                      walkthrough -&gt;                    </Link>
                  ) : null}
                  <a
                    href={agent.docs}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1 text-[12px] text-ink-muted hover:text-ink"
                  >
                    docs <ArrowUpRight size={11} />
                  </a>
                </div>
              </div>
            </motion.article>
          ))}
        </div>

        <div className="mt-10 flex items-center gap-3 rounded-2xl border border-line bg-term-900 p-5">
          <Boxes size={18} className="shrink-0 text-phos-400" />
          <p className="flex-1 text-[13px] leading-relaxed text-ink-muted">
            Not sure where to start? opencode is the one to learn first - it is open source, runs any
            model provider, has the free Zen catalogue built in, and it exposes every one of these
            concepts (plans, subagents, permissions, MCP, automation) in one tool.
          </p>
          <Link to="/walkthrough/opencode-first-hour" className="btn btn-primary shrink-0">
            Start with opencode
          </Link>
        </div>
      </div>
    </section>
  );
}
