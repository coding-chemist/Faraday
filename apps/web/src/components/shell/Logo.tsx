// The F+ tile — deep forest square with a serif F and a 4-point sparkle.
// Sparkle replaces the previous plain plus sign per mockup.

import { faradayTokens } from "../../design/theme";

interface Props {
  size?: number;
}

export function Logo({ size = 56 }: Props) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 56 56"
      role="img"
      aria-label="Faraday"
      style={{ display: "block" }}
    >
      <rect x={0} y={0} width={56} height={56} rx={12} fill={faradayTokens.color.forest[700]} />

      {/* Serif F — Fraunces forced via inline style so SVG picks up the loaded webfont */}
      <text
        x={14}
        y={43}
        fontSize={40}
        fontWeight={600}
        fill="#FFFFFF"
        style={{ fontFamily: '"Fraunces", "Tiempos Headline", Georgia, serif' }}
      >
        F
      </text>

      {/* 4-point sparkle (✦) — kite shape with long vertical points */}
      <path
        d="M44.5 11 L45.5 17.5 L52 18.5 L45.5 19.5 L44.5 26 L43.5 19.5 L37 18.5 L43.5 17.5 Z"
        fill="#FFFFFF"
      />
    </svg>
  );
}
