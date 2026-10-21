import { useQuery } from "@tanstack/react-query";

import { fetchSiteContent } from "../services/api";

export function useSiteContent() {
  return useQuery({
    queryKey: ["site"],
    queryFn: fetchSiteContent,
    staleTime: 5 * 60_000,
  });
}
