// The F+ tile — deep forest square with a monospaced F (JetBrains Mono) and a
// Material AutoAwesome sparkle icon in the top-right corner. The F is text
// (letter, not icon); the sparkle is Google's Material AutoAwesome icon.

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
          fontSize: size * 0.6,
          fontWeight: 600,
          color: "#FFFFFF",
          lineHeight: 1,
          // Shift left + tiny down for breathing room next to the sparkle
          transform: "translate(-7%, 2%)",
        }}
      >
        F
      </Typography>
      <AutoAwesomeIcon
        sx={{
          position: "absolute",
          top: size * 0.1,
          right: size * 0.08,
          color: "#FFFFFF",
          fontSize: size * 0.2,
        }}
      />
    </Box>
  );
}
