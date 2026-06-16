import {
  CartesianGrid,
  Scatter,
  ScatterChart as RScatter,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  ZAxis,
} from "recharts";

import type { ChartData } from "../../types/analysis";
import { AXIS_INK, GRID_STROKE, axisLabelStyle, axisTickStyle, colorForCategory } from "./theme";

interface Props {
  data: ChartData;
}

interface SeriesGroup {
  name: string;
  points: { x: number; y: number; id?: string | null }[];
}

function groupBySeries(data: ChartData): SeriesGroup[] {
  const groups = new Map<string, SeriesGroup>();
  for (const p of data.points) {
    if (p.y == null) continue;
    const key = p.color ?? "all";
    const x = typeof p.x === "string" ? new Date(p.x).getTime() : Number(p.x);
    if (!groups.has(key)) {
      groups.set(key, { name: key, points: [] });
    }
    groups.get(key)!.points.push({ x, y: p.y, id: p.id });
  }
  return Array.from(groups.values());
}

export function ScatterChart({ data }: Props) {
  const series = groupBySeries(data);

  return (
    <ResponsiveContainer width="100%" height={420}>
      <RScatter margin={{ top: 16, right: 24, bottom: 32, left: 24 }}>
        <CartesianGrid stroke={GRID_STROKE} strokeDasharray="3 3" opacity={0.3} />
        <XAxis
          type="number"
          dataKey="x"
          domain={["dataMin", "dataMax"]}
          tickFormatter={(v) => new Date(v).toISOString().slice(0, 10)}
          tick={axisTickStyle}
          axisLine={{ stroke: AXIS_INK }}
          tickLine={{ stroke: AXIS_INK }}
          label={{
            value: data.x_label || "Date",
            position: "insideBottom",
            offset: -10,
            style: axisLabelStyle,
          }}
        />
        <YAxis
          type="number"
          dataKey="y"
          tick={axisTickStyle}
          axisLine={{ stroke: AXIS_INK }}
          tickLine={{ stroke: AXIS_INK }}
          label={{
            value: data.y_label || "",
            angle: -90,
            position: "insideLeft",
            style: axisLabelStyle,
          }}
        />
        <ZAxis range={[80, 80]} />
        <Tooltip
          cursor={{ strokeDasharray: "3 3" }}
          contentStyle={{ background: "#FFFFFF", borderColor: GRID_STROKE, fontSize: 12 }}
          labelFormatter={(v) => new Date(v as number).toISOString().slice(0, 10)}
        />
        {series.map((s) => (
          <Scatter key={s.name} name={s.name} data={s.points} fill={colorForCategory(s.name)} />
        ))}
      </RScatter>
    </ResponsiveContainer>
  );
}
