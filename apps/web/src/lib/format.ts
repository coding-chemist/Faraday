/**
 * Convert a snake_case enum value to display form.
 *
 *   humanize("amide_coupling")     → "Amide coupling"
 *   humanize("buchwald_hartwig")   → "Buchwald hartwig"
 *   humanize("palladium(II) acetate") → "Palladium(II) acetate"   // no-op for spaces
 *
 * Sentence case only — first character capitalized, rest left alone — so multi-word
 * catalyst names with embedded capitals (e.g. "(II)", "EDC", "HATU") survive intact.
 */
export function humanize(value: string | null | undefined): string {
  if (value == null || value === "") return "";
  const spaced = value.replace(/_/g, " ");
  return spaced.charAt(0).toUpperCase() + spaced.slice(1);
}
