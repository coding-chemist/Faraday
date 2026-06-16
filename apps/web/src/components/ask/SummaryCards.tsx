import { Box, Card, Typography } from "@mui/material";

import { faradayTokens } from "../../design/theme";
import type { SummaryCard as SummaryCardType } from "../../types/analysis";

interface Props {
  cards: SummaryCardType[];
}

export function SummaryCards({ cards }: Props) {
  if (cards.length === 0) return null;

  return (
    <Box
      sx={{
        display: "grid",
        gridTemplateColumns: {
          xs: "1fr",
          sm: "repeat(2, 1fr)",
          md: `repeat(${Math.min(cards.length, 4)}, 1fr)`,
        },
        gap: 2.5,
      }}
    >
      {cards.map((card) => (
        <Card
          key={card.label}
          elevation={0}
          sx={{
            background: faradayTokens.color.surface.elevated,
            border: "1px solid #E5E2DA",
            borderRadius: 2,
            p: 3,
          }}
        >
          <Typography
            sx={{
              color: faradayTokens.color.ink.secondary,
              fontFamily: faradayTokens.font.mono,
              fontSize: 11,
              letterSpacing: "0.08em",
              textTransform: "uppercase",
            }}
          >
            {card.label}
          </Typography>
          <Typography
            sx={{
              fontSize: 32,
              fontWeight: 600,
              fontFamily: faradayTokens.font.display,
              mt: 0.5,
              lineHeight: 1.1,
              color: faradayTokens.color.ink.primary,
            }}
          >
            {card.value}
          </Typography>
          {card.sublabel && (
            <Typography
              sx={{
                fontSize: 13,
                color: faradayTokens.color.ink.secondary,
                mt: 1,
                fontStyle: "italic",
              }}
            >
              {card.sublabel}
            </Typography>
          )}
        </Card>
      ))}
    </Box>
  );
}
