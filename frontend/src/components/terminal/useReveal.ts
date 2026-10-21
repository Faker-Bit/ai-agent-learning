import { useEffect, useMemo, useRef, useState } from "react";

import type { TerminalLine } from "../../types";

/**
 * Character-by-character reveal of a block of terminal lines.
 *
 * Returns the number of characters currently visible. Pass it to <TypedLines />
 * to render the partial output.
 */
export function useReveal(
  lines: TerminalLine[],
  options: { speed?: number; playing?: boolean; loop?: boolean; onDone?: () => void },
) {
  const { speed = 1, playing = true, loop = false, onDone } = options;
  const total = useMemo(
    () => lines.reduce((sum, line) => sum + line.text.length, 0),
    [lines],
  );
  const [revealed, setRevealed] = useState(0);
  const [prevTotal, setPrevTotal] = useState(total);
  const doneRef = useRef(false);
  const onDoneRef = useRef(onDone);

  useEffect(() => {
    onDoneRef.current = onDone;
  }, [onDone]);

  // Reset the reveal when the content changes (derived state, not an effect).
  if (prevTotal !== total) {
    setPrevTotal(total);
    setRevealed(0);
  }

  useEffect(() => {
    doneRef.current = false;
  }, [total]);

  useEffect(() => {
    if (!playing) return;
    if (revealed >= total) {
      if (!doneRef.current) {
        doneRef.current = true;
        onDoneRef.current?.();
      }
      if (!loop) return;
      const timer = window.setTimeout(() => {
        setRevealed(0);
        doneRef.current = false;
      }, 2600);
      return () => window.clearTimeout(timer);
    }
    const chunk = Math.max(1, Math.round(2.5 * speed));
    const timer = window.setTimeout(() => {
      setRevealed((value) => Math.min(total, value + chunk));
    }, 16);
    return () => window.clearTimeout(timer);
  }, [revealed, total, playing, speed, loop]);

  return revealed;
}
