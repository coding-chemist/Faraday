// Minimal placeholder landing — full marketing-grade rebuild lives in Task #25.
// What's here is the wiring: clear CTA into Lab Memory Ask, plus three
// example queries that deep-link via /memory/ask?q=...&run=1 so the
// chemist lands on a populated Ask page on click (handoff works).

import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import { Box, Button, Container, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import { Link as RouterLink } from "react-router-dom";

import { faradayTokens } from "../design/theme";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api";

interface HealthResponse {
  status: string;
  env: string;
  uptime_s: number;
}

const EXAMPLE_QUERIES: readonly string[] = [
  "Show Suzuki couplings with yield below 70% in the last six months",
  "Compare HATU vs EDC amide coupling yields",
  "Yield by catalyst across solvents",
];

function askLink(query: string): string {
  return `/memory/ask?q=${encodeURIComponent(query)}&run=1`;
}

export function Landing() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [warming, setWarming] = useState(false);

  useEffect(() => {
    const t = setTimeout(() => setWarming(true), 3000);
    fetch(`${API_BASE}/health`)
      .then((r) => r.json())
      .then((data) => {
        clearTimeout(t);
        setWarming(false);
        setHealth(data);
      })
      .catch(() => {
        clearTimeout(t);
        setWarming(false);
      });
    return () => clearTimeout(t);
  }, []);

  return (
    <Box
      sx={{
        minHeight: "100vh",
        background: faradayTokens.color.surface.base,
      }}
    >
      <Container maxWidth="md" sx={{ pt: { xs: 8, md: 12 }, pb: 12 }}>
        <Typography
          component="h1"
          sx={{
            fontFamily: faradayTokens.font.display,
            fontSize: { xs: 48, md: 80 },
            fontWeight: 600,
            lineHeight: 1.0,
            color: faradayTokens.color.ink.primary,
            mb: 1.5,
          }}
        >
          Your lab's{" "}
          <Box
            component="span"
            sx={{
              fontStyle: "italic",
              color: faradayTokens.color.forest[700],
            }}
          >
            memory
          </Box>
          .
        </Typography>

        <Typography
          sx={{
            fontFamily: faradayTokens.font.body,
            fontSize: { xs: 17, md: 19 },
            color: faradayTokens.color.ink.secondary,
            fontStyle: "italic",
            mb: 5,
          }}
        >
          Record like Faraday. Search like Google.
        </Typography>

        <Button
          component={RouterLink}
          to="/memory/ask"
          variant="contained"
          endIcon={<ArrowForwardIcon />}
          sx={{
            background: faradayTokens.color.forest[700],
            color: "#FFFFFF",
            borderRadius: 999,
            px: 4,
            py: 1.5,
            fontSize: 16,
            fontWeight: 500,
            textTransform: "none",
            boxShadow: "none",
            "&:hover": {
              background: faradayTokens.color.forest[900],
              boxShadow: "0 4px 12px rgba(45, 106, 79, 0.15)",
            },
          }}
        >
          Open Lab Memory
        </Button>

        <Box sx={{ mt: 8 }}>
          <Typography
            sx={{
              fontFamily: faradayTokens.font.mono,
              fontSize: 11,
              letterSpacing: "0.16em",
              textTransform: "uppercase",
              color: faradayTokens.color.ink.secondary,
              mb: 2,
            }}
          >
            Or jump straight in
          </Typography>
          <Box sx={{ display: "flex", flexDirection: "column", gap: 1 }}>
            {EXAMPLE_QUERIES.map((q) => (
              <RouterLink
                key={q}
                to={askLink(q)}
                style={{
                  textDecoration: "none",
                  color: faradayTokens.color.ink.primary,
                  fontFamily: faradayTokens.font.body,
                  fontSize: 15,
                  padding: "10px 16px",
                  borderRadius: 8,
                  border: `1px solid ${faradayTokens.color.forest[100]}`,
                  background: faradayTokens.color.surface.elevated,
                  display: "inline-flex",
                  alignItems: "center",
                  gap: 8,
                  width: "fit-content",
                  transition: "border-color 180ms ease-out, background 180ms ease-out",
                }}
                onMouseEnter={(e) => {
                  (e.currentTarget as HTMLAnchorElement).style.borderColor =
                    faradayTokens.color.forest[300];
                  (e.currentTarget as HTMLAnchorElement).style.background =
                    faradayTokens.color.forest[50];
                }}
                onMouseLeave={(e) => {
                  (e.currentTarget as HTMLAnchorElement).style.borderColor =
                    faradayTokens.color.forest[100];
                  (e.currentTarget as HTMLAnchorElement).style.background =
                    faradayTokens.color.surface.elevated;
                }}
              >
                <span style={{ color: faradayTokens.color.forest[700] }}>›</span>
                {q}
              </RouterLink>
            ))}
          </Box>
        </Box>

        <Box
          className="font-mono"
          sx={{
            mt: 10,
            fontSize: 11,
            color: faradayTokens.color.ink.tertiary,
            letterSpacing: "0.04em",
          }}
        >
          {warming && <span>warming up the lab…</span>}
          {health && (
            <span>
              api: <span style={{ color: faradayTokens.color.state.confirmed }}>{health.status}</span> ·
              env: {health.env} · uptime: {health.uptime_s}s
            </span>
          )}
        </Box>

        <Box sx={{ mt: 1, fontSize: 11 }}>
          <RouterLink
            to="/charts-demo"
            style={{
              color: faradayTokens.color.ink.tertiary,
              textDecoration: "underline",
              fontFamily: faradayTokens.font.mono,
            }}
          >
            → preview chart components
          </RouterLink>
        </Box>
      </Container>
    </Box>
  );
}
