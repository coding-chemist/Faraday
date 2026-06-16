// Left sidebar with the F+ logo, primary nav, and Lab Memory sub-nav.
//
// Active state derives from current pathname. Items that route to pages
// we haven't built yet (Notebook, Reagents, Data, Structure, Protocols,
// Templates, Settings) are rendered with reduced opacity + "coming" tooltip
// so the chrome feels complete without misleading clicks.

import BarChartIcon from "@mui/icons-material/BarChart";
import CompareArrowsIcon from "@mui/icons-material/CompareArrows";
import DescriptionIcon from "@mui/icons-material/DescriptionOutlined";
import ExpandLess from "@mui/icons-material/ExpandLess";
import ExpandMore from "@mui/icons-material/ExpandMore";
import GridViewIcon from "@mui/icons-material/GridViewOutlined";
import HubIcon from "@mui/icons-material/Hub";
import ListAltIcon from "@mui/icons-material/ListAltOutlined";
import PsychologyAltIcon from "@mui/icons-material/PsychologyAltOutlined";
import ScienceIcon from "@mui/icons-material/ScienceOutlined";
import SearchIcon from "@mui/icons-material/SearchOutlined";
import SettingsIcon from "@mui/icons-material/SettingsOutlined";
import VisibilityIcon from "@mui/icons-material/VisibilityOutlined";
import { Box, Tooltip } from "@mui/material";
import type { ComponentType } from "react";
import { Link as RouterLink, useLocation } from "react-router-dom";

import { faradayTokens } from "../../design/theme";
import { Logo } from "./Logo";

interface NavItem {
  label: string;
  href: string;
  icon: ComponentType<{ sx?: object }>;
  /** When true, the item is rendered greyed-out with a 'coming soon' tooltip. */
  comingSoon?: boolean;
  children?: NavItem[];
}

const PRIMARY_NAV: NavItem[] = [
  { label: "Notebook", href: "/notebook", icon: DescriptionIcon, comingSoon: true },
  { label: "Reagents", href: "/reagents", icon: ScienceIcon, comingSoon: true },
  { label: "Data", href: "/data", icon: BarChartIcon, comingSoon: true },
  { label: "Structure", href: "/structure", icon: HubIcon, comingSoon: true },
  { label: "Protocols", href: "/protocols", icon: ListAltIcon, comingSoon: true },
  { label: "Templates", href: "/templates", icon: GridViewIcon, comingSoon: true },
  {
    label: "Lab Memory",
    href: "/memory",
    icon: PsychologyAltIcon,
    children: [
      { label: "Watch", href: "/memory/watch", icon: VisibilityIcon, comingSoon: true },
      { label: "Ask", href: "/memory/ask", icon: SearchIcon },
      { label: "Compare", href: "/memory/compare", icon: CompareArrowsIcon, comingSoon: true },
    ],
  },
];

const FOOTER_NAV: NavItem[] = [
  { label: "Settings", href: "/settings", icon: SettingsIcon, comingSoon: true },
];

interface NavRowProps {
  item: NavItem;
  active: boolean;
  depth?: number;
  expanded?: boolean;
  onToggleExpand?: () => void;
}

function NavRow({ item, active, depth = 0, expanded, onToggleExpand }: NavRowProps) {
  const Icon = item.icon;
  const isExpandable = !!item.children?.length;
  const isComing = !!item.comingSoon;

  const content = (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        gap: 1.5,
        px: 1.5,
        py: 1,
        ml: depth * 2,
        borderRadius: 1.5,
        fontFamily: faradayTokens.font.body,
        fontSize: 14,
        fontWeight: active ? 600 : 500,
        color: active
          ? faradayTokens.color.forest[900]
          : isComing
            ? faradayTokens.color.ink.tertiary
            : faradayTokens.color.ink.secondary,
        background: active ? faradayTokens.color.surface.sunken : "transparent",
        transition: "background 180ms ease-out, color 180ms ease-out",
        cursor: isComing && !isExpandable ? "default" : "pointer",
        "&:hover": {
          background: isComing ? "transparent" : faradayTokens.color.forest[50],
          color: isComing ? faradayTokens.color.ink.tertiary : faradayTokens.color.forest[900],
        },
      }}
    >
      <Icon sx={{ fontSize: 20, color: "inherit" }} />
      <Box sx={{ flex: 1 }}>{item.label}</Box>
      {isExpandable && (expanded ? <ExpandLess fontSize="small" /> : <ExpandMore fontSize="small" />)}
    </Box>
  );

  if (isExpandable) {
    return (
      <Box onClick={onToggleExpand} role="button" aria-expanded={expanded}>
        {content}
      </Box>
    );
  }

  if (isComing) {
    return (
      <Tooltip title="Coming soon" placement="right" arrow>
        <Box>{content}</Box>
      </Tooltip>
    );
  }

  return (
    <RouterLink to={item.href} style={{ textDecoration: "none", display: "block" }}>
      {content}
    </RouterLink>
  );
}

export function Sidebar() {
  const { pathname } = useLocation();
  const isMemorySection = pathname.startsWith("/memory");

  return (
    <Box
      component="nav"
      aria-label="Primary"
      sx={{
        width: 240,
        flexShrink: 0,
        background: faradayTokens.color.surface.base,
        borderRight: `1px solid ${faradayTokens.color.forest[100]}`,
        display: "flex",
        flexDirection: "column",
        py: 3,
        px: 2.5,
        gap: 0.5,
      }}
    >
      <Box sx={{ mb: 3, ml: 1 }}>
        <Logo size={56} />
      </Box>

      <Box sx={{ display: "flex", flexDirection: "column", gap: 0.5 }}>
        {PRIMARY_NAV.map((item) => {
          const isActiveTop = item.children
            ? item.children.some((c) => c.href === pathname) || pathname === item.href
            : item.href === pathname;
          const showChildren = item.children && (isMemorySection || isActiveTop);

          return (
            <Box key={item.href}>
              <NavRow
                item={item}
                active={!item.children && isActiveTop}
                expanded={showChildren}
              />
              {showChildren &&
                item.children!.map((child) => (
                  <NavRow
                    key={child.href}
                    item={child}
                    active={child.href === pathname}
                    depth={1}
                  />
                ))}
            </Box>
          );
        })}
      </Box>

      <Box sx={{ flex: 1 }} />

      <Box sx={{ display: "flex", flexDirection: "column", gap: 0.5 }}>
        {FOOTER_NAV.map((item) => (
          <NavRow key={item.href} item={item} active={item.href === pathname} />
        ))}
      </Box>
    </Box>
  );
}
