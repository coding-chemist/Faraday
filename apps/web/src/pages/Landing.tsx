// Marketing landing — discipline: real components only, one polished product
// asset (editor.png — a screenshot of the in-app editor, used the way Linear
// and Notion use their product UI), Material outlined icons for any iconography,
// generous whitespace, no decorative SVG hand-drawing anywhere.
//
// Forest/sage/mint register throughout. No amber.

import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import GitHubIcon from "@mui/icons-material/GitHub";
import InsightsOutlinedIcon from "@mui/icons-material/InsightsOutlined";
import PsychologyOutlinedIcon from "@mui/icons-material/PsychologyOutlined";
import ScienceOutlinedIcon from "@mui/icons-material/ScienceOutlined";
import WarningAmberOutlinedIcon from "@mui/icons-material/WarningAmberOutlined";
import type { SvgIconComponent } from "@mui/icons-material";
import { Box, Button, Stack, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import { Link as RouterLink } from "react-router-dom";

import { faradayTokens } from "../design/theme";
import { WatercolorWash } from "../components/shell/WatercolorWash";
import { LiveAskPreview } from "../components/landing/LiveAskPreview";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api";

const FOREST = faradayTokens.color.forest[700];
const FOREST_DEEP = faradayTokens.color.forest[900];
const FOREST_INK = faradayTokens.color.ink.primary;
const SAGE = faradayTokens.color.forest[300];
const MINT = faradayTokens.color.forest[100];
const PAGE_BG = faradayTokens.color.surface.base;
const PAPER = faradayTokens.color.surface.elevated;

interface HealthResponse {
  status: string;
  env: string;
  uptime_s: number;
}

const NAV_LINKS = [
  { label: "Product", href: "#features" },
  { label: "How it works", href: "#how" },
  { label: "Pricing", href: "#pricing" },
];

const CAPABILITY_CHIPS = ["21 CFR Part 11", "AI-grounded", "Editable"];

interface Feature {
  icon: SvgIconComponent;
  title: string;
  body: string;
  href?: string;
  hrefLabel?: string;
}

const FEATURES: Feature[] = [
  {
    icon: PsychologyOutlinedIcon,
    title: "Lab Memory",
    body: "Watch · Ask · Compare — three modes that surface every past run. The actual problem with ELNs isn't recording. It's finding the 8-month-old run that worked.",
    href: "/memory/ask",
    hrefLabel: "Try Ask mode",
  },
  {
    icon: WarningAmberOutlinedIcon,
    title: "Anomaly catches",
    body: "Stoichiometry checks, SOP-deviation flags, history comparison against your own past yields — all in the editor, as you write. Not in a post-hoc audit.",
  },
  {
    icon: InsightsOutlinedIcon,
    title: "Instrument-native ingest",
    body: "NMR (.jdx, .csv) and HPLC (.csv) auto-structured into the notebook — real peak tables, not screenshots. Audit trail is automatic.",
  },
];

// ─── Marketing nav ─────────────────────────────────────────────────────────
function MarketingNav() {
  return (
    <Box
      component="nav"
      sx={{
        position: "sticky",
        top: 0,
        zIndex: 10,
        backdropFilter: "blur(14px)",
        WebkitBackdropFilter: "blur(14px)",
        background: "rgba(247, 250, 246, 0.72)",
        borderBottom: `1px solid rgba(201, 228, 210, 0.5)`,
      }}
    >
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          px: { xs: 3, md: 6 },
          py: 2,
          maxWidth: 1440,
          mx: "auto",
        }}
      >
        <Typography
          component={RouterLink}
          to="/"
          sx={{
            fontFamily: faradayTokens.font.display,
            fontSize: 24,
            fontWeight: 600,
            color: FOREST_INK,
            textDecoration: "none",
            letterSpacing: "-0.01em",
          }}
        >
          Faraday
        </Typography>

        <Stack direction="row" spacing={4} sx={{ display: { xs: "none", md: "flex" } }}>
          {NAV_LINKS.map((l) => (
            <Box
              key={l.label}
              component="a"
              href={l.href}
              sx={{
                fontFamily: faradayTokens.font.mono,
                fontSize: 13,
                color: faradayTokens.color.ink.secondary,
                textDecoration: "none",
                transition: "color 180ms ease-out",
                "&:hover": { color: FOREST_INK },
              }}
            >
              {l.label}
            </Box>
          ))}
        </Stack>

        <Stack direction="row" spacing={2} alignItems="center">
          <Box
            component="a"
            href="#signin"
            sx={{
              fontFamily: faradayTokens.font.mono,
              fontSize: 13,
              color: faradayTokens.color.ink.secondary,
              textDecoration: "none",
              display: { xs: "none", sm: "inline" },
              "&:hover": { color: FOREST_INK },
            }}
          >
            Sign in
          </Box>
          <Button
            component={RouterLink}
            to="/memory/ask"
            sx={{
              background: FOREST,
              color: "#FFFFFF",
              borderRadius: 999,
              px: 2.5,
              py: 0.85,
              fontFamily: faradayTokens.font.mono,
              fontSize: 12,
              fontWeight: 600,
              textTransform: "none",
              letterSpacing: "0.02em",
              boxShadow: "none",
              "&:hover": { background: FOREST_DEEP, boxShadow: "none" },
            }}
          >
            Get started
          </Button>
        </Stack>
      </Box>
    </Box>
  );
}

