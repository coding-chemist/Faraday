// Right rail — pronounced sage watercolor backdrop. Optional botanical PNG
// overlays in two corners (top-right + bottom-left); each is opt-in via the
// presence of the file under /illustrations/. When missing, the corner is
// simply empty — no fake hand-drawn fallback that looks worse than nothing.

import { Box } from "@mui/material";

import { faradayTokens } from "../../design/theme";
import { WatercolorWash } from "./WatercolorWash";

interface Props {
  children: React.ReactNode;
}

function CornerImage({
  src,
  position,
}: {
  src: string;
  position: "top-right" | "bottom-left";
}) {
  const positionStyle =
    position === "top-right"
      ? { top: 0, right: 0 }
      : { bottom: 0, left: 0, transform: "scaleY(-1)" };
  return (
    <img
      src={src}
      alt=""
      aria-hidden
      style={{
        position: "absolute",
        width: 160,
        height: "auto",
        opacity: 0.5,
        pointerEvents: "none",
        ...positionStyle,
      }}
      onError={(e) => {
        // PNG missing — hide silently. Nothing is better than fake hand-drawn.
        (e.currentTarget as HTMLImageElement).style.display = "none";
      }}
    />
  );
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
      <CornerImage src="/illustrations/eucalyptus.png" position="top-right" />
      <CornerImage src="/illustrations/fern.png" position="bottom-left" />
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
