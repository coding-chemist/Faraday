// Realistic watercolor backdrop — SVG with discrete color "puddles", soft
// edge bleed via feDisplacementMap, and paper-grain texture via feTurbulence.
//
// The "pronounced" variant uses more puddles + bigger displacement to read
// like real watercolor paint on paper.
//
// Three variants:
//   subtle     main content panels — very faint sage wash + paper grain
//   pronounced right rail / hero illustration — visible sage + mint
//              variation, darker forest in corners, watercolor edge bleed
//   card       inner card backdrop — barely-there mint hint

import { useId } from "react";

type Variant = "subtle" | "pronounced" | "card";

interface Props {
  variant?: Variant;
  fill?: boolean;
  seed?: number;
}

interface WashSpec {
  cx: number;
  cy: number;
  r: number;
  color: string;
  opacity: number;
}

interface VariantConfig {
  base: string;
  paperFrequency: number;
  paperOpacity: number;
  edgeFrequency: number;
  edgeScale: number;
  washes: WashSpec[];
}

export function WatercolorWash({ variant = "subtle", fill = true, seed = 3 }: Props) {
  const uid = useId().replace(/:/g, "");
  const noiseId = `wc-noise-${uid}`;
  const edgeId = `wc-edge-${uid}`;

  const cfg = VARIANT_CONFIG[variant];

  return (
    <svg
      aria-hidden
      preserveAspectRatio="xMidYMid slice"
      style={
        fill
          ? {
              position: "absolute",
              inset: 0,
              width: "100%",
              height: "100%",
              pointerEvents: "none",
            }
          : { width: "100%", height: "100%" }
      }
    >
      <defs>
        {/* Paper grain */}
        <filter id={noiseId}>
          <feTurbulence
            type="fractalNoise"
            baseFrequency={cfg.paperFrequency}
            numOctaves={2}
            seed={seed}
          />
          <feColorMatrix
            values={`0 0 0 0 0.93
                     0 0 0 0 0.96
                     0 0 0 0 0.91
                     0 0 0 ${cfg.paperOpacity} 0`}
          />
        </filter>

        {/* Watercolor edge bleed — feDisplacementMap on the wash group */}
        <filter id={edgeId} x="-8%" y="-8%" width="116%" height="116%">
          <feTurbulence
            type="fractalNoise"
            baseFrequency={cfg.edgeFrequency}
            numOctaves={3}
            seed={seed + 7}
          />
          <feDisplacementMap in="SourceGraphic" scale={cfg.edgeScale} />
        </filter>

        {cfg.washes.map((w, i) => (
          <radialGradient key={i} id={`wc-w-${uid}-${i}`} cx={`${w.cx}%`} cy={`${w.cy}%`} r={`${w.r}%`}>
            <stop offset="0%" stopColor={w.color} stopOpacity={w.opacity} />
            <stop offset="50%" stopColor={w.color} stopOpacity={w.opacity * 0.55} />
            <stop offset="100%" stopColor={w.color} stopOpacity={0} />
          </radialGradient>
        ))}
      </defs>

      {/* Base paper */}
      <rect width="100%" height="100%" fill={cfg.base} />

      {/* Layered washes with organic edge displacement */}
      <g filter={`url(#${edgeId})`}>
        {cfg.washes.map((_, i) => (
          <rect key={i} width="100%" height="100%" fill={`url(#wc-w-${uid}-${i})`} />
        ))}
      </g>

      {/* Paper grain overlay */}
      <rect width="100%" height="100%" filter={`url(#${noiseId})`} />
    </svg>
  );
}

const VARIANT_CONFIG: Record<Variant, VariantConfig> = {
  subtle: {
    base: "#F4F9F2",
    paperFrequency: 0.7,
    paperOpacity: 0.22,
    edgeFrequency: 0.012,
    edgeScale: 8,
    washes: [
      { cx: 12, cy: 18, r: 50, color: "#C9E4D2", opacity: 0.75 },
      { cx: 78, cy: 32, r: 45, color: "#8FB89A", opacity: 0.45 },
      { cx: 32, cy: 72, r: 55, color: "#E6F2EA", opacity: 0.85 },
      { cx: 88, cy: 85, r: 50, color: "#52B788", opacity: 0.22 },
      { cx: 60, cy: 50, r: 40, color: "#C9E4D2", opacity: 0.5 },
    ],
  },
  pronounced: {
    base: "#E8F2EA",
    paperFrequency: 0.55,
    paperOpacity: 0.32,
    edgeFrequency: 0.02,
    edgeScale: 18,
    washes: [
      // Top-left mint puddle
      { cx: 18, cy: 12, r: 50, color: "#C9E4D2", opacity: 0.95 },
      // Top-right sage patch
      { cx: 80, cy: 22, r: 45, color: "#8FB89A", opacity: 0.75 },
      // Mid-right forest deepening
      { cx: 90, cy: 55, r: 40, color: "#52B788", opacity: 0.55 },
      // Center sage wash
      { cx: 45, cy: 50, r: 55, color: "#8FB89A", opacity: 0.45 },
      // Bottom-left light wash
      { cx: 15, cy: 75, r: 45, color: "#E6F2EA", opacity: 0.85 },
      // Bottom-right deep forest shadow
      { cx: 85, cy: 88, r: 38, color: "#2D6A4F", opacity: 0.28 },
      // Scattered mint highlight
      { cx: 50, cy: 90, r: 30, color: "#C9E4D2", opacity: 0.7 },
    ],
  },
  card: {
    base: "#FBFDFA",
    paperFrequency: 0.8,
    paperOpacity: 0.1,
    edgeFrequency: 0.015,
    edgeScale: 4,
    washes: [
      { cx: 15, cy: 20, r: 65, color: "#E6F2EA", opacity: 0.65 },
      { cx: 85, cy: 80, r: 60, color: "#C9E4D2", opacity: 0.4 },
      { cx: 50, cy: 50, r: 50, color: "#EFF5EF", opacity: 0.5 },
      { cx: 80, cy: 25, r: 30, color: "#8FB89A", opacity: 0.12 },
    ],
  },
};
