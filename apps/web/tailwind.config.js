/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  // Avoid clashes with MUI's reset
  corePlugins: { preflight: false },
  theme: {
    extend: {
      colors: {
        // Faraday design tokens — spec §3.0.1
        surface: {
          warm: "#FAF8F3",
          elevated: "#FFFFFF",
        },
        ink: {
          primary: "#1B1F1A",
          secondary: "#5C6360",
          tertiary: "#A8AFAB",
        },
        accent: {
          faraday: "#B45309",
          curie: "#7C3AED",
        },
        state: {
          aiSuggest: "#8B5CF6",
          confirmed: "#059669",
          warn: "#D97706",
          error: "#B91C1C",
        },
        botanical: {
          line: "#9CA89A",
        },
      },
      fontFamily: {
        display: ["Fraunces", "Tiempos Headline", "Georgia", "serif"],
        body: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
      },
      spacing: {
        // 8px base
        "card": "24px",
        "section": "48px",
        "hero": "96px",
      },
      borderRadius: {
        editorial: "12px",
      },
      transitionDuration: {
        DEFAULT: "250ms",
      },
    },
  },
  plugins: [],
};
