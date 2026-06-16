// Registry-as-map dispatch — adding a chart_type = one new component + one map entry.
//
// Mirrors the backend's AnalyzerRegistry pattern. Chart_type names are the SAME
// strings on both sides (TypeScript ChartType union matches the Pydantic StrEnum).

import { ComponentType } from "react";

import type { AnalysisResult, ChartData, ChartType } from "../../types/analysis";
import { BarChart } from "./BarChart";
import { HeatmapChart } from "./HeatmapChart";
import { HistogramChart } from "./HistogramChart";
import { ListView } from "./ListView";
import { ScatterChart } from "./ScatterChart";
import { TimeseriesChart } from "./TimeseriesChart";

interface ChartProps {
  data: ChartData;
}

// Charts that take a ChartData. ListView is special-cased (it takes experiments).
const CHART_COMPONENTS: Record<Exclude<ChartType, "list">, ComponentType<ChartProps>> = {
  scatter: ScatterChart,
  timeseries: TimeseriesChart,
  bar: BarChart,
  histogram: HistogramChart,
  heatmap: HeatmapChart,
};

interface RendererProps {
  result: AnalysisResult;
}

export function ChartRenderer({ result }: RendererProps) {
  if (result.chart_data.chart_type === "list") {
    return <ListView experiments={result.matched_experiments} />;
  }
  const Component = CHART_COMPONENTS[result.chart_data.chart_type];
  if (!Component) {
    return (
      <div className="font-mono text-sm">
        Unknown chart type: {result.chart_data.chart_type}
      </div>
    );
  }
  return <Component data={result.chart_data} />;
}
