// "Faraday" serif wordmark for the top bar.
import { Box } from "@mui/material";
import { Link as RouterLink } from "react-router-dom";

import { faradayTokens } from "../../design/theme";

export function Wordmark() {
  return (
    <Box
      component={RouterLink}
      to="/"
      sx={{
        fontFamily: faradayTokens.font.display,
        fontSize: 28,
        fontWeight: 600,
        color: faradayTokens.color.ink.primary,
        textDecoration: "none",
        letterSpacing: "-0.01em",
        lineHeight: 1,
      }}
    >
      Faraday
    </Box>
  );
}
