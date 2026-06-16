// Right rail — sage watercolor backdrop with botanical eucalyptus accents.

import { Box } from "@mui/material";

import { faradayTokens } from "../../design/theme";
import { BotanicalCorner } from "../illustrations/BotanicalCorner";
import { WatercolorWash } from "./WatercolorWash";

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
        overflow: "hidden",
      }}
    >
      <WatercolorWash variant="pronounced" seed={11} />
      <BotanicalCorner position="top-right" variant="eucalyptus" size={160} opacity={0.45} />
      <BotanicalCorner position="bottom-left" variant="fern" size={140} opacity={0.4} />
      <Box
        sx={{
          position: "relative",
          px: 3,
          py: 4,
          height: "100%",
          overflowY: "auto",
        }}
      >
        {children}
      </Box>
    </Box>
  );
}
