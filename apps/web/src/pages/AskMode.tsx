import { Alert, Box, Container, Typography } from "@mui/material";
import { useState } from "react";
import { Link as RouterLink } from "react-router-dom";

import { AskResultView } from "../components/ask/AskResultView";
import { QueryInput } from "../components/ask/QueryInput";
import { faradayTokens } from "../design/theme";
import { ApiError, ask } from "../lib/api";
import type { AnalysisResult } from "../types/analysis";

export function AskMode() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (nlQuery: string) => {
    setQuery(nlQuery);
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

  return (
    <Box className="min-h-screen bg-surface-warm">
      <Container maxWidth="lg" sx={{ pt: 8, pb: 12 }}>
        <Box sx={{ textAlign: "center", mb: 5 }}>
          <Box className="font-mono" sx={{ fontSize: 12, mb: 4 }}>
            <RouterLink to="/" style={{ color: faradayTokens.color.accent.faraday }}>
              ← back to landing
            </RouterLink>
          </Box>
          <Typography
            sx={{
              fontSize: { xs: 36, md: 56 },
              fontFamily: faradayTokens.font.display,
              fontWeight: 600,
              color: faradayTokens.color.ink.primary,
              mb: 1,
              lineHeight: 1.05,
            }}
          >
            Lab Memory
          </Typography>
          <Typography
            sx={{
              fontSize: { xs: 16, md: 18 },
              fontStyle: "italic",
              color: faradayTokens.color.ink.secondary,
            }}
          >
            Ask anything about your experiments.
          </Typography>
        </Box>

        <QueryInput onSubmit={handleSubmit} disabled={loading} initialValue={query} />

        {loading && (
          <Box sx={{ textAlign: "center", mt: 8 }}>
            <Typography
              sx={{
                color: faradayTokens.color.ink.secondary,
                fontStyle: "italic",
                fontSize: 15,
              }}
            >
              searching the lab memory…
            </Typography>
          </Box>
        )}

        {error && !loading && (
          <Alert
            severity="error"
            sx={{
              mt: 5,
              maxWidth: 760,
              mx: "auto",
              background: "#FDF1EC",
              borderRadius: 2,
              "& .MuiAlert-message": { fontFamily: faradayTokens.font.body },
            }}
            onClose={() => setError(null)}
          >
            {error}
          </Alert>
        )}

        {result && !loading && <AskResultView result={result} />}
      </Container>
    </Box>
  );
}
