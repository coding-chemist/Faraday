// Two design registers per spec §3 — never mix.
//
//   productTokens   fresh greens, powder-white. Used by every app screen
//                   the chemist sees (Landing, Editor, Lab Memory).
//   editorialTokens cream + amber + violet. Used only for marketing
//                   assets, README hero, architecture diagrams.
//
// faradayTokens defaults to productTokens because 99% of UI code is product UI.
//
// See feedback_design_two_registers.md.

import { createTheme } from "@mui/material/styles";

const ink = {
  primary: "#1B1F1A",
  secondary: "#5C6360",
  tertiary: "#A8AFAB",
} as const;

const state = {
  confirmed: "#059669",
  warn: "#D97706",
  error: "#B91C1C",
  aiSuggest: "#8B5CF6",
} as const;

const botanical = {
  line: "#9CA89A",
} as const;

// JetBrains Mono is the entire typography system — same family on
// headlines, body, numerals, code. Slot names kept (display / body / mono)
// so component sx that reads font.display vs font.body still works; they
// just resolve to the same stack now.
const FAMILY = '"JetBrains Mono", ui-monospace, "SFMono-Regular", Menlo, monospace';
const font = {
  display: FAMILY,
  body: FAMILY,
  mono: FAMILY,
} as const;

export const productTokens = {
  color: {
    surface: {
      base: "#F7FAF6",       // powder-white page background
      elevated: "#FFFFFF",   // cards
      muted: "#EFF5EF",      // sidebar / muted panels
      sunken: "#E6F2EA",     // hover / subtle inset
    },
    forest: {
      50: "#E6F2EA",
      100: "#C9E4D2",        // mint
      300: "#8FB89A",        // sage
      500: "#52B788",
      700: "#2D6A4F",        // forest — primary
      900: "#1B4332",
    },
    ink,
    state,
    botanical,
  },
  font,
} as const;

export const editorialTokens = {
  color: {
    surface: {
      warm: "#FAF8F3",
      elevated: "#FFFFFF",
    },
    accent: {
      faraday: "#B45309",
      curie: "#7C3AED",
    },
    ink,
    state,
    botanical,
  },
  font,
} as const;

// Default export — app code uses this everywhere.
export const faradayTokens = productTokens;

export const faradayTheme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: productTokens.color.forest[700],
      dark: productTokens.color.forest[900],
      light: productTokens.color.forest[500],
      contrastText: "#FFFFFF",
    },
    secondary: {
      main: productTokens.color.forest[300],
      contrastText: productTokens.color.ink.primary,
    },
    background: {
      default: productTokens.color.surface.base,
      paper: productTokens.color.surface.elevated,
    },
    text: {
      primary: productTokens.color.ink.primary,
      secondary: productTokens.color.ink.secondary,
      disabled: productTokens.color.ink.tertiary,
    },
    success: { main: productTokens.color.state.confirmed },
    warning: { main: productTokens.color.state.warn },
    error: { main: productTokens.color.state.error },
  },
  typography: {
    fontFamily: productTokens.font.body,
    h1: { fontFamily: productTokens.font.display, fontWeight: 600, lineHeight: 1.05 },
    h2: { fontFamily: productTokens.font.display, fontWeight: 600 },
    h3: { fontFamily: productTokens.font.display, fontWeight: 600 },
    button: { textTransform: "none", fontWeight: 500 },
  },
  shape: { borderRadius: 12 },
  transitions: { duration: { standard: 250 } },
});
