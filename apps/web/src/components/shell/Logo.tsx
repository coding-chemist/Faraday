// The F+ tile — deep forest square with white serif F and a small sparkle plus.
// Matches the corner sigil shown on every page mockup.

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
      <text
        x={18}
        y={40}
        fontFamily='"Fraunces", Georgia, serif'
        fontSize={32}
        fontWeight={600}
        fill="#FFFFFF"
      >
        F
      </text>
      <g transform="translate(38, 14)">
        <line x1={0} y1={5} x2={10} y2={5} stroke="#FFFFFF" strokeWidth={1.5} strokeLinecap="round" />
        <line x1={5} y1={0} x2={5} y2={10} stroke="#FFFFFF" strokeWidth={1.5} strokeLinecap="round" />
      </g>
    </svg>
  );
}
