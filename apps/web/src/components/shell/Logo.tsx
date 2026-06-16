// The F+ tile — deep forest square with white serif F and a small sparkle plus
// in the top-right corner. Matches the corner sigil on every page mockup.

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
      <rect
        x={0}
        y={0}
        width={56}
        height={56}
        rx={12}
        fill={faradayTokens.color.forest[700]}
      />
      {/* Serif F */}
      <text
        x={14}
        y={42}
        fontFamily='"Fraunces", "Tiempos Headline", Georgia, serif'
        fontSize={38}
        fontWeight={600}
        fill="#FFFFFF"
      >
        F
      </text>
      {/* Sparkle plus — small + symbol in the top-right */}
      <g
        transform="translate(42, 12)"
        stroke="#FFFFFF"
        strokeWidth={1.6}
        strokeLinecap="round"
        fill="none"
      >
        <line x1={0} y1={5} x2={10} y2={5} />
        <line x1={5} y1={0} x2={5} y2={10} />
      </g>
    </svg>
  );
}
