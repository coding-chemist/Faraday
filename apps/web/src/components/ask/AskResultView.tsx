import { Box, Typography } from "@mui/material";

import { faradayTokens } from "../../design/theme";
import type { AnalysisResult } from "../../types/analysis";
import { ChartRenderer } from "../chart/ChartRenderer";
import { ListView } from "../chart/ListView";
import { SummaryCards } from "./SummaryCards";

interface Props {
  result: AnalysisResult;
}

export function AskResultView({ result }: Props) {
  const isListChart = result.chart_data.chart_type === "list";

  return (
    <Box component="section" aria-label="query result" sx={{ mt: 8 }}>
      <Typography
        component="div"
        sx={{
          color: faradayTokens.color.ink.secondary,
          fontFamily: faradayTokens.font.mono,
          fontSize: 11,
          letterSpacing: "0.08em",
          textTransform: "uppercase",
          mb: 1,
        }}
      >
        Showing
      </Typography>
      <Typography
        component="h2"
        sx={{
          fontSize: { xs: 22, md: 28 },
          fontFamily: faradayTokens.font.display,
          fontWeight: 500,
          color: faradayTokens.color.ink.primary,
          mb: 5,
          lineHeight: 1.25,
        }}
      >
        {result.intent}
      </Typography>

      <SummaryCards cards={result.summary_cards} />

      {!isListChart && (
        <Box
          sx={{
            mt: 6,
            background: faradayTokens.color.surface.elevated,
            border: `1px solid ${faradayTokens.color.forest[100]}`,
            borderRadius: 2,
            p: { xs: 2, md: 4 },
          }}
        >
          <ChartRenderer result={result} />
        </Box>
      )}

      {result.matched_experiments.length > 0 && (
        <Box sx={{ mt: 6 }}>
          <Typography
            component="h3"
            sx={{
              fontSize: 18,
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
