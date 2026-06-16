// Left sidebar — Lab Memory parent gets a featured green tile around its icon
// (the brand-accent treatment shown in the mockup). When /icons/lab-memory.png
// is present, it replaces the SVG fallback for that one icon.

import ExpandLess from "@mui/icons-material/ExpandLess";
import ExpandMore from "@mui/icons-material/ExpandMore";
import { Box, Tooltip } from "@mui/material";
import type { ComponentType } from "react";
import { Link as RouterLink, useLocation } from "react-router-dom";

import { faradayTokens } from "../../design/theme";
import { Logo } from "./Logo";
import {
  AskIcon,
  CompareIcon,
  DataIcon,
  LabMemoryIcon,
  NotebookIcon,
  ProtocolsIcon,
  ReagentsIcon,
  SettingsIcon,
  StructureIcon,
  TemplatesIcon,
  WatchIcon,
} from "./icons";

interface NavItem {
  label: string;
  href: string;
  icon: ComponentType;
  /** When true, the item is rendered greyed-out with a 'coming soon' tooltip. */
  comingSoon?: boolean;
  /** When true, the icon renders inside a featured forest-green tile (brand accent). */
  featured?: boolean;
  /** Optional PNG asset under public/icons/ used in place of the SVG icon. */
  iconImage?: string;
  children?: NavItem[];
}

const PRIMARY_NAV: NavItem[] = [
  { label: "Notebook", href: "/notebook", icon: NotebookIcon, comingSoon: true },
  { label: "Reagents", href: "/reagents", icon: ReagentsIcon, comingSoon: true },
  { label: "Data", href: "/data", icon: DataIcon, comingSoon: true },
  { label: "Structure", href: "/structure", icon: StructureIcon, comingSoon: true },
  { label: "Protocols", href: "/protocols", icon: ProtocolsIcon, comingSoon: true },
  { label: "Templates", href: "/templates", icon: TemplatesIcon, comingSoon: true },
  {
    label: "Lab Memory",
    href: "/memory",
    icon: LabMemoryIcon,
    featured: true,
    iconImage: "/icons/lab-memory.png",
    children: [
      { label: "Watch", href: "/memory/watch", icon: WatchIcon, comingSoon: true },
      { label: "Ask", href: "/memory/ask", icon: AskIcon },
      { label: "Compare", href: "/memory/compare", icon: CompareIcon, comingSoon: true },
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
  const isFeatured = !!item.featured;

  const iconColor = isFeatured
    ? "#FFFFFF"
    : active
      ? faradayTokens.color.forest[900]
      : isComing
        ? faradayTokens.color.ink.tertiary
        : faradayTokens.color.ink.secondary;

  const content = (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        gap: 1.5,
        px: 1.5,
        py: 1.1,
        ml: depth * 2,
        borderRadius: 1.5,
        fontFamily: faradayTokens.font.body,
        fontSize: 14.5,
        fontWeight: active || isFeatured ? 600 : 500,
        color: active
          ? faradayTokens.color.forest[900]
          : isFeatured
            ? faradayTokens.color.forest[900]
            : isComing
              ? faradayTokens.color.ink.tertiary
              : faradayTokens.color.ink.secondary,
        background: active && !isFeatured ? faradayTokens.color.surface.sunken : "transparent",
        transition: "background 180ms ease-out, color 180ms ease-out",
        cursor: isComing && !isExpandable ? "default" : "pointer",
        "&:hover": {
          background: isComing ? "transparent" : faradayTokens.color.forest[50],
          color: isComing ? faradayTokens.color.ink.tertiary : faradayTokens.color.forest[900],
        },
      }}
    >
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          width: isFeatured ? 30 : 20,
          height: isFeatured ? 30 : 20,
          borderRadius: isFeatured ? 1.5 : 0,
          background: isFeatured ? faradayTokens.color.forest[700] : "transparent",
          color: iconColor,
          flexShrink: 0,
        }}
      >
        {item.iconImage ? (
          <img
            src={item.iconImage}
            alt=""
            width={isFeatured ? 20 : 16}
            height={isFeatured ? 20 : 16}
            style={{ display: "block" }}
            onError={(e) => {
              // PNG missing — fall back to inline SVG by hiding the img
              (e.currentTarget as HTMLImageElement).style.display = "none";
              const sibling = (e.currentTarget as HTMLImageElement)
                .nextElementSibling as HTMLElement | null;
              if (sibling) sibling.style.display = "block";
            }}
          />
        ) : null}
        <Box
          sx={{
            display: item.iconImage ? "none" : "block",
            color: "inherit",
            lineHeight: 0,
          }}
        >
          <Icon />
        </Box>
      </Box>
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
