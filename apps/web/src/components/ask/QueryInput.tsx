import SearchIcon from "@mui/icons-material/Search";
import { Box, Button, TextField } from "@mui/material";

import { faradayTokens } from "../../design/theme";

interface Props {
  /** Fully controlled — parent owns the text. */
  value: string;
  onChange: (next: string) => void;
  disabled?: boolean;
  onSubmit: (query: string) => void;
}

export function QueryInput({ value, onChange, disabled = false, onSubmit }: Props) {
  const trimmed = value.trim();
  const canSubmit = trimmed.length >= 2 && !disabled;

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (!canSubmit) return;
    onSubmit(trimmed);
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{
        display: "flex",
        gap: 1.5,
        maxWidth: 760,
        mx: "auto",
        width: "100%",
      }}
    >
      <TextField
        fullWidth
        autoFocus
        placeholder="Show Suzuki couplings with yield below 70% in the last six months…"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        InputProps={{
          startAdornment: (
            <SearchIcon
              sx={{ color: faradayTokens.color.ink.tertiary, mr: 1, fontSize: 22 }}
            />
          ),
        }}
        sx={{
          "& .MuiOutlinedInput-root": {
            background: faradayTokens.color.surface.elevated,
            borderRadius: 999,
            fontFamily: faradayTokens.font.mono,
            fontSize: 14,
            paddingLeft: 2,
            paddingRight: 2,
          },
          "& .MuiOutlinedInput-input::placeholder": {
            fontFamily: faradayTokens.font.mono,
            fontSize: 13,
            opacity: 0.6,
          },
          "& .MuiOutlinedInput-notchedOutline": {
            borderColor: "#E5E2DA",
          },
          "& .MuiOutlinedInput-root:hover .MuiOutlinedInput-notchedOutline": {
            borderColor: faradayTokens.color.botanical.line,
          },
          "& .MuiOutlinedInput-root.Mui-focused .MuiOutlinedInput-notchedOutline": {
            borderColor: faradayTokens.color.forest[700],
            borderWidth: 1,
          },
        }}
        inputProps={{ "aria-label": "natural-language query" }}
      />
      <Button
        type="submit"
        variant="contained"
        disabled={!canSubmit}
        aria-label={canSubmit ? "submit query" : "enter at least 2 characters to submit"}
        sx={{
          borderRadius: 999,
          px: 4,
          fontFamily: faradayTokens.font.mono,
          fontSize: 13,
          fontWeight: 600,
          letterSpacing: "0.04em",
          background: faradayTokens.color.forest[700],
          color: "#FFFFFF",
          boxShadow: "none",
          "&:hover": { background: faradayTokens.color.forest[900], boxShadow: "none" },
          "&.Mui-disabled": { background: faradayTokens.color.forest[100], color: faradayTokens.color.ink.tertiary },
        }}
      >
        Ask
      </Button>
    </Box>
  );
}
