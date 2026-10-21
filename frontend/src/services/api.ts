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

export interface ResourcePayload {
  generated: string;
  categories: {
    id: string;
    short: string;
    title: string;
    blurb: string;
    count: number;
  }[];
  resources: {
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
  }[];
  total: number;
  matched: number;
}

/** Loads the GitHub research catalogue, filtered server-side. */
export async function fetchResources(
  query: string,
  category: string,
): Promise<ResourcePayload> {
  const params = new URLSearchParams();
  if (query.trim()) params.set("q", query.trim());
  if (category && category !== "all") params.set("category", category);
  const suffix = params.toString() ? `?${params}` : "";
  const res = await fetch(`${BASE}/site/resources${suffix}`, {
    headers: { Accept: "application/json" },
  });
  if (!res.ok) {
    throw new ApiRequestError(
      `The catalogue API returned ${res.status}. Start the backend with start.bat and retry.`,
      "http_error",
      res.status,
    );
  }
  return res.json() as Promise<ResourcePayload>;
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
