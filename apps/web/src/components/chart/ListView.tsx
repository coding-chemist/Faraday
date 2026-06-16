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

// Single mono font stack for every text node in this view — keeps numerals,
// status pills, and ellipsized cells visually consistent at any width.
const MONO_FONT = faradayTokens.font.mono;
const TNUM = '"tnum" 1';

const HEADER_SX = {
  fontFamily: MONO_FONT,
  fontSize: 11,
  fontWeight: 600,
  letterSpacing: "0.06em",
  textTransform: "uppercase",
  color: faradayTokens.color.ink.secondary,
  borderBottom: `1px solid ${faradayTokens.color.forest[100]}`,
  py: 1.25,
};

const CELL_SX = {
  fontFamily: MONO_FONT,
  fontSize: 12.5,
  py: 1.25,
  borderBottom: `1px solid ${faradayTokens.color.forest[50]}`,
};

const TRUNCATE = {
  overflow: "hidden",
  textOverflow: "ellipsis",
  whiteSpace: "nowrap" as const,
};

const TITLE_CLAMP = {
  display: "-webkit-box",
  WebkitLineClamp: 2,
  WebkitBoxOrient: "vertical" as const,
  overflow: "hidden",
  lineHeight: 1.35,
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
      <Box sx={{ color: faradayTokens.color.ink.secondary, fontFamily: MONO_FONT, fontSize: 13 }}>
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
            sx: {
              fontFamily: MONO_FONT,
              fontSize: 13,
            },
          }}
          sx={{
            maxWidth: { sm: 360 },
            "& .MuiOutlinedInput-root": {
              background: "rgba(255, 255, 255, 0.7)",
              backdropFilter: "blur(8px)",
              WebkitBackdropFilter: "blur(8px)",
              borderRadius: 1.5,
            },
            "& .MuiOutlinedInput-notchedOutline": { borderColor: "rgba(201, 228, 210, 0.7)" },
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
                fontSize: 11.5,
                fontFamily: MONO_FONT,
                borderRadius: 1.5,
                borderColor: "rgba(201, 228, 210, 0.7)",
                ...(statusFilter === f.value
                  ? {
                      background: faradayTokens.color.forest[700],
                      color: "#FFFFFF",
                      "&:hover": { background: faradayTokens.color.forest[900] },
                    }
                  : {
                      background: "rgba(255, 255, 255, 0.7)",
                      backdropFilter: "blur(8px)",
                      WebkitBackdropFilter: "blur(8px)",
                      color: faradayTokens.color.ink.primary,
                      "&:hover": { background: "rgba(255, 255, 255, 0.9)" },
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
            fontFamily: MONO_FONT,
            fontSize: 13,
            p: 3,
            textAlign: "center",
            background: "rgba(255, 255, 255, 0.55)",
            backdropFilter: "blur(12px)",
            WebkitBackdropFilter: "blur(12px)",
            borderRadius: 1.5,
            border: "1px solid rgba(255, 255, 255, 0.5)",
          }}
        >
          No matches for {search ? `"${search}"` : "this filter"}.
        </Box>
      ) : (
        <TableContainer
          sx={{
            background: "rgba(255, 255, 255, 0.55)",
            backdropFilter: "blur(14px)",
            WebkitBackdropFilter: "blur(14px)",
            borderRadius: 1.5,
            border: "1px solid rgba(255, 255, 255, 0.55)",
            boxShadow: "0 4px 24px rgba(45, 106, 79, 0.06)",
            overflow: "hidden",
          }}
        >
          <Table size="small" sx={{ tableLayout: "fixed", width: "100%" }}>
            <colgroup>
              <col style={{ width: "28%" }} />
              <col style={{ width: "12%" }} />
              <col style={{ width: "22%" }} />
              <col style={{ width: "12%" }} />
              <col style={{ width: "9%" }} />
              <col style={{ width: "10%" }} />
              <col style={{ width: "7%" }} />
            </colgroup>
            <TableHead>
              <TableRow>
                <TableCell sx={HEADER_SX}>Title</TableCell>
                <TableCell sx={HEADER_SX}>Type</TableCell>
                <TableCell sx={HEADER_SX}>Catalyst</TableCell>
                <TableCell sx={HEADER_SX}>Solvent</TableCell>
                <TableCell sx={HEADER_SX} align="right">Yield</TableCell>
                <TableCell sx={HEADER_SX}>Date</TableCell>
                <TableCell sx={HEADER_SX}>Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {pageRows.map((exp) => (
                <TableRow
                  key={exp.id}
                  hover
                  sx={{
                    "&:last-child td": { borderBottom: 0 },
                    "&:hover": { background: "rgba(230, 242, 234, 0.4)" },
                  }}
                >
                  <TableCell sx={{ ...CELL_SX, ...TITLE_CLAMP }} title={exp.title}>
                    {exp.title}
                  </TableCell>
                  <TableCell sx={{ ...CELL_SX, ...TRUNCATE, fontSize: 11.5, color: faradayTokens.color.ink.secondary }} title={exp.type}>
                    {exp.type.replace(/_/g, " ")}
                  </TableCell>
                  <TableCell sx={{ ...CELL_SX, ...TRUNCATE }} title={exp.catalyst ?? ""}>
                    {exp.catalyst ?? "—"}
                  </TableCell>
                  <TableCell sx={{ ...CELL_SX, ...TRUNCATE }} title={exp.solvent ?? ""}>
                    {exp.solvent ?? "—"}
                  </TableCell>
                  <TableCell align="right" sx={{ ...CELL_SX, fontFeatureSettings: TNUM, fontWeight: 600 }}>
                    {exp.yield_pct != null ? `${exp.yield_pct.toFixed(1)}%` : "—"}
                  </TableCell>
                  <TableCell sx={{ ...CELL_SX, fontFeatureSettings: TNUM, color: faradayTokens.color.ink.secondary }}>
                    {exp.started_at ? exp.started_at.slice(0, 10) : "—"}
                  </TableCell>
                  <TableCell sx={CELL_SX}>
                    <span
                      style={{
                        fontFamily: MONO_FONT,
                        fontSize: 10.5,
                        padding: "2px 6px",
                        borderRadius: 4,
                        background: statusColor(exp.status, 0.15),
                        color: statusColor(exp.status, 1),
                        whiteSpace: "nowrap",
                      }}
                    >
                      {exp.status === "in_progress" ? "running" : exp.status}
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
            fontFamily: MONO_FONT,
            color: faradayTokens.color.ink.secondary,
            "& .MuiTablePagination-displayedRows, & .MuiTablePagination-selectLabel, & .MuiTablePagination-select": {
              fontFamily: MONO_FONT,
              fontSize: 12,
            },
          }}
        />
      )}

      {search || statusFilter !== "all" ? (
        <Typography
          sx={{
            fontFamily: MONO_FONT,
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
