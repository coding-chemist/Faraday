import { Box, Stack, Typography } from "@mui/material";

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
  const matchedCount = result.matched_experiments.length;

  return (
    <Box component="section" aria-label="query result" sx={{ mt: 4 }}>
      {!isListChart && (
        <WatercolorPanel variant="subtle" seed={5} sx={{ mb: 3 }}>
          <Typography
            component="h2"
            sx={{
              fontFamily: faradayTokens.font.mono,
              fontSize: { xs: 15, md: 16 },
              fontWeight: 600,
              letterSpacing: "-0.005em",
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

      {matchedCount > 0 && (
        <Box sx={{ mt: 5 }}>
          <Stack
            direction="row"
            spacing={1.5}
            alignItems="baseline"
            sx={{
              mb: 2,
              pb: 1,
              borderBottom: `1px solid ${faradayTokens.color.forest[100]}`,
            }}
          >
            <Typography
              component="h3"
              sx={{
                fontFamily: faradayTokens.font.mono,
                fontSize: 12,
                fontWeight: 600,
                letterSpacing: "0.1em",
                textTransform: "uppercase",
                color: faradayTokens.color.forest[700],
              }}
            >
              From the notebook
            </Typography>
            <Typography
              component="span"
              sx={{
                fontFamily: faradayTokens.font.mono,
                fontSize: 11,
                color: faradayTokens.color.ink.tertiary,
                fontFeatureSettings: '"tnum" 1',
              }}
            >
              {matchedCount} {matchedCount === 1 ? "entry" : "entries"}
            </Typography>
          </Stack>
          <ListView experiments={result.matched_experiments} />
        </Box>
      )}
    </Box>
  );
}
