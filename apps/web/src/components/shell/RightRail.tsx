// Right rail container — soft watercolor sage wash backdrop per mockup.
// Page passes children (e.g. Watch teaser, past-runs widget).

import { Box } from "@mui/material";

import { faradayTokens } from "../../design/theme";

interface Props {
  children: React.ReactNode;
}

export function RightRail({ children }: Props) {
  return (
    <Box
      component="aside"
      aria-label="Contextual sidebar"
      sx={{
        width: 320,
        flexShrink: 0,
        position: "relative",
        borderLeft: `1px solid ${faradayTokens.color.forest[100]}`,
        background: `linear-gradient(180deg, ${faradayTokens.color.surface.muted} 0%, ${faradayTokens.color.forest[50]} 100%)`,
        px: 3,
        py: 4,
        overflowY: "auto",
      }}
    >
      {/* Faint watercolor wash decoration */}
      <Box
        aria-hidden
        sx={{
          position: "absolute",
          top: 0,
          right: 0,
          width: "100%",
          height: 280,
          background:
            "radial-gradient(circle at 80% 20%, rgba(82, 183, 136, 0.18) 0%, transparent 60%)",
          pointerEvents: "none",
        }}
      />
      <Box sx={{ position: "relative" }}>{children}</Box>
    </Box>
  );
}
