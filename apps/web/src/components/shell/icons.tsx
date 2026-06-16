// Hand-drawn editorial line-work icons for the sidebar.
//
// All icons share: 20x20 viewBox, 1.5 stroke width, currentColor stroke,
// no fill, round line caps + joins. They inherit color from the parent
// (so active state shifts the icon color along with the text).

import type { SVGProps } from "react";

const base: SVGProps<SVGSVGElement> = {
  width: 20,
  height: 20,
  viewBox: "0 0 20 20",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.5,
  strokeLinecap: "round",
  strokeLinejoin: "round",
  "aria-hidden": true,
};

export function NotebookIcon() {
  return (
    <svg {...base}>
      {/* Spiral binding holes on the left */}
      <circle cx={3.5} cy={5.5} r={0.9} />
      <circle cx={3.5} cy={10} r={0.9} />
      <circle cx={3.5} cy={14.5} r={0.9} />
      {/* Notebook body */}
      <rect x={5.5} y={2.5} width={11} height={15} rx={1.2} />
      {/* Ruled lines */}
      <line x1={8} y1={6.5} x2={14} y2={6.5} />
      <line x1={8} y1={10} x2={14} y2={10} />
      <line x1={8} y1={13.5} x2={12.5} y2={13.5} />
    </svg>
  );
}

export function ReagentsIcon() {
  return (
    <svg {...base}>
      {/* Erlenmeyer flask outline */}
      <path d="M8 2.5 L8 7.5 L4.2 15.5 Q4 17 5.5 17 L14.5 17 Q16 17 15.8 15.5 L12 7.5 L12 2.5" />
      {/* Top rim */}
      <line x1={7} y1={2.5} x2={13} y2={2.5} />
      {/* Liquid surface waves */}
      <path d="M6 13 Q7.3 12.3 8.5 13 Q9.8 13.7 11.5 13 Q12.7 12.4 14 13" />
    </svg>
  );
}

export function DataIcon() {
  return (
    <svg {...base}>
      {/* Axes */}
      <line x1={3} y1={3} x2={3} y2={17} />
      <line x1={3} y1={17} x2={17} y2={17} />
      {/* Bars */}
      <line x1={6.5} y1={13} x2={6.5} y2={17} strokeWidth={2.5} />
      <line x1={10} y1={9.5} x2={10} y2={17} strokeWidth={2.5} />
      <line x1={13.5} y1={6.5} x2={13.5} y2={17} strokeWidth={2.5} />
    </svg>
  );
}

export function StructureIcon() {
  return (
    <svg {...base}>
      {/* Central atom */}
      <circle cx={10} cy={10} r={1.8} />
      {/* Outer atoms */}
      <circle cx={4} cy={5} r={1.4} />
      <circle cx={16} cy={5} r={1.4} />
      <circle cx={4} cy={15} r={1.4} />
      <circle cx={16} cy={15} r={1.4} />
      {/* Bonds */}
      <line x1={5} y1={6} x2={8.7} y2={9} />
      <line x1={15} y1={6} x2={11.3} y2={9} />
      <line x1={5} y1={14} x2={8.7} y2={11} />
      <line x1={15} y1={14} x2={11.3} y2={11} />
    </svg>
  );
}

export function ProtocolsIcon() {
  return (
    <svg {...base}>
      {/* Clipboard body */}
      <rect x={4} y={4} width={12} height={14} rx={1.2} />
      {/* Clip at top */}
      <rect x={7.5} y={2} width={5} height={3} rx={0.6} />
      {/* Checklist lines */}
      <line x1={9} y1={8.5} x2={13.5} y2={8.5} />
      <line x1={9} y1={12} x2={13.5} y2={12} />
      <line x1={9} y1={15.5} x2={13.5} y2={15.5} />
      {/* Check mark on first item */}
      <polyline points="6,8.5 6.8,9.3 8,7.7" />
    </svg>
  );
}

export function TemplatesIcon() {
  return (
    <svg {...base}>
      <rect x={3} y={3} width={6} height={6} rx={1} />
      <rect x={11} y={3} width={6} height={6} rx={1} />
      <rect x={3} y={11} width={6} height={6} rx={1} />
      <rect x={11} y={11} width={6} height={6} rx={1} />
    </svg>
  );
}

export function LabMemoryIcon() {
  return (
    <svg {...base}>
      {/* Brain — two lobes */}
      <path d="M10 3.5 Q6.5 2.5 5 5 Q3.5 6 3.5 8 Q3 10 4.5 11 Q4 13 5.5 14 Q5.5 16 7.5 16.5 Q9 17 10 16.5" />
      <path d="M10 3.5 Q13.5 2.5 15 5 Q16.5 6 16.5 8 Q17 10 15.5 11 Q16 13 14.5 14 Q14.5 16 12.5 16.5 Q11 17 10 16.5" />
      {/* Center seam */}
      <line x1={10} y1={3.5} x2={10} y2={16.5} />
      {/* Wrinkles */}
      <path d="M5.5 7.5 Q6.5 7 7.5 7.5" />
      <path d="M5.5 11 Q6.5 10.5 7.5 11" />
      <path d="M12.5 7.5 Q13.5 7 14.5 7.5" />
      <path d="M12.5 11 Q13.5 10.5 14.5 11" />
    </svg>
  );
}

export function WatchIcon() {
  return (
    <svg {...base}>
      {/* Eye almond shape */}
      <path d="M2.5 10 Q5.5 4.5 10 4.5 Q14.5 4.5 17.5 10 Q14.5 15.5 10 15.5 Q5.5 15.5 2.5 10 Z" />
      {/* Pupil */}
      <circle cx={10} cy={10} r={2.3} />
      {/* Highlight (filled small dot) */}
      <circle cx={10} cy={10} r={0.8} fill="currentColor" stroke="none" />
    </svg>
  );
}

export function AskIcon() {
  return (
    <svg {...base}>
      {/* Magnifying glass circle */}
      <circle cx={8.5} cy={8.5} r={4.8} />
      {/* Handle */}
      <line x1={12.2} y1={12.2} x2={16.5} y2={16.5} />
    </svg>
  );
}

export function CompareIcon() {
  return (
    <svg {...base}>
      {/* Vertical post */}
      <line x1={10} y1={4} x2={10} y2={16.5} />
      {/* Center hub */}
      <circle cx={10} cy={3.5} r={1} />
      {/* Crossbar */}
      <line x1={3.5} y1={6.5} x2={16.5} y2={6.5} />
      {/* Left pan */}
      <path d="M3.5 6.5 L2 11 L5 11 Z" />
      {/* Right pan */}
      <path d="M16.5 6.5 L15 11 L18 11 Z" />
      {/* Base */}
      <line x1={7} y1={16.5} x2={13} y2={16.5} />
    </svg>
  );
}

export function SettingsIcon() {
  return (
    <svg {...base}>
      {/* Gear teeth — 8 short radial lines */}
      <line x1={10} y1={2.5} x2={10} y2={4.5} />
      <line x1={10} y1={15.5} x2={10} y2={17.5} />
      <line x1={2.5} y1={10} x2={4.5} y2={10} />
      <line x1={15.5} y1={10} x2={17.5} y2={10} />
      <line x1={4.7} y1={4.7} x2={6.1} y2={6.1} />
      <line x1={13.9} y1={13.9} x2={15.3} y2={15.3} />
      <line x1={15.3} y1={4.7} x2={13.9} y2={6.1} />
      <line x1={6.1} y1={13.9} x2={4.7} y2={15.3} />
      {/* Center circle */}
      <circle cx={10} cy={10} r={3} />
    </svg>
  );
}
