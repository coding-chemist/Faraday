// "LAB MEMORY — watch" right-rail teaser.
// Hand-drawn line-work illustration: a thought cloud holding a notebook + a
// chart panel, with trailing thought bubbles. Sits on the pronounced
// watercolor backdrop provided by the parent RightRail.

import { Box, Typography } from "@mui/material";

import { faradayTokens } from "../../design/theme";

function WatchIllustration() {
  const ink = faradayTokens.color.forest[900];
  const accent = faradayTokens.color.forest[700];

  return (
    <svg
      width="100%"
      height={170}
      viewBox="0 0 220 170"
      role="img"
      aria-label="Faraday watching"
      style={{ display: "block", margin: "0 auto", maxWidth: 220 }}
    >
      {/* Thought cloud — drawn as a series of overlapping arcs */}
      <g fill="none" stroke={ink} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
        <path d="M40,60 Q26,60 22,46 Q22,32 36,30 Q40,18 56,18 Q72,16 80,28 Q98,22 108,34 Q124,30 130,46 Q132,60 116,62 Q108,72 92,68 Q78,76 64,68 Q50,72 40,60 Z" />

        {/* Notebook inside cloud */}
        <g transform="translate(48, 30)">
          <rect x={0} y={0} width={20} height={26} rx={1.5} />
          <line x1={4} y1={6} x2={16} y2={6} strokeWidth={1.2} />
          <line x1={4} y1={11} x2={14} y2={11} strokeWidth={1.2} />
          <line x1={4} y1={16} x2={15} y2={16} strokeWidth={1.2} />
          <line x1={4} y1={21} x2={12} y2={21} strokeWidth={1.2} />
        </g>

        {/* Chart panel inside cloud */}
        <g transform="translate(76, 32)">
          <rect x={0} y={0} width={26} height={22} rx={1.5} />
          <polyline points="3,18 7,12 11,14 15,8 19,11 23,6" stroke={accent} strokeWidth={1.4} fill="none" />
          <line x1={3} y1={18} x2={23} y2={18} strokeWidth={1} />
        </g>
      </g>

      {/* Trailing thought bubbles */}
      <g fill="none" stroke={accent} strokeWidth={1.4}>
        <circle cx={60} cy={90} r={5} />
        <circle cx={48} cy={108} r={3.5} />
        <circle cx={40} cy={122} r={2.5} />
      </g>
    </svg>
  );
}

export function WatchTeaser() {
  return (
    <Box>
      <Typography
        sx={{
          fontFamily: faradayTokens.font.mono,
          fontSize: 11,
          letterSpacing: "0.16em",
          textTransform: "uppercase",
          color: faradayTokens.color.ink.secondary,
          mb: 4,
        }}
      >
        Lab memory <span style={{ color: faradayTokens.color.ink.tertiary }}>—</span> watch
      </Typography>

      <WatchIllustration />

      <Typography
        sx={{
          mt: 4,
          fontFamily: faradayTokens.font.body,
          fontSize: 14,
          color: faradayTokens.color.ink.primary,
          textAlign: "center",
          lineHeight: 1.55,
          maxWidth: 220,
          mx: "auto",
        }}
      >
        Faraday is also watching while you work.
      </Typography>
    </Box>
  );
}
