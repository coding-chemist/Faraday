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
import { AXIS_INK, GRID_STROKE, SERIES_COLORS, axisLabelStyle, axisTickStyle } from "./theme";

interface Props {
  data: ChartData;
}

export function BarChart({ data }: Props) {
  const rows = data.points.map((p) => ({ x: String(p.x), y: p.y ?? 0, count: p.count }));

  return (
    <ResponsiveContainer width="100%" height={420}>
      <RBar data={rows} margin={{ top: 16, right: 24, bottom: 56, left: 24 }}>
        <CartesianGrid stroke={GRID_STROKE} strokeDasharray="3 3" opacity={0.3} vertical={false} />
        <XAxis
          dataKey="x"
          tick={axisTickStyle}
          axisLine={{ stroke: AXIS_INK }}
          tickLine={{ stroke: AXIS_INK }}
          interval={0}
          angle={-25}
          textAnchor="end"
          height={56}
          label={{
            value: data.x_label,
            position: "insideBottom",
            offset: -48,
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
