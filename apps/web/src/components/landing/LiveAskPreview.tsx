// Live Ask-mode preview for the landing hero.
//
// Real product UI rendered from real components — same fonts, same color
// register, same structural shape as the deployed /memory/ask page (frozen
// snapshot of the "Compare HATU vs EDC amide coupling yields" result).
//
// Why this and not editor.png:
//   - Linear / Vercel / Stripe anchor their hero with real software, not a
//     designer mockup. The hero IS the product.
//   - Sharp corners, thin borders, flat surfaces — no AI-mockup
//     mood-board rounding.
//   - Zero new dependencies — Recharts not pulled in here, just SVG bars,
//     so the landing stays light.
//
// The whole card is wrapped in a RouterLink to /memory/ask so a click on
// the preview opens the actually-working demo.

import ArrowOutwardIcon from "@mui/icons-material/ArrowOutward";
import BarChartOutlinedIcon from "@mui/icons-material/BarChartOutlined";
import HubOutlinedIcon from "@mui/icons-material/HubOutlined";
import MenuBookOutlinedIcon from "@mui/icons-material/MenuBookOutlined";
import SearchIcon from "@mui/icons-material/Search";
import type { SvgIconComponent } from "@mui/icons-material";
import { Box, Stack, Typography } from "@mui/material";
import { Link as RouterLink } from "react-router-dom";

import { faradayTokens } from "../../design/theme";

const FOREST = faradayTokens.color.forest[700];
const FOREST_DEEP = faradayTokens.color.forest[900];
const FOREST_500 = faradayTokens.color.forest[500];
const FOREST_300 = faradayTokens.color.forest[300];
const MINT = faradayTokens.color.forest[100];
const SOFT = faradayTokens.color.forest[50];
const PAPER = faradayTokens.color.surface.elevated;
const INK = faradayTokens.color.ink.primary;
const INK_SOFT = faradayTokens.color.ink.secondary;
const INK_FAINT = faradayTokens.color.ink.tertiary;

const MONO = faradayTokens.font.mono;

// Hardcoded snapshot of a real query result — matches what the live API
// returns for "Compare HATU vs EDC amide coupling yields".
const QUERY = "Compare HATU vs EDC amide coupling yields";
const INTENT = "Average amide coupling yields compared across coupling reagents";

interface Bar {
  label: string;
  yield_pct: number;
  n: number;
}

const BARS: Bar[] = [
  { label: "T3P", yield_pct: 89.3, n: 14 },
  { label: "HATU", yield_pct: 88.9, n: 22 },
  { label: "PyBOP", yield_pct: 83.8, n: 8 },
  { label: "DCC", yield_pct: 83.2, n: 6 },
  { label: "EDC", yield_pct: 83.0, n: 7 },
];

const BAR_MAX = 100;

interface SummaryCard {
  icon: SvgIconComponent;
  label: string;
  value: string;
  sub: string;
}

const CARDS: SummaryCard[] = [
  { icon: MenuBookOutlinedIcon, label: "Matched", value: "60", sub: "of 210" },
  { icon: BarChartOutlinedIcon, label: "Avg yield", value: "86.9%", sub: "median 89.5%" },
  { icon: HubOutlinedIcon, label: "Top catalyst", value: "HATU", sub: "37% of runs" },
];

// ─── pieces ────────────────────────────────────────────────────────────────

function QueryBar() {
  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        gap: 1.25,
        background: PAPER,
        border: `1px solid ${MINT}`,
        borderRadius: 1,
        px: 1.5,
        py: 1,
      }}
    >
      <SearchIcon sx={{ fontSize: 16, color: INK_FAINT }} />
      <Typography
        sx={{
          flex: 1,
          fontFamily: MONO,
          fontSize: 12.5,
          color: INK,
          whiteSpace: "nowrap",
          overflow: "hidden",
          textOverflow: "ellipsis",
        }}
      >
        {QUERY}
      </Typography>
      <Box
        sx={{
          background: FOREST,
          color: "#FFFFFF",
          borderRadius: 0.75,
          px: 1.5,
          py: 0.5,
          fontFamily: MONO,
          fontSize: 10.5,
          fontWeight: 600,
          letterSpacing: "0.04em",
        }}
      >
        ASK
      </Box>
    </Box>
  );
}

