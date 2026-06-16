// "LAB MEMORY — watch" right-rail teaser.
//
// Illustration loaded from /illustrations/watch.png (drop a real PNG into
// apps/web/public/illustrations/watch.png). When missing, no illustration
// is shown — header + body text alone. See illustrations/README.md for the
// generation prompt.

import { Box, Typography } from "@mui/material";
import { useState } from "react";

import { faradayTokens } from "../../design/theme";

export function WatchTeaser() {
  const [imageOk, setImageOk] = useState(true);

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

      {imageOk && (
        <Box sx={{ textAlign: "center", mb: 4 }}>
          <img
            src="/illustrations/watch.png"
            alt=""
            aria-hidden
            style={{ maxWidth: 220, width: "100%", height: "auto" }}
            onError={() => setImageOk(false)}
          />
        </Box>
      )}

      <Typography
        sx={{
          mt: imageOk ? 0 : 6,
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
