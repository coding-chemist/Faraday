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
            fontSize: 13,
            color: faradayTokens.color.ink.secondary,
            fontStyle: "italic",
            mb: 1.5,
          }}
        >
          Try one of these:
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
              background: faradayTokens.color.surface.elevated,
              border: `1px solid ${faradayTokens.color.forest[100]}`,
              fontSize: 13,
              fontFamily: faradayTokens.font.body,
              color: faradayTokens.color.ink.primary,
              height: "auto",
              py: 1,
              px: 0.5,
              "& .MuiChip-label": { px: 1.5, whiteSpace: "normal", lineHeight: 1.4 },
              "&:hover": {
                background: faradayTokens.color.surface.sunken,
                borderColor: faradayTokens.color.forest[300],
              },
            }}
          />
        ))}
      </Box>
    </Box>
  );
}
