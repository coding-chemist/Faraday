import { Alert, Box, Button, Typography } from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";
import { useState } from "react";

import { AskResultView } from "../components/ask/AskResultView";
import { LoadingSkeleton } from "../components/ask/LoadingSkeleton";
import { QueryInput } from "../components/ask/QueryInput";
import { SuggestedQueries } from "../components/ask/SuggestedQueries";
import { WatchTeaser } from "../components/ask/WatchTeaser";
import { AppShell, WatercolorPanel } from "../components/shell";
import { faradayTokens } from "../design/theme";
import { ApiError, ask } from "../lib/api";
import type { AnalysisResult } from "../types/analysis";

export function AskMode() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastQuery, setLastQuery] = useState<string | null>(null);

  const handleSubmit = async (nlQuery: string) => {
    setQuery(nlQuery);
    setLastQuery(nlQuery);
    setLoading(true);
    setError(null);
    try {
      const data = await ask(nlQuery);
      setResult(data);
    } catch (err) {
      const message =
        err instanceof ApiError
          ? err.detail
          : err instanceof Error
            ? err.message
            : "Something went wrong";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const handleRetry = () => {
    if (lastQuery) handleSubmit(lastQuery);
  };

  const showEmptyState = result && !loading && result.total_matched === 0;
  const showResult = result && !loading && result.total_matched > 0;

  return (
    <AppShell
      crumbs={[{ label: "Lab memory" }, { label: "Ask" }]}
      rightRail={<WatchTeaser />}
    >
      <Box sx={{ maxWidth: 1040, mx: "auto" }}>
        <WatercolorPanel variant="subtle" seed={3}>
          <QueryInput onSubmit={handleSubmit} disabled={loading} initialValue={query} />
          {!result && !loading && !error && (
            <Box sx={{ mt: 2 }}>
              <Typography
                sx={{
                  fontSize: 13,
                  color: faradayTokens.color.ink.secondary,
                  fontStyle: "italic",
                  textAlign: "center",
                }}
              >
                Try: 'find experiments where I used Pd(OAc)₂' or 'average yield for recrystallization in ethanol'
              </Typography>
            </Box>
          )}
        </WatercolorPanel>

        {!result && !loading && !error && (
          <Box sx={{ mt: 3 }}>
            <SuggestedQueries onSelect={handleSubmit} disabled={loading} />
          </Box>
        )}

        {loading && (
          <Box sx={{ mt: 4 }} aria-live="polite" aria-busy="true">
            <LoadingSkeleton />
          </Box>
        )}

        {error && !loading && (
          <Box sx={{ mt: 4, maxWidth: 760, mx: "auto" }} role="alert">
            <Alert
              severity="error"
              variant="outlined"
              sx={{
                background: "#FDF1EC",
                borderRadius: 2,
                border: `1px solid #F5C2A7`,
                color: faradayTokens.color.ink.primary,
                "& .MuiAlert-icon": { color: faradayTokens.color.state.error },
                "& .MuiAlert-message": {
                  fontFamily: faradayTokens.font.body,
                  width: "100%",
                },
              }}
            >
              <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 2 }}>
                <span>{error}</span>
                {lastQuery && (
                  <Button
                    size="small"
                    onClick={handleRetry}
                    startIcon={<RefreshIcon />}
                    sx={{
                      color: faradayTokens.color.forest[700],
                      whiteSpace: "nowrap",
                      "&:hover": { background: faradayTokens.color.forest[50] },
                    }}
                  >
                    Try again
                  </Button>
                )}
              </Box>
            </Alert>
          </Box>
        )}

        {showEmptyState && (
          <Box
            className="faraday-fade-in"
            sx={{
              mt: 4,
              textAlign: "center",
              maxWidth: 560,
              mx: "auto",
              p: 4,
              background: faradayTokens.color.surface.muted,
              borderRadius: 2,
            }}
          >
            <Typography
              sx={{
                fontFamily: faradayTokens.font.mono,
                fontSize: 11,
                letterSpacing: "0.08em",
                textTransform: "uppercase",
                color: faradayTokens.color.ink.secondary,
                mb: 1,
              }}
            >
              No matches
            </Typography>
            <Typography
              sx={{
                fontSize: 20,
                fontFamily: faradayTokens.font.display,
                fontWeight: 500,
                color: faradayTokens.color.ink.primary,
                mb: 2,
                lineHeight: 1.3,
              }}
            >
              The lab doesn't remember anything like that.
            </Typography>
            <Typography
              sx={{
                fontSize: 14,
                color: faradayTokens.color.ink.secondary,
                fontStyle: "italic",
                mb: 3,
              }}
            >
              {result?.intent && `Interpreted as: ${result.intent}`}
            </Typography>
            <SuggestedQueries onSelect={handleSubmit} disabled={loading} compact />
          </Box>
        )}

        {showResult && (
          <Box className="faraday-fade-in">
            <AskResultView result={result!} />
          </Box>
        )}
      </Box>
    </AppShell>
  );
}