function BarRow({ bar, isMax }: { bar: Bar; isMax: boolean }) {
  const widthPct = (bar.yield_pct / BAR_MAX) * 100;
  return (
    <Box sx={{ display: "grid", gridTemplateColumns: "44px 1fr 56px", alignItems: "center", gap: 1.25 }}>
      <Typography
        sx={{
          fontFamily: MONO,
          fontSize: 10.5,
          color: INK_SOFT,
          textAlign: "right",
        }}
      >
        {bar.label}
      </Typography>
      <Box sx={{ position: "relative", height: 14, background: SOFT, borderRadius: 0.5 }}>
        <Box
          sx={{
            position: "absolute",
            top: 0,
            left: 0,
            bottom: 0,
            width: `${widthPct}%`,
            background: isMax ? FOREST_DEEP : FOREST,
            borderRadius: 0.5,
          }}
        />
      </Box>
      <Typography
        sx={{
          fontFamily: MONO,
          fontSize: 10.5,
          fontWeight: 600,
          color: INK,
          fontFeatureSettings: '"tnum" 1',
          textAlign: "right",
        }}
      >
        {bar.yield_pct.toFixed(1)}%
      </Typography>
    </Box>
  );
}

function ChartCard() {
  const max = Math.max(...BARS.map((b) => b.yield_pct));
  return (
    <Box
      sx={{
        background: PAPER,
        border: `1px solid ${MINT}`,
        borderRadius: 1,
        p: 2,
      }}
    >
      <Stack direction="row" spacing={1.5} alignItems="baseline" sx={{ mb: 2 }}>
        <Typography
          sx={{
            fontFamily: MONO,
            fontSize: 10,
            letterSpacing: "0.1em",
            textTransform: "uppercase",
            color: FOREST,
            fontWeight: 600,
          }}
        >
          intent
        </Typography>
        <Typography
          sx={{
            fontFamily: MONO,
            fontSize: 12,
            color: INK,
            lineHeight: 1.4,
          }}
        >
          {INTENT}
        </Typography>
      </Stack>
      <Stack spacing={1.25}>
        {BARS.map((b) => (
          <BarRow key={b.label} bar={b} isMax={b.yield_pct === max} />
        ))}
      </Stack>
      <Typography
        sx={{
          fontFamily: MONO,
          fontSize: 9.5,
          color: INK_FAINT,
          mt: 1.5,
          letterSpacing: "0.04em",
        }}
      >
        n = {BARS.reduce((s, b) => s + b.n, 0)} amide coupling runs · mean yield
      </Typography>
    </Box>
  );
}

function SummaryStrip() {
  return (
    <Box
      sx={{
        display: "grid",
        gridTemplateColumns: "repeat(3, 1fr)",
        gap: 1,
      }}
    >
      {CARDS.map((c) => {
        const Icon = c.icon;
        return (
          <Box
            key={c.label}
            sx={{
              background: PAPER,
              border: `1px solid ${MINT}`,
              borderRadius: 1,
              p: 1.25,
            }}
          >
            <Icon sx={{ fontSize: 14, color: FOREST, mb: 0.5 }} />
            <Typography
              sx={{
                fontFamily: MONO,
                fontSize: 9,
                letterSpacing: "0.08em",
                textTransform: "uppercase",
                color: INK_SOFT,
                lineHeight: 1.1,
              }}
            >
              {c.label}
            </Typography>
            <Typography
              sx={{
                fontFamily: MONO,
                fontSize: 16,
                fontWeight: 600,
                fontFeatureSettings: '"tnum" 1',
                color: FOREST_DEEP,
                lineHeight: 1.15,
                mt: 0.25,
              }}
            >
              {c.value}
            </Typography>
            <Typography
              sx={{
                fontFamily: MONO,
                fontSize: 9.5,
                color: INK_FAINT,
                lineHeight: 1.2,
                mt: 0.25,
              }}
            >
              {c.sub}
            </Typography>
          </Box>
        );
      })}
    </Box>
  );
}

