import { motion, useInView } from "framer-motion";
import { ArrowRight, Quote } from "lucide-react";
import { useRef } from "react";

import { SectionHeading } from "./Chrome";
import { CopyButton, TerminalFrame, TypedLines } from "../terminal/Terminal";
import { useReveal } from "../terminal/useReveal";
import type { Craft, ConfigSnippet } from "../../types";

export function CraftSection({
  craft,
  snippets,
}: {
  craft: Craft[];
  snippets: ConfigSnippet[];
}) {
  return (
    <section id="craft" className="border-b border-line bg-term-900/40 py-20">
      <div className="mx-auto max-w-7xl px-5">
        <SectionHeading
          eyebrow="The craft"
          title={
            <>
              How to talk to an agent{" "}
              <span className="text-phos-400">so it does what you meant</span>
            </>
          }
          body="Seven rules that survive every agent, every model and every codebase. Each one is a before-and-after you can watch play out in a real terminal."
        />

        <div className="mt-12 space-y-6">
          {craft.map((item, index) => (
            <CraftCard key={item.id} item={item} index={index} />
          ))}
        </div>

        <div className="mt-14">
          <h3 className="text-lg font-semibold text-ink-strong">Config worth copying</h3>
          <p className="mt-2 text-[14px] text-ink-muted">
            Real opencode configuration. Save as <code className="font-mono text-phos-300">opencode.json</code>{" "}
            in the project root.
          </p>
          <div className="mt-6 grid gap-4 lg:grid-cols-2">
            {snippets.map((snippet) => (
              <div key={snippet.title} className="panel overflow-hidden rounded-2xl">
                <div className="flex items-center justify-between gap-3 border-b border-line bg-term-900 px-4 py-2.5">
                  <span className="text-[12px] text-ink">{snippet.title}</span>
                  <CopyButton value={snippet.code} />
                </div>
                <pre className="overflow-x-auto px-4 py-4 font-mono text-[12px] leading-relaxed text-ink">
                  {snippet.code}
                </pre>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function CraftCard({ item, index }: { item: Craft; index: number }) {
  const ref = useRef<HTMLDivElement | null>(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });
  const beforeRevealed = useReveal(item.before.lines, { playing: inView, speed: 1.4 });
  const afterRevealed = useReveal(item.after.lines, { playing: inView, speed: 1.4 });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-60px" }}
      transition={{ duration: 0.45, delay: Math.min(index * 0.04, 0.2) }}
      className="panel rounded-2xl p-6"
    >
      <div className="flex flex-wrap items-baseline justify-between gap-3">
        <h3 className="text-lg font-semibold text-ink-strong">
          <span className="mr-2 font-mono text-[13px] text-phos-500">
            {String(index + 1).padStart(2, "0")}
          </span>
          {item.title}
        </h3>
        <span className="chip chip-phos">
          <Quote size={10} /> {item.rule}
        </span>
      </div>

      <p className="mt-3 max-w-3xl text-[14px] leading-relaxed text-ink-muted">{item.body}</p>

      <div className="mt-5 grid gap-4 lg:grid-cols-2">
        <div>
          <p className="mb-2 text-[11px] uppercase tracking-[0.14em] text-amber-350">the vague version</p>
          <TerminalFrame title="what you typed" bodyClassName="!text-[12px]">
            <TypedLines lines={item.before.lines} revealed={beforeRevealed} showCaret={false} />
          </TerminalFrame>
        </div>
        <div>
          <p className="mb-2 flex items-center gap-1.5 text-[11px] uppercase tracking-[0.14em] text-phos-400">
            <ArrowRight size={11} /> the version that works
          </p>
          <TerminalFrame title="what an agent needs" bodyClassName="!text-[12px]">
            <TypedLines lines={item.after.lines} revealed={afterRevealed} showCaret={false} />
          </TerminalFrame>
        </div>
      </div>
    </motion.div>
  );
}
