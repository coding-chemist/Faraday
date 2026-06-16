import { Box, Container, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import { Link as RouterLink } from "react-router-dom";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api";

interface HealthResponse {
  status: string;
  env: string;
  uptime_s: number;
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
    <Box className="min-h-screen bg-surface-warm">
      <Container maxWidth="md" className="pt-hero pb-section">
        <Typography
          variant="h1"
          className="font-display text-ink-primary"
          sx={{ fontSize: { xs: 48, md: 72 }, fontWeight: 600, lineHeight: 1.05 }}
        >
          Your lab's memory.
        </Typography>
        <Typography
          className="font-body text-ink-secondary mt-4 italic"
          sx={{ fontSize: 18 }}
        >
          Record like Faraday. Search like Google.
        </Typography>

        <Box className="mt-section font-mono text-xs text-ink-tertiary">
          {warming && <span>warming up the lab…</span>}
          {health && (
            <span>
              api: <span className="text-state-confirmed">{health.status}</span> ·
              env: {health.env} · uptime: {health.uptime_s}s
            </span>
          )}
        </Box>

        <Box className="mt-section font-mono text-sm" sx={{ display: "flex", gap: 3, flexWrap: "wrap" }}>
          <RouterLink to="/ask" style={{ color: "#B45309", textDecoration: "underline" }}>
            → open lab memory
          </RouterLink>
          <RouterLink to="/charts-demo" style={{ color: "#5C6360", textDecoration: "underline" }}>
            → preview chart components
          </RouterLink>
        </Box>
      </Container>
    </Box>
  );
}