// ─── Capability chip ───────────────────────────────────────────────────────
function CapabilityChip({ label }: { label: string }) {
  return (
    <Box
      sx={{
        display: "inline-flex",
        alignItems: "center",
        gap: 0.75,
        px: 1.75,
        py: 0.65,
        background: MINT,
        border: `1px solid ${SAGE}`,
        borderRadius: 999,
        fontFamily: faradayTokens.font.mono,
        fontSize: 11.5,
        color: FOREST_DEEP,
        letterSpacing: "0.01em",
      }}
    >
      <Box component="span" sx={{ width: 6, height: 6, borderRadius: "50%", background: FOREST }} />
      {label}
    </Box>
  );
}

// ─── Hero ──────────────────────────────────────────────────────────────────
function Hero() {
  return (
    <Box
      component="section"
      sx={{
        display: "grid",
        gridTemplateColumns: { xs: "1fr", md: "1fr 1.15fr" },
        gap: { xs: 6, md: 8 },
        alignItems: "center",
        px: { xs: 3, md: 6 },
        pt: { xs: 6, md: 10 },
        pb: { xs: 8, md: 12 },
        maxWidth: 1440,
        mx: "auto",
      }}
    >
      <Box>
        <Box
          sx={{
            display: "inline-flex",
            alignItems: "center",
            gap: 0.75,
            px: 1.25,
            py: 0.4,
            background: PAPER,
            border: `1px solid ${MINT}`,
            borderRadius: 999,
            fontFamily: faradayTokens.font.mono,
            fontSize: 11,
            color: FOREST,
            mb: 3,
            letterSpacing: "0.04em",
          }}
        >
          <Box sx={{ width: 5, height: 5, borderRadius: "50%", background: FOREST }} />
          v0.1 · Lab Memory live demo
        </Box>

        <Typography
          component="h1"
          sx={{
            fontFamily: faradayTokens.font.display,
            fontSize: { xs: 56, sm: 72, md: 96 },
            fontWeight: 600,
            lineHeight: 0.96,
            letterSpacing: "-0.03em",
            color: FOREST_INK,
            mb: 2,
          }}
        >
          Your lab's
          <br />
          <Box component="span" sx={{ fontStyle: "italic", color: FOREST }}>
            memory
          </Box>
          .
        </Typography>

        <Typography
          sx={{
            fontFamily: faradayTokens.font.body,
            fontSize: { xs: 17, md: 20 },
            color: faradayTokens.color.ink.secondary,
            fontStyle: "italic",
            mb: 4,
            maxWidth: 500,
            lineHeight: 1.4,
          }}
        >
          Record like Faraday. Search like Google.
        </Typography>

        <Stack direction="row" spacing={1} sx={{ mb: 5, flexWrap: "wrap", gap: 1 }}>
          {CAPABILITY_CHIPS.map((label) => (
            <CapabilityChip key={label} label={label} />
          ))}
        </Stack>

        <Stack direction={{ xs: "column", sm: "row" }} spacing={2.5} alignItems={{ xs: "stretch", sm: "center" }}>
          <Button
            component={RouterLink}
            to="/experiment/new"
            endIcon={<ArrowForwardIcon />}
            sx={{
              background: FOREST,
              color: "#FFFFFF",
              borderRadius: 999,
              px: 4,
              py: 1.65,
              fontFamily: faradayTokens.font.body,
              fontSize: 16,
              fontWeight: 600,
              textTransform: "none",
              boxShadow: "0 6px 18px rgba(45, 106, 79, 0.22)",
              "&:hover": {
                background: FOREST_DEEP,
                boxShadow: "0 8px 24px rgba(45, 106, 79, 0.30)",
                transform: "translateY(-1px)",
              },
              transition: "transform 180ms ease-out, box-shadow 180ms ease-out, background 180ms ease-out",
            }}
          >
            Start your first experiment
          </Button>

          <Box
            component={RouterLink}
            to="/memory/ask"
            sx={{
              fontFamily: faradayTokens.font.mono,
              fontSize: 13,
              color: faradayTokens.color.ink.secondary,
              textDecoration: "none",
              display: "inline-flex",
              alignItems: "center",
              gap: 0.75,
              borderBottom: `1px solid transparent`,
              pb: 0.25,
              transition: "color 180ms ease-out, border-color 180ms ease-out",
              "&:hover": { color: FOREST, borderBottomColor: FOREST },
            }}
          >
            Try Lab Memory <span aria-hidden>→</span>
          </Box>
        </Stack>
      </Box>

      {/* Live Lab Memory Ask preview — real components, real chart, real
          summary cards. Clicks through to the working demo. */}
      <Box
        sx={{
          position: "relative",
          display: "flex",
          justifyContent: { xs: "center", md: "flex-end" },
          alignItems: "center",
        }}
      >
        <LiveAskPreview />
      </Box>
    </Box>
  );
}

