import { BookOpen, ChevronRight, Command, Cpu, Terminal } from "lucide-react";
import { Link } from "react-router-dom";

const NAV = [
  { href: "/#loop", label: "How it works" },
  { href: "/#harness", label: "Harness" },
  { href: "/#skills", label: "Skills" },
  { href: "/#agents", label: "Agents" },
  { href: "/#model-hub", label: "Models" },
  { href: "/#security", label: "Security lab" },
  { href: "/#resources", label: "Resources" },
  { href: "/#walkthroughs", label: "Walkthroughs" },
  { href: "/#cheatsheet", label: "Commands" },
];

export function SiteHeader() {
  return (
    <header className="glass sticky top-0 z-50">
      <div className="mx-auto flex h-14 max-w-7xl items-center gap-6 px-5">
        <Link to="/" className="flex items-center gap-2.5">
          <span className="pulse-ring flex h-8 w-8 items-center justify-center rounded-lg bg-phos-400 text-term-950">
            <Terminal size={16} strokeWidth={2.6} />
          </span>
          <span className="font-mono text-sm font-semibold tracking-tight text-ink-strong">
            agent<span className="text-phos-400">pilot</span>
          </span>
        </Link>

        <nav className="hidden items-center gap-1 md:flex">
          {NAV.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className="rounded-lg px-3 py-1.5 text-[13px] text-ink-muted transition hover:bg-term-800 hover:text-ink-strong"
            >
              {item.label}
            </a>
          ))}
        </nav>

        <div className="ml-auto flex items-center gap-2">
          <span className="hidden items-center gap-1.5 text-[11px] text-ink-muted lg:flex">
            <Cpu size={12} className="text-phos-500" /> opencode | zen | codex | claude | gemini | aider | pi
          </span>
          <Link
            to="/walkthrough/opencode-first-hour"
            className="btn btn-primary !py-1.5 !text-[13px]"
          >
            <Command size={13} />
            <span className="hidden sm:inline">Start walkthrough</span>
            <span className="sm:hidden">Start</span>
          </Link>
        </div>
      </div>
    </header>
  );
}

export function SiteFooter() {
  return (
    <footer className="border-t border-line bg-term-900">
      <div className="mx-auto grid max-w-7xl gap-10 px-5 py-14 md:grid-cols-[1.4fr_1fr_1fr_1fr]">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-phos-400 text-term-950">
              <Terminal size={16} strokeWidth={2.6} />
            </span>
            <span className="font-mono text-sm font-semibold text-ink-strong">agentpilot</span>
          </div>
          <p className="mt-4 max-w-sm text-[13px] leading-relaxed text-ink-muted">
            A hands-on manual for driving AI coding agents. Every command on this site is taken from the
            tool's own documentation - no invented flags, no invented output.
          </p>
          <p className="mt-4 font-mono text-[11px] text-ink-muted/70">
            last verified against upstream docs | October 2026
          </p>
        </div>

        <FooterColumn
          title="Tools"
          items={[
            ["opencode", "https://opencode.ai/docs/"],
            ["OpenCode Zen", "https://opencode.ai/console"],
            ["Codex CLI", "https://developers.openai.com/codex"],
            ["Claude Code", "https://docs.anthropic.com/en/docs/claude-code/overview"],
            ["Gemini CLI", "https://geminicli.com/docs/"],
            ["Aider", "https://aider.chat/docs/"],
          ]}
        />
        <FooterColumn
          title="Concepts"
          items={[
            ["How the loop works", "/#loop"],
            ["Agent directory", "/#agents"],
            ["Walkthroughs", "/#walkthroughs"],
            ["Prompt craft", "/#craft"],
            ["Choosing a model", "/#models"],
            ["Command reference", "/#cheatsheet"],
          ]}
        />
        <FooterColumn
          title="Compare"
          items={[
            ["CLI vs IDE agents", "/#compare"],
            ["Free vs paid tiers", "/#models"],
            ["Rules files", "/#craft"],
            ["MCP servers", "/walkthrough/opencode-mcp"],
            ["Automation", "/walkthrough/opencode-automation"],
            ["Model routing", "/walkthrough/opencode-free-models"],
          ]}
        />
      </div>

      <div className="border-t border-line">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-3 px-5 py-5 text-[11px] text-ink-muted">
          <span>Built for people who read the diff before they read the summary.</span>
          <span className="font-mono">~/agent-pilot $</span>
        </div>
      </div>
    </footer>
  );
}

function FooterColumn({
  title,
  items,
}: {
  title: string;
  items: [string, string][];
}) {
  return (
    <div>
      <p className="text-[11px] uppercase tracking-[0.14em] text-ink-muted">{title}</p>
      <ul className="mt-4 space-y-2.5">
        {items.map(([label, href]) => {
          const external = href.startsWith("http");
          return (
            <li key={label}>
              {external ? (
                <a
                  href={href}
                  target="_blank"
                  rel="noreferrer"
                  className="group inline-flex items-center gap-1 text-[13px] text-ink-muted transition hover:text-phos-300"
                >
                  {label}
                  <ChevronRight size={12} className="opacity-0 transition group-hover:opacity-100" />
                </a>
              ) : (
                <a
                  href={href}
                  className="group inline-flex items-center gap-1 text-[13px] text-ink-muted transition hover:text-phos-300"
                >
                  {label}
                  <ChevronRight size={12} className="opacity-0 transition group-hover:opacity-100" />
                </a>
              )}
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export function SectionHeading({
  eyebrow,
  title,
  body,
  icon,
}: {
  eyebrow: string;
  title: React.ReactNode;
  body?: string;
  icon?: React.ReactNode;
}) {
  return (
    <div className="max-w-3xl">
      <div className="flex items-center gap-2 text-[11px] uppercase tracking-[0.18em] text-phos-500">
        {icon ?? <BookOpen size={12} />}
        {eyebrow}
      </div>
      <h2 className="mt-3 text-2xl font-semibold tracking-tight text-ink-strong sm:text-3xl">{title}</h2>
      {body ? <p className="mt-3 text-[15px] leading-relaxed text-ink-muted">{body}</p> : null}
    </div>
  );
}
