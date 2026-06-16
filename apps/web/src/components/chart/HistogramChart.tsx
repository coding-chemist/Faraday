import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { ChartData } from "../../types/analysis";
import { AXIS_INK, GRID_STROKE, axisLabelStyle, axisTickStyle } from "./theme";
import { faradayTokens } from "../../design/theme";

interface Props {
  data: ChartData;
}

export function HistogramChart({ data }: Props) {
  const rows = data.histogram_bins.map((b) => ({
    label: `${b.bin_low.toFixed(1)}–${b.bin_high.toFixed(1)}`,
    count: b.count,
  }));

  return (
    <ResponsiveContainer width="100%" height={420}>
      <BarChart data={rows} margin={{ top: 16, right: 24, bottom: 56, left: 24 }} barCategoryGap={1}>
        <CartesianGrid stroke={GRID_STROKE} strokeDasharray="3 3" opacity={0.3} vertical={false} />
        <XAxis
          dataKey="label"
          tick={axisTickStyle}
          axisLine={{ stroke: AXIS_INK }}
          tickLine={{ stroke: AXIS_INK }}
          interval={0}
          angle={-30}
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
            value: data.y_label || "Count",
            angle: -90,
            position: "insideLeft",
            style: axisLabelStyle,
          }}
          allowDecimals={false}
        />
        <Tooltip
          contentStyle={{ background: "#FFFFFF", borderColor: GRID_STROKE, fontSize: 12 }}
        />
        <Bar dataKey="count" fill={faradayTokens.color.forest[700]} radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
