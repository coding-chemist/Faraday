// Visual smoke test for the 6 chart types — sample data hand-crafted to exercise each shape.
// Hit /charts-demo after `make web` to verify the editorial palette + Recharts wiring
// without needing the API or Ollama running.

import { Box, Container, Divider, Typography } from "@mui/material";
import { Link as RouterLink } from "react-router-dom";

import { ChartRenderer } from "../components/chart";
import type { AnalysisResult } from "../types/analysis";

const SAMPLE_MATCHED = [
  { id: "exp_a1", title: "Suzuki coupling of 4-bromoanisole", type: "suzuki_coupling", status: "completed", yield_pct: 85.3, started_at: "2026-03-12T09:14:00", catalyst: "Pd(OAc)2", solvent: "toluene" },
  { id: "exp_a2", title: "Suzuki coupling of methyl 4-bromobenzoate", type: "suzuki_coupling", status: "completed", yield_pct: 72.1, started_at: "2026-03-22T10:30:00", catalyst: "Pd(OAc)2", solvent: "dioxane" },
  { id: "exp_a3", title: "Suzuki coupling of 4-bromobenzonitrile", type: "suzuki_coupling", status: "failed", yield_pct: null, started_at: "2026-04-05T11:00:00", catalyst: "Pd(PPh3)4", solvent: "toluene" },
  { id: "exp_a4", title: "Amide coupling of benzoic acid + piperidine", type: "amide_coupling", status: "in_progress", yield_pct: null, started_at: "2026-05-01T14:20:00", catalyst: "HATU", solvent: "DMF" },
];

const scatter: AnalysisResult = {
  chart_data: {
    chart_type: "scatter",
    x_label: "Date",
    y_label: "Yield %",
    points: [
      { x: "2026-01-15", y: 85, color: "Pd(OAc)2", id: "e1" },
      { x: "2026-02-10", y: 72, color: "Pd(OAc)2", id: "e2" },
      { x: "2026-02-28", y: 45, color: "Pd(PPh3)4", id: "e3" },
      { x: "2026-03-15", y: 92, color: "Pd(dppf)Cl2", id: "e4" },
      { x: "2026-04-02", y: 68, color: "Pd(OAc)2", id: "e5" },
      { x: "2026-04-20", y: 30, color: "Pd(PPh3)4", id: "e6" },
      { x: "2026-05-10", y: 88, color: "Pd(dppf)Cl2", id: "e7" },
      { x: "2026-05-28", y: 78, color: "Pd(OAc)2", id: "e8" },
    ],
    heatmap_cells: [],
    histogram_bins: [],
  },
  summary_cards: [],
  matched_experiments: [],
  total_matched: 8,
  intent: "Yields over time, colored by catalyst",
};

const bar: AnalysisResult = {
  chart_data: {
    chart_type: "bar",
    x_label: "Catalyst",
    y_label: "Mean Yield %",
    points: [
      { x: "Pd(dppf)Cl2", y: 90.0, count: 2 },
      { x: "Pd(OAc)2", y: 75.0, count: 3 },
      { x: "Pd(PPh3)4", y: 37.5, count: 2 },
    ],
    heatmap_cells: [],
    histogram_bins: [],
  },
  summary_cards: [],
  matched_experiments: [],
  total_matched: 7,
  intent: "Mean yield by catalyst",
};

const timeseries: AnalysisResult = {
  chart_data: {
    chart_type: "timeseries",
    x_label: "Month",
    y_label: "Mean Yield %",
    points: [
      { x: "2026-01", y: 78.5, series: "Pd(OAc)2", count: 4 },
      { x: "2026-02", y: 71.2, series: "Pd(OAc)2", count: 6 },
      { x: "2026-03", y: 82.0, series: "Pd(OAc)2", count: 5 },
      { x: "2026-04", y: 79.1, series: "Pd(OAc)2", count: 7 },
      { x: "2026-01", y: 65.0, series: "Pd(PPh3)4", count: 3 },
      { x: "2026-02", y: 58.4, series: "Pd(PPh3)4", count: 4 },
      { x: "2026-03", y: 62.1, series: "Pd(PPh3)4", count: 3 },
      { x: "2026-04", y: 55.0, series: "Pd(PPh3)4", count: 2 },
    ],
    heatmap_cells: [],
    histogram_bins: [],
  },
  summary_cards: [],
  matched_experiments: [],
  total_matched: 34,
  intent: "Monthly yield trend by catalyst",
};

