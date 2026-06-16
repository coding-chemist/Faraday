// Editorial chart palette — derived from productTokens (fresh greens).
//
// Three forest shades for the most common categorical case (the mockup has 3
// catalysts). Editorial accents (violet / amber) are reserved for emphasis —
// e.g. a highlighted outlier — not used by default series.

import { faradayTokens } from "../../design/theme";

export const SERIES_COLORS: readonly string[] = [
  faradayTokens.color.forest[700], // deep forest
  faradayTokens.color.forest[500], // mid forest
  faradayTokens.color.forest[300], // sage
  faradayTokens.color.forest[900], // deepest — fourth series
  faradayTokens.color.state.confirmed, // emerald — fifth
  faradayTokens.color.botanical.line, // moss — sixth
  faradayTokens.color.state.aiSuggest, // violet (editorial accent for emphasis)
  faradayTokens.color.state.warn,      // warm orange (used sparingly for outliers)
];

const _seriesAssignments = new Map<string, string>();

export function colorForCategory(category: string | null | undefined): string {
  if (!category) return faradayTokens.color.forest[700];
  const existing = _seriesAssignments.get(category);
  if (existing) return existing;
  const next = SERIES_COLORS[_seriesAssignments.size % SERIES_COLORS.length];
  _seriesAssignments.set(category, next);
  return next;
}

export function resetCategoryColors(): void {
  _seriesAssignments.clear();
}

export const CHART_BG = faradayTokens.color.surface.elevated;
export const GRID_STROKE = faradayTokens.color.forest[100];
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

// Heatmap color scale — mint -> deep forest (product UI register).
export function heatmapColor(value: number, vmin: number, vmax: number): string {
  if (vmax === vmin) return faradayTokens.color.forest[700];
  const t = Math.max(0, Math.min(1, (value - vmin) / (vmax - vmin)));
  // From #E6F2EA (forest 50, near-mint) -> #1B4332 (forest 900, deepest)
  const start = { r: 0xe6, g: 0xf2, b: 0xea };
  const end = { r: 0x1b, g: 0x43, b: 0x32 };
  const r = Math.round(start.r + (end.r - start.r) * t);
  const g = Math.round(start.g + (end.g - start.g) * t);
  const b = Math.round(start.b + (end.b - start.b) * t);
  return `rgb(${r}, ${g}, ${b})`;
}
