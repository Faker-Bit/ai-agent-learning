import { motion } from "framer-motion";
import {
  ArrowUpRight,
  BookOpen,
  Braces,
  Check,
  Code2,
  Cpu,
  Globe,
  KeyRound,
  Search,
  Terminal,
  Zap,
} from "lucide-react";
import { useMemo, useState } from "react";

import { SectionHeading } from "./Chrome";
import { CopyButton, TerminalFrame } from "../terminal/Terminal";
import type { ModelInfo } from "../../types";

interface HubEntry {
  id: string;
  name: string;
  vendor: string;
  tier: string;
  blurb: string;
  best_for: string[];
  surfaces: string[][];
  api: {
    base_url: string;
    style: string;
    key_url: string;
    env: string;
    install: string;
    code: string;
  };
  prompting: string[];
  agent_notes: string[];
  limits: string[];
  links: string[][];
}

interface HubIntro {
  title: string;
  body: string;
  principles: string[][];
}

const TIER_STYLES: Record<string, string> = {
  free: "chip-phos",
  paid: "chip-amber",
  local: "chip-cyan",
  "free+paid": "chip-violet",
};

export function ModelHubSection({
  models,
  intro,
}: {
  models: HubEntry[];
  intro: HubIntro;
}) {
  const [query, setQuery] = useState("");
  const [vendor, setVendor] = useState("all");
  const [open, setOpen] = useState<string | null>(models[0]?.id ?? null);

  const vendors = useMemo(
    () => ["all", ...Array.from(new Set(models.map((model) => model.vendor)))],
    [models],
  );

  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return models.filter((model) => {
      if (vendor !== "all" && model.vendor !== vendor) return false;
      if (!needle) return true;
      return (
        model.name.toLowerCase().includes(needle) ||
        model.vendor.toLowerCase().includes(needle) ||
        model.blurb.toLowerCase().includes(needle) ||
        model.best_for.join(" ").toLowerCase().includes(needle)
      );
    });
  }, [models, query, vendor]);

  return (
    <section id="model-hub" className="border-b border-line py-20">
      <div className="mx-auto max-w-7xl px-5">
        <SectionHeading
          eyebrow="Model learning hub"
          title={
            <>
              Every major model,{" "}
              <span className="text-phos-400">one page each</span>
            </>
          }
          body={intro.body}
        />

        <div className="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {intro.principles.map(([title, body]) => (
            <div key={title} className="rounded-xl border border-line bg-term-800 p-4">
              <p className="text-[13px] font-medium text-ink-strong">{title}</p>
              <p className="mt-1.5 text-[12.5px] leading-relaxed text-ink-muted">{body}</p>
            </div>
          ))}
        </div>

        <div className="mt-8 flex flex-wrap items-center gap-3">
          <div className="relative min-w-[240px] flex-1">
            <Search
              size={15}
              className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-ink-muted"
            />
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search models - try 'coding', 'free', 'local'..."
              className="w-full rounded-xl border border-line bg-term-900 py-2.5 pl-10 pr-4 text-[13px] text-ink outline-none transition focus:border-phos-500/60"
            />
          </div>
          <select
            value={vendor}
            onChange={(event) => setVendor(event.target.value)}
            className="rounded-xl border border-line bg-term-900 px-3 py-2.5 text-[13px] text-ink outline-none focus:border-phos-500/60"
          >
            {vendors.map((item) => (
              <option key={item} value={item}>
                {item === "all" ? "all vendors" : item}
              </option>
            ))}
          </select>
          <span className="font-mono text-[12px] text-ink-muted">
            {filtered.length}/{models.length}
          </span>
        </div>

        <div className="mt-6 space-y-3">
          {filtered.map((model, index) => {
            const isOpen = open === model.id;
            return (
              <motion.div
                key={model.id}
                initial={{ opacity: 0, y: 12 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-60px" }}
                transition={{ duration: 0.35, delay: Math.min(index * 0.02, 0.2) }}
                className="card overflow-hidden rounded-2xl"
              >
                <button
                  onClick={() => setOpen(isOpen ? null : model.id)}
                  className="flex w-full items-start gap-4 p-5 text-left"
                >
                  <div className="min-w-0 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <h3 className="font-mono text-[16px] font-semibold text-ink-strong">
                        {model.name}
                      </h3>
                      <span className="chip">{model.vendor}</span>
                      <span className={`chip ${TIER_STYLES[model.tier] ?? "chip"}`}>
                        {model.tier}
                      </span>
                    </div>
                    <p className="mt-2 text-[13.5px] leading-relaxed text-ink-muted">{model.blurb}</p>
                  </div>
                  <span className="shrink-0 text-[12px] text-phos-300">
                    {isOpen ? "close" : "open"}
                  </span>
                </button>

                {isOpen ? (
                  <div className="border-t border-line bg-term-900/60 p-5">
                    <div className="grid gap-5 lg:grid-cols-2">
                      <div className="space-y-5">
                        <Block title="Where to use it" icon={<Globe size={12} />}>
                          <ul className="space-y-1.5">
                            {model.surfaces.map(([label, detail]) => (
                              <li key={label} className="flex gap-2 text-[13px] leading-relaxed">
                                <span className="shrink-0 font-mono text-[11px] text-accent-300">
                                  {label}
                                </span>
                                <span className="text-ink-muted">{detail}</span>
                              </li>
                            ))}
                          </ul>
                        </Block>

                        <Block title="Best for" icon={<Zap size={12} />}>
                          <ul className="space-y-1.5">
                            {model.best_for.map((item) => (
                              <li key={item} className="flex gap-2 text-[13px] leading-relaxed text-ink-muted">
                                <Check size={13} className="mt-0.5 shrink-0 text-phos-500" />
                                {item}
                              </li>
                            ))}
                          </ul>
                        </Block>

                        <Block title="How to prompt it" icon={<Braces size={12} />}>
                          <ul className="space-y-2">
                            {model.prompting.map((tip) => (
                              <li
                                key={tip}
                                className="rounded-lg border border-line bg-term-950 px-3 py-2 text-[12.5px] leading-relaxed text-ink-muted"
                              >
                                {tip}
                              </li>
                            ))}
                          </ul>
                        </Block>

                        <Block title="In a coding agent" icon={<Terminal size={12} />}>
                          <ul className="space-y-1.5">
                            {model.agent_notes.map((note) => (
                              <li key={note} className="flex gap-2 text-[12.5px] leading-relaxed text-ink-muted">
                                <Cpu size={13} className="mt-0.5 shrink-0 text-cyan-450" />
                                {note}
                              </li>
                            ))}
                          </ul>
                        </Block>

                        <Block title="Limits to know" icon={<BookOpen size={12} />}>
                          <ul className="space-y-1.5">
                            {model.limits.map((limit) => (
                              <li key={limit} className="flex gap-2 text-[12.5px] leading-relaxed text-ink-muted">
                                <span className="mt-[7px] h-1 w-1 shrink-0 rounded-full bg-amber-400" />
                                {limit}
                              </li>
                            ))}
                          </ul>
                        </Block>
                      </div>

                      <div className="space-y-4">
                        <div className="rounded-xl border border-line bg-term-950 p-4">
                          <div className="flex items-center justify-between gap-2">
                            <p className="flex items-center gap-1.5 text-[11px] uppercase tracking-wide text-ink-muted">
                              <KeyRound size={12} /> API
                            </p>
                            <CopyButton
                              value={`export ${model.api.env}="..."`}
                              label="copy env"
                            />
                          </div>
                          <dl className="mt-3 space-y-1.5 font-mono text-[11.5px]">
                            <Row label="base_url" value={model.api.base_url} />
                            <Row label="style" value={model.api.style} />
                            <Row label="env" value={model.api.env} />
                            <Row label="install" value={model.api.install} />
                          </dl>
                          {model.api.key_url ? (
                            <a
                              href={model.api.key_url}
                              target="_blank"
                              rel="noreferrer"
                              className="mt-3 inline-flex items-center gap-1 text-[12px] text-phos-300 hover:text-phos-200"
                            >
                              get an API key <ArrowUpRight size={11} />
                            </a>
                          ) : null}
                        </div>

                        <TerminalFrame
                          title={`${model.name.toLowerCase()}-client.py`}
                          right={<CopyButton value={model.api.code} />}
                        >
                          <pre className="overflow-x-auto whitespace-pre text-[12px] leading-relaxed text-ink">
                            {model.api.code}
                          </pre>
                        </TerminalFrame>

                        <div className="rounded-xl border border-line bg-term-950 p-4">
                          <p className="flex items-center gap-1.5 text-[11px] uppercase tracking-wide text-ink-muted">
                            <Code2 size={12} /> links
                          </p>
                          <ul className="mt-2 space-y-1.5">
                            {model.links.map(([label, href]) => (
                              <li key={href}>
                                <a
                                  href={href}
                                  target="_blank"
                                  rel="noreferrer"
                                  className="inline-flex items-center gap-1.5 text-[12.5px] text-ink-muted transition hover:text-phos-300"
                                >
                                  {label}
                                  <ArrowUpRight size={11} />
                                </a>
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                ) : null}
              </motion.div>
            );
          })}
        </div>

        {!filtered.length ? (
          <div className="mt-8 rounded-2xl border border-dashed border-line px-6 py-12 text-center text-[13px] text-ink-muted">
            No model matches that. Try a vendor name, or clear the search.
          </div>
        ) : null}
      </div>
    </section>
  );
}

function Block({
  title,
  icon,
  children,
}: {
  title: string;
  icon: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <div>
      <p className="flex items-center gap-1.5 text-[11px] uppercase tracking-[0.14em] text-ink-muted">
        {icon}
        {title}
      </p>
      <div className="mt-2.5">{children}</div>
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex gap-2">
      <dt className="w-20 shrink-0 text-ink-muted">{label}</dt>
      <dd className="min-w-0 flex-1 break-all text-phos-300">{value}</dd>
    </div>
  );
}

export function ModelBadge({ model }: { model: ModelInfo }) {
  return (
    <span className="chip">
      <Cpu size={11} /> {model.name}
    </span>
  );
}
