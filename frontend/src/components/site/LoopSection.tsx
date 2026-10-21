import { motion, useInView } from "framer-motion";
import { AlertTriangle, ArrowRight, Hand, Wrench } from "lucide-react";
import { useEffect, useRef, useState } from "react";

import { SectionHeading } from "./Chrome";
import type { LoopStage } from "../../types";

export function LoopSection({ stages }: { stages: LoopStage[] }) {
  const ref = useRef<HTMLDivElement | null>(null);
  const inView = useInView(ref, { once: true, margin: "-120px" });
  const [active, setActive] = useState(0);
  const running = inView;

  useEffect(() => {
    if (!running) return;
    const timer = window.setInterval(() => {
      setActive((value) => (value + 1) % stages.length);
    }, 2600);
    return () => window.clearInterval(timer);
  }, [running, stages.length]);

  const current = stages[active];

  return (
    <section id="loop" className="border-b border-line bg-term-900/40 py-20">
      <div className="mx-auto max-w-7xl px-5">
        <SectionHeading
          eyebrow="The core idea"
          title={
            <>
              One loop, six stages,{" "}
              <span className="text-phos-400">every agent you will ever use</span>
            </>
          }
          body="opencode, Codex, Claude Code, Gemini CLI, Cline, Aider - different shells, different names for their tools, same skeleton. Learn the skeleton and the tools become interchangeable."
        />

        <div ref={ref} className="mt-12 grid gap-6 lg:grid-cols-[1.35fr_1fr]">
          <div className="panel rounded-2xl p-6">
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {stages.map((stage, index) => {
                const isActive = index === active;
                return (
                  <button
                    key={stage.id}
                    onClick={() => setActive(index)}
                    className={`relative overflow-hidden rounded-xl border p-4 text-left transition ${
                      isActive
                        ? "border-phos-500/60 bg-phos-500/8"
                        : "border-line bg-term-900 hover:border-phos-500/30"
                    }`}
                  >
                    {isActive ? (
                      <motion.span
                        layoutId="loop-active"
                        className="absolute inset-x-0 top-0 h-px bg-phos-400"
                        transition={{ duration: 0.4 }}
                      />
                    ) : null}
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-[10px] text-ink-muted">
                        {String(index + 1).padStart(2, "0")}
                      </span>
                      {isActive ? (
                        <motion.span
                          className="h-1.5 w-1.5 rounded-full bg-phos-400"
                          animate={{ opacity: [1, 0.25, 1] }}
                          transition={{ duration: 1.6, repeat: Infinity }}
                        />
                      ) : null}
                    </div>
                    <p
                      className={`mt-2 text-[13px] font-medium ${
                        isActive ? "text-phos-200" : "text-ink"
                      }`}
                    >
                      {stage.title}
                    </p>
                  </button>
                );
              })}
            </div>

            <div className="mt-5 rounded-xl border border-line bg-term-950 p-5">
              <div className="flex items-center gap-2 text-[11px] uppercase tracking-wide text-ink-muted">
                <motion.span
                  key={current.id}
                  initial={{ opacity: 0, y: 6 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="text-phos-400"
                >
                  stage {active + 1} / {stages.length}
                </motion.span>
                <span>| {current.title}</span>
              </div>
              <p className="mt-3 text-[14px] leading-relaxed text-ink">{current.body}</p>
              <div className="mt-4 grid gap-3 sm:grid-cols-2">
                <div className="rounded-lg border border-phos-500/25 bg-phos-500/5 p-3">
                  <p className="flex items-center gap-1.5 text-[11px] uppercase tracking-wide text-phos-400">
                    <Hand size={11} /> you control
                  </p>
                  <p className="mt-1.5 text-[13px] leading-relaxed text-ink-muted">{current.you_control}</p>
                </div>
                <div className="rounded-lg border border-amber-500/25 bg-amber-500/5 p-3">
                  <p className="flex items-center gap-1.5 text-[11px] uppercase tracking-wide text-amber-350">
                    <AlertTriangle size={11} /> how it fails
                  </p>
                  <p className="mt-1.5 text-[13px] leading-relaxed text-ink-muted">{current.failure}</p>
                </div>
              </div>
            </div>
          </div>

          <div className="panel flex flex-col justify-between rounded-2xl p-6">
            <div>
              <div className="flex items-center gap-2 text-[11px] uppercase tracking-[0.16em] text-ink-muted">
                <Wrench size={12} className="text-phos-500" /> where the leverage is
              </div>
              <h3 className="mt-3 text-lg font-semibold text-ink-strong">
                You are not chatting with the model. You are supervising a loop.
              </h3>
              <div className="mt-4 space-y-3 text-[14px] leading-relaxed text-ink-muted">
                <p>
                  The agent proposes, the tools run, the model reacts. Every failure mode is one of
                  three things: a bad request at the top, a bad context in the middle, or a missing
                  check at the bottom.
                </p>
                <p>
                  That is why the same prompt can produce a clean 6-line diff with one agent and a
                  400-line refactor with another - the difference is usually how much context the
                  agent had and whether anyone asked it to prove the result.
                </p>
              </div>
            </div>

            <div className="mt-6 space-y-2 rounded-xl border border-line bg-term-950 p-4 font-mono text-[12px]">
              {[
                ["request", "-> what you type"],
                ["context", "-> what it can see"],
                ["model", "-> what it chooses"],
                ["tools", "-> what it can touch"],
                ["verify", "-> what proves it works"],
              ].map(([left, right]) => (
                <div key={left} className="flex items-center gap-2">
                  <span className="text-phos-400">{left}</span>
                  <ArrowRight size={11} className="text-ink-muted" />
                  <span className="text-ink-muted">{right}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
