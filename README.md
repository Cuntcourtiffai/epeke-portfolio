# Epeke Vuyisani — UGC Portfolio (website + PDF)

## Structure
- `website/` Vite + React site (`src/content.json` holds ALL text, contacts and projects; the PDF reads the same file)
- `pdf/` `build_pdf.py` -> `portfolio.html` (editable source) -> `Epeke_Vuyisani_UGC_Portfolio.pdf`
- `assets/` halftone generator and static flower render

## Run locally
```
cd website && npm install && npm run dev      # dev server
npm run build && npm run preview               # production check
```
## Rebuild the PDF
```
pip install playwright && playwright install chromium
python3 pdf/build_pdf.py
```
## Deploy free (not yet deployed)
Run `npm run build`, then upload `website/dist/` to Netlify Drop, Cloudflare Pages or GitHub Pages (`base` is already `./`). Afterwards put the public URL in `siteUrl` in `content.json`, update `og:image` in `index.html` to an absolute URL, and rebuild the PDF.

## Replace or add a video
1. Put `name.mp4` in `website/public/videos/` and a poster `name.jpg` in `website/public/posters/`.
2. Add an entry to `projects` in `content.json` (`featured: true` puts it in the PDF; the PDF layout fits 4 featured).
3. For the PDF add stills `pdf/assets/name-1.jpg`, `-2.jpg`, `-3.jpg` (e.g. `ffmpeg -ss 2 -i name.mp4 -frames:v 1 name-1.jpg`), then rebuild.
4. Fill `url` with the public TikTok/Instagram link; it appears on the site and in the PDF automatically.

## Remaining placeholders
- Public URL for each of the 6 videos (`url` is empty; the PDF says "link to be added")
- Website URL (`siteUrl`) after deployment
- `og:image` absolute URL after deployment

## Visual system (flat, no 3D)
- `assets/make_halftone.py` draws a flat flower and converts it to ~2.9k gold halftone dots -> `website/src/halftone.json` (+ static `halftone-flower.png`, used in the PDF and as fallback).
- `Flower.jsx` (2D canvas): dots drift away from the cursor and slowly return; a flat offset shadow answers the cursor's motion at a right angle; the image dissolves and reassembles on load, on tap/click in the hero, and when you scroll back to it.
- `Atmosphere.jsx`: emerald/amber haze that follows the pointer with delay and reveals blurred image fragments beneath it; grain, dust and cracks; a slow scroll drift in opposition to content.
- Headline: three stacked copies (ivory, pink, gold) that slip out of register on hover/tap and once after load, with a slow scroll stretch. Worn-ink look comes from a baked mask (`public/img/wear.png`).
- Touch devices: no pointer effects; the haze drifts on its own and tapping the hero dissolves the flower. `prefers-reduced-motion`: everything is static and fully formed.
- Videos and faces get no distortion: effects live in the haze, borders and headline only.

## Repository report
| Repo | Status |
|---|---|
| React Three Fiber | Used in v1, REMOVED in this version (flat direction). `three` and `@react-three/fiber` are no longer dependencies. |
| Liquid Logo | Used in v1, REMOVED (chrome-like metal contradicts the flat brief). |
| Grainy Image | Used in v1, REMOVED. Grain is now an own SVG-noise layer plus a baked wear mask, which was cheaper. |
| Webcore UI, Puxel | Inspected earlier, not used. |
| Signal and Noise | Unreachable (`git.mitgai.net` did not resolve). Its themes (overlapping serif type, mono captions, texture) were done independently. |
No repository code is used in this version; it is plain React, CSS, SVG and canvas.

## Honesty notes
- Videos are labelled "creator concept video"; no clients, results or testimonials are claimed.
- Several clips look AI-generated or storyboard-styled. If that is true, disclose it in captions and to brands, as platforms and clients increasingly require.
- Original mp4s are 360x640 (one is 720x960): fine for portfolio viewing, low for client delivery.
