// TypeScript mirror of engine/domain/analysis_result.py + query_spec.py.
// Kept in sync manually for v0.1. When the API surface grows, swap to OpenAPI codegen
// via openapi-typescript-codegen (Task #18).

export type ChartType =
  | "scatter"
  | "timeseries"
  | "bar"
  | "list"
  | "histogram"
  | "heatmap";

export interface ChartPoint {
  x: string | number;
  y?: number | null;
  color?: string | null;
  series?: string | null;
  count?: number | null;
  id?: string | null;
}

export interface HeatmapCell {
  x: string;
  y: string;
  value: number | null;
  count: number;
}

export interface HistogramBin {
  bin_low: number;
  bin_high: number;
  count: number;
}

export interface ChartData {
  chart_type: ChartType;
  x_label: string;
  y_label: string;
  points: ChartPoint[];
  heatmap_cells: HeatmapCell[];
  histogram_bins: HistogramBin[];
  threshold_y?: number | null;
  threshold_y_label?: string | null;
}

export interface SummaryCard {
  label: string;
  value: string;
  sublabel?: string | null;
}

export interface MatchedExperiment {
  id: string;
  title: string;
  type: string;
  status: string;
  yield_pct: number | null;
  started_at: string | null;
  catalyst?: string | null;
  solvent?: string | null;
}

export interface AnalysisResult {
  chart_data: ChartData;
  summary_cards: SummaryCard[];
  matched_experiments: MatchedExperiment[];
  total_matched: number;
  intent: string;
}
