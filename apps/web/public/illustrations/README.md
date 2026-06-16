# Illustration assets

Drop AI-generated or hand-painted **PNG illustrations** here. The dev/prod
server makes them available at `/illustrations/<filename>.png`.

If a file is missing, components silently render without it (no fake
hand-drawn fallback that looks worse than nothing).

## Currently expected

| File | Used by | Position |
|---|---|---|
| `eucalyptus.png` | RightRail | top-right corner of every right-rail panel |
| `fern.png` | RightRail | bottom-left corner (rendered flipped vertically for visual variation) |

## ChatGPT / DALL-E / Midjourney prompts

### `eucalyptus.png`

```
A single naturalist line-art illustration of a eucalyptus sprig with
6–8 oval silver-dollar leaves arranged alternately along a gently
curving woody stem. Style: hand-drawn fine-art botanical specimen,
the kind found in a 1900s herbarium or vintage natural-history journal.

Strict requirements:
- 600×600 PNG with FULLY TRANSPARENT background (no white box, no shadow)
- Line-only — single hairline weight (~3 pixels) in deep sage green
  (#7A8F7E). NO color fills inside leaves. NO gradients. NO shadows.
  NO botanical name label or text anywhere.
- Stem curves diagonally from the top-right corner toward bottom-left,
  so the sprig "lays" across the corner of a panel
- Leaves are clearly recognizable as eucalyptus: rounded ovals,
  approximately 1.5x as long as wide, each with a single faint
  central vein
- Composition: stem + leaves take ~80% of canvas, gentle negative
  space around it
- AVOID: photorealism, watercolor wash, color fills, cartoonish
  exaggeration, text labels, signature
```

### `fern.png`

```
A single naturalist line-art illustration of one fern frond — a curved
central stem (rachis) with 10–14 pinnate leaflets feathering out in
pairs, larger at the base and tapering to small leaflets at the tip.
Style: hand-drawn fine-art botanical specimen from a vintage natural-
history plate.

Strict requirements:
- 600×600 PNG with FULLY TRANSPARENT background
- Line-only — single hairline weight (~3 pixels) in deep sage green
  (#7A8F7E). NO fills, NO gradients, NO shadows. NO text.
- Frond stem curves diagonally so the frond can sit in a corner
- Leaflets are clearly pinnate-fern shape — narrow lance-shaped,
  attached opposite each other along the rachis, each leaflet's edge
  showing 3–5 small serrations or gentle scallops
- Composition: frond fills ~85% of canvas, gentle negative space
- AVOID: photorealism, color, leaf fills, cartoonish style, text
```

### Notes

- Save files as PNG with **transparent background** so they composite
  cleanly over the sage watercolor wash already on the right rail
- Lower the source-image opacity in your generator if it comes out too
  dark — the `RightRail` component renders them at 50% opacity already
- After generating, save into this folder and reload the dev server —
  Vite will serve them at `/illustrations/<name>.png` automatically
- If you want **different botanical species** (e.g. cedar sprig, oak
  leaf, etc.) just swap the filename and update `RightRail.tsx`
