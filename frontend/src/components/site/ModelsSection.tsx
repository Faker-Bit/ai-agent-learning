import { motion } from "framer-motion";
import { ArrowUpRight, KeyRound, Server, Zap } from "lucide-react";
import { useMemo, useState } from "react";

import { SectionHeading } from "./Chrome";
import { CopyButton } from "../terminal/Terminal";
import type { ModelGuide, ModelInfo, ProviderInfo } from "../../types";

export function ModelsSection({
  guides,
  providers,
  models,
}: {
  guides: ModelGuide[];
  providers: ProviderInfo[];
  models: ModelInfo[];
}) {
  const [showAllModels, setShowAllModels] = useState(false);
  const [tier, setTier] = useState<"all" | "free">("all");

  const visibleModels = useMemo(() => {
    const filtered = tier === "free" ? models.filter((model) => model.free) : models;
    return showAllModels ? filtered : filtered.slice(0, 12);
  }, [models, tier, showAllModels]);

  const freeProviders = providers.filter((provider) => provider.tier !== "paid");
  const paidProviders = providers.filter((provider) => provider.tier === "paid");

  return (
    <section id="models" className="border-b border-line py-20">
      <div className="mx-auto max-w-7xl px-5">
        <SectionHeading
          eyebrow="Choosing a model"
          title={
            <>
              The model is a{" "}
              <span className="text-phos-400">tool choice</span>, not a personality
            </>
          }
          body="Which model an agent uses changes how much it costs, how fast it feels and how often it needs a second try. Here is how to route models instead of guessing."
        />

        <div className="mt-10 grid gap-4 lg:grid-cols-2">
          {guides.map((guide, index) => (
            <motion.div
              key={guide.id}
              initial={{ opacity: 0, y: 14 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-60px" }}
              transition={{ duration: 0.4, delay: Math.min(index * 0.05, 0.2) }}
              className="panel rounded-2xl p-6"
            >
              <h3 className="text-[15px] font-semibold text-ink-strong">{guide.title}</h3>
              <p className="mt-2 text-[13.5px] leading-relaxed text-ink-muted">{guide.body}</p>
              <div className="mt-4 overflow-hidden rounded-lg border border-line">
                <table className="w-full text-left text-[12.5px]">
                  <tbody>
                    {guide.rows.map((row) => (
                      <tr key={row[0]} className="border-b border-line/70 last:border-0">
                        <td className="px-3 py-2.5 font-medium text-phos-300">{row[0]}</td>
                        <td className="px-3 py-2.5 text-ink-muted">{row[1]}</td>
                        <td className="hidden px-3 py-2.5 text-ink-muted sm:table-cell">{row[2]}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </motion.div>
          ))}
        </div>

        <div className="mt-14 grid gap-4 lg:grid-cols-2">
          <ProviderColumn
            title="Free tiers"
            subtitle="No credit card, enough to learn and to ship side projects."
            providers={freeProviders}
          />
          <ProviderColumn
            title="Paid tiers"
            subtitle="Frontier models for the hard reasoning and the big diffs."
            providers={paidProviders}
          />
        </div>

        <div className="mt-14">
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <h3 className="text-lg font-semibold text-ink-strong">Model catalogue</h3>
              <p className="mt-1.5 text-[13.5px] text-ink-muted">
                {models.filter((model) => model.free).length} of {models.length} entries run on a free
                tier. Model ids are what you paste into a config.
              </p>
            </div>
            <div className="flex items-center gap-2">
              <div className="flex items-center gap-1 rounded-xl border border-line bg-term-900 p-1">
                {(["all", "free"] as const).map((option) => (
                  <button
                    key={option}
                    onClick={() => setTier(option)}
                    className={`rounded-lg px-3 py-1.5 text-[12px] transition ${
                      tier === option
                        ? "bg-phos-500/15 text-phos-300"
                        : "text-ink-muted hover:text-ink"
                    }`}
                  >
                    {option === "all" ? "all" : "free tier"}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="panel mt-5 overflow-hidden rounded-2xl">
            <div className="overflow-x-auto">
              <table className="w-full min-w-[640px] text-left text-[12.5px]">
                <thead className="border-b border-line bg-term-900 text-[10.5px] uppercase tracking-[0.14em] text-ink-muted">
                  <tr>
                    <th className="px-4 py-3 font-medium">Model</th>
                    <th className="px-4 py-3 font-medium">Provider</th>
                    <th className="px-4 py-3 font-medium">Context</th>
                    <th className="px-4 py-3 font-medium">Notes</th>
                    <th className="px-4 py-3 font-medium">Tier</th>
                  </tr>
                </thead>
                <tbody>
                  {visibleModels.map((model) => (
                    <tr key={`${model.provider}:${model.id}`} className="border-b border-line/60 last:border-0">
                      <td className="px-4 py-2.5">
                        <span className="text-ink">{model.name}</span>
                        <span className="ml-2 font-mono text-[10.5px] text-ink-muted">{model.id}</span>
                      </td>
                      <td className="px-4 py-2.5 text-ink-muted">{model.provider_label}</td>
                      <td className="px-4 py-2.5 text-ink-muted">{model.context_window}</td>
                      <td className="px-4 py-2.5 text-ink-muted">{model.description}</td>
                      <td className="px-4 py-2.5">
                        {model.free ? <span className="chip chip-phos">free</span> : <span className="chip">paid</span>}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {models.length > 12 ? (
              <div className="border-t border-line px-4 py-3 text-center">
                <button onClick={() => setShowAllModels((value) => !value)} className="btn btn-ghost">
                  {showAllModels ? "show less" : `show all ${models.length} models`}
                </button>
              </div>
            ) : null}
          </div>
        </div>

        <div className="mt-8 rounded-2xl border border-phos-500/25 bg-phos-500/5 p-5">
          <div className="flex flex-wrap items-center gap-3">
            <Zap size={17} className="text-phos-400" />
            <p className="flex-1 text-[13.5px] leading-relaxed text-ink-muted">
              The fastest way to a working setup: pick one free tier, point an agent at it, and learn
              the loop on a model that costs nothing. Upgrade only when a specific task earns it.
            </p>
            <a
              href="https://opencode.ai/console"
              target="_blank"
              rel="noreferrer"
              className="btn btn-ghost shrink-0"
            >
              OpenCode Zen <ArrowUpRight size={13} />
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}

function ProviderColumn({
  title,
  subtitle,
  providers,
}: {
  title: string;
  subtitle: string;
  providers: ProviderInfo[];
}) {
  return (
    <div className="panel rounded-2xl p-6">
      <div className="flex items-center gap-2">
        <Server size={15} className="text-phos-500" />
        <h3 className="text-[15px] font-semibold text-ink-strong">{title}</h3>
      </div>
      <p className="mt-1.5 text-[13px] text-ink-muted">{subtitle}</p>
      <ul className="mt-4 divide-y divide-line/70">
        {providers.map((provider) => (
          <li key={provider.id} className="py-3 first:pt-0 last:pb-0">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-[13.5px] font-medium text-ink">{provider.label}</span>
              {provider.has_key ? <span className="chip chip-phos">key present</span> : null}
              {provider.signup_url ? (
                <a
                  href={provider.signup_url}
                  target="_blank"
                  rel="noreferrer"
                  className="ml-auto inline-flex items-center gap-1 text-[11.5px] text-ink-muted hover:text-phos-300"
                >
                  get a key <ArrowUpRight size={10} />
                </a>
              ) : null}
            </div>
            {provider.note ? (
              <p className="mt-1 text-[12.5px] leading-relaxed text-ink-muted">{provider.note}</p>
            ) : null}
            <div className="mt-1.5 flex items-center gap-2">
              <KeyRound size={11} className="text-ink-muted" />
              <code className="font-mono text-[11px] text-ink-muted">
                {provider.env_key || "no key needed"}
              </code>
              <CopyButton value={provider.env_key || provider.default_base_url} label="copy" />
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
