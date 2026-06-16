import { createTheme } from "@mui/material/styles";

// Faraday design tokens — mirrors spec §3.0.1 and tailwind.config.js
export const faradayTokens = {
  color: {
    surface: { warm: "#FAF8F3", elevated: "#FFFFFF" },
    ink: { primary: "#1B1F1A", secondary: "#5C6360", tertiary: "#A8AFAB" },
    accent: { faraday: "#B45309", curie: "#7C3AED" },
    state: {
      aiSuggest: "#8B5CF6",
      confirmed: "#059669",
      warn: "#D97706",
      error: "#B91C1C",
    },
    botanical: { line: "#9CA89A" },
  },
  font: {
    display: '"Fraunces", "Tiempos Headline", Georgia, serif',
    body: '"Inter", system-ui, sans-serif',
    mono: '"JetBrains Mono", ui-monospace, monospace',
  },
} as const;

export const faradayTheme = createTheme({
  palette: {
    mode: "light",
    primary: { main: faradayTokens.color.accent.faraday },
    secondary: { main: faradayTokens.color.accent.curie },
    background: {
      default: faradayTokens.color.surface.warm,
      paper: faradayTokens.color.surface.elevated,
    },
    text: {
      primary: faradayTokens.color.ink.primary,
      secondary: faradayTokens.color.ink.secondary,
      disabled: faradayTokens.color.ink.tertiary,
    },
    success: { main: faradayTokens.color.state.confirmed },
    warning: { main: faradayTokens.color.state.warn },
    error: { main: faradayTokens.color.state.error },
  },
  typography: {
    fontFamily: faradayTokens.font.body,
    h1: { fontFamily: faradayTokens.font.display, fontWeight: 600, lineHeight: 1.1 },
    h2: { fontFamily: faradayTokens.font.display, fontWeight: 600 },
    h3: { fontFamily: faradayTokens.font.display, fontWeight: 600 },
    button: { textTransform: "none", fontWeight: 500 },
  },
  shape: { borderRadius: 12 },
  transitions: { duration: { standard: 250 } },
});
