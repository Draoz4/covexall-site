# Covexall — Home / Sales Page

Static site (HTML + CSS + vanilla JS). No build step.

- `index.html` — the page
- `styles.css` — design tokens + all styles
- `main.js` — nav, reveal-on-scroll, FAQ, newsletter (front-end only), "Ask Cove" chat (n8n RAG webhook)
- `assets/` — optimized WebP cutouts of the 3D crew (Cove, Viro, Bac, Snot, Maya, Mom), photos, product renders
- `tools/prep_assets.py` — regenerates the character cutouts from `../creatives/animation/*.png`

## Before launch
1. Set the real store / contact / social URLs in the `LINKS` object at the top of `main.js`.
2. Replace the sample reviews in the "Loved by families" section with verified customer reviews (and delete the `.sample-note` line).
3. Wire the newsletter forms to your email provider (currently front-end only).

## Deploy
Pushes to `main` deploy automatically via Vercel. Local preview: `npx serve .`
