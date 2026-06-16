import SearchIcon from "@mui/icons-material/Search";
import {
  Box,
  Chip,
  InputAdornment,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import { useMemo, useState } from "react";

import type { MatchedExperiment } from "../../types/analysis";
import { faradayTokens } from "../../design/theme";

interface Props {
  experiments: MatchedExperiment[];
}

type StatusFilter = "all" | "completed" | "in_progress" | "failed";

const STATUS_FILTERS: { value: StatusFilter; label: string }[] = [
  { value: "all", label: "All" },
  { value: "completed", label: "Completed" },
  { value: "in_progress", label: "In progress" },
  { value: "failed", label: "Failed" },
];

const MONO_CELL_SX = {
  fontFamily: faradayTokens.font.mono,
  fontFeatureSettings: '"tnum" 1',
  fontSize: 12,
};

export function ListView({ experiments }: Props) {
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("all");
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase();
    return experiments.filter((exp) => {
      if (statusFilter !== "all" && exp.status !== statusFilter) return false;
      if (!q) return true;
      const haystack = [exp.title, exp.type, exp.catalyst, exp.solvent, exp.id]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      return haystack.includes(q);
    });
  }, [experiments, search, statusFilter]);

  const pageRows = useMemo(
    () => filtered.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage),
    [filtered, page, rowsPerPage],
  );

  if (experiments.length === 0) {
    return (
      <Box sx={{ color: faradayTokens.color.ink.secondary, fontFamily: faradayTokens.font.mono, fontSize: 13 }}>
        No experiments matched.
      </Box>
    );
  }

  return (
    <Box>
      <Stack
        direction={{ xs: "column", sm: "row" }}
        spacing={1.5}
        alignItems={{ xs: "stretch", sm: "center" }}
        sx={{ mb: 2 }}
      >
        <TextField
          size="small"
          fullWidth
          placeholder="Search title, catalyst, solvent…"
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setPage(0);
          }}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon sx={{ color: faradayTokens.color.ink.tertiary, fontSize: 18 }} />
              </InputAdornment>
            ),
          }}
          sx={{
            maxWidth: { sm: 360 },
            "& .MuiOutlinedInput-root": {
              background: faradayTokens.color.surface.elevated,
              borderRadius: 2,
              fontSize: 14,
            },
            "& .MuiOutlinedInput-notchedOutline": { borderColor: "#E5E2DA" },
          }}
          inputProps={{ "aria-label": "search matched experiments" }}
        />
        <Stack direction="row" spacing={0.75} sx={{ flexWrap: "wrap" }}>
          {STATUS_FILTERS.map((f) => (
            <Chip
              key={f.value}
              label={f.label}
              size="small"
              onClick={() => {
                setStatusFilter(f.value);
                setPage(0);
              }}
              variant={statusFilter === f.value ? "filled" : "outlined"}
              sx={{
                fontSize: 12,
                fontFamily: faradayTokens.font.body,
                borderColor: faradayTokens.color.forest[100],
                ...(statusFilter === f.value
                  ? {
                      background: faradayTokens.color.forest[700],
                      color: "#FFFFFF",
                      "&:hover": { background: faradayTokens.color.forest[900] },
                    }
                  : {
                      background: faradayTokens.color.surface.elevated,
                      color: faradayTokens.color.ink.primary,
                      "&:hover": { background: faradayTokens.color.surface.sunken },
                    }),
              }}
            />
          ))}
        </Stack>
      </Stack>

      {filtered.length === 0 ? (
        <Box
          sx={{
            color: faradayTokens.color.ink.secondary,
            fontFamily: faradayTokens.font.mono,
            fontSize: 13,
            p: 3,
            textAlign: "center",
            background: faradayTokens.color.surface.muted,
            borderRadius: 2,
          }}
        >
          No matches for {search ? `"${search}"` : "this filter"}.
        </Box>
      ) : (
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
              {pageRows.map((exp) => (
                <TableRow key={exp.id} hover sx={{ "&:last-child td": { borderBottom: 0 } }}>
                  <TableCell>{exp.title}</TableCell>
                  <TableCell sx={MONO_CELL_SX}>{exp.type.replace(/_/g, " ")}</TableCell>
                  <TableCell>{exp.catalyst ?? "—"}</TableCell>
                  <TableCell>{exp.solvent ?? "—"}</TableCell>
                  <TableCell align="right" sx={MONO_CELL_SX}>
                    {exp.yield_pct != null ? `${exp.yield_pct.toFixed(1)}%` : "—"}
                  </TableCell>
                  <TableCell sx={MONO_CELL_SX}>
                    {exp.started_at ? exp.started_at.slice(0, 10) : "—"}
                  </TableCell>
                  <TableCell>
                    <span
                      style={{
                        fontFamily: faradayTokens.font.mono,
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
      )}

      {filtered.length > 0 && (
        <TablePagination
          component="div"
          count={filtered.length}
          page={page}
          onPageChange={(_, p) => setPage(p)}
          rowsPerPage={rowsPerPage}
          onRowsPerPageChange={(e) => {
            setRowsPerPage(parseInt(e.target.value, 10));
            setPage(0);
          }}
          rowsPerPageOptions={[5, 10, 25]}
          labelRowsPerPage="Per page:"
          sx={{
            mt: 1,
            fontFamily: faradayTokens.font.body,
            color: faradayTokens.color.ink.secondary,
            "& .MuiTablePagination-displayedRows, & .MuiTablePagination-selectLabel": {
              fontFamily: faradayTokens.font.body,
              fontSize: 13,
            },
            "& .MuiTablePagination-select": {
              fontFamily: faradayTokens.font.mono,
              fontSize: 13,
            },
          }}
        />
      )}

      {search || statusFilter !== "all" ? (
        <Typography
          sx={{
            fontFamily: faradayTokens.font.mono,
            fontSize: 11,
            color: faradayTokens.color.ink.tertiary,
            mt: 0.5,
          }}
        >
          Showing {filtered.length} of {experiments.length}
        </Typography>
      ) : null}
    </Box>
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
  const m = base.match(/^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i);
  if (!m) return base;
  const r = parseInt(m[1], 16);
  const g = parseInt(m[2], 16);
  const b = parseInt(m[3], 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}
