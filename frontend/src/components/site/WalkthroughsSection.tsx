import { motion } from "framer-motion";
import { ArrowRight, Clock, ListChecks, PlayCircle, Terminal } from "lucide-react";
import { Link } from "react-router-dom";

import { SectionHeading } from "./Chrome";
import type { Agent, Walkthrough } from "../../types";

export function WalkthroughsSection({
  walkthroughs,
  agents,
}: {
  walkthroughs: Walkthrough[];
  agents: Agent[];
}) {
  const agentName = (id: string) => agents.find((agent) => agent.id === id)?.name ?? id;

  return (
    <section id="walkthroughs" className="border-b border-line py-20">
      <div className="mx-auto max-w-7xl px-5">
        <SectionHeading
          eyebrow="Full walkthroughs"
          title={
            <>
              Sit through a real session,{" "}
              <span className="text-phos-400">step by step</span>
            </>
          }
          body="Each walkthrough is an animated terminal replay: the exact commands, the exact output, and the reasoning behind every step. Press play and watch it happen."
        />

        <div className="mt-10 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {walkthroughs.map((walkthrough, index) => (
            <motion.div
              key={walkthrough.id}
              initial={{ opacity: 0, y: 14 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-60px" }}
              transition={{ duration: 0.4, delay: Math.min(index * 0.04, 0.24) }}
            >
              <Link
                to={`/walkthrough/${walkthrough.id}`}
                className="card group flex h-full flex-col rounded-2xl p-5"
              >
                <div className="flex items-center justify-between gap-3">
                  <span className="chip chip-phos">{agentName(walkthrough.agent)}</span>
                  <span className="chip">{walkthrough.level}</span>
                </div>

                <h3 className="mt-4 text-[16px] font-semibold leading-snug text-ink-strong">
                  {walkthrough.title}
                </h3>
                <p className="mt-2.5 flex-1 text-[13px] leading-relaxed text-ink-muted">
                  {walkthrough.summary}
                </p>

                <div className="mt-4 flex flex-wrap items-center gap-3 border-t border-line pt-4 text-[11.5px] text-ink-muted">
                  <span className="inline-flex items-center gap-1.5">
                    <Clock size={12} /> {walkthrough.duration_min} min
                  </span>
                  <span className="inline-flex items-center gap-1.5">
                    <ListChecks size={12} /> {walkthrough.steps.length} steps
                  </span>
                  <span className="ml-auto inline-flex items-center gap-1 text-phos-300">
                    <PlayCircle size={13} />
                    play
                    <ArrowRight
                      size={12}
                      className="transition group-hover:translate-x-0.5"
                    />
                  </span>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

export function CtaSection() {
  return (
    <section className="relative overflow-hidden py-24">
      <div className="grid-bg pointer-events-none absolute inset-0" />
      <div className="relative mx-auto max-w-3xl px-5 text-center">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-phos-500/15 text-phos-400">
          <Terminal size={22} />
        </div>
        <h2 className="mt-6 text-3xl font-semibold tracking-tight text-ink-strong sm:text-4xl">
          Install one agent. Run one task.{" "}
          <span className="gradient-text">Read the diff.</span>
        </h2>
        <p className="mx-auto mt-4 max-w-xl text-[15px] leading-relaxed text-ink-muted">
          The whole site exists to get you to that first loop. Start with opencode, use the free Zen
          models, and let the agent prove the change with a test run before you read a single line of
          the diff.
        </p>
        <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
          <Link to="/walkthrough/opencode-first-hour" className="btn btn-primary !px-6 !py-3">
            Start the first walkthrough <ArrowRight size={15} />
          </Link>
          <a
            href="https://opencode.ai/docs/"
            target="_blank"
            rel="noreferrer"
            className="btn btn-ghost !px-6 !py-3"
          >
            Read the opencode docs
          </a>
        </div>
      </div>
    </section>
  );
}
