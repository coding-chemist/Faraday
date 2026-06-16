import { Box, Chip, Typography } from "@mui/material";

import { faradayTokens } from "../../design/theme";

const EXAMPLES: readonly string[] = [
  "Show Suzuki couplings with yield below 70% in the last six months",
  "Compare HATU vs EDC amide coupling yields",
  "Average yield by reaction type this year",
  "Yield by catalyst across solvents",
  "Distribution of yields for all reactions",
];

interface Props {
  onSelect: (query: string) => void;
  disabled?: boolean;
  /** compact = used inside the empty-state card; smaller chips, no helper text. */
  compact?: boolean;
}

export function SuggestedQueries({ onSelect, disabled = false, compact = false }: Props) {
  return (
    <Box sx={{ textAlign: "center", maxWidth: 760, mx: "auto" }}>
      {!compact && (
        <Typography
          sx={{
            fontFamily: faradayTokens.font.mono,
            fontSize: 11,
            letterSpacing: "0.08em",
            textTransform: "uppercase",
            color: faradayTokens.color.ink.secondary,
            mb: 1.5,
          }}
        >
          Try one of these
        </Typography>
      )}
      <Box
        sx={{
          display: "flex",
          flexWrap: "wrap",
          gap: 1,
          justifyContent: "center",
        }}
      >
        {EXAMPLES.slice(0, compact ? 3 : EXAMPLES.length).map((example) => (
          <Chip
            key={example}
            label={example}
            onClick={() => onSelect(example)}
            disabled={disabled}
            clickable
            sx={{
              background: "rgba(255, 255, 255, 0.7)",
              backdropFilter: "blur(8px)",
              WebkitBackdropFilter: "blur(8px)",
              border: `1px solid ${faradayTokens.color.forest[100]}`,
              borderRadius: 1.5,
              fontSize: 12,
              fontFamily: faradayTokens.font.mono,
              color: faradayTokens.color.ink.primary,
              height: "auto",
              py: 1,
              px: 0.5,
              "& .MuiChip-label": { px: 1.5, whiteSpace: "normal", lineHeight: 1.4 },
              "&:hover": {
                background: "rgba(255, 255, 255, 0.9)",
                borderColor: faradayTokens.color.forest[300],
              },
            }}
          />
        ))}
      </Box>
    </Box>
  );
}
