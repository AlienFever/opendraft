# Tendon Isometrics

A personal, single-page web app / installable PWA with isometric exercises for tendon
health, grouped by the tendon/body region they target. Each exercise has step-by-step
instructions, a suggested hold/rep protocol, and an embedded video demonstration.

Covers: Achilles tendon, patellar tendon, elbow (tennis elbow / golfer's elbow),
rotator cuff & biceps tendon, and hip/groin (gluteal, adductor, proximal hamstring).

## Running it

No build step — it's static HTML/CSS/JS. Either:

- Open `index.html` directly in a browser, or
- Serve it locally so the service worker and manifest work correctly:

  ```bash
  cd tendon-health
  python3 -m http.server 8080
  ```

  then visit `http://localhost:8080`.

To use it like a mobile app, deploy the folder to any static host (GitHub Pages,
Netlify, Vercel) and use "Add to Home Screen" on your phone — it installs as a
standalone PWA and caches itself for offline use.

## Personal progress tracking

Each exercise has a "Mark done today" checkbox. Progress is stored only in your
browser's `localStorage` (no account, no backend, no data leaves your device).

## Editing exercises

All exercise content lives in `data.js` — add, remove, or edit entries there;
the UI renders directly from that file.

## Disclaimer

This is a personal reference tool, not medical advice. Protocols are general
starting points drawn from common tendon-rehab guidance. Back off any exercise
that pushes pain past a mild, tolerable level, and check with a physiotherapist
or doctor before starting a new program — especially for an acute or worsening
injury.
