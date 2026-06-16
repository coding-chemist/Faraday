import {
  Bar,
  BarChart as RBar,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { ChartData } from "../../types/analysis";
import { humanize } from "../../lib/format";
import { AXIS_INK, GRID_STROKE, SERIES_COLORS, axisLabelStyle, axisTickStyle } from "./theme";

interface Props {
  data: ChartData;
}

export function BarChart({ data }: Props) {
  // Filter out (unknown) buckets when there's real data to show beside them —
  // they're a hint that some rows lack the grouping field, not actual content.
  const filtered = data.points.filter((p) => p.x !== "(unknown)");
  const rows = (filtered.length > 0 ? filtered : data.points).map((p) => ({
    x: humanize(String(p.x)),
    y: p.y ?? 0,
    count: p.count,
  }));

  // Truncate long category names so the 0° x-axis stays legible at any width.
  // Full name remains in the tooltip.
  const tickFormatter = (value: string) =>
    value.length > 14 ? `${value.slice(0, 13)}…` : value;

  return (
    <ResponsiveContainer width="100%" height={420}>
      <RBar data={rows} margin={{ top: 16, right: 24, bottom: 40, left: 24 }}>
        <CartesianGrid stroke={GRID_STROKE} strokeDasharray="3 3" opacity={0.3} vertical={false} />
        <XAxis
          dataKey="x"
          tick={axisTickStyle}
          tickFormatter={tickFormatter}
          axisLine={{ stroke: AXIS_INK }}
          tickLine={{ stroke: AXIS_INK }}
          interval={0}
          angle={0}
          textAnchor="middle"
          height={36}
          label={{
            value: data.x_label,
            position: "insideBottom",
            offset: -20,
            style: axisLabelStyle,
          }}
        />
        <YAxis
          tick={axisTickStyle}
          axisLine={{ stroke: AXIS_INK }}
          tickLine={{ stroke: AXIS_INK }}
          label={{
            value: data.y_label,
            angle: -90,
            position: "insideLeft",
            style: axisLabelStyle,
          }}
        />
        <Tooltip
          contentStyle={{ background: "#FFFFFF", borderColor: GRID_STROKE, fontSize: 12 }}
          // Default Recharts cursor is a full-height grey bar that visually
          // suggests the actual bar reaches the top of the chart — misleading.
          // Use a soft forest tint that just frames the column instead.
          cursor={{ fill: "rgba(45, 106, 79, 0.06)" }}
          formatter={(value: number, _name, { payload }) => [
            payload?.count != null ? `${value} (n=${payload.count})` : value,
            data.y_label,
          ]}
        />
        <Bar dataKey="y" radius={[6, 6, 0, 0]}>
          {rows.map((_, i) => (
            <Cell key={i} fill={SERIES_COLORS[i % SERIES_COLORS.length]} />
          ))}
        </Bar>
      </RBar>
    </ResponsiveContainer>
  );
}
