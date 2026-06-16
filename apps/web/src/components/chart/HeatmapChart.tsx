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
  const bottomPad = 56;
  const cellsRegionWidth = layout.xCats.length * cellW + 20;
  const cellsRegionHeight = layout.yCats.length * cellH;

  // One 2D scroll container with CSS sticky on each edge — Y labels stick
  // to the left, X labels stick to the top, X axis title sticks to the
  // bottom, and the two corner cells stick at their intersections. Cells
  // scroll freely in the middle when the matrix exceeds maxHeight.
  const STICKY_BG = faradayTokens.color.surface.base;

  return (
    <div style={{ position: "relative", width: "100%" }}>
      <div
        style={{
          maxHeight: 520,
          overflow: "auto",
          border: `1px solid ${GRID_STROKE}`,
          borderRadius: 8,
        }}
      >
        <div
          style={{
            display: "grid",
            gridTemplateColumns: `${leftPad}px ${cellsRegionWidth}px`,
            gridTemplateRows: `${topPad}px ${cellsRegionHeight}px ${bottomPad}px`,
            width: "max-content",
          }}
        >
          {/* TL corner — sits above both sticky edges */}
          <div
            style={{
              position: "sticky",
              top: 0,
              left: 0,
              zIndex: 4,
              background: STICKY_BG,
            }}
          />

          {/* Top: X tick labels — sticky top, scrolls horizontally with cells */}
          <div
            style={{
              position: "sticky",
              top: 0,
              zIndex: 3,
              background: STICKY_BG,
            }}
          >
            <svg width={cellsRegionWidth} height={topPad} style={{ display: "block" }}>
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
            </svg>
          </div>

          {/* Left: Y tick labels + Y axis title — sticky left */}
          <div
            style={{
              position: "sticky",
              left: 0,
              zIndex: 3,
              background: STICKY_BG,
            }}
          >
            <svg width={leftPad} height={cellsRegionHeight} style={{ display: "block" }}>
              {layout.yCats.map((cat, j) => (
                <text
                  key={cat}
                  x={leftPad - 12}
                  y={j * cellH + cellH / 2 + 4}
                  textAnchor="end"
                  style={axisTickStyle}
                >
                  <title>{cat}</title>
                  {shortLabel(cat, 16)}
                </text>
              ))}
              <text
                transform={`rotate(-90, 20, ${cellsRegionHeight / 2})`}
                x={20}
                y={cellsRegionHeight / 2}
                textAnchor="middle"
                style={axisLabelStyle}
              >
                {data.y_label}
              </text>
            </svg>
          </div>

          {/* Body: cells — scrolls in both directions */}
          <div>
            <svg width={cellsRegionWidth} height={cellsRegionHeight} style={{ display: "block" }}>
              {layout.xCats.map((x, i) =>
                layout.yCats.map((y, j) => {
                  const cell = layout.cellsByKey.get(`${x}|${y}`);
                  const cx = i * cellW;
                  const cy = j * cellH;
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
            </svg>
          </div>

          {/* BL corner — sticky bottom + left */}
          <div
            style={{
              position: "sticky",
              bottom: 0,
              left: 0,
              zIndex: 4,
              background: STICKY_BG,
            }}
          />

          {/* Bottom: X axis title — sticky bottom */}
          <div
            style={{
              position: "sticky",
              bottom: 0,
              zIndex: 3,
              background: STICKY_BG,
            }}
          >
            <svg width={cellsRegionWidth} height={bottomPad} style={{ display: "block" }}>
              <text
                x={(layout.xCats.length * cellW) / 2}
                y={bottomPad - 20}
                textAnchor="middle"
                style={axisLabelStyle}
              >
                {data.x_label}
              </text>
            </svg>
          </div>
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