// ─── Feature card ──────────────────────────────────────────────────────────
function FeatureCard({ icon: Icon, title, body, href, hrefLabel }: Feature) {
  return (
    <Box
      sx={{
        background: PAPER,
        border: `1px solid ${MINT}`,
        borderRadius: 3,
        p: { xs: 3, md: 4 },
        display: "flex",
        flexDirection: "column",
        gap: 2,
        transition: "transform 220ms ease-out, box-shadow 220ms ease-out, border-color 220ms ease-out",
        "&:hover": {
          borderColor: SAGE,
          transform: "translateY(-2px)",
          boxShadow: "0 10px 28px rgba(45, 106, 79, 0.08)",
        },
      }}
    >
      <Box
        sx={{
          width: 44,
          height: 44,
          borderRadius: 2,
          background: MINT,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Icon sx={{ fontSize: 24, color: FOREST_DEEP }} />
      </Box>
      <Typography
        component="h3"
        sx={{
          fontFamily: faradayTokens.font.display,
          fontSize: 22,
          fontWeight: 600,
          color: FOREST_INK,
          letterSpacing: "-0.01em",
        }}
      >
        {title}
      </Typography>
      <Typography
        sx={{
          fontFamily: faradayTokens.font.body,
          fontSize: 15,
          color: faradayTokens.color.ink.secondary,
          lineHeight: 1.55,
          flex: 1,
        }}
      >
        {body}
      </Typography>
      {href && (
        <Box
          component={RouterLink}
          to={href}
          sx={{
            mt: "auto",
            fontFamily: faradayTokens.font.mono,
            fontSize: 12,
            color: FOREST,
            textDecoration: "none",
            display: "inline-flex",
            alignItems: "center",
            gap: 0.75,
            letterSpacing: "0.04em",
            textTransform: "uppercase",
            transition: "gap 180ms ease-out",
            "&:hover": { gap: 1.25 },
          }}
        >
          {hrefLabel} <span aria-hidden>→</span>
        </Box>
      )}
    </Box>
  );
}

// ─── Features section ──────────────────────────────────────────────────────
function FeaturesSection() {
  return (
    <Box
      component="section"
      id="features"
      sx={{
        position: "relative",
        background: faradayTokens.color.surface.muted,
        py: { xs: 8, md: 12 },
        px: { xs: 3, md: 6 },
        borderTop: `1px solid ${MINT}`,
      }}
    >
      <Box sx={{ maxWidth: 1280, mx: "auto" }}>
        <Box sx={{ maxWidth: 680, mb: { xs: 5, md: 7 } }}>
          <Typography
            sx={{
              fontFamily: faradayTokens.font.mono,
              fontSize: 11,
              letterSpacing: "0.14em",
              textTransform: "uppercase",
              color: FOREST,
              mb: 2,
            }}
          >
            The wedge
          </Typography>
          <Typography
            component="h2"
            sx={{
              fontFamily: faradayTokens.font.display,
              fontSize: { xs: 32, md: 44 },
              fontWeight: 600,
              lineHeight: 1.05,
              letterSpacing: "-0.02em",
              color: FOREST_INK,
              mb: 2,
            }}
          >
            Three primitives no ELN ships today.
          </Typography>
          <Typography
            sx={{
              fontFamily: faradayTokens.font.body,
              fontSize: 17,
              color: faradayTokens.color.ink.secondary,
              lineHeight: 1.5,
            }}
          >
            Existing ELNs are expensive, form-heavy, and bad at search. Many chemists pay for compliance and still keep paper notebooks at the bench. Faraday collapses that tradeoff.
          </Typography>
        </Box>

        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: { xs: "1fr", md: "repeat(3, 1fr)" },
            gap: { xs: 2.5, md: 3 },
          }}
        >
          {FEATURES.map((f) => (
            <FeatureCard key={f.title} {...f} />
          ))}
        </Box>
      </Box>
    </Box>
  );
}

