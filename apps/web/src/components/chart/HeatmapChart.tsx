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

function buildLayout(cells: HeatmapCell[]): Layout {
  const xCats = Array.from(new Set(cells.map((c) => c.x))).sort();
  const yCats = Array.from(new Set(cells.map((c) => c.y))).sort();
  const cellsByKey = new Map(cells.map((c) => [`${c.x}|${c.y}`, c]));
  const values = cells.map((c) => c.value).filter((v): v is number => v != null);
  const vmin = values.length ? Math.min(...values) : 0;
  const vmax = values.length ? Math.max(...values) : 1;
  return { xCats, yCats, cellsByKey, vmin, vmax };
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
  const width = leftPad + layout.xCats.length * cellW + 20;
  const height = topPad + layout.yCats.length * cellH + bottomPad;

  return (
    <div style={{ position: "relative", width: "100%", overflowX: "auto" }}>
      <svg width={width} height={height}>
        {/* X axis tick labels */}
        {layout.xCats.map((cat, i) => (
          <text
            key={cat}
            x={leftPad + i * cellW + cellW / 2}
            y={topPad - 12}
            textAnchor="middle"
            style={axisTickStyle}
          >
            {cat}
          </text>
        ))}

        {/* Y axis tick labels */}
        {layout.yCats.map((cat, j) => (
          <text
            key={cat}
            x={leftPad - 12}
            y={topPad + j * cellH + cellH / 2 + 4}
            textAnchor="end"
            style={axisTickStyle}
          >
            {cat}
          </text>
        ))}

        {/* Cells */}
        {layout.xCats.map((x, i) =>
          layout.yCats.map((y, j) => {
            const cell = layout.cellsByKey.get(`${x}|${y}`);
            const cx = leftPad + i * cellW;
            const cy = topPad + j * cellH;
            const fill = cell?.value != null ? heatmapColor(cell.value, layout.vmin, layout.vmax) : faradayTokens.color.surface.muted;
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

        {/* Axis labels */}
        <text
          x={leftPad + (layout.xCats.length * cellW) / 2}
          y={height - 20}
          textAnchor="middle"
          style={axisLabelStyle}
        >
          {data.x_label}
        </text>
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
