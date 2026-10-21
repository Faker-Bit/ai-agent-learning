import {
  ChevronLeft,
  ChevronRight,
  Gauge,
  Lightbulb,
  Pause,
  Play,
  RotateCcw,
} from "lucide-react";
import { useCallback, useEffect, useRef, useState } from "react";

import { CopyButton, StaticLines, TerminalFrame, TypedLines } from "../terminal/Terminal";
import { useReveal } from "../terminal/useReveal";
import type { TerminalLine, Walkthrough } from "../../types";

const SPEEDS = [1, 2, 4];

export function WalkthroughPlayer({ walkthrough }: { walkthrough: Walkthrough }) {
  const [stepIndex, setStepIndex] = useState(0);
  const [playing, setPlaying] = useState(true);
  const [speed, setSpeed] = useState(1);
  const [autoAdvance, setAutoAdvance] = useState(true);
  const [cycle, setCycle] = useState(0);
  const stepIndexRef = useRef(stepIndex);

  useEffect(() => {
    stepIndexRef.current = stepIndex;
  }, [stepIndex]);

  const step = walkthrough.steps[stepIndex];
  const activeLines: TerminalLine[] = step?.lines ?? [];

  const onTyped = useCallback(() => {
    if (!autoAdvance) return;
    const next = stepIndexRef.current + 1;
    if (next < walkthrough.steps.length) {
      window.setTimeout(() => {
        setStepIndex(next);
        setCycle((value) => value + 1);
      }, 1100);
    }
  }, [autoAdvance, walkthrough.steps.length]);

  const revealed = useReveal(activeLines, {
    speed,
    playing,
    onDone: onTyped,
  });

  const go = (index: number) => {
    const clamped = Math.max(0, Math.min(walkthrough.steps.length - 1, index));
    setStepIndex(clamped);
    setCycle((value) => value + 1);
  };

  const replay = () => {
    setStepIndex(0);
    setCycle((value) => value + 1);
    setPlaying(true);
  };

  const completedLines = walkthrough.steps
    .slice(0, stepIndex)
    .flatMap((item) => item.lines as TerminalLine[]);

  return (
    <div className="grid gap-6 lg:grid-cols-[300px_1fr]">
      <aside className="panel h-fit rounded-2xl p-4 lg:sticky lg:top-20">
        <div className="mb-3 flex items-center justify-between">
          <p className="text-[11px] uppercase tracking-[0.14em] text-ink-muted">Steps</p>
          <span className="font-mono text-[11px] text-phos-400">
            {stepIndex + 1}/{walkthrough.steps.length}
          </span>
        </div>

        <div className="mb-4 h-1 w-full overflow-hidden rounded-full bg-term-700">
          <div
            className="h-full rounded-full bg-gradient-to-r from-phos-500 to-cyan-450 transition-all duration-500"
            style={{ width: `${((stepIndex + 1) / walkthrough.steps.length) * 100}%` }}
          />
        </div>

        <ol className="space-y-1">
          {walkthrough.steps.map((item, index) => {
            const isActive = index === stepIndex;
            const isDone = index < stepIndex;
            return (
              <li key={item.id}>
                <button
                  onClick={() => go(index)}
                  className={`flex w-full items-start gap-2.5 rounded-lg px-2.5 py-2 text-left transition ${
                    isActive
                      ? "bg-phos-500/12 text-ink-strong"
                      : "text-ink-muted hover:bg-term-800 hover:text-ink"
                  }`}
                >
                  <span
                    className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-md font-mono text-[10px] ${
                      isActive
                        ? "bg-phos-500 text-term-950"
                        : isDone
                          ? "bg-phos-500/20 text-phos-300"
                          : "bg-term-700 text-ink-muted"
                    }`}
                  >
                    {index + 1}
                  </span>
                  <span className="text-[12.5px] leading-snug">{item.title}</span>
                </button>
              </li>
            );
          })}
        </ol>

        <div className="mt-5 space-y-2 border-t border-line pt-4">
          <label className="flex items-center justify-between text-[12px] text-ink-muted">
            auto-advance
            <input
              type="checkbox"
              checked={autoAdvance}
              onChange={(event) => setAutoAdvance(event.target.checked)}
              className="h-3.5 w-3.5 accent-[#46e08a]"
            />
          </label>
          <label className="flex items-center justify-between text-[12px] text-ink-muted">
            speed
            <span className="flex gap-1">
              {SPEEDS.map((value) => (
                <button
                  key={value}
                  onClick={() => setSpeed(value)}
                  className={`rounded-md px-2 py-0.5 font-mono text-[11px] transition ${
                    speed === value
                      ? "bg-phos-500/15 text-phos-300"
                      : "text-ink-muted hover:text-ink"
                  }`}
                >
                  {value}x
                </button>
              ))}
            </span>
          </label>
        </div>
      </aside>

      <div className="min-w-0 space-y-4">
        <TerminalFrame
          title={walkthrough.title}
          subtitle={`${walkthrough.agent} | ${step?.title ?? ""}`}
          right={
            <>
              <button
                onClick={() => setPlaying((value) => !value)}
                className="btn btn-ghost !px-2 !py-1 !text-[11px]"
                aria-label={playing ? "Pause" : "Play"}
              >
                {playing ? <Pause size={11} /> : <Play size={11} />}
              </button>
              <button onClick={replay} className="btn btn-ghost !px-2 !py-1 !text-[11px]" aria-label="Replay">
                <RotateCcw size={11} />
              </button>
            </>
          }
        >
          {completedLines.length ? <StaticLines lines={completedLines} /> : null}
          {completedLines.length ? (
            <div className="my-1 border-t border-dashed border-line" />
          ) : null}
          <TypedLines key={`${stepIndex}-${cycle}`} lines={activeLines} revealed={revealed} />
        </TerminalFrame>

        <div className="panel rounded-2xl p-5">
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="text-[11px] uppercase tracking-[0.14em] text-phos-500">
                step {stepIndex + 1} - {step?.title}
              </p>
              <p className="mt-2 text-[14px] leading-relaxed text-ink">{step?.narration}</p>
            </div>
            <div className="flex shrink-0 items-center gap-2">
              <button
                onClick={() => go(stepIndex - 1)}
                disabled={stepIndex === 0}
                className="btn btn-ghost !px-2.5 !py-1.5"
                aria-label="Previous step"
              >
                <ChevronLeft size={14} />
              </button>
              <button
                onClick={() => go(stepIndex + 1)}
                disabled={stepIndex === walkthrough.steps.length - 1}
                className="btn btn-ghost !px-2.5 !py-1.5"
                aria-label="Next step"
              >
                <ChevronRight size={14} />
              </button>
            </div>
          </div>

          {step?.command ? (
            <div className="mt-4 rounded-lg border border-line bg-term-950 p-3">
              <div className="flex items-center justify-between gap-2">
                <span className="text-[10px] uppercase tracking-wide text-ink-muted">command</span>
                <CopyButton value={step.command} />
              </div>
              <code className="mt-1.5 block overflow-x-auto font-mono text-[12px] text-phos-300">
                {step.command}
              </code>
            </div>
          ) : null}

          {step?.tip ? (
            <div className="mt-4 flex gap-2.5 rounded-lg border border-cyan-450/25 bg-cyan-450/5 p-3.5">
              <Lightbulb size={14} className="mt-0.5 shrink-0 text-cyan-450" />
              <p className="text-[13px] leading-relaxed text-ink-muted">{step.tip}</p>
            </div>
          ) : null}
        </div>

        <div className="flex items-center justify-between gap-3 text-[11px] text-ink-muted">
          <span className="inline-flex items-center gap-1.5">
            <Gauge size={12} /> {walkthrough.level} | about {walkthrough.duration_min} minutes
          </span>
          <span className="font-mono">
            {stepIndex + 1} of {walkthrough.steps.length}
          </span>
        </div>
      </div>
    </div>
  );
}
