// Lab Memory "sees your past runs" right-rail widget — shown on Experiment
// pages (Task #26) to surface 3 similar past experiments from FAISS search.
// Built now so it's ready to drop into the Experiment shell when that page lands.

import { Box, Typography } from "@mui/material";

import { faradayTokens } from "../../design/theme";

export interface PastRun {
  reactionType: string;       // "Suzuki"
  paragraph: number;          // 2,801
  catalyst: string;           // "Pd(PPh3)4"
  yieldPct: number | null;    // 78
  agoLabel: string;           // "3 weeks ago"
}

interface Props {
  runs: PastRun[];
  /** Optional summary line, e.g. "Your last 3 Pd-catalyzed runs averaged 70.3%". */
  summaryLabel?: string;
  summaryValue?: string;
}

function FlaskGlyph({ fillLevel = 0.6 }: { fillLevel?: number }) {
  const stroke = faradayTokens.color.forest[700];
  const liquid = faradayTokens.color.forest[300];
  return (
    <svg width={36} height={42} viewBox="0 0 36 42" fill="none" aria-hidden>
      {/* Flask outline — Erlenmeyer */}
      <path
        d="M 13 4 L 13 14 L 5 34 Q 5 38 9 38 L 27 38 Q 31 38 31 34 L 23 14 L 23 4"
        stroke={stroke}
        strokeWidth={1.3}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {/* Top rim */}
      <line x1={11} y1={4} x2={25} y2={4} stroke={stroke} strokeWidth={1.3} strokeLinecap="round" />
      {/* Liquid — clipped polygon at fillLevel */}
      <defs>
        <clipPath id="flask-body">
          <path d="M 13 14 L 5 34 Q 5 38 9 38 L 27 38 Q 31 38 31 34 L 23 14 Z" />
        </clipPath>
      </defs>
      <g clipPath="url(#flask-body)">
        <rect
          x={4}
          y={14 + (38 - 14) * (1 - fillLevel)}
          width={28}
          height={(38 - 14) * fillLevel}
          fill={liquid}
          opacity={0.55}
        />
      </g>
    </svg>
  );
}

export function PastRunsWidget({ runs, summaryLabel, summaryValue }: Props) {
  return (
    <Box>
      <Typography
        sx={{
          fontFamily: faradayTokens.font.mono,
          fontSize: 11,
          letterSpacing: "0.16em",
          textTransform: "uppercase",
          color: faradayTokens.color.ink.secondary,
          mb: 3,
        }}
      >
        Lab memory <span style={{ color: faradayTokens.color.ink.tertiary }}>—</span> sees your past runs
      </Typography>

      <Box sx={{ display: "flex", flexDirection: "column", gap: 1.5 }}>
        {runs.map((run, i) => (
          <Box
            key={i}
            sx={{
              display: "flex",
              gap: 1.5,
              p: 1.5,
              borderRadius: 2,
              background: faradayTokens.color.surface.elevated,
              border: `1px solid ${faradayTokens.color.forest[100]}`,
              transition: "border-color 180ms ease-out",
              "&:hover": { borderColor: faradayTokens.color.forest[300] },
            }}
          >
            <FlaskGlyph fillLevel={Math.min(1, Math.max(0.2, (run.yieldPct ?? 50) / 100))} />
            <Box sx={{ flex: 1, minWidth: 0 }}>
              <Typography
                sx={{
                  fontFamily: faradayTokens.font.mono,
                  fontSize: 12,
                  color: faradayTokens.color.ink.secondary,
                  lineHeight: 1.3,
                }}
              >
                {run.reactionType} ¶ {run.paragraph.toLocaleString()}
              </Typography>
              <Typography
                sx={{
                  fontFamily: faradayTokens.font.body,
                  fontSize: 13,
                  fontWeight: 500,
                  color: faradayTokens.color.ink.primary,
                  lineHeight: 1.3,
                }}
              >
                {run.catalyst}
              </Typography>
              <Typography
                sx={{
                  fontFamily: faradayTokens.font.body,
                  fontSize: 12,
                  color: faradayTokens.color.forest[900],
                  fontWeight: 600,
                  mt: 0.25,
                }}
              >
                {run.yieldPct != null ? `${run.yieldPct}% yield` : "—"}
              </Typography>
              <Typography
                sx={{
                  fontFamily: faradayTokens.font.body,
                  fontSize: 11,
                  color: faradayTokens.color.ink.tertiary,
                  fontStyle: "italic",
                  mt: 0.25,
                }}
              >
                {run.agoLabel}
              </Typography>
            </Box>
          </Box>
        ))}
      </Box>

      {summaryLabel && summaryValue && (
        <Box
          sx={{
            mt: 2.5,
            p: 2,
            borderRadius: 2,
            background: faradayTokens.color.surface.muted,
            border: `1px solid ${faradayTokens.color.forest[100]}`,
            textAlign: "center",
          }}
        >
          <Typography
            sx={{
              fontFamily: faradayTokens.font.body,
              fontSize: 12,
              color: faradayTokens.color.ink.secondary,
              lineHeight: 1.4,
            }}
          >
            {summaryLabel}
          </Typography>
          <Typography
            sx={{
              fontFamily: faradayTokens.font.display,
              fontSize: 20,
              fontWeight: 600,
              color: faradayTokens.color.forest[900],
              mt: 0.5,
            }}
          >
            {summaryValue}
          </Typography>
        </Box>
      )}
    </Box>
  );
}
