// Custom SVG heatmap — Recharts doesn't ship one.
//
// Grid of group_by × group_by_secondary cells. Cell color interpolates from cream
// (low value) to deep amber (high value). Empty cells (no data) render with a soft
// botanical-line cross-hatch. Hover shows value + count tooltip.

import { useMemo, useState } from "react";

import type { ChartData, HeatmapCell } from "../../types/analysis";
import { AXIS_INK, GRID_STROKE, axisLabelStyle, axisTickStyle, heatmapColor } from "./theme";
import { faradayTokens } from "../../design/theme";

interface Props {
  data: ChartData;
}

interface Layout {
  xCats: string[];
  yCats: string[];
  cellsByKey: Map<string, HeatmapCell>;
  vmin: number;
  vmax: number;
}

// Axes with no value-bearing cells just create empty columns/rows that push
// the real data off-screen. Same rule as the bar chart: drop "(unknown)"
// buckets when there's named data alongside them.
function filterAxis(axis: string[], hasValueOn: (cat: string) => boolean): string[] {
  const withData = axis.filter(hasValueOn);
  const named = withData.filter((c) => c !== "(unknown)");
  return named.length > 0 ? named : withData;
}

function buildLayout(cells: HeatmapCell[]): Layout {
  const cellsByKey = new Map(cells.map((c) => [`${c.x}|${c.y}`, c]));
  const hasValue = (cat: string, axis: "x" | "y") =>
    cells.some((c) => c[axis] === cat && c.value != null);

  const rawX = Array.from(new Set(cells.map((c) => c.x))).sort();
  const rawY = Array.from(new Set(cells.map((c) => c.y))).sort();
  const xCats = filterAxis(rawX, (cat) => hasValue(cat, "x"));
  const yCats = filterAxis(rawY, (cat) => hasValue(cat, "y"));

  const values = cells.map((c) => c.value).filter((v): v is number => v != null);
  const vmin = values.length ? Math.min(...values) : 0;
  const vmax = values.length ? Math.max(...values) : 1;
  return { xCats, yCats, cellsByKey, vmin, vmax };
}

// Truncate so column headers can't bleed into neighbors at 0° rotation.
// Full label is preserved in the SVG <title> for hover.
function shortLabel(s: string, max = 12): string {
  return s.length > max ? `${s.slice(0, max - 1)}…` : s;
}

export function HeatmapChart({ data }: Props) {
  const [hover, setHover] = useState<HeatmapCell | null>(null);
  const layout = useMemo(() => buildLayout(data.heatmap_cells), [data.heatmap_cells]);

  if (data.heatmap_cells.length === 0) {
    return (
      <div className="font-mono text-sm" style={{ color: AXIS_INK }}>
        No data to render.
      </div>
    );
  }

  const cellW = 80;
  const cellH = 56;
  const leftPad = 140;
  const topPad = 40;
  const bottomPad = 64;
  // Split into two SVGs side-by-side so the Y axis stays visible when the
  // cells region scrolls horizontally — same frozen-first-column pattern
  // Excel / Google Sheets use.
  const cellsRegionWidth = layout.xCats.length * cellW + 20;
  const height = topPad + layout.yCats.length * cellH + bottomPad;

  return (
    <div style={{ position: "relative", width: "100%" }}>
      <div style={{ display: "flex", alignItems: "stretch" }}>
        {/* Frozen left axis — Y tick labels + Y axis title. Sits outside the
            overflow container, so it doesn't move when the cells region
            scrolls horizontally. */}
        <svg
          width={leftPad}
          height={height}
          style={{ flexShrink: 0, display: "block" }}
          aria-hidden="false"
        >
          {layout.yCats.map((cat, j) => (
            <text
              key={cat}
              x={leftPad - 12}
              y={topPad + j * cellH + cellH / 2 + 4}
              textAnchor="end"
              style={axisTickStyle}
            >
              <title>{cat}</title>
              {shortLabel(cat, 16)}
            </text>
          ))}
          <text
            transform={`rotate(-90, 20, ${topPad + (layout.yCats.length * cellH) / 2})`}
            x={20}
            y={topPad + (layout.yCats.length * cellH) / 2}
            textAnchor="middle"
            style={axisLabelStyle}
          >
            {data.y_label}
          </text>
        </svg>

        {/* Scrollable cells region — X labels, cells, and X axis title.
            Only this band moves under the user's horizontal scroll. */}
        <div style={{ overflowX: "auto", flex: 1, minWidth: 0 }}>
          <svg width={cellsRegionWidth} height={height} style={{ display: "block" }}>
            {/* X axis tick labels — horizontal, truncated, full name on hover */}
            {layout.xCats.map((cat, i) => (
              <text
                key={cat}
                x={i * cellW + cellW / 2}
                y={topPad - 12}
                textAnchor="middle"
                style={axisTickStyle}
              >
                <title>{cat}</title>
                {shortLabel(cat, 12)}
              </text>
            ))}

            {/* Cells */}
            {layout.xCats.map((x, i) =>
              layout.yCats.map((y, j) => {
                const cell = layout.cellsByKey.get(`${x}|${y}`);
                const cx = i * cellW;
                const cy = topPad + j * cellH;
                const fill = cell?.value != null
                  ? heatmapColor(cell.value, layout.vmin, layout.vmax)
                  : faradayTokens.color.surface.muted;
                return (
                  <g key={`${x}|${y}`}>
                    <rect
                      x={cx}
                      y={cy}
                      width={cellW - 2}
                      height={cellH - 2}
                      fill={fill}
                      stroke={GRID_STROKE}
                      strokeWidth={cell ? 1 : 0.5}
                      strokeDasharray={cell ? "0" : "3 3"}
                      onMouseEnter={() => setHover(cell ?? null)}
                      onMouseLeave={() => setHover(null)}
                      style={{ cursor: cell ? "pointer" : "default" }}
                    />
                    {cell?.value != null && (
                      <text
                        x={cx + cellW / 2 - 1}
                        y={cy + cellH / 2 + 4}
                        textAnchor="middle"
                        style={{ ...axisTickStyle, fill: faradayTokens.color.ink.primary, fontWeight: 500 }}
                      >
                        {cell.value.toFixed(1)}
                      </text>
                    )}
                  </g>
                );
              })
            )}

            <text
              x={(layout.xCats.length * cellW) / 2}
              y={height - 20}
              textAnchor="middle"
              style={axisLabelStyle}
            >
              {data.x_label}
            </text>
          </svg>
        </div>
      </div>

      {hover && (
        <div
          className="font-mono text-xs"
          style={{
            position: "absolute",
            top: 8,
            right: 8,
            padding: "8px 12px",
            background: "#FFFFFF",
            border: `1px solid ${GRID_STROKE}`,
            borderRadius: 6,
          }}
        >
          <div>{hover.x} × {hover.y}</div>
          <div>value: {hover.value?.toFixed(2) ?? "—"}</div>
          <div>n = {hover.count}</div>
        </div>
      )}
    </div>
  );
}
