/** @type {import('tailwindcss').Config} */
// Mirrors productTokens in src/design/theme.ts. App UI uses fresh greens
// (product register); editorial palette (cream/amber) is intentionally absent here.
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  corePlugins: { preflight: false },
  theme: {
    extend: {
      colors: {
        surface: {
          base: "#F7FAF6",
          elevated: "#FFFFFF",
          muted: "#EFF5EF",
          sunken: "#E6F2EA",
        },
        forest: {
          50: "#E6F2EA",
          100: "#C9E4D2",
          300: "#8FB89A",
          500: "#52B788",
          700: "#2D6A4F",
          900: "#1B4332",
        },
        ink: {
          primary: "#1B1F1A",
          secondary: "#5C6360",
          tertiary: "#A8AFAB",
        },
        state: {
          confirmed: "#059669",
          warn: "#D97706",
          error: "#B91C1C",
          aiSuggest: "#8B5CF6",
        },
        botanical: {
          line: "#9CA89A",
        },
      },
      fontFamily: {
        // Single-family system — JetBrains Mono everywhere. Slot names kept
        // so `font-display` / `font-body` Tailwind classes still resolve.
        display: ["JetBrains Mono", "ui-monospace", "SFMono-Regular", "Menlo", "monospace"],
        body: ["JetBrains Mono", "ui-monospace", "SFMono-Regular", "Menlo", "monospace"],
        mono: ["JetBrains Mono", "ui-monospace", "SFMono-Regular", "Menlo", "monospace"],
      },
      spacing: {
        card: "24px",
        section: "48px",
        hero: "96px",
      },
      borderRadius: {
        editorial: "12px",
      },
      transitionDuration: {
        DEFAULT: "250ms",
      },
      boxShadow: {
        card: "0 1px 2px rgba(45, 106, 79, 0.06)",
        "card-hover": "0 4px 12px rgba(45, 106, 79, 0.10)",
      },
    },
  },
  plugins: [],
};
