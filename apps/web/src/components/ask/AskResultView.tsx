import { Box, Typography } from "@mui/material";

import { faradayTokens } from "../../design/theme";
import type { AnalysisResult } from "../../types/analysis";
import { ChartRenderer } from "../chart/ChartRenderer";
import { ListView } from "../chart/ListView";
import { WatercolorPanel } from "../shell/WatercolorPanel";
import { SummaryCards } from "./SummaryCards";

interface Props {
  result: AnalysisResult;
}

export function AskResultView({ result }: Props) {
  const isListChart = result.chart_data.chart_type === "list";

  return (
    <Box component="section" aria-label="query result" sx={{ mt: 4 }}>
      {!isListChart && (
        <WatercolorPanel variant="subtle" seed={5} sx={{ mb: 3 }}>
          <Typography
            component="h2"
            sx={{
              fontFamily: faradayTokens.font.display,
              fontSize: { xs: 18, md: 20 },
              fontWeight: 600,
              color: faradayTokens.color.ink.primary,
              mb: 0.5,
            }}
          >
            {result.intent}
          </Typography>
          <Box sx={{ height: 8 }} />
          <ChartRenderer result={result} />
        </WatercolorPanel>
      )}

      <SummaryCards cards={result.summary_cards} />

      {result.matched_experiments.length > 0 && (
        <Box sx={{ mt: 5 }}>
          <Typography
            component="h3"
            sx={{
              fontSize: 16,
              fontWeight: 600,
              fontFamily: faradayTokens.font.display,
              mb: 2,
              color: faradayTokens.color.ink.primary,
            }}
          >
            {isListChart ? "Matched experiments" : "All matches"}
          </Typography>
          <ListView experiments={result.matched_experiments} />
        </Box>
      )}
    </Box>
  );
}