// ─── Footer ────────────────────────────────────────────────────────────────
function Footer() {
  const [health, setHealth] = useState<HealthResponse | null>(null);

  useEffect(() => {
    fetch(`${API_BASE}/health`)
      .then((r) => r.json())
      .then(setHealth)
      .catch(() => {});
  }, []);

  return (
    <Box
      component="footer"
      sx={{
        borderTop: `1px solid ${MINT}`,
        py: { xs: 5, md: 6 },
        px: { xs: 3, md: 6 },
      }}
    >
      <Box
        sx={{
          maxWidth: 1280,
          mx: "auto",
          display: "flex",
          flexDirection: { xs: "column", md: "row" },
          gap: 3,
          alignItems: { xs: "flex-start", md: "center" },
          justifyContent: "space-between",
        }}
      >
        <Box>
          <Typography
            sx={{
              fontFamily: faradayTokens.font.display,
              fontSize: 18,
              fontWeight: 600,
              color: FOREST_INK,
              mb: 0.5,
            }}
          >
            Faraday
          </Typography>
          <Typography
            sx={{
              fontFamily: faradayTokens.font.body,
              fontSize: 13,
              color: faradayTokens.color.ink.secondary,
              fontStyle: "italic",
            }}
          >
            Record like Faraday. Search like Google.
          </Typography>
        </Box>

        <Stack direction="row" spacing={3} alignItems="center" flexWrap="wrap">
          <Box
            component="a"
            href="https://github.com/coding-chemist/Curie"
            target="_blank"
            rel="noreferrer"
            sx={{
              fontFamily: faradayTokens.font.mono,
              fontSize: 12,
              color: faradayTokens.color.ink.secondary,
              textDecoration: "none",
              display: "inline-flex",
              alignItems: "center",
              gap: 0.5,
              "&:hover": { color: FOREST },
            }}
          >
            <ScienceOutlinedIcon sx={{ fontSize: 14 }} /> Curie
          </Box>
          <Box
            component="a"
            href="https://github.com/coding-chemist/Darwin"
            target="_blank"
            rel="noreferrer"
            sx={{
              fontFamily: faradayTokens.font.mono,
              fontSize: 12,
              color: faradayTokens.color.ink.secondary,
              textDecoration: "none",
              "&:hover": { color: FOREST },
            }}
          >
            Darwin
          </Box>
          <Box
            component="a"
            href="https://github.com/coding-chemist"
            target="_blank"
            rel="noreferrer"
            sx={{
              fontFamily: faradayTokens.font.mono,
              fontSize: 12,
              color: faradayTokens.color.ink.secondary,
              textDecoration: "none",
              display: "inline-flex",
              alignItems: "center",
              gap: 0.5,
              "&:hover": { color: FOREST },
            }}
          >
            <GitHubIcon sx={{ fontSize: 14 }} /> GitHub
          </Box>
          {health && (
            <Typography
              sx={{
                fontFamily: faradayTokens.font.mono,
                fontSize: 11,
                color: faradayTokens.color.ink.tertiary,
                letterSpacing: "0.04em",
              }}
            >
              api: <span style={{ color: faradayTokens.color.state.confirmed }}>{health.status}</span>
            </Typography>
          )}
        </Stack>
      </Box>
    </Box>
  );
}

// ─── Page ──────────────────────────────────────────────────────────────────
export function Landing() {
  return (
    <Box
      sx={{
        position: "relative",
        minHeight: "100vh",
        background: PAGE_BG,
      }}
    >
      {/* Soft sage/mint watercolor — same green family as the rest of the app */}
      <Box sx={{ position: "absolute", inset: 0, zIndex: 0, pointerEvents: "none" }} aria-hidden>
        <WatercolorWash variant="subtle" seed={11} />
      </Box>

      <Box sx={{ position: "relative", zIndex: 1 }}>
        <MarketingNav />
        <Hero />
        <FeaturesSection />
        <Footer />
      </Box>
    </Box>
  );
}
