import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { ChartData, ChartPoint } from "../../types/analysis";
import { AXIS_INK, GRID_STROKE, axisLabelStyle, axisTickStyle, colorForCategory } from "./theme";

interface Props {
  data: ChartData;
}

function pivotByMonth(points: ChartPoint[]): { rows: Record<string, string | number>[]; series: string[] } {
  // Recharts LineChart wants rows keyed by month, columns per series
  const months = new Set<string>();
  const seriesNames = new Set<string>();
  const byMonth: Record<string, Record<string, number | null>> = {};

  for (const p of points) {
    if (p.y == null) continue;
    const month = String(p.x);
    const series = p.series ?? "all";
    months.add(month);
    seriesNames.add(series);
    if (!byMonth[month]) byMonth[month] = {};
    byMonth[month][series] = p.y;
  }

  const sortedMonths = Array.from(months).sort();
  const rows = sortedMonths.map((m) => ({ x: m, ...(byMonth[m] ?? {}) }));
  return { rows, series: Array.from(seriesNames) };
}

export function TimeseriesChart({ data }: Props) {
  const { rows, series } = pivotByMonth(data.points);

  return (
    <ResponsiveContainer width="100%" height={420}>
      <LineChart data={rows} margin={{ top: 16, right: 24, bottom: 32, left: 24 }}>
        <CartesianGrid stroke={GRID_STROKE} strokeDasharray="3 3" opacity={0.3} />
        <XAxis
          dataKey="x"
          tick={axisTickStyle}
          axisLine={{ stroke: AXIS_INK }}
          tickLine={{ stroke: AXIS_INK }}
          label={{
            value: data.x_label,
            position: "insideBottom",
            offset: -10,
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
        />
        {series.map((s) => (
          <Line
            key={s}
            type="monotone"
            dataKey={s}
            stroke={colorForCategory(s)}
            strokeWidth={2}
            dot={{ r: 3 }}
            activeDot={{ r: 5 }}
            connectNulls
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}
