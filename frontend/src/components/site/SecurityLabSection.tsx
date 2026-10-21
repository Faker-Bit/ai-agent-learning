import { motion } from "framer-motion";
import {
  AlertTriangle,
  ArrowUpRight,
  BookOpen,
  ClipboardCheck,
  FileSearch,
  FlaskConical,
  Layers,
  Radar,
  ShieldCheck,
  Terminal,
} from "lucide-react";
import { useState } from "react";

import { SectionHeading } from "./Chrome";
import { CopyButton } from "../terminal/Terminal";

interface TaxonomyEntry {
  id: string;
  name: string;
  owasp: string;
  atlas: string;
  mechanism: string;
  pattern: string;
  example: string;
  breaks: string;
  detect: string;
  defend: string;
}

interface Signature {
  name: string;
  pattern: string;
  channel: string;
  use: string;
}

interface Defence {
  id: string;
  title: string;
  how: string;
  owasp: string;
  limits: string;
}

interface PlaybookStep {
  id: string;
  title: string;
  body: string;
}

interface Finding {
  id: string;
  title: string;
  source: string;
  link: string;
  body: string;
  rows: string[][];
  lesson: string;
}

interface Framework {
  name: string;
  link: string;
  note: string;
}

interface LabStep {
  id: string;
  title: string;
  body: string;
  try: string;
}

interface SecurityLab {
  taxonomy: TaxonomyEntry[];
  signatures: Signature[];
  defences: Defence[];
  playbook: PlaybookStep[];
  findings: Finding[];
  frameworks: Framework[];
  where_to_look: Framework[];
  lab: LabStep[];
}