function Header() {
  return (
    <Stack
      direction="row"
      alignItems="center"
      justifyContent="space-between"
      sx={{ mb: 1.5 }}
    >
      <Stack direction="row" spacing={1} alignItems="center">
        <Box sx={{ display: "flex", gap: 0.5 }}>
          <Box sx={{ width: 7, height: 7, borderRadius: "50%", background: "#E5E2DA" }} />
          <Box sx={{ width: 7, height: 7, borderRadius: "50%", background: "#E5E2DA" }} />
          <Box sx={{ width: 7, height: 7, borderRadius: "50%", background: "#E5E2DA" }} />
        </Box>
        <Typography
          sx={{
            fontFamily: MONO,
            fontSize: 10,
            color: INK_FAINT,
            letterSpacing: "0.06em",
            ml: 1,
          }}
        >
          faraday.app / memory / ask
        </Typography>
      </Stack>
      <Box
        sx={{
          display: "inline-flex",
          alignItems: "center",
          gap: 0.5,
          fontFamily: MONO,
          fontSize: 9.5,
          color: FOREST,
          letterSpacing: "0.06em",
          textTransform: "uppercase",
        }}
      >
        live
        <Box sx={{ width: 5, height: 5, borderRadius: "50%", background: FOREST_500 }} />
      </Box>
    </Stack>
  );
}

// ─── exported card ─────────────────────────────────────────────────────────

export function LiveAskPreview() {
  return (
    <Box
      component={RouterLink}
      to="/memory/ask"
      aria-label="Open Lab Memory Ask mode"
      sx={{
        position: "relative",
        display: "block",
        textDecoration: "none",
        width: "100%",
        maxWidth: 540,
        background: faradayTokens.color.surface.muted,
        border: `1px solid ${FOREST_300}`,
        borderRadius: 1.5,
        p: { xs: 2, md: 2.5 },
        boxShadow:
          "0 24px 60px rgba(27, 67, 50, 0.16), 0 6px 18px rgba(27, 67, 50, 0.08)",
        transition: "transform 320ms ease-out, box-shadow 320ms ease-out, border-color 320ms ease-out",
        "&:hover": {
          transform: "translateY(-3px)",
          borderColor: FOREST_500,
          boxShadow:
            "0 30px 70px rgba(27, 67, 50, 0.20), 0 8px 22px rgba(27, 67, 50, 0.10)",
        },
        "&:focus-visible": {
          outline: `2px solid ${FOREST}`,
          outlineOffset: 4,
        },
      }}
    >
      <Header />

      <Stack spacing={1.5}>
        <QueryBar />
        <ChartCard />
        <SummaryStrip />
      </Stack>

      <Stack
        direction="row"
        alignItems="center"
        justifyContent="space-between"
        sx={{ mt: 2, pt: 1.5, borderTop: `1px solid ${MINT}` }}
      >
        <Typography
          sx={{
            fontFamily: MONO,
            fontSize: 10,
            color: INK_FAINT,
            letterSpacing: "0.04em",
          }}
        >
          parsed by gpt-oss:20b · pandas aggregate · 210 experiments
        </Typography>
        <Box
          sx={{
            display: "inline-flex",
            alignItems: "center",
            gap: 0.5,
            fontFamily: MONO,
            fontSize: 11,
            color: FOREST,
            fontWeight: 600,
            letterSpacing: "0.04em",
          }}
        >
          OPEN <ArrowOutwardIcon sx={{ fontSize: 12 }} />
        </Box>
      </Stack>
    </Box>
  );
}
