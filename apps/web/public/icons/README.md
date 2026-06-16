# Custom icon assets

Drop AI-generated or hand-painted PNG icons here.

When a file lives at `/icons/<name>.png` it becomes referenceable from
React components as `<img src="/icons/<name>.png" />` (Vite serves
everything under `public/` at the URL root).

## Currently expected

- `lab-memory.png` — brain icon for the Lab Memory sidebar tile (used
  inside the featured green tile next to the "Lab Memory" label). Falls
  back to the hand-drawn SVG `LabMemoryIcon` if absent.

## Prompt to generate `lab-memory.png`

Paste this into ChatGPT/DALL-E or any image generator:

```
A minimalist hand-drawn line-art icon of a human brain, viewed from a
3/4 angle. Single-weight line work in pure white (#FFFFFF) on a fully
transparent background. Show two hemispheres separated by a soft center
seam, with 3–4 gentle curved wrinkles (gyri) per hemisphere — not
anatomically detailed, more like a stylized editorial illustration.

Style references: artisanal botanical line drawings, the kind of
hand-drawn icon you'd see on a vintage apothecary label or a fine-art
chemistry notebook. Warm, organic, scientifically suggestive without
being clinical.

Strict requirements:
- 256x256 PNG with transparent background
- Line-only, NO fills, NO gradients, NO shadows
- Lines in #FFFFFF, ~3–4 pixels wide
- Brain centered, occupying ~75% of the canvas
- Rounded silhouette, friendly proportions
- NOT photoreal, NOT anatomically detailed, NOT cartoonish
```

After generating, save the file as `lab-memory.png` here and refresh
the dev server.
