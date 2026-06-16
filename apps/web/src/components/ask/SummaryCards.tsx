// Summary cards — vertical stat-tile layout. Icon top-left, eyebrow label,
// large mono value, optional sublabel. Material icons (forest-green tint) so
// they read as familiar rather than illustrated.

import BarChartOutlinedIcon from "@mui/icons-material/BarChartOutlined";
import HubOutlinedIcon from "@mui/icons-material/HubOutlined";
import MenuBookOutlinedIcon from "@mui/icons-material/MenuBookOutlined";
import TrendingDownOutlinedIcon from "@mui/icons-material/TrendingDownOutlined";
import TrendingUpOutlinedIcon from "@mui/icons-material/TrendingUpOutlined";
import ScienceOutlinedIcon from "@mui/icons-material/ScienceOutlined";
import type { SvgIconProps } from "@mui/material";
import { Box, Card, Typography } from "@mui/material";

import { faradayTokens } from "../../design/theme";
import type { SummaryCard as SummaryCardType } from "../../types/analysis";
import { WatercolorWash } from "../shell/WatercolorWash";

interface Props {
  cards: SummaryCardType[];
}

type IconComponent = React.ComponentType<SvgIconProps>;

const ICONS: Record<string, IconComponent> = {
  "matched experiments": MenuBookOutlinedIcon,
  "average yield": BarChartOutlinedIcon,
  "most common catalyst": HubOutlinedIcon,
  "worst yield": TrendingDownOutlinedIcon,
  "best yield": TrendingUpOutlinedIcon,
};

function iconFor(label: string): IconComponent {
  return ICONS[label.toLowerCase()] ?? ScienceOutlinedIcon;
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
        gap: 2,
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
              borderRadius: 1.5,
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
                p: 2,
                display: "flex",
                flexDirection: "column",
                gap: 0.5,
                minHeight: 132,
              }}
            >
              <Box sx={{ mb: 0.5 }}>
                <Icon
                  sx={{
                    fontSize: 28,
                    color: faradayTokens.color.forest[700],
                  }}
                />
              </Box>
              <Typography
                component="div"
                sx={{
                  fontFamily: faradayTokens.font.mono,
                  fontSize: 10.5,
                  fontWeight: 500,
                  letterSpacing: "0.09em",
                  textTransform: "uppercase",
                  color: faradayTokens.color.ink.secondary,
                  lineHeight: 1.2,
                }}
              >
                {card.label}
              </Typography>
              <Typography
                component="div"
                sx={{
                  fontFamily: faradayTokens.font.mono,
                  fontSize: 22,
                  fontWeight: 600,
                  fontFeatureSettings: '"tnum" 1',
                  lineHeight: 1.2,
                  letterSpacing: "-0.01em",
                  color: faradayTokens.color.forest[900],
                  wordBreak: "break-word",
                }}
                title={card.value}
              >
                {card.value}
              </Typography>
              {card.sublabel && (
                <Typography
                  component="div"
                  sx={{
                    fontFamily: faradayTokens.font.mono,
                    fontSize: 11,
                    color: faradayTokens.color.ink.secondary,
                    lineHeight: 1.35,
                    mt: "auto",
                  }}
                  title={card.sublabel}
                >
                  {card.sublabel}
                </Typography>
              )}
            </Box>
          </Card>
        );
      })}
    </Box>
  );
}
