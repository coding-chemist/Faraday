// Reusable rounded panel with watercolor backdrop + optional botanical corner.

import { Box } from "@mui/material";

import { faradayTokens } from "../../design/theme";
import { BotanicalCorner } from "../illustrations/BotanicalCorner";
import { WatercolorWash } from "./WatercolorWash";

interface Props {
  children: React.ReactNode;
  /** Subtle for big content panels, card for inner nested panels. */
  variant?: "subtle" | "card";
  /** Distinct seed per panel so multiple panels on screen don't look identical. */
  seed?: number;
  /** Outer corner radius in pixels. Defaults to 22 to match mockup. */
  radius?: number;
  /** When set, draws a botanical line accent in the chosen corner. */
  botanical?: {
    position: "top-left" | "top-right" | "bottom-left" | "bottom-right";
    variant?: "eucalyptus" | "fern";
    size?: number;
    opacity?: number;
  };
  /** sx pass-through for padding overrides. */
  sx?: object;
}

export function WatercolorPanel({
  children,
  variant = "subtle",
  seed,
  radius = 22,
  botanical,
  sx,
}: Props) {
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
      {botanical && (
        <BotanicalCorner
          position={botanical.position}
          variant={botanical.variant ?? "eucalyptus"}
          size={botanical.size ?? 120}
          opacity={botanical.opacity ?? 0.4}
        />
      )}
      <Box sx={{ position: "relative", p: { xs: 3, md: 4 } }}>{children}</Box>
    </Box>
  );
}
