// Botanical line-corner accent — eucalyptus branch or fern frond, sage line work.
// Spec §3.0.4: "botanical line corners on hero / landing / empty states — same
// eucalyptus + fern style as Curie + Darwin."
//
// Decorative only. Positioned absolutely in a corner of its parent (which must
// have position: relative + overflow: hidden). Low-opacity so it reads as a
// quiet watermark behind content, not a competing visual.

import { faradayTokens } from "../../design/theme";

type Position = "top-left" | "top-right" | "bottom-left" | "bottom-right";
type Variant = "eucalyptus" | "fern";

interface Props {
  size?: number;
  position?: Position;
  variant?: Variant;
  /** 0..1 — lower = more watermark-like. Defaults to 0.55. */
  opacity?: number;
}

export function BotanicalCorner({
  size = 140,
  position = "top-right",
  variant = "eucalyptus",
  opacity = 0.55,
}: Props) {
  const positionStyle = positionStyles[position];
  return (
    <div
      aria-hidden
      style={{
        position: "absolute",
        width: size,
        height: size,
        opacity,
        pointerEvents: "none",
        ...positionStyle,
      }}
    >
      {variant === "eucalyptus" ? <Eucalyptus /> : <Fern />}
    </div>
  );
}

const positionStyles: Record<Position, React.CSSProperties> = {
  "top-left": { top: -12, left: -12, transform: "rotate(180deg)" },
  "top-right": { top: -12, right: -12, transform: "scaleX(-1) rotate(180deg)" },
  "bottom-left": { bottom: -12, left: -12, transform: "rotate(0deg)" },
  "bottom-right": { bottom: -12, right: -12, transform: "scaleX(-1)" },
};

function Eucalyptus() {
  const stroke = faradayTokens.color.botanical.line;
  return (
    <svg
      viewBox="0 0 140 140"
      width="100%"
      height="100%"
      fill="none"
      stroke={stroke}
      strokeWidth={1.2}
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      {/* Stem — curves from top-right toward bottom-left */}
      <path d="M 128 12 Q 100 32 80 60 Q 55 95 18 122" />

      {/* Leaves — alternating left/right pairs along the stem */}
      <Leaf cx={115} cy={20} rx={5.5} ry={11} angle={-58} stroke={stroke} />
      <Leaf cx={105} cy={28} rx={5.5} ry={11} angle={35} stroke={stroke} />

      <Leaf cx={92} cy={44} rx={5.5} ry={11} angle={-50} stroke={stroke} />
      <Leaf cx={83} cy={52} rx={5.5} ry={11} angle={42} stroke={stroke} />

      <Leaf cx={72} cy={70} rx={5.5} ry={11} angle={-48} stroke={stroke} />
      <Leaf cx={62} cy={78} rx={5.5} ry={11} angle={45} stroke={stroke} />

      <Leaf cx={48} cy={94} rx={5.5} ry={11} angle={-46} stroke={stroke} />
      <Leaf cx={37} cy={103} rx={5.5} ry={11} angle={47} stroke={stroke} />

      <Leaf cx={25} cy={115} rx={4.5} ry={9} angle={-44} stroke={stroke} />
    </svg>
  );
}

interface LeafProps {
  cx: number;
  cy: number;
  rx: number;
  ry: number;
  angle: number;
  stroke: string;
}

function Leaf({ cx, cy, rx, ry, angle, stroke }: LeafProps) {
  return (
    <g transform={`rotate(${angle} ${cx} ${cy})`}>
      <ellipse cx={cx} cy={cy} rx={rx} ry={ry} fill="none" stroke={stroke} />
      {/* Central vein */}
      <line
        x1={cx}
        y1={cy - ry + 1.5}
        x2={cx}
        y2={cy + ry - 1.5}
        stroke={stroke}
        strokeWidth={0.7}
      />
    </g>
  );
}

function Fern() {
  const stroke = faradayTokens.color.botanical.line;
  return (
    <svg
      viewBox="0 0 110 140"
      width="100%"
      height="100%"
      fill="none"
      stroke={stroke}
      strokeWidth={1.1}
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      {/* Central stem — gentle S-curve */}
      <path d="M 80 8 Q 70 50 58 90 Q 50 115 38 132" />

      {/* Pinnate leaflets — pairs from base (large) to tip (small) */}
      {LEAFLET_PAIRS.map((p, i) => (
        <g key={i}>
          {/* Left leaflet */}
          <path d={`M ${p.x} ${p.y} Q ${p.x - p.len * 0.45} ${p.y + p.curve} ${p.x - p.len} ${p.y + p.tipOffset}`} />
          {/* Right leaflet */}
          <path d={`M ${p.x} ${p.y} Q ${p.x + p.len * 0.45} ${p.y + p.curve} ${p.x + p.len} ${p.y + p.tipOffset}`} />
        </g>
      ))}
    </svg>
  );
}

const LEAFLET_PAIRS: { x: number; y: number; len: number; curve: number; tipOffset: number }[] = [
  { x: 78, y: 16, len: 14, curve: 4, tipOffset: 8 },
  { x: 75, y: 30, len: 18, curve: 5, tipOffset: 10 },
  { x: 71, y: 45, len: 22, curve: 6, tipOffset: 12 },
  { x: 66, y: 62, len: 24, curve: 7, tipOffset: 14 },
  { x: 60, y: 80, len: 22, curve: 6, tipOffset: 12 },
  { x: 54, y: 98, len: 18, curve: 5, tipOffset: 10 },
  { x: 47, y: 115, len: 13, curve: 4, tipOffset: 7 },
];