export function SecurityLabSection({ lab }: { lab: SecurityLab }) {
  const [tab, setTab] = useState<"taxonomy" | "signatures" | "defences" | "playbook" | "research">(
    "taxonomy",
  );

  return (
    <section id="security" className="border-b border-line bg-term-900/40 py-20">
      <div className="mx-auto max-w-7xl px-5">
        <SectionHeading
          eyebrow="Prompt lab & AI security"
          title={
            <>
              Attack research, <span className="text-phos-400">defensively</span>
            </>
          }
          body="The uncomfortable half of prompt engineering: how models get manipulated, how the security community measures it, how to detect it in your own logs, and how to test it safely. Everything here is framed as authorised testing of systems you own."
        />

        <div className="mt-8 rounded-xl border border-line bg-term-900 p-1">
          <div className="no-scrollbar flex items-center gap-1 overflow-x-auto">
            {(
              [
                ["taxonomy", "Attack taxonomy", Radar],
                ["signatures", "Detection signatures", FileSearch],
                ["defences", "Defence layers", ShieldCheck],
                ["playbook", "Safe testing", ClipboardCheck],
                ["research", "Research & sources", BookOpen],
              ] as const
            ).map(([id, label, Icon]) => {
              const active = tab === id;
              return (
                <button
                  key={id}
                  onClick={() => setTab(id)}
                  className={`relative shrink-0 whitespace-nowrap rounded-lg px-3.5 py-2 text-[12.5px] font-medium transition ${
                    active ? "text-term-950" : "text-ink-muted hover:text-ink"
                  }`}
                >
                  {active ? (
                    <motion.span
                      layoutId="security-tab"
                      className="absolute inset-0 rounded-lg bg-phos-400"
                      transition={{ type: "spring", stiffness: 380, damping: 32 }}
                    />
                  ) : null}
                  <span className="relative z-10 inline-flex items-center gap-1.5">
                    <Icon size={13} />
                    {label}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        <div className="mt-6">
          {tab === "taxonomy" ? <TaxonomyTab entries={lab.taxonomy} /> : null}
          {tab === "signatures" ? <SignaturesTab signatures={lab.signatures} /> : null}
          {tab === "defences" ? <DefencesTab defences={lab.defences} /> : null}
          {tab === "playbook" ? <PlaybookTab steps={lab.playbook} /> : null}
          {tab === "research" ? <ResearchTab lab={lab} /> : null}
        </div>
      </div>
    </section>
  );
}

function TaxonomyTab({ entries }: { entries: TaxonomyEntry[] }) {
  const [open, setOpen] = useState<string | null>(entries[0]?.id ?? null);

  return (
    <div className="space-y-3">
      <p className="text-[13px] leading-relaxed text-ink-muted">
        Ten attack classes, mapped to OWASP LLM Top 10 and MITRE ATLAS. The examples are structural
        patterns for building your own test corpus - not turnkey payloads.
      </p>
      {entries.map((entry) => {
        const isOpen = open === entry.id;
        return (
          <div key={entry.id} className="card overflow-hidden rounded-2xl">
            <button
              onClick={() => setOpen(isOpen ? null : entry.id)}
              className="flex w-full items-center gap-3 p-4 text-left"
            >
              <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-term-700 text-[11px] font-semibold text-phos-300">
                {entry.atlas.split(".").pop()?.replace(/\D/g, "") || "!"}
              </span>
              <span className="min-w-0 flex-1">
                <span className="block text-[14px] font-medium text-ink-strong">{entry.name}</span>
                <span className="mt-0.5 block font-mono text-[10.5px] text-ink-muted">
                  {entry.owasp} Â· {entry.atlas}
                </span>
              </span>
              <span className="shrink-0 text-[11.5px] text-phos-300">
                {isOpen ? "close" : "expand"}
              </span>
            </button>

            {isOpen ? (
              <div className="grid gap-4 border-t border-line bg-term-900/60 p-5 lg:grid-cols-2">
                <div className="space-y-3">
                  <p className="text-[13px] leading-relaxed text-ink">{entry.mechanism}</p>
                  <div className="rounded-lg border border-line bg-term-950 p-3">
                    <p className="text-[10px] uppercase tracking-wide text-ink-muted">pattern</p>
                    <p className="mt-1 font-mono text-[11.5px] text-phos-300">{entry.pattern}</p>
                  </div>
                  <div className="rounded-lg border border-line bg-term-950 p-3">
                    <p className="flex items-center gap-1.5 text-[10px] uppercase tracking-wide text-ink-muted">
                      <FlaskConical size={11} /> sanitised structure
                    </p>
                    <pre className="mt-1.5 whitespace-pre-wrap font-mono text-[11px] leading-relaxed text-ink-muted">
                      {entry.example}
                    </pre>
                  </div>
                </div>

                <div className="space-y-3">
                  <Field body={entry.breaks} tone="warn" />
                  <Field body={entry.detect} tone="info" />
                  <Field body={entry.defend} tone="ok" />
                </div>
              </div>
            ) : null}
          </div>
        );
      })}
    </div>
  );
}

function SignaturesTab({ signatures }: { signatures: Signature[] }) {
  return (
    <div className="space-y-3">
      <p className="text-[13px] leading-relaxed text-ink-muted">
        Log-side signatures. Run them against every user turn, every retrieved chunk and every tool
        result. The channel matters more than the pattern: the same words are routine in a chat and
        alarming in a document.
      </p>
      {signatures.map((signature) => (
        <div key={signature.name} className="card rounded-2xl p-4">
          <div className="flex flex-wrap items-center gap-2">
            <h4 className="text-[14px] font-medium text-ink-strong">{signature.name}</h4>
            <span className="chip chip-cyan">channel: {signature.channel}</span>
            <CopyButton value={signature.pattern} label="copy regex" />
          </div>
          <p className="mt-2.5 rounded-lg border border-line bg-term-950 px-3 py-2 font-mono text-[11px] leading-relaxed text-phos-300">
            {signature.pattern}
          </p>
          <p className="mt-2 text-[12.5px] leading-relaxed text-ink-muted">{signature.use}</p>
        </div>
      ))}
    </div>
  );
}

function DefencesTab({ defences }: { defences: Defence[] }) {
  return (
    <div className="grid gap-3 md:grid-cols-2">
      {defences.map((defence, index) => (
        <motion.div
          key={defence.id}
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 0.35, delay: Math.min(index * 0.04, 0.2) }}
          className="card rounded-2xl p-5"
        >
          <div className="flex items-start justify-between gap-3">
            <h4 className="text-[14.5px] font-semibold text-ink-strong">{defence.title}</h4>
            <span className="chip shrink-0">{defence.owasp}</span>
          </div>
          <p className="mt-2.5 text-[13px] leading-relaxed text-ink-muted">{defence.how}</p>
          <p className="mt-3 flex gap-2 rounded-lg border border-amber-500/25 bg-amber-500/5 p-3 text-[12px] leading-relaxed text-ink-muted">
            <AlertTriangle size={13} className="mt-0.5 shrink-0 text-amber-350" />
            {defence.limits}
          </p>
        </motion.div>
      ))}
    </div>
  );
}

function PlaybookTab({ steps }: { steps: PlaybookStep[] }) {
  return (
    <div className="grid gap-3 md:grid-cols-2">
      {steps.map((step, index) => (
        <div key={step.id} className="card rounded-2xl p-5">
          <div className="flex items-start gap-3">
            <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-lg bg-term-700 font-mono text-[11px] text-phos-300">
              {index + 1}
            </span>
            <div>
              <h4 className="text-[14px] font-medium text-ink-strong">{step.title}</h4>
              <p className="mt-1.5 text-[13px] leading-relaxed text-ink-muted">{step.body}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

function ResearchTab({ lab }: { lab: SecurityLab }) {
  return (
    <div className="space-y-8">
      <div>
        <h3 className="text-lg font-semibold text-ink-strong">What the measurements say</h3>
        <div className="mt-4 space-y-4">
          {lab.findings.map((finding) => (
            <div key={finding.id} className="card rounded-2xl p-5">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <h4 className="text-[15px] font-semibold text-ink-strong">{finding.title}</h4>
                <a
                  href={finding.link}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-1 text-[12px] text-phos-300 hover:text-phos-200"
                >
                  source <ArrowUpRight size={11} />
                </a>
              </div>
              <p className="mt-1 text-[11.5px] text-ink-muted">{finding.source}</p>
              <p className="mt-2.5 text-[13px] leading-relaxed text-ink-muted">{finding.body}</p>
              <div className="mt-4 overflow-x-auto rounded-lg border border-line">
                <table className="w-full text-left text-[12.5px]">
                  <tbody>
                    {finding.rows.map((row, index) => (
                      <tr
                        key={row[0]}
                        className={`border-b border-line/60 last:border-0 ${
                          index === 0 ? "bg-term-900 text-ink-muted" : ""
                        }`}
                      >
                        <td className="px-3 py-2 text-ink-strong">{row[0]}</td>
                        <td className="px-3 py-2 text-ink-muted">{row[1]}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <p className="mt-3 flex gap-2 rounded-lg border border-phos-500/25 bg-phos-500/5 p-3 text-[12.5px] leading-relaxed text-ink-muted">
                <Radar size={13} className="mt-0.5 shrink-0 text-phos-400" />
                {finding.lesson}
              </p>
            </div>
          ))}
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div>
          <h3 className="text-lg font-semibold text-ink-strong">Frameworks to read</h3>
          <div className="mt-3 space-y-2">
            {lab.frameworks.map((framework) => (
              <a
                key={framework.link}
                href={framework.link}
                target="_blank"
                rel="noreferrer"
                className="card group block rounded-xl p-4"
              >
                <p className="flex items-center gap-1.5 text-[13.5px] font-medium text-ink-strong">
                  <Layers size={13} className="text-phos-500" />
                  {framework.name}
                  <ArrowUpRight size={12} className="ml-auto opacity-0 transition group-hover:opacity-100" />
                </p>
                <p className="mt-1.5 text-[12.5px] leading-relaxed text-ink-muted">{framework.note}</p>
              </a>
            ))}
          </div>
        </div>

        <div>
          <h3 className="text-lg font-semibold text-ink-strong">Where the research lives</h3>
          <div className="mt-3 space-y-2">
            {lab.where_to_look.map((place) => (
              <a
                key={place.link}
                href={place.link}
                target="_blank"
                rel="noreferrer"
                className="card group block rounded-xl p-4"
              >
                <p className="flex items-center gap-1.5 text-[13.5px] font-medium text-ink-strong">
                  <Terminal size={13} className="text-cyan-450" />
                  {place.name}
                  <ArrowUpRight size={12} className="ml-auto opacity-0 transition group-hover:opacity-100" />
                </p>
                <p className="mt-1.5 text-[12.5px] leading-relaxed text-ink-muted">{place.note}</p>
              </a>
            ))}
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold text-ink-strong">The prompt lab</h3>
        <p className="mt-2 text-[13px] text-ink-muted">
          Six things you can do today, in order, with your own system.
        </p>
        <div className="mt-4 grid gap-3 md:grid-cols-2">
          {lab.lab.map((step) => (
            <div key={step.id} className="card rounded-2xl p-5">
              <h4 className="text-[14px] font-medium text-ink-strong">{step.title}</h4>
              <p className="mt-2 text-[13px] leading-relaxed text-ink-muted">{step.body}</p>
              <p className="mt-3 flex gap-2 rounded-lg border border-phos-500/25 bg-phos-500/5 p-3 text-[12.5px] leading-relaxed text-ink-muted">
                <FlaskConical size={13} className="mt-0.5 shrink-0 text-phos-400" />
                {step.try}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function Field({
  body,
  tone,
}: {
  body: string;
  tone: "warn" | "info" | "ok";
}) {
  const styles = {
    warn: "border-amber-500/25 bg-amber-500/5",
    info: "border-cyan-450/25 bg-cyan-450/5",
    ok: "border-phos-500/25 bg-phos-500/5",
  };
  const labels = { warn: "what it breaks", info: "how to detect it", ok: "how to defend" };
  return (
    <div className={`rounded-lg border p-3 ${styles[tone]}`}>
      <p className="text-[10px] uppercase tracking-wide text-ink-muted">{labels[tone]}</p>
      <p className="mt-1 text-[12.5px] leading-relaxed text-ink-muted">{body}</p>
    </div>
  );
}
