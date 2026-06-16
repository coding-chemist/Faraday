// "LAB MEMORY — watch" right-rail teaser (Task #29 first cut).
// Placeholder illustration: thought-cloud over notebook + chart paper, hand-drawn
// SVG line work in the editorial-illustration register.

import { Box, Typography } from "@mui/material";

import { faradayTokens } from "../../design/theme";

function WatchIllustration() {
  return (
    <svg
      width={180}
      height={140}
      viewBox="0 0 180 140"
      role="img"
      aria-label="Faraday watching"
      style={{ display: "block", margin: "0 auto" }}
    >
      {/* Thought cloud */}
      <g fill="none" stroke={faradayTokens.color.forest[700]} strokeWidth={1.4} strokeLinecap="round">
        <path d="M40,55 q-12,-4 -12,-16 q0,-14 16,-14 q4,-12 18,-12 q14,0 18,12 q14,0 14,14 q0,12 -12,16 z" />
        {/* Notebook icon inside cloud */}
        <rect x={52} y={28} width={16} height={20} rx={1.5} />
        <line x1={56} y1={34} x2={64} y2={34} />
        <line x1={56} y1={38} x2={62} y2={38} />
        {/* Chart paper inside cloud */}
        <rect x={74} y={28} width={20} height={20} rx={1.5} />
        <polyline points="76,46 80,40 84,42 88,36 92,38" />
      </g>
      {/* Small thought bubbles trailing down */}
      <g fill="none" stroke={faradayTokens.color.forest[300]} strokeWidth={1.4}>
        <circle cx={56} cy={72} r={4} />
        <circle cx={48} cy={88} r={3} />
        <circle cx={42} cy={100} r={2} />
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
          letterSpacing: "0.12em",
          textTransform: "uppercase",
          color: faradayTokens.color.ink.secondary,
          mb: 3,
        }}
      >
        Lab memory — watch
      </Typography>

      <WatchIllustration />

      <Typography
        sx={{
          mt: 3,
          fontFamily: faradayTokens.font.body,
          fontSize: 14,
          color: faradayTokens.color.ink.primary,
          textAlign: "center",
          lineHeight: 1.5,
        }}
      >
        Faraday is also watching while you work.
      </Typography>
    </Box>
  );
}
