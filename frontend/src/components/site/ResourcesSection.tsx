import { motion } from "framer-motion";
import { ArrowUpRight, Boxes, Download, Filter, Search, Star, Terminal } from "lucide-react";
import { useEffect, useState } from "react";

import { SectionHeading } from "./Chrome";
import { CopyButton } from "../terminal/Terminal";

interface Resource {
  id: string;
  name: string;
  repo: string;
  url: string;
  category: string;
  category_title: string;
  stars: number;
  license: string;
  pushed: string;
  description: string;
  topics: string[];
  language: string;
  install: string;
  example: string[];
  note: string;
  homepage: string;
}

interface ResourceCategory {
  id: string;
  title: string;
  blurb: string;
  count: number;
}

interface ResourcePayload {
  generated: string;
  categories: ResourceCategory[];
  resources: Resource[];
  total: number;
  matched: number;
}

export function ResourcesSection() {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("all");
  const [payload, setPayload] = useState<ResourcePayload | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    const handle = window.setTimeout(async () => {
      setLoading(true);
      try {
        const params = new URLSearchParams();
        if (query.trim()) params.set("q", query.trim());
        if (category !== "all") params.set("category", category);
        const res = await fetch(`/api/resources${params.toString() ? `?${params}` : ""}`);
        if (!res.ok) throw new Error(`The catalogue API returned ${res.status}`);
        const data = (await res.json()) as ResourcePayload;
        if (!cancelled) {
          setPayload(data);
          setError(null);
        }
      } catch (err) {
        if (!cancelled) setError((err as Error).message);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }, 220);
    return () => {
      cancelled = true;
      window.clearTimeout(handle);
    };
  }, [query, category]);

  const resources = payload?.resources ?? [];
  const categories = payload?.categories ?? [];

  const grouped = groupByCategory(resources);

  return (
    <section id="resources" className="border-b border-line py-20">
      <div className="mx-auto max-w-7xl px-5">
        <SectionHeading
          eyebrow="Research catalogue"
          title={
            <>
              {payload?.total ?? 80}+ verified repos,{" "}
              <span className="text-phos-400">searchable</span>
            </>
          }
          body="Every entry was fetched from the GitHub API with its install command and usage example pulled from the project README. Star counts and last-push dates are a snapshot, so you can tell an active project from an abandoned one at a glance."
        />

        <div className="mt-8 flex flex-wrap items-center gap-3">
          <div className="relative min-w-[240px] flex-1">
            <Search
              size={15}
              className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-ink-muted"
            />
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search the catalogue - 'garak', 'mcp', 'guardrails', 'qwen'..."
              className="w-full rounded-xl border border-line bg-term-900 py-2.5 pl-10 pr-4 text-[13px] text-ink outline-none transition focus:border-phos-500/60"
            />
          </div>
          <div className="flex items-center gap-1.5 rounded-xl border border-line bg-term-900 p-1">
            <Filter size={13} className="ml-2 text-ink-muted" />
            <button
              onClick={() => setCategory("all")}
              className={`rounded-lg px-3 py-1.5 text-[12px] transition ${
                category === "all" ? "bg-phos-500/15 text-phos-300" : "text-ink-muted hover:text-ink"
              }`}
            >
              all
            </button>
            {categories.map((item) => (
              <button
                key={item.id}
                onClick={() => setCategory(item.id)}
                className={`rounded-lg px-3 py-1.5 text-[12px] transition ${
                  category === item.id
                    ? "bg-phos-500/15 text-phos-300"
                    : "text-ink-muted hover:text-ink"
                }`}
              >
                {item.title.split(" ")[0].toLowerCase()}
              </button>
            ))}
          </div>
          <span className="font-mono text-[12px] text-ink-muted">
            {payload ? `${payload.matched}/${payload.total}` : "..."}
          </span>
        </div>

        {error ? (
          <div className="mt-6 rounded-xl border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-[13px] text-rose-200">
            {error}
          </div>
        ) : null}

        {loading && !payload ? (
          <div className="mt-8 space-y-3">
            {[0, 1, 2].map((row) => (
              <div key={row} className="shimmer h-24 rounded-2xl" />
            ))}
          </div>
        ) : null}

        <div className="mt-8 space-y-10">
          {grouped.map(([group, items]) => (
            <div key={group}>
              <div className="flex items-baseline gap-3">
                <h3 className="text-[15px] font-semibold text-ink-strong">{group}</h3>
                <span className="text-[11.5px] text-ink-muted">{items.length} projects</span>
              </div>
              <div className="mt-3 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
                {items.map((item, index) => (
                  <motion.article
                    key={item.id}
                    initial={{ opacity: 0, y: 10 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: "-40px" }}
                    transition={{ duration: 0.3, delay: Math.min(index * 0.02, 0.18) }}
                    className="card flex flex-col rounded-2xl p-4"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <a
                        href={item.url}
                        target="_blank"
                        rel="noreferrer"
                        className="group min-w-0"
                      >
                        <p className="truncate font-mono text-[13px] font-semibold text-ink-strong group-hover:text-phos-300">
                          {item.repo}
                        </p>
                      </a>
                      <span className="flex shrink-0 items-center gap-1 text-[11.5px] text-phos-300">
                        <Star size={11} />
                        {formatStars(item.stars)}
                      </span>
                    </div>

                    <p className="mt-1.5 line-clamp-2 text-[12.5px] leading-relaxed text-ink-muted">
                      {item.description}
                    </p>

                    {item.note ? (
                      <p className="mt-2.5 text-[12.5px] leading-relaxed text-ink">{item.note}</p>
                    ) : null}

                    {item.install ? (
                      <div className="mt-3 rounded-lg border border-line bg-term-950 p-2.5">
                        <div className="flex items-center justify-between gap-2">
                          <span className="flex items-center gap-1.5 text-[10px] uppercase tracking-wide text-ink-muted">
                            <Download size={10} /> install
                          </span>
                          <CopyButton value={item.install} label="copy" />
                        </div>
                        <code className="mt-1 block overflow-x-auto font-mono text-[11px] text-phos-300">
                          {item.install}
                        </code>
                      </div>
                    ) : null}

                    {item.example.length ? (
                      <div className="mt-2 rounded-lg border border-line bg-term-950 p-2.5">
                        <span className="flex items-center gap-1.5 text-[10px] uppercase tracking-wide text-ink-muted">
                          <Terminal size={10} /> example
                        </span>
                        <pre className="mt-1 max-h-24 overflow-auto whitespace-pre font-mono text-[10.5px] leading-relaxed text-ink-muted">
                          {item.example.slice(0, 5).join("\n")}
                        </pre>
                      </div>
                    ) : null}

                    <div className="mt-auto flex flex-wrap items-center gap-2 border-t border-line pt-3 text-[11px] text-ink-muted">
                      <span className="chip">{item.license}</span>
                      {item.language ? <span className="chip">{item.language}</span> : null}
                      <span className="chip">pushed {item.pushed || "unknown"}</span>
                      <a
                        href={item.url}
                        target="_blank"
                        rel="noreferrer"
                        className="ml-auto inline-flex items-center gap-1 text-phos-300 hover:text-phos-200"
                      >
                        open <ArrowUpRight size={11} />
                      </a>
                    </div>
                  </motion.article>
                ))}
              </div>
            </div>
          ))}
        </div>

        {!loading && !resources.length && !error ? (
          <div className="mt-8 rounded-2xl border border-dashed border-line px-6 py-12 text-center">
            <Boxes size={22} className="mx-auto text-ink-muted" />
            <p className="mt-3 text-[13px] text-ink-muted">
              Nothing matches that search. Try a tool name, a topic, or clear the filter.
            </p>
          </div>
        ) : null}

        {payload ? (
          <p className="mt-8 text-center font-mono text-[11px] text-ink-muted">
            catalogue generated {payload.generated} Â· re-run backend/tools/research.py to refresh
          </p>
        ) : null}
      </div>
    </section>
  );
}

function formatStars(stars: number): string {
  if (stars >= 1000) return `${(stars / 1000).toFixed(stars >= 10000 ? 0 : 1)}k`;
  return String(stars);
}

function groupByCategory(resources: Resource[]): [string, Resource[]][] {
  const map = new Map<string, Resource[]>();
  for (const item of resources) {
    const list = map.get(item.category_title) ?? [];
    list.push(item);
    map.set(item.category_title, list);
  }
  return [...map.entries()];
}
