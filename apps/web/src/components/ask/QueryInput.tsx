import SearchIcon from "@mui/icons-material/Search";
import { Box, Button, TextField } from "@mui/material";
import { useState } from "react";

import { faradayTokens } from "../../design/theme";

interface Props {
  initialValue?: string;
  disabled?: boolean;
  onSubmit: (query: string) => void;
}

export function QueryInput({ initialValue = "", disabled = false, onSubmit }: Props) {
  const [value, setValue] = useState(initialValue);
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
        onChange={(e) => setValue(e.target.value)}
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
            fontSize: 16,
            paddingLeft: 2,
            paddingRight: 2,
          },
          "& .MuiOutlinedInput-notchedOutline": {
            borderColor: "#E5E2DA",
          },
          "& .MuiOutlinedInput-root:hover .MuiOutlinedInput-notchedOutline": {
            borderColor: faradayTokens.color.botanical.line,
          },
          "& .MuiOutlinedInput-root.Mui-focused .MuiOutlinedInput-notchedOutline": {
            borderColor: faradayTokens.color.accent.faraday,
          },
        }}
      />
      <Button
        type="submit"
        variant="contained"
        disabled={!canSubmit}
        sx={{
          borderRadius: 999,
          px: 3.5,
          fontSize: 15,
          fontWeight: 500,
          background: faradayTokens.color.accent.faraday,
          "&:hover": { background: "#9C470A" },
        }}
      >
        Ask
      </Button>
    </Box>
  );
}
