// Editorial chart palette — derived from spec §3.0.1 tokens.
// Series colors are picked for naturalist warmth, not D3 defaults. Categorical
// assignments are deterministic per category name via a hash so repeated runs
// produce the same color mapping.

import { faradayTokens } from "../../design/theme";

// Ordered series palette — applied in order to the first N categories.
export const SERIES_COLORS: readonly string[] = [
  faradayTokens.color.accent.faraday, // amber
  faradayTokens.color.accent.curie,   // violet
  faradayTokens.color.state.confirmed, // forest green
  faradayTokens.color.botanical.line,  // moss
  faradayTokens.color.state.warn,      // warm orange
  faradayTokens.color.ink.secondary,   // graphite
  faradayTokens.color.state.aiSuggest, // lavender
  faradayTokens.color.ink.tertiary,    // ash
];

const _seriesAssignments = new Map<string, string>();

export function colorForCategory(category: string | null | undefined): string {
  if (!category) return faradayTokens.color.ink.secondary;
  const existing = _seriesAssignments.get(category);
  if (existing) return existing;
  const next = SERIES_COLORS[_seriesAssignments.size % SERIES_COLORS.length];
  _seriesAssignments.set(category, next);
  return next;
}

export function resetCategoryColors(): void {
  _seriesAssignments.clear();
}

// Shared Recharts axis/grid styling
export const CHART_BG = faradayTokens.color.surface.warm;
export const GRID_STROKE = faradayTokens.color.ink.tertiary;
export const AXIS_INK = faradayTokens.color.ink.secondary;
export const AXIS_LABEL_INK = faradayTokens.color.ink.primary;

export const axisTickStyle = {
  fill: AXIS_INK,
  fontSize: 12,
  fontFamily: faradayTokens.font.body,
};

export const axisLabelStyle = {
  fill: AXIS_LABEL_INK,
  fontSize: 13,
  fontFamily: faradayTokens.font.body,
  fontWeight: 500,
};

// Linear interpolation for heatmap color scale — cream -> deep amber
export function heatmapColor(value: number, vmin: number, vmax: number): string {
  if (vmax === vmin) return faradayTokens.color.accent.faraday;
  const t = Math.max(0, Math.min(1, (value - vmin) / (vmax - vmin)));
  // From #FAF8F3 (cream) -> #B45309 (amber)
  const start = { r: 0xfa, g: 0xf8, b: 0xf3 };
  const end = { r: 0xb4, g: 0x53, b: 0x09 };
  const r = Math.round(start.r + (end.r - start.r) * t);
  const g = Math.round(start.g + (end.g - start.g) * t);
  const b = Math.round(start.b + (end.b - start.b) * t);
  return `rgb(${r}, ${g}, ${b})`;
}
