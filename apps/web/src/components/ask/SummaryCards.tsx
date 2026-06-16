// Summary cards — icon + inline label/value layout per mockup.
// Icons are hand-drawn SVGs in the editorial line-work register, not MUI defaults.

import { Box, Card, Typography } from "@mui/material";

import { faradayTokens } from "../../design/theme";
import type { SummaryCard as SummaryCardType } from "../../types/analysis";
import { WatercolorWash } from "../shell/WatercolorWash";

interface Props {
  cards: SummaryCardType[];
}

/** Notebook-paper icon for "experiments matched". */
function NotebookIcon() {
  return (
    <svg width={44} height={48} viewBox="0 0 44 48" fill="none" aria-hidden>
      <rect x={6} y={3} width={32} height={42} rx={2.5}
        stroke={faradayTokens.color.forest[700]} strokeWidth={1.4} fill="#FFFFFF" />
      <line x1={6} y1={9} x2={2} y2={9} stroke={faradayTokens.color.forest[700]} strokeWidth={1.4} strokeLinecap="round" />
      <line x1={6} y1={17} x2={2} y2={17} stroke={faradayTokens.color.forest[700]} strokeWidth={1.4} strokeLinecap="round" />
      <line x1={6} y1={25} x2={2} y2={25} stroke={faradayTokens.color.forest[700]} strokeWidth={1.4} strokeLinecap="round" />
      <line x1={6} y1={33} x2={2} y2={33} stroke={faradayTokens.color.forest[700]} strokeWidth={1.4} strokeLinecap="round" />
      <line x1={12} y1={14} x2={32} y2={14} stroke={faradayTokens.color.forest[500]} strokeWidth={1} />
      <line x1={12} y1={20} x2={28} y2={20} stroke={faradayTokens.color.forest[500]} strokeWidth={1} />
      <line x1={12} y1={26} x2={30} y2={26} stroke={faradayTokens.color.forest[500]} strokeWidth={1} />
      <line x1={12} y1={32} x2={26} y2={32} stroke={faradayTokens.color.forest[500]} strokeWidth={1} />
    </svg>
  );
}

/** Mini bar-chart icon for "average yield". */
function BarChartIcon() {
  return (
    <svg width={48} height={48} viewBox="0 0 48 48" fill="none" aria-hidden>
      <line x1={6} y1={42} x2={42} y2={42} stroke={faradayTokens.color.forest[700]} strokeWidth={1.4} strokeLinecap="round" />
      <line x1={6} y1={42} x2={6} y2={6} stroke={faradayTokens.color.forest[700]} strokeWidth={1.4} strokeLinecap="round" />
      <rect x={12} y={26} width={5} height={16} fill={faradayTokens.color.forest[300]} rx={0.5} />
      <rect x={20} y={18} width={5} height={24} fill={faradayTokens.color.forest[500]} rx={0.5} />
      <rect x={28} y={14} width={5} height={28} fill={faradayTokens.color.forest[700]} rx={0.5} />
      <rect x={36} y={22} width={5} height={20} fill={faradayTokens.color.forest[300]} rx={0.5} />
    </svg>
  );
}

/** Molecule (hexagon with a bond) icon for "most common catalyst". */
function MoleculeIcon() {
  return (
    <svg width={52} height={48} viewBox="0 0 52 48" fill="none" aria-hidden>
      <g stroke={faradayTokens.color.forest[700]} strokeWidth={1.4} strokeLinecap="round" fill="none">
        {/* Hexagon */}
        <polygon points="32,8 42,14 42,26 32,32 22,26 22,14" />
        {/* Bond stub */}
        <line x1={22} y1={20} x2={12} y2={20} />
        <circle cx={10} cy={20} r={2.5} fill="#FFFFFF" />
        {/* Inner ring (aromatic) */}
        <circle cx={32} cy={20} r={5} stroke={faradayTokens.color.forest[500]} />
        {/* Branch */}
        <line x1={42} y1={14} x2={48} y2={10} />
        <circle cx={49} cy={9} r={2} fill="#FFFFFF" />
      </g>
    </svg>
  );
}

const ICONS: Record<string, React.ComponentType> = {
  "matched experiments": NotebookIcon,
  "average yield": BarChartIcon,
  "most common catalyst": MoleculeIcon,
};

function iconFor(label: string): React.ComponentType {
  return ICONS[label.toLowerCase()] ?? NotebookIcon;
}

export function SummaryCards({ cards }: Props) {
  if (cards.length === 0) return null;

  return (
    <Box
      role="list"
      aria-label="result summary"
      sx={{
        display: "grid",
        gridTemplateColumns: {
          xs: "1fr",
          sm: "repeat(2, 1fr)",
          md: `repeat(${Math.min(cards.length, 4)}, 1fr)`,
        },
        gap: 2.5,
      }}
    >
      {cards.map((card, i) => {
        const Icon = iconFor(card.label);
        return (
          <Card
            key={card.label}
            role="listitem"
            elevation={0}
            sx={{
              position: "relative",
              borderRadius: 2,
              overflow: "hidden",
              border: `1px solid ${faradayTokens.color.forest[100]}`,
              transition: "border-color 200ms ease-out, box-shadow 200ms ease-out",
              "&:hover": {
                borderColor: faradayTokens.color.forest[300],
                boxShadow: "0 4px 12px rgba(45, 106, 79, 0.10)",
              },
            }}
          >
            <WatercolorWash variant="card" seed={11 + i * 3} />
            <Box
              sx={{
                position: "relative",
                p: 2.5,
                display: "flex",
                alignItems: "center",
                gap: 2,
                minHeight: 96,
              }}
            >
              <Box sx={{ flexShrink: 0 }}>
                <Icon />
              </Box>
              <Box sx={{ flex: 1, minWidth: 0 }}>
                <Typography
                  component="div"
                  sx={{
                    fontSize: 13,
                    color: faradayTokens.color.ink.secondary,
                    fontFamily: faradayTokens.font.body,
                    mb: 0.25,
                  }}
                >
                  {card.label}:
                </Typography>
                <Typography
                  component="div"
                  sx={{
                    fontSize: 24,
                    fontWeight: 600,
                    // JetBrains Mono on the numeric value matches Curie's editorial
                    // numerals — same family across portfolio for stat displays.
                    fontFamily: faradayTokens.font.mono,
                    fontFeatureSettings: '"tnum" 1',
                    lineHeight: 1.15,
                    letterSpacing: "-0.01em",
                    color: faradayTokens.color.forest[900],
                  }}
                >
                  {card.value}
                </Typography>
                {card.sublabel && (
                  <Typography
                    component="div"
                    sx={{
                      fontSize: 12,
                      color: faradayTokens.color.ink.secondary,
                      mt: 0.25,
                      fontStyle: "italic",
                    }}
                  >
                    {card.sublabel}
                  </Typography>
                )}
              </Box>
            </Box>
          </Card>
        );
      })}
    </Box>
  );
}