const histogram: AnalysisResult = {
  chart_data: {
    chart_type: "histogram",
    x_label: "Yield %",
    y_label: "Count",
    points: [],
    heatmap_cells: [],
    histogram_bins: [
      { bin_low: 10, bin_high: 19, count: 2 },
      { bin_low: 19, bin_high: 28, count: 4 },
      { bin_low: 28, bin_high: 37, count: 7 },
      { bin_low: 37, bin_high: 46, count: 12 },
      { bin_low: 46, bin_high: 55, count: 18 },
      { bin_low: 55, bin_high: 64, count: 28 },
      { bin_low: 64, bin_high: 73, count: 42 },
      { bin_low: 73, bin_high: 82, count: 51 },
      { bin_low: 82, bin_high: 91, count: 32 },
      { bin_low: 91, bin_high: 99, count: 14 },
    ],
  },
  summary_cards: [],
  matched_experiments: [],
  total_matched: 210,
  intent: "Yield distribution across all reactions",
};

const heatmap: AnalysisResult = {
  chart_data: {
    chart_type: "heatmap",
    x_label: "Catalyst",
    y_label: "Solvent",
    points: [],
    histogram_bins: [],
    heatmap_cells: [
      { x: "Pd(OAc)2", y: "toluene", value: 76.5, count: 6 },
      { x: "Pd(OAc)2", y: "dioxane", value: 81.2, count: 9 },
      { x: "Pd(OAc)2", y: "DMF", value: 64.8, count: 4 },
      { x: "Pd(PPh3)4", y: "toluene", value: 52.0, count: 3 },
      { x: "Pd(PPh3)4", y: "dioxane", value: 47.5, count: 5 },
      { x: "Pd(PPh3)4", y: "DMF", value: null, count: 0 },
      { x: "Pd(dppf)Cl2", y: "toluene", value: 88.0, count: 4 },
      { x: "Pd(dppf)Cl2", y: "dioxane", value: 91.4, count: 6 },
      { x: "Pd(dppf)Cl2", y: "DMF", value: 79.5, count: 2 },
    ],
  },
  summary_cards: [],
  matched_experiments: [],
  total_matched: 39,
  intent: "Mean yield as heatmap of catalyst × solvent",
};

const list: AnalysisResult = {
  chart_data: {
    chart_type: "list",
    x_label: "",
    y_label: "",
    points: [],
    heatmap_cells: [],
    histogram_bins: [],
  },
  summary_cards: [],
  matched_experiments: SAMPLE_MATCHED,
  total_matched: SAMPLE_MATCHED.length,
  intent: "Latest experiments",
};

interface SectionProps {
  title: string;
  intent: string;
  children: React.ReactNode;
}

function Section({ title, intent, children }: SectionProps) {
  return (
    <Box sx={{ mb: 8 }}>
      <Typography
        variant="h2"
        className="font-display text-ink-primary"
        sx={{ fontSize: 28, fontWeight: 600, mb: 0.5 }}
      >
        {title}
      </Typography>
      <Typography
        className="font-body italic"
        sx={{ fontSize: 14, color: "#5C6360", mb: 3 }}
      >
        {intent}
      </Typography>
      <Box sx={{ background: "#FFFFFF", borderRadius: 2, p: 3, border: "1px solid #E5E2DA" }}>
        {children}
      </Box>
    </Box>
  );
}

export function ChartsDemo() {
  return (
    <Box className="min-h-screen bg-surface-warm">
      <Container maxWidth="lg" sx={{ py: 6 }}>
        <Typography
          variant="h1"
          className="font-display"
          sx={{ fontSize: 40, fontWeight: 600, mb: 1 }}
        >
          Chart components
        </Typography>
        <Typography
          className="font-body italic"
          sx={{ fontSize: 16, color: "#5C6360", mb: 1 }}
        >
          Each chart type rendered with sample data. Editorial palette per spec §3.0.4.
        </Typography>
        <Box className="font-mono" sx={{ fontSize: 12, mb: 5 }}>
          <RouterLink to="/" style={{ color: "#B45309" }}>
            ← back to landing
          </RouterLink>
        </Box>

        <Divider sx={{ mb: 5 }} />

        <Section title="Scatter" intent={scatter.intent}>
          <ChartRenderer result={scatter} />
        </Section>

        <Section title="Bar" intent={bar.intent}>
          <ChartRenderer result={bar} />
        </Section>

        <Section title="Timeseries" intent={timeseries.intent}>
          <ChartRenderer result={timeseries} />
        </Section>

        <Section title="Histogram" intent={histogram.intent}>
          <ChartRenderer result={histogram} />
        </Section>

        <Section title="Heatmap" intent={heatmap.intent}>
          <ChartRenderer result={heatmap} />
        </Section>

        <Section title="List" intent={list.intent}>
          <ChartRenderer result={list} />
        </Section>
      </Container>
    </Box>
  );
}
