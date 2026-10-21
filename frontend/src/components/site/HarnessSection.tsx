import { motion, useInView } from "framer-motion";
import {
  AlertTriangle,
  ArrowUpRight,
  Boxes,
  Cable,
  GitBranch,
  Layers,
  ScrollText,
  Wrench,
} from "lucide-react";
import { useEffect, useRef, useState } from "react";

import { SectionHeading } from "./Chrome";
import { CopyButton, TerminalFrame } from "../terminal/Terminal";
import type {
  ContextEntry,
  HarnessLayer,
  HarnessProject,
  Orchestrator,
  Protocol,
  SkillFormat,
  SkillPackage,
} from "../../types";

export function HarnessSection({
  layers,
  projects,
  skillFormat,
  skillPackages,
  orchestrators,
  protocols,
  playbook,
}: {
  layers: HarnessLayer[];
  projects: HarnessProject[];
  skillFormat: SkillFormat;
  skillPackages: SkillPackage[];
  orchestrators: Orchestrator[];
  protocols: Protocol[];
  playbook: ContextEntry[];
}) {
  return (
    <section id="harness" className="border-b border-line bg-term-900/40 py-20">
      <div className="mx-auto max-w-7xl px-5">
        <SectionHeading
          eyebrow="The harness"
          title={
            <>
              The model is half the system.{" "}
              <span className="text-phos-400">The harness is the other half</span>
            </>
          }
          body="Every agent - opencode, Claude Code, Codex, pi, the ones on this page - is the same model behind different scaffolding. Learn the scaffolding and you can read any agent's source, or write your own."
        />

        <HarnessStack layers={layers} />

        <div className="mt-14">
          <h3 className="text-lg font-semibold text-ink-strong">Read a harness, or build one</h3>
          <p className="mt-2 max-w-3xl text-[14px] leading-relaxed text-ink-muted">
            These projects exist to show a different piece of the loop. Star counts are a snapshot from
            GitHub on 20 October 2026.
          </p>
          <div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            {projects.map((project) => (
              <ProjectCard key={project.id} project={project} />
            ))}
          </div>
        </div>

        <div id="skills" className="mt-16 scroll-mt-24">
          <div className="flex items-center gap-2 text-[11px] uppercase tracking-[0.18em] text-phos-500">
            <ScrollText size={12} />
            Skills
          </div>
          <h3 className="mt-3 text-2xl font-semibold tracking-tight text-ink-strong">
            Skills: procedures the agent loads on demand
          </h3>
          <p className="mt-3 max-w-3xl text-[15px] leading-relaxed text-ink-muted">
            {skillFormat.body}
          </p>
          <p className="mt-3 max-w-3xl text-[14px] leading-relaxed text-ink">
            {skillFormat.why_it_matters}
          </p>

          <div className="mt-6 grid gap-4 lg:grid-cols-[1.1fr_1fr]">
            <div>
              <p className="mb-2 text-[11px] uppercase tracking-[0.14em] text-ink-muted">
                a skill file
              </p>
              <TerminalFrame
                title=".opencode/skills/git-release/SKILL.md"
                right={<CopyButton value={skillFormat.example} />}
              >
                <pre className="whitespace-pre-wrap break-words text-[12px] leading-relaxed text-ink">
                  {skillFormat.example}
                </pre>
              </TerminalFrame>

              <p className="mb-2 mt-5 text-[11px] uppercase tracking-[0.14em] text-ink-muted">
                discovery paths
              </p>
              <div className="rounded-xl border border-line bg-term-900 p-4">
                {skillFormat.locations.map((location) => (
                  <p key={location} className="font-mono text-[12px] text-phos-300">
                    {location}
                  </p>
                ))}
              </div>
            </div>

            <div>
              <p className="mb-2 text-[11px] uppercase tracking-[0.14em] text-ink-muted">
                frontmatter fields
              </p>
              <div className="rounded-xl border border-line bg-term-900 p-4">
                {Object.entries(skillFormat.frontmatter).map(([key, value]) => (
                  <div key={key} className="border-b border-line/60 py-2 last:border-0">
                    <p className="font-mono text-[12px] text-accent-300">{key}</p>
                    <p className="mt-0.5 text-[12.5px] leading-relaxed text-ink-muted">{value}</p>
                  </div>
                ))}
              </div>

              <p className="mb-2 mt-5 text-[11px] uppercase tracking-[0.14em] text-ink-muted">
                permission by pattern
              </p>
              <TerminalFrame
                title="opencode.json"
                right={<CopyButton value={skillFormat.permissions} />}
              >
                <pre className="whitespace-pre-wrap break-words text-[12px] leading-relaxed text-ink">
                  {skillFormat.permissions}
                </pre>
              </TerminalFrame>

              <div className="mt-4 rounded-xl border border-amber-500/25 bg-amber-500/5 p-4">
                <p className="flex items-center gap-2 text-[11px] uppercase tracking-wide text-amber-350">
                  <AlertTriangle size={12} /> when it does not show up
                </p>
                <ul className="mt-2 space-y-1">
                  {skillFormat.troubleshooting.map((item) => (
                    <li key={item} className="text-[12.5px] leading-relaxed text-ink-muted">
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          <div className="mt-8 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
            {skillPackages.map((pack) => (
              <SkillCard key={pack.id} pack={pack} />
            ))}
          </div>
        </div>

        <div className="mt-16 grid gap-4 lg:grid-cols-2">
          <div>
            <div className="flex items-center gap-2 text-[11px] uppercase tracking-[0.18em] text-phos-500">
              <Cable size={12} />
              Protocols
            </div>
            <h3 className="mt-3 text-lg font-semibold text-ink-strong">
              The wiring an agent speaks
            </h3>
            <div className="mt-4 space-y-3">
              {protocols.map((protocol) => (
                <ProtocolCard key={protocol.id} protocol={protocol} />
              ))}
            </div>
          </div>

          <div>
            <div className="flex items-center gap-2 text-[11px] uppercase tracking-[0.18em] text-phos-500">
              <Layers size={12} />
              Context
            </div>
            <h3 className="mt-3 text-lg font-semibold text-ink-strong">
              The context playbook
            </h3>
            <div className="mt-4 space-y-3">
              {playbook.map((entry) => (
                <div key={entry.id} className="rounded-xl border border-line bg-term-900 p-4">
                  <p className="text-[14px] font-medium text-ink-strong">{entry.title}</p>
                  <p className="mt-1.5 text-[13px] leading-relaxed text-ink-muted">{entry.body}</p>
                  <div className="mt-3 grid gap-2 sm:grid-cols-2">
                    <div className="rounded-lg border border-rose-500/25 bg-rose-500/5 p-2.5">
                      <p className="text-[10px] uppercase tracking-wide text-rose-300">instead of</p>
                      <p className="mt-1 text-[12.5px] leading-relaxed text-ink-muted">{entry.bad}</p>
                    </div>
                    <div className="rounded-lg border border-phos-500/25 bg-phos-500/5 p-2.5">
                      <p className="text-[10px] uppercase tracking-wide text-phos-300">do this</p>
                      <p className="mt-1 text-[12.5px] leading-relaxed text-ink-muted">{entry.good}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="mt-14">
          <div className="flex items-center gap-2 text-[11px] uppercase tracking-[0.18em] text-phos-500">
            <GitBranch size={12} />
            Orchestration
          </div>
          <h3 className="mt-3 text-lg font-semibold text-ink-strong">
            When one agent is not enough
          </h3>
          <p className="mt-2 max-w-3xl text-[14px] leading-relaxed text-ink-muted">
            Control planes, session managers and source control for agents. They all answer the same
            question: how do you run five agents on one repo without losing track of who changed what.
          </p>
          <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {orchestrators.map((orchestrator) => (
              <a
                key={orchestrator.id}
                href={`https://github.com/${orchestrator.repo}`}
                target="_blank"
                rel="noreferrer"
                className="card group rounded-xl p-4"
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="font-mono text-[13px] text-ink-strong">{orchestrator.name}</span>
                  <span className="text-[11px] text-ink-muted">{orchestrator.stars}</span>
                </div>
                <p className="mt-1 text-[11px] uppercase tracking-wide text-accent-300">
                  {orchestrator.kind}
                </p>
                <p className="mt-2 text-[12.5px] leading-relaxed text-ink-muted">{orchestrator.what}</p>
                <span className="mt-2 inline-flex items-center gap-1 text-[11.5px] text-ink-muted group-hover:text-phos-300">
                  github <ArrowUpRight size={10} />
                </span>
              </a>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function HarnessStack({ layers }: { layers: HarnessLayer[] }) {
  const ref = useRef<HTMLDivElement | null>(null);
  const inView = useInView(ref, { once: true, margin: "-100px" });
  const [active, setActive] = useState(0);

  useEffect(() => {
    if (!inView) return;
    const timer = window.setInterval(() => {
      setActive((value) => (value + 1) % layers.length);
    }, 2400);
    return () => window.clearInterval(timer);
  }, [inView, layers.length]);

  const current = layers[active];

  return (
    <div ref={ref} className="mt-10 grid gap-6 lg:grid-cols-[1fr_1fr]">
      <div className="panel rounded-2xl p-6">
        <p className="flex items-center gap-2 text-[11px] uppercase tracking-[0.14em] text-ink-muted">
          <Layers size={12} className="text-phos-500" /> the stack, top to bottom
        </p>
        <div className="mt-4 space-y-1.5">
          {layers.map((layer, index) => {
            const isActive = index === active;
            return (
              <button
                key={layer.id}
                onClick={() => setActive(index)}
                className={`flex w-full items-center gap-3 rounded-xl border px-4 py-3 text-left transition ${
                  isActive
                    ? "border-phos-500/60 bg-phos-500/8"
                    : "border-line bg-term-900 hover:border-phos-500/30"
                }`}
              >
                <span className="font-mono text-[11px] text-ink-muted">
                  {String(index + 1).padStart(2, "0")}
                </span>
                <span
                  className={`flex-1 text-[14px] font-medium ${
                    isActive ? "text-phos-200" : "text-ink"
                  }`}
                >
                  {layer.title}
                </span>
                {isActive ? (
                  <motion.span
                    className="h-1.5 w-1.5 rounded-full bg-phos-400"
                    animate={{ opacity: [1, 0.25, 1] }}
                    transition={{ duration: 1.6, repeat: Infinity }}
                  />
                ) : null}
              </button>
            );
          })}
        </div>
      </div>

      <div className="panel rounded-2xl p-6">
        <motion.div
          key={current.id}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <p className="text-[11px] uppercase tracking-[0.14em] text-phos-500">
            layer {active + 1} / {layers.length}
          </p>
          <h4 className="mt-2 text-lg font-semibold text-ink-strong">{current.title}</h4>
          <p className="mt-2 text-[14px] leading-relaxed text-ink-muted">{current.body}</p>
          <div className="mt-4 space-y-2">
            <div className="rounded-lg border border-phos-500/25 bg-phos-500/5 p-3">
              <p className="flex items-center gap-1.5 text-[11px] uppercase tracking-wide text-phos-400">
                <Wrench size={11} /> you control
              </p>
              <p className="mt-1.5 text-[13px] leading-relaxed text-ink-muted">{current.control}</p>
            </div>
            <div className="rounded-lg border border-amber-500/25 bg-amber-500/5 p-3">
              <p className="flex items-center gap-1.5 text-[11px] uppercase tracking-wide text-amber-350">
                <AlertTriangle size={11} /> how it fails
              </p>
              <p className="mt-1.5 text-[13px] leading-relaxed text-ink-muted">{current.fails}</p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}

function ProjectCard({ project }: { project: HarnessProject }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-60px" }}
      transition={{ duration: 0.4 }}
      className="card flex flex-col rounded-2xl p-5"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="font-mono text-[14px] font-semibold text-ink-strong">{project.name}</p>
          <p className="mt-1 truncate font-mono text-[11px] text-ink-muted">{project.repo}</p>
        </div>
        <span className="shrink-0 text-[12px] text-phos-300">{project.stars}</span>
      </div>

      <p className="mt-3 text-[13px] leading-relaxed text-ink-muted">{project.tagline}</p>
      <p className="mt-3 flex-1 text-[12.5px] leading-relaxed text-ink">{project.why}</p>

      <div className="mt-4 rounded-lg border border-phos-500/25 bg-phos-500/5 p-3">
        <p className="text-[10px] uppercase tracking-wide text-phos-400">steal this</p>
        <p className="mt-1 text-[12.5px] leading-relaxed text-ink-muted">{project.steal}</p>
      </div>

      <div className="mt-4 flex items-center justify-between border-t border-line pt-3">
        <span className="text-[11px] text-ink-muted">{project.license}</span>
        <a
          href={`https://github.com/${project.repo}`}
          target="_blank"
          rel="noreferrer"
          className="inline-flex items-center gap-1 text-[12px] text-ink-muted hover:text-phos-300"
        >
          github <ArrowUpRight size={11} />
        </a>
      </div>
    </motion.div>
  );
}

function SkillCard({ pack }: { pack: SkillPackage }) {
  return (
    <a
      href={`https://github.com/${pack.repo}`}
      target="_blank"
      rel="noreferrer"
      className="card group rounded-xl p-4"
    >
      <div className="flex items-center justify-between gap-2">
        <span className="font-mono text-[13px] font-medium text-ink-strong">{pack.name}</span>
        <span className="text-[11.5px] text-phos-300">{pack.stars}</span>
      </div>
      <p className="mt-1 truncate font-mono text-[11px] text-ink-muted">{pack.repo}</p>
      <p className="mt-2 text-[12.5px] leading-relaxed text-ink">{pack.tagline}</p>
      <p className="mt-2 text-[12.5px] leading-relaxed text-ink-muted">{pack.what}</p>
      <span className="mt-2 inline-flex items-center gap-1 text-[11.5px] text-ink-muted group-hover:text-phos-300">
        github <ArrowUpRight size={10} />
      </span>
    </a>
  );
}

function ProtocolCard({ protocol }: { protocol: Protocol }) {
  return (
    <div className="rounded-xl border border-line bg-term-900 p-4">
      <div className="flex items-start justify-between gap-3">
        <p className="text-[14px] font-semibold text-ink-strong">{protocol.name}</p>
        <CopyButton value={protocol.example} label="copy" />
      </div>
      <p className="mt-2 text-[13px] leading-relaxed text-ink-muted">{protocol.what}</p>
      <p className="mt-2.5 rounded-lg border border-line bg-term-950 px-3 py-2 font-mono text-[11.5px] text-phos-300">
        {protocol.example}
      </p>
      <div className="mt-2.5 grid gap-2 sm:grid-cols-2">
        <div className="rounded-lg border border-line bg-term-950 p-2.5">
          <p className="text-[10px] uppercase tracking-wide text-accent-300">portable</p>
          <p className="mt-1 text-[12.5px] leading-relaxed text-ink-muted">{protocol.portable}</p>
        </div>
        <div className="rounded-lg border border-line bg-term-950 p-2.5">
          <p className="text-[10px] uppercase tracking-wide text-amber-350">the catch</p>
          <p className="mt-1 text-[12.5px] leading-relaxed text-ink-muted">{protocol.cost}</p>
        </div>
      </div>
    </div>
  );
}

export function HarnessBadge() {
  return (
    <span className="chip chip-cyan">
      <Boxes size={11} /> harness
    </span>
  );
}
