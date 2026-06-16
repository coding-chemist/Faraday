// Thin fetch wrapper for the Faraday API.
// Routes through Vite's /api proxy during dev (-> :8000); production reads VITE_API_BASE_URL.

import type { AnalysisResult } from "../types/analysis";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api";

export class ApiError extends Error {
  constructor(public status: number, public detail: string) {
    super(detail);
    this.name = "ApiError";
  }
}

export async function ask(query: string): Promise<AnalysisResult> {
  const response = await fetch(`${API_BASE}/memory/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    let detail = `${response.status} ${response.statusText}`;
    try {
      const body = await response.json();
      if (body?.detail) detail = body.detail;
    } catch {
      // body wasn't JSON — keep the default detail
    }
    throw new ApiError(response.status, detail);
  }

  return response.json();
}
