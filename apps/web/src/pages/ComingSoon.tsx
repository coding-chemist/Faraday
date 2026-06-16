// Placeholder for sidebar destinations not yet built in v0.1.
// Lives inside AppShell so the chrome looks alive when chemist clicks
// Watch, Compare, Notebook, etc.

import { Box, Typography } from "@mui/material";
import { Link as RouterLink } from "react-router-dom";

import { AppShell } from "../components/shell";
import { faradayTokens } from "../design/theme";

interface Props {
  title: string;
  crumbs: { label: string }[];
  blurb?: string;
}

export function ComingSoon({ title, crumbs, blurb }: Props) {
  return (
    <AppShell crumbs={crumbs}>
      <Box sx={{ maxWidth: 640, mx: "auto", pt: 6, textAlign: "center" }}>
        <Typography
          sx={{
            fontFamily: faradayTokens.font.mono,
            fontSize: 11,
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            color: faradayTokens.color.ink.secondary,
            mb: 2,
          }}
        >
          Coming in v0.2
        </Typography>
        <Typography
          component="h1"
          sx={{
            fontSize: { xs: 36, md: 48 },
            fontFamily: faradayTokens.font.display,
            fontWeight: 600,
            color: faradayTokens.color.ink.primary,
            mb: 2,
            lineHeight: 1.1,
          }}
        >
          {title}
        </Typography>
        {blurb && (
          <Typography
            sx={{
              fontSize: 17,
              color: faradayTokens.color.ink.secondary,
              fontStyle: "italic",
              mb: 4,
              lineHeight: 1.6,
            }}
          >
            {blurb}
          </Typography>
        )}
        <RouterLink
          to="/memory/ask"
          style={{
            color: faradayTokens.color.forest[700],
            fontFamily: faradayTokens.font.body,
            fontSize: 15,
            textDecoration: "none",
          }}
        >
          → try Ask mode instead
        </RouterLink>
      </Box>
    </AppShell>
  );
}
