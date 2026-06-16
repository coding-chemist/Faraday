// Reusable rounded panel with watercolor backdrop.

import { Box } from "@mui/material";

import { faradayTokens } from "../../design/theme";
import { WatercolorWash } from "./WatercolorWash";

interface Props {
  children: React.ReactNode;
  variant?: "subtle" | "card";
  seed?: number;
  /** Outer corner radius in pixels. Defaults to 22 to match mockup. */
  radius?: number;
  sx?: object;
}

export function WatercolorPanel({ children, variant = "subtle", seed, radius = 22, sx }: Props) {
  return (
    <Box
      sx={{
        position: "relative",
        borderRadius: `${radius}px`,
        overflow: "hidden",
        border: `1px solid ${faradayTokens.color.forest[100]}`,
        ...sx,
      }}
    >
      <WatercolorWash variant={variant} seed={seed} />
      <Box sx={{ position: "relative", p: { xs: 3, md: 4 } }}>{children}</Box>
    </Box>
  );
}
