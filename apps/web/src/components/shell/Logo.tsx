// The F+ tile — deep forest square with a serif F (Fraunces) and a Material
// AutoAwesome sparkle icon in the top-right corner. The F is text (letter,
// not icon); the sparkle is Google's Material AutoAwesome icon.

import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import { Box, Typography } from "@mui/material";

import { faradayTokens } from "../../design/theme";

interface Props {
  size?: number;
}

export function Logo({ size = 56 }: Props) {
  return (
    <Box
      role="img"
      aria-label="Faraday"
      sx={{
        position: "relative",
        width: size,
        height: size,
        background: faradayTokens.color.forest[700],
        borderRadius: `${size * 0.22}px`,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        flexShrink: 0,
      }}
    >
      <Typography
        component="span"
        sx={{
          fontFamily: faradayTokens.font.display,
          fontSize: size * 0.62,
          fontWeight: 600,
          color: "#FFFFFF",
          lineHeight: 1,
          // Slight optical lift so the F sits centred above the letterform's descent
          transform: "translateY(2%)",
        }}
      >
        F
      </Typography>
      <AutoAwesomeIcon
        sx={{
          position: "absolute",
          top: size * 0.18,
          right: size * 0.16,
          color: "#FFFFFF",
          fontSize: size * 0.22,
        }}
      />
    </Box>
  );
}
