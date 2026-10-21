import bundled from "../content/site.json";
import type { SiteContent } from "../types";

const BASE = (import.meta.env.VITE_API_BASE as string) || "/api";

export class ApiRequestError extends Error {
  code: string;
  status: number;
  constructor(message: string, code: string, status: number) {
    super(message);
    this.code = code;
    this.status = status;
  }
}

export interface SitePayload {
  content: SiteContent;
  offline: boolean;
  error?: string;
}

/**
 * Loads the site content from the API, falling back to the copy bundled at
 * build time. The site therefore still renders when the backend is stopped,
 * when it is serving an older build, or when the page is hosted statically.
 */
export async function fetchSiteContent(): Promise<SitePayload> {
  try {
    const res = await fetch(`${BASE}/site`, { headers: { Accept: "application/json" } });
    if (!res.ok) {
      let message = `The content API returned ${res.status}.`;
      try {
        const data = await res.json();
        if (data?.error?.message) message = data.error.message;
      } catch {
        /* keep default */
      }
      throw new ApiRequestError(message, "http_error", res.status);
    }
    const content = (await res.json()) as SiteContent;
    if (!content?.agents?.length) {
      throw new ApiRequestError("The content API returned an empty payload.", "empty_payload", res.status);
    }
    return { content, offline: false };
  } catch (error) {
    const message =
      error instanceof Error ? error.message : "The content API could not be reached.";
    if (bundled && Array.isArray(bundled.agents) && bundled.agents.length) {
      return { content: bundled as unknown as SiteContent, offline: true, error: message };
    }
    throw new ApiRequestError(message, "api_unreachable", 0);
  }
}
