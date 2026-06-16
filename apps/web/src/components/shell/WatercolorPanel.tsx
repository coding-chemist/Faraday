// Reusable rounded panel with watercolor backdrop — used to wrap main content
// on Lab Memory screens so the page reads as one continuous watercolor canvas
// rather than disconnected white cards on a flat background.
//
// Border radius tuned to match the mockup: ~22px outer corner (softer than
// 32px but more definite than 16px). Tweak the `radius` prop if a specific
// caller needs different rounding.

import { Box } from "@mui/material";

import { faradayTokens } from "../../design/theme";
import { WatercolorWash } from "./WatercolorWash";

interface Props {
  children: React.ReactNode;
  /** Subtle for big content panels, card for inner nested panels. */
  variant?: "subtle" | "card";
  /** Distinct seed per panel so multiple panels on screen don't look identical. */
  seed?: number;
  /** Outer corner radius in pixels. Defaults to 22 to match mockup. */
  radius?: number;
  /** sx pass-through for padding overrides. */
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
