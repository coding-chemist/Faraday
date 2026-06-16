// Realistic watercolor backdrop — SVG with multiple overlapping radial gradients,
// fractal-noise paper texture, and soft edge bleed. Matches the spec §3.0.4
// "naturalist editorial style" / "soft watercolor backdrop" for product UI.
//
// Variants:
//   subtle     main content panels — very faint sage wash + paper grain
//   pronounced right rail / hero illustration backdrops — visible sage + mint
//              variation, darker in corners, watercolor edge
//   card       inner card backdrop — barely-there mint hint

import { useId } from "react";

type Variant = "subtle" | "pronounced" | "card";

interface Props {
  variant?: Variant;
  /** Position absolute fill behind content (default true). */
  fill?: boolean;
  /** Override seed for reproducible-but-distinct washes on each component. */
  seed?: number;
}

export function WatercolorWash({ variant = "subtle", fill = true, seed = 3 }: Props) {
  // useId gives unique filter/gradient IDs per instance so multiple washes coexist
  const uid = useId().replace(/:/g, "");

  const noiseId = `wc-noise-${uid}`;
  const edgeId = `wc-edge-${uid}`;
  const wash1Id = `wc-w1-${uid}`;
  const wash2Id = `wc-w2-${uid}`;
  const wash3Id = `wc-w3-${uid}`;
  const wash4Id = `wc-w4-${uid}`;

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
        {/* Paper grain — fractal noise tinted to a near-paper hue, low opacity */}
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

        {/* Watercolor edge — slight displacement so washes bleed organically */}
        <filter id={edgeId} x="-5%" y="-5%" width="110%" height="110%">
          <feTurbulence type="fractalNoise" baseFrequency={cfg.edgeFrequency} numOctaves={3} seed={seed + 7} />
          <feDisplacementMap in="SourceGraphic" scale={cfg.edgeScale} />
        </filter>

        {cfg.washes.map((w, i) => {
          const ids = [wash1Id, wash2Id, wash3Id, wash4Id];
          return (
            <radialGradient
              key={i}
              id={ids[i]}
              cx={`${w.cx}%`}
              cy={`${w.cy}%`}
              r={`${w.r}%`}
            >
              <stop offset="0%" stopColor={w.color} stopOpacity={w.opacity} />
              <stop offset="60%" stopColor={w.color} stopOpacity={w.opacity * 0.4} />
              <stop offset="100%" stopColor={w.color} stopOpacity={0} />
            </radialGradient>
          );
        })}
      </defs>

      {/* Base paper color */}
      <rect width="100%" height="100%" fill={cfg.base} />

      {/* Layered washes with soft edge displacement */}
      <g filter={`url(#${edgeId})`}>
        {cfg.washes.map((_, i) => {
          const ids = [wash1Id, wash2Id, wash3Id, wash4Id];
          return <rect key={i} width="100%" height="100%" fill={`url(#${ids[i]})`} />;
        })}
      </g>

      {/* Paper grain overlay */}
      <rect width="100%" height="100%" filter={`url(#${noiseId})`} />
    </svg>
  );
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

const VARIANT_CONFIG: Record<Variant, VariantConfig> = {
  subtle: {
    base: "#F7FAF6",
    paperFrequency: 0.7,
    paperOpacity: 0.18,
    edgeFrequency: 0.012,
    edgeScale: 6,
    washes: [
      { cx: 15, cy: 25, r: 65, color: "#E6F2EA", opacity: 0.85 },
      { cx: 75, cy: 35, r: 55, color: "#C9E4D2", opacity: 0.45 },
      { cx: 50, cy: 80, r: 70, color: "#EFF5EF", opacity: 0.7 },
      { cx: 90, cy: 90, r: 50, color: "#8FB89A", opacity: 0.18 },
    ],
  },
  pronounced: {
    base: "#EFF5EF",
    paperFrequency: 0.55,
    paperOpacity: 0.28,
    edgeFrequency: 0.018,
    edgeScale: 14,
    washes: [
      { cx: 20, cy: 15, r: 70, color: "#C9E4D2", opacity: 0.85 },
      { cx: 75, cy: 30, r: 60, color: "#8FB89A", opacity: 0.55 },
      { cx: 50, cy: 75, r: 80, color: "#52B788", opacity: 0.28 },
      { cx: 90, cy: 95, r: 55, color: "#2D6A4F", opacity: 0.16 },
    ],
  },
  card: {
    base: "#FFFFFF",
    paperFrequency: 0.8,
    paperOpacity: 0.08,
    edgeFrequency: 0.015,
    edgeScale: 3,
    washes: [
      { cx: 10, cy: 10, r: 80, color: "#E6F2EA", opacity: 0.5 },
      { cx: 90, cy: 90, r: 70, color: "#C9E4D2", opacity: 0.3 },
      { cx: 50, cy: 50, r: 60, color: "#EFF5EF", opacity: 0.4 },
      { cx: 80, cy: 20, r: 40, color: "#8FB89A", opacity: 0.08 },
    ],
  },
};
