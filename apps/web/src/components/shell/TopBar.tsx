import { Avatar, Box } from "@mui/material";
import { Fragment } from "react";

import { faradayTokens } from "../../design/theme";
import { Wordmark } from "./Wordmark";

export interface Crumb {
  label: string;
  href?: string;
}

interface Props {
  /** Breadcrumb items shown in the center. */
  crumbs?: Crumb[];
  /** Optional right-side action (e.g. 'Witnessed' pill on Experiment view). */
  action?: React.ReactNode;
}

export function TopBar({ crumbs = [], action }: Props) {
  return (
    <Box
      component="header"
      sx={{
        height: 72,
        px: 4,
        display: "grid",
        gridTemplateColumns: "1fr auto 1fr",
        alignItems: "center",
        gap: 3,
        background: faradayTokens.color.surface.base,
        borderBottom: `1px solid ${faradayTokens.color.forest[100]}`,
      }}
    >
      <Box>
        <Wordmark />
      </Box>

      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 1.5,
          fontFamily: faradayTokens.font.body,
          fontSize: 15,
          color: faradayTokens.color.ink.secondary,
        }}
      >
        {crumbs.map((crumb, i) => (
          <Fragment key={`${crumb.label}-${i}`}>
            {i > 0 && (
              <span aria-hidden style={{ color: faradayTokens.color.ink.tertiary }}>•</span>
            )}
            <span
              style={{
                color:
                  i === crumbs.length - 1
                    ? faradayTokens.color.ink.primary
                    : faradayTokens.color.ink.secondary,
                fontWeight: i === crumbs.length - 1 ? 500 : 400,
              }}
            >
              {crumb.label}
            </span>
          </Fragment>
        ))}
      </Box>

      <Box sx={{ display: "flex", alignItems: "center", justifyContent: "flex-end", gap: 2 }}>
        {action}
        <Avatar
          alt="Account"
          sx={{
            width: 38,
            height: 38,
            background: faradayTokens.color.forest[100],
            color: faradayTokens.color.forest[900],
            fontFamily: faradayTokens.font.body,
            fontWeight: 600,
            fontSize: 14,
          }}
        >
          SS
        </Avatar>
      </Box>
    </Box>
  );
}
