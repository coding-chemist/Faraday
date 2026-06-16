import { Box, Skeleton } from "@mui/material";

import { faradayTokens } from "../../design/theme";

/** Pulse-animated placeholder mirroring the result layout — sets reading expectations
 * during the 2-15s LLM call without leaving the page blank. */
export function LoadingSkeleton() {
  return (
    <Box className="faraday-fade-in" aria-label="loading results">
      <Box sx={{ textAlign: "center", mb: 4 }}>
        <Box
          className="font-mono faraday-pulse"
          sx={{
            display: "inline-block",
            color: faradayTokens.color.forest[700],
            fontSize: 13,
            letterSpacing: "0.04em",
          }}
        >
          searching the lab memory…
        </Box>
      </Box>

      {/* Intent placeholder */}
      <Box sx={{ mb: 5 }}>
        <Skeleton variant="text" width={120} height={16} />
        <Skeleton variant="text" width="60%" height={36} />
      </Box>

      {/* Summary cards row */}
      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: { xs: "1fr", sm: "repeat(3, 1fr)" },
          gap: 2.5,
          mb: 6,
        }}
      >
        {[0, 1, 2].map((i) => (
          <Box
            key={i}
            sx={{
              background: faradayTokens.color.surface.elevated,
              border: `1px solid ${faradayTokens.color.forest[100]}`,
              borderRadius: 2,
              p: 3,
            }}
          >
            <Skeleton variant="text" width="40%" height={12} />
            <Skeleton variant="text" width="70%" height={42} sx={{ mt: 0.5 }} />
            <Skeleton variant="text" width="50%" height={14} sx={{ mt: 0.5 }} />
          </Box>
        ))}
      </Box>

      {/* Chart placeholder */}
      <Box
        sx={{
          background: faradayTokens.color.surface.elevated,
          border: `1px solid ${faradayTokens.color.forest[100]}`,
          borderRadius: 2,
          p: 4,
        }}
      >
        <Skeleton variant="rectangular" width="100%" height={380} sx={{ borderRadius: 1 }} />
      </Box>
    </Box>
  );
}
