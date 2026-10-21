import { motion } from "framer-motion";
import { ArrowRight, Pause, Play, RotateCcw, Sparkles } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";

import { TerminalFrame, TypedLines } from "../terminal/Terminal";
import { useReveal } from "../terminal/useReveal";
import type { TerminalLine } from "../../types";

const HERO_SESSION: TerminalLine[] = [
  { type: "input", text: "cd ~/projects/deal-hub && opencode" },
  { type: "muted", text: "  opencode | provider opencode | model opencode/mimo-v2.5-pro-free" },
  { type: "muted", text: "" },
  { type: "input", text: "add a GET /health endpoint returning {\"status\":\"ok\"} and a test for it" },
  { type: "tool", text: "Read(2)    backend/app/api/routes/health.py" },
  { type: "tool", text: "Read(1)    backend/tests/test_health.py" },
  { type: "tool", text: "Edit(1)    backend/app/api/routes/health.py" },
  { type: "tool", text: "Write(1)   backend/tests/test_health.py" },
  { type: "tool", text: "Bash(1)    cd backend && pytest -q" },
  { type: "output", text: "28 passed in 1.9s" },
  { type: "success", text: "/api/health -> {\"status\":\"ok\"}" },
  { type: "muted", text: "" },
  { type: "muted", text: "tab plan/build | @file | !command | ctrl+t reasoning | /undo" },
];

export function Hero() {
  const [playing, setPlaying] = useState(true);
  const [cycle, setCycle] = useState(0);
  const revealed = useReveal(HERO_SESSION, { speed: 1.6, playing, loop: true });

  return (
    <section className="relative overflow-hidden border-b border-line">
      <div className="grid-bg pointer-events-none absolute inset-0" />
      <div className="pointer-events-none absolute -top-40 left-1/3 h-[520px] w-[520px] rounded-full bg-phos-500/10 blur-[120px]" />

      <div className="relative mx-auto grid max-w-7xl items-center gap-12 px-5 py-16 lg:grid-cols-[1fr_1.15fr] lg:py-24">
        <motion.div
          initial={{ opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
        >
          <div className="inline-flex items-center gap-2 rounded-full border border-phos-500/30 bg-phos-500/8 px-3 py-1 font-mono text-[11px] text-phos-300">
            <Sparkles size={12} /> opencode | zen | codex | claude code | gemini cli | aider
          </div>

          <h1 className="mt-6 text-4xl font-semibold leading-[1.08] tracking-tight text-ink-strong sm:text-5xl lg:text-[3.4rem]">
            Learn to drive
            <br />
            <span className="gradient-text">AI coding agents</span>
          </h1>

          <p className="mt-6 max-w-xl text-[15px] leading-relaxed text-ink-muted">
            Every terminal agent works the same way underneath: a request, some context, a model that
            picks tools, a verification loop, a diff you still have to read. Learn that loop once and
            every agent becomes a variation on a theme you already know.
          </p>

          <div className="mt-8 flex flex-wrap items-center gap-3">
            <Link to="/walkthrough/opencode-first-hour" className="btn btn-primary !px-5 !py-2.5">
              Start your first hour <ArrowRight size={15} />
            </Link>
            <a href="#loop" className="btn btn-ghost !px-5 !py-2.5">
              How the loop works
            </a>
          </div>

          <dl className="mt-10 grid max-w-lg grid-cols-3 gap-4">
            {[
              ["12", "agents mapped"],
              ["8", "full walkthroughs"],
              ["80+", "real commands"],
            ].map(([value, label]) => (
              <div key={label} className="border-l border-line pl-3">
                <dt className="font-mono text-xl font-semibold text-phos-300">{value}</dt>
                <dd className="mt-0.5 text-[11px] uppercase tracking-wide text-ink-muted">{label}</dd>
              </div>
            ))}
          </dl>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 26 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.12, ease: "easeOut" }}
        >
          <TerminalFrame
            title="opencode"
            subtitle="~/projects/deal-hub"
            right={
              <>
                <button
                  onClick={() => setPlaying((value) => !value)}
                  className="btn btn-ghost !px-2 !py-1 !text-[11px]"
                  aria-label={playing ? "Pause animation" : "Play animation"}
                >
                  {playing ? <Pause size={11} /> : <Play size={11} />}
                </button>
                <button
                  onClick={() => {
                    setCycle((value) => value + 1);
                    setPlaying(true);
                  }}
                  className="btn btn-ghost !px-2 !py-1 !text-[11px]"
                  aria-label="Replay animation"
                >
                  <RotateCcw size={11} />
                </button>
              </>
            }
          >
            <TypedLines key={cycle} lines={HERO_SESSION} revealed={revealed} />
          </TerminalFrame>

          <p className="mt-3 text-center font-mono text-[11px] text-ink-muted">
            real opencode output - plan, edit, verify, diff
          </p>
        </motion.div>
      </div>
    </section>
  );
}
