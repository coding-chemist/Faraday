// AppShell — 3-column layout matching the Experiment + Ask mockups.
//
//   ┌──────────────────────────────────────────────────────────────────────┐
//   │  Wordmark            ·  breadcrumb  ·            avatar + action     │  TopBar
//   ├─────────┬────────────────────────────────────────────────┬───────────┤
//   │         │                                                │           │
//   │ Sidebar │             {children}                         │ RightRail │
//   │ (left)  │                                                │ (right)   │
//   │         │                                                │           │
//   └─────────┴────────────────────────────────────────────────┴───────────┘

import { Box } from "@mui/material";

import { faradayTokens } from "../../design/theme";
import { RightRail } from "./RightRail";
import { Sidebar } from "./Sidebar";
import { TopBar, type Crumb } from "./TopBar";

interface Props {
  crumbs?: Crumb[];
  topBarAction?: React.ReactNode;
  /** When provided, renders the right rail with this content. Omit on screens that don't need it. */
  rightRail?: React.ReactNode;
  children: React.ReactNode;
}

export function AppShell({ crumbs, topBarAction, rightRail, children }: Props) {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        minHeight: "100vh",
        background: faradayTokens.color.surface.base,
      }}
    >
      <TopBar crumbs={crumbs} action={topBarAction} />

      <Box sx={{ display: "flex", flex: 1, minHeight: 0 }}>
        <Sidebar />

        <Box
          component="main"
          sx={{
            flex: 1,
            overflowY: "auto",
            px: { xs: 3, md: 5 },
            py: 4,
          }}
        >
          {children}
        </Box>

        {rightRail && <RightRail>{rightRail}</RightRail>}
      </Box>
    </Box>
  );
}
