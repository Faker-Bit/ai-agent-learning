import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { lazy, Suspense } from "react";

import { Home } from "./pages/Home";

const WalkthroughPage = lazy(() =>
  import("./pages/WalkthroughPage").then((m) => ({ default: m.WalkthroughPage })),
);
const AgentPage = lazy(() => import("./pages/AgentPage").then((m) => ({ default: m.AgentPage })));

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, refetchOnWindowFocus: false, staleTime: 5 * 60_000 },
  },
});

function Loading() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-term-950">
      <div className="shimmer h-10 w-48 rounded-xl" />
    </div>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Suspense fallback={<Loading />}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/walkthrough/:walkthroughId" element={<WalkthroughPage />} />
            <Route path="/agent/:agentId" element={<AgentPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Suspense>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
