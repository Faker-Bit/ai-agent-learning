import { Check, Minus, Search, X } from "lucide-react";
import { useMemo, useState } from "react";

import { SectionHeading } from "./Chrome";
import type { Agent, CheatsheetRow, ComparisonRow } from "../../types";

export function CheatsheetSection({
  rows,
  groups,
  agents,
}: {
  rows: CheatsheetRow[];
  groups: string[];
  agents: Agent[];
}) {
  const [query, setQuery] = useState("");
  const [agentFilter, setAgentFilter] = useState("all");
  const [groupFilter, setGroupFilter] = useState("all");

  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return rows.filter((row) => {
      if (agentFilter !== "all" && row.agent !== agentFilter) return false;
      if (groupFilter !== "all" && row.group !== groupFilter) return false;
      if (!needle) return true;
      return (
        row.command.toLowerCase().includes(needle) ||
        row.description.toLowerCase().includes(needle) ||
        row.agent.toLowerCase().includes(needle)
      );
    });
  }, [rows, query, agentFilter, groupFilter]);

  const grouped = useMemo(() => {
    const map = new Map<string, CheatsheetRow[]>();
    for (const row of filtered) {
      const list = map.get(row.group) ?? [];
      list.push(row);
      map.set(row.group, list);
    }
    return [...map.entries()];
  }, [filtered]);

  return (
    <section id="cheatsheet" className="border-b border-line bg-term-900/40 py-20">
      <div className="mx-auto max-w-7xl px-5">
        <SectionHeading
          eyebrow="Command reference"
          title={
            <>
              Every command worth <span className="text-phos-400">memorising</span>
            </>
          }
          body="Search across the whole directory. Copy anything with one click."
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
              placeholder="Search commands - try 'undo', 'mcp', 'json'..."
              className="w-full rounded-xl border border-line bg-term-900 py-2.5 pl-10 pr-4 text-[13px] text-ink outline-none transition focus:border-phos-500/60"
            />
          </div>

          <select
            value={agentFilter}
            onChange={(event) => setAgentFilter(event.target.value)}
            className="rounded-xl border border-line bg-term-900 px-3 py-2.5 text-[13px] text-ink outline-none focus:border-phos-500/60"
          >
            <option value="all">all agents</option>
            {agents.map((agent) => (
              <option key={agent.id} value={agent.id}>
                {agent.name}
              </option>
            ))}
          </select>

          <select
            value={groupFilter}
            onChange={(event) => setGroupFilter(event.target.value)}
            className="rounded-xl border border-line bg-term-900 px-3 py-2.5 text-[13px] text-ink outline-none focus:border-phos-500/60"
          >
            <option value="all">all groups</option>
            {groups.map((group) => (
              <option key={group} value={group}>
                {group}
              </option>
            ))}
          </select>

          <span className="font-mono text-[12px] text-ink-muted">
            {filtered.length}/{rows.length}
          </span>
        </div>

        <div className="mt-8 grid gap-6 lg:grid-cols-2">
          {grouped.map(([group, items]) => (
            <div key={group} className="panel overflow-hidden rounded-2xl">
              <div className="border-b border-line bg-term-900 px-4 py-2.5 text-[11px] uppercase tracking-[0.14em] text-ink-muted">
                {group}
              </div>
              <ul className="divide-y divide-line/60">
                {items.map((row) => (
                  <li key={`${row.agent}-${row.command}`} className="group flex items-start gap-3 px-4 py-2.5">
                    <code className="min-w-0 flex-1 font-mono text-[12px] text-phos-300">{row.command}</code>
                    <span className="hidden max-w-[46%] text-right text-[12px] text-ink-muted sm:block">
                      {row.description}
                    </span>
                    <span className="chip shrink-0">{row.agent}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {!filtered.length ? (
          <div className="mt-8 rounded-2xl border border-dashed border-line px-6 py-12 text-center text-[13px] text-ink-muted">
            No command matches that. Try a shorter search.
          </div>
        ) : null}
      </div>
    </section>
  );
}

export function CompareSection({
  rows,
  agents,
}: {
  rows: ComparisonRow[];
  agents: Agent[];
}) {
  const compared = agents.filter((agent) =>
    ["opencode", "codex", "gemini", "claude", "aider", "goose", "openhands"].includes(agent.id),
  );

  return (
    <section id="compare" className="border-b border-line py-20">
      <div className="mx-auto max-w-7xl px-5">
        <SectionHeading
          eyebrow="Side by side"
          title={
            <>
              The shortlist, <span className="text-phos-400">compared</span>
            </>
          }
          body="The CLI agents people actually use day to day. Open source means you can read the tool that is editing your code."
        />

        <div className="panel mt-8 overflow-hidden rounded-2xl">
          <div className="overflow-x-auto">
            <table className="w-full min-w-[820px] text-left text-[12.5px]">
              <thead className="border-b border-line bg-term-900">
                <tr>
                  <th className="px-4 py-3 text-[10.5px] uppercase tracking-[0.14em] text-ink-muted">
                    capability
                  </th>
                  {compared.map((agent) => (
                    <th key={agent.id} className="px-4 py-3 text-[12.5px] font-semibold text-ink-strong">
                      {agent.name}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {rows.map((row) => (
                  <tr key={row.feature} className="border-b border-line/60 last:border-0">
                    <td className="px-4 py-3 text-ink-muted">{row.feature}</td>
                    {compared.map((agent) => {
                      const value = row.values[agent.id];
                      return (
                        <td key={agent.id} className="px-4 py-3">
                          {value === true ? (
                            <Check size={15} className="text-phos-400" />
                          ) : value === false ? (
                            <Minus size={15} className="text-ink-muted/50" />
                          ) : (
                            <X size={15} className="text-ink-muted/40" />
                          )}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="mt-6 flex flex-wrap items-center gap-3 text-[12.5px] text-ink-muted">
          <span className="inline-flex items-center gap-1.5">
            <Check size={13} className="text-phos-400" /> yes
          </span>
          <span className="inline-flex items-center gap-1.5">
            <Minus size={13} className="text-ink-muted/60" /> no
          </span>
          <span className="ml-auto">
            Full command lists for every agent live in the{" "}
            <a href="#cheatsheet" className="text-phos-300 underline underline-offset-2">
              command reference
            </a>
            .
          </span>
        </div>
      </div>
    </section>
  );
}
