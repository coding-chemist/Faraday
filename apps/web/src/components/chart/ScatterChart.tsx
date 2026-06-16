import {
  CartesianGrid,
  Legend,
  ReferenceLine,
  Scatter,
  ScatterChart as RScatter,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  ZAxis,
} from "recharts";

import { faradayTokens } from "../../design/theme";
import type { ChartData, ChartPoint } from "../../types/analysis";
import {
  AXIS_INK,
  GRID_STROKE,
  axisLabelStyle,
  axisTickStyle,
  colorForCategory,
} from "./theme";

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

function ScatterTooltip({ active, payload }: { active?: boolean; payload?: any[] }) {
  if (!active || !payload?.length) return null;
  const p = payload[0]?.payload as { x: number; y: number; id?: string | null };
  const series = payload[0]?.name as string | undefined;
  const date = new Date(p.x).toISOString().slice(0, 10);
  const idShort = p.id ? p.id.replace(/^exp_/, "").slice(0, 6) : "—";

  return (
    <div
      style={{
        background: "#FFFFFF",
        border: `1px solid ${faradayTokens.color.forest[100]}`,
        borderRadius: 8,
        padding: "10px 14px",
        boxShadow: "0 4px 12px rgba(45, 106, 79, 0.10)",
        fontFamily: faradayTokens.font.body,
        fontSize: 13,
        color: faradayTokens.color.ink.primary,
        minWidth: 220,
      }}
    >
      <div style={{ fontWeight: 600, marginBottom: 4 }}>
        <span style={{ color: faradayTokens.color.ink.secondary, fontFamily: faradayTokens.font.mono, fontSize: 11 }}>
          ¶ {idShort}
        </span>
        {series && (
          <>
            <span style={{ color: faradayTokens.color.ink.tertiary, margin: "0 6px" }}>·</span>
            <span>{series}</span>
          </>
        )}
      </div>
      <div style={{ color: faradayTokens.color.ink.secondary, marginBottom: 6 }}>
        {p.y.toFixed(1)}% yield · {date}
      </div>
      <div
        style={{
          color: faradayTokens.color.forest[700],
          fontSize: 12,
          fontWeight: 500,
          display: "flex",
          alignItems: "center",
          gap: 4,
        }}
      >
        ▸ open experiment
      </div>
    </div>
  );
}

export function ScatterChart({ data }: Props) {
  const series = groupBySeries(data);

  return (
    <ResponsiveContainer width="100%" height={420}>
      <RScatter margin={{ top: 16, right: 24, bottom: 40, left: 24 }}>
        <CartesianGrid stroke={GRID_STROKE} strokeDasharray="3 3" opacity={0.45} />
        <XAxis
          type="number"
          dataKey="x"
          domain={["dataMin", "dataMax"]}
          tickFormatter={(v) => {
            const d = new Date(v);
            const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
            return `${months[d.getMonth()]} '${String(d.getFullYear()).slice(-2)}`;
          }}
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
        <ZAxis range={[140, 140]} />
        {data.threshold_y != null && (
          <ReferenceLine
            y={data.threshold_y}
            stroke={faradayTokens.color.ink.secondary}
            strokeDasharray="6 4"
            strokeWidth={1.4}
            label={{
              value: data.threshold_y_label ?? `${data.threshold_y}`,
              position: "right",
              fill: faradayTokens.color.ink.secondary,
              fontSize: 11,
              fontFamily: faradayTokens.font.mono,
            }}
          />
        )}
        <Tooltip content={<ScatterTooltip />} cursor={{ strokeDasharray: "3 3" }} />
        <Legend
          verticalAlign="top"
          align="right"
          height={28}
          iconType="circle"
          iconSize={10}
          wrapperStyle={{ fontFamily: faradayTokens.font.body, fontSize: 13 }}
        />
        {series.map((s) => (
          <Scatter
            key={s.name}
            name={s.name}
            data={s.points}
            fill={colorForCategory(s.name)}
            fillOpacity={0.85}
          />
        ))}
      </RScatter>
    </ResponsiveContainer>
  );
}
