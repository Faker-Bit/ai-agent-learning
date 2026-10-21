import { Check, Copy, Terminal as TerminalIcon } from "lucide-react";
import { useCallback, useMemo, useState } from "react";

import type { LineType, TerminalLine } from "../../types";

const LINE_PREFIX: Record<LineType, string> = {
  input: "$ ",
  output: "  ",
  tool: "  > ",
  success: "  ok ",
  info: "  ",
  warn: "  !  ",
  muted: "  ",
  accent: "  ",
  diff: "  ",
};

const LINE_CLASS: Record<LineType, string> = {
  input: "text-phos-300",
  output: "text-ink",
  tool: "text-cyan-450",
  success: "text-phos-300",
  info: "text-ink",
  warn: "text-amber-350",
  muted: "text-ink-muted",
  accent: "text-violet-350",
  diff: "text-ink",
};

function diffClass(text: string): string {
  if (text.startsWith("+")) return "text-phos-300";
  if (text.startsWith("-")) return "text-rose-300/80";
  return "text-ink";
}

export function TerminalFrame({
  title,
  subtitle,
  right,
  children,
  className = "",
  bodyClassName = "",
}: {
  title: string;
  subtitle?: string;
  right?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
  bodyClassName?: string;
}) {
  return (
    <div className={`term ${className}`}>
      <div className="term-bar">
        <span className="term-dot bg-[#ff5f57]" />
        <span className="term-dot bg-[#febc2e]" />
        <span className="term-dot bg-[#28c840]" />
        <span className="ml-2 truncate text-[11px] text-ink-muted">{title}</span>
        {subtitle ? <span className="ml-2 truncate text-[11px] text-ink-muted/70">{subtitle}</span> : null}
        {right ? <div className="ml-auto flex items-center gap-2">{right}</div> : null}
      </div>
      <div className={`scanlines relative px-4 py-4 text-[12.5px] leading-[1.75] sm:text-[13px] ${bodyClassName}`}>
        {children}
      </div>
    </div>
  );
}

export function TypedLines({
  lines,
  revealed,
  showCaret = true,
}: {
  lines: TerminalLine[];
  revealed: number;
  showCaret?: boolean;
}) {
  const offsets = useMemo(() => {
    const result: number[] = [];
    let cursor = 0;
    for (const line of lines) {
      result.push(cursor);
      cursor += line.text.length;
    }
    return result;
  }, [lines]);

  const rendered = lines.map((line, index) => {
    const start = offsets[index] ?? 0;
    const visible = Math.max(0, Math.min(line.text.length, revealed - start));
    const text = line.text.slice(0, visible);
    const isLast = index === lines.length - 1;
    const caret = showCaret && isLast && visible >= line.text.length;
    return (
      <div key={index} className={`whitespace-pre-wrap break-words ${LINE_CLASS[line.type]}`}>
        {line.type === "diff" ? (
          <span className={diffClass(line.text)}>{text}</span>
        ) : (
          <>
            <span className="text-ink-muted/80">{LINE_PREFIX[line.type]}</span>
            {text}
          </>
        )}
        {caret ? <span className="caret ml-0.5" /> : null}
      </div>
    );
  });
  return <>{rendered}</>;
}

export function StaticLines({ lines }: { lines: TerminalLine[] }) {
  return (
    <>
      {lines.map((line, index) => (
        <div key={index} className={`whitespace-pre-wrap break-words ${LINE_CLASS[line.type]}`}>
          {line.type === "diff" ? (
            <span className={diffClass(line.text)}>{line.text}</span>
          ) : (
            <>
              <span className="text-ink-muted/80">{LINE_PREFIX[line.type]}</span>
              {line.text}
            </>
          )}
        </div>
      ))}
    </>
  );
}

export function CopyButton({ value, label = "copy" }: { value: string; label?: string }) {
  const [copied, setCopied] = useState(false);
  const copy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(value);
    } catch {
      /* clipboard unavailable */
    }
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1600);
  }, [value]);

  return (
    <button
      onClick={() => void copy()}
      className="btn btn-ghost !px-2.5 !py-1 !text-[11px]"
      title="Copy to clipboard"
    >
      {copied ? <Check size={12} className="text-phos-400" /> : <Copy size={12} />}
      {copied ? "copied" : label}
    </button>
  );
}

export function TerminalBadge({ text }: { text: string }) {
  return (
    <span className="chip chip-phos">
      <TerminalIcon size={11} /> {text}
    </span>
  );
}
