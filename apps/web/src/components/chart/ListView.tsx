import {
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";

import type { MatchedExperiment } from "../../types/analysis";
import { faradayTokens } from "../../design/theme";

interface Props {
  experiments: MatchedExperiment[];
}

export function ListView({ experiments }: Props) {
  if (experiments.length === 0) {
    return (
      <Box className="font-mono text-sm" sx={{ color: faradayTokens.color.ink.secondary }}>
        No experiments matched.
      </Box>
    );
  }

  return (
    <TableContainer sx={{ background: faradayTokens.color.surface.elevated, borderRadius: 2 }}>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell sx={{ fontWeight: 600 }}>Title</TableCell>
            <TableCell sx={{ fontWeight: 600 }}>Type</TableCell>
            <TableCell sx={{ fontWeight: 600 }}>Catalyst</TableCell>
            <TableCell sx={{ fontWeight: 600 }}>Solvent</TableCell>
            <TableCell sx={{ fontWeight: 600 }} align="right">Yield</TableCell>
            <TableCell sx={{ fontWeight: 600 }}>Date</TableCell>
            <TableCell sx={{ fontWeight: 600 }}>Status</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {experiments.map((exp) => (
            <TableRow key={exp.id} hover sx={{ "&:last-child td": { borderBottom: 0 } }}>
              <TableCell>{exp.title}</TableCell>
              <TableCell sx={{ fontFamily: faradayTokens.font.mono, fontSize: 12 }}>
                {exp.type.replace(/_/g, " ")}
              </TableCell>
              <TableCell>{exp.catalyst ?? "—"}</TableCell>
              <TableCell>{exp.solvent ?? "—"}</TableCell>
              <TableCell align="right">
                {exp.yield_pct != null ? `${exp.yield_pct.toFixed(1)}%` : "—"}
              </TableCell>
              <TableCell sx={{ fontFamily: faradayTokens.font.mono, fontSize: 12 }}>
                {exp.started_at ? exp.started_at.slice(0, 10) : "—"}
              </TableCell>
              <TableCell>
                <span
                  className="font-mono"
                  style={{
                    fontSize: 11,
                    padding: "2px 8px",
                    borderRadius: 12,
                    background: statusColor(exp.status, 0.15),
                    color: statusColor(exp.status, 1),
                  }}
                >
                  {exp.status.replace(/_/g, " ")}
                </span>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

function statusColor(status: string, alpha: number): string {
  const base = (() => {
    switch (status) {
      case "completed":
        return faradayTokens.color.state.confirmed;
      case "failed":
        return faradayTokens.color.state.error;
      case "in_progress":
        return faradayTokens.color.state.warn;
      default:
        return faradayTokens.color.ink.secondary;
    }
  })();
  if (alpha === 1) return base;
  // Convert hex to rgba
  const m = base.match(/^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i);
  if (!m) return base;
  const r = parseInt(m[1], 16);
  const g = parseInt(m[2], 16);
  const b = parseInt(m[3], 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}
