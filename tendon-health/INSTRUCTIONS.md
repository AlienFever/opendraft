# Deploying Tendon Isometrics

This folder is a complete, working static website — no build step, no dependencies.
It's a personal isometric-exercise reference app (PWA) with embedded YouTube videos.

If you're an AI assistant picking this up in a new session: the app is finished.
The only remaining task is deployment. Follow the steps below.

## What's here

```
index.html    - page structure
styles.css    - all styling (light theme)
app.js        - rendering + localStorage progress tracking logic
data.js       - the exercise database (edit this to add/change exercises)
manifest.json - PWA manifest (installable on phone home screen)
sw.js         - service worker (offline caching)
icon.svg      - app icon
icons/        - PNG icons for the manifest (192px, 512px)
```

## Important: don't open index.html by double-clicking it

YouTube's embedded player rejects pages with no real HTTP referrer, which is what
happens when a file is opened via `file://` (double-click). This produces
"Error 153: Video player configuration error." The site **must** be served over
http/https — locally or deployed — for the embedded videos to load. (There's also
a "Watch on YouTube" link on every card as a fallback either way.)

To sanity-check locally before deploying:

```bash
cd tendon-health   # this folder
python3 -m http.server 8080
# open http://localhost:8080 in a browser
```

## Deploying to Vercel

Preferred path — the Vercel CLI:

```bash
npm install -g vercel
cd tendon-health          # this folder — deploy this folder itself, not a parent folder
vercel login              # opens a browser to authenticate
vercel --prod              # deploys as a static site, no build command needed
```

When prompted:
- "Set up and deploy?" → yes
- Link to existing project? → no (unless you already made one)
- Project name → anything, e.g. `tendon-isometrics`
- Directory → `./` (current directory, since you're already inside `tendon-health`)
- Override settings? → no (it's static; Vercel auto-detects "Other" framework, no build step)

Vercel will print a live `https://*.vercel.app` URL when done — that's the one to open on your phone and "Add to Home Screen."

### Alternative: Vercel dashboard (no CLI)

1. Push this folder to a GitHub repo (see below), or drag-and-drop the folder at https://vercel.com/new
2. If importing from GitHub: Root Directory → this folder if it's nested in a larger repo, otherwise leave as `/`
3. Framework Preset → "Other" (static site, no build command)
4. Deploy

## Turning this into its own GitHub repo (optional, needed for git-based auto-deploy)

```bash
cd tendon-health
git init
git add .
git commit -m "Initial commit: Tendon Isometrics app"
git branch -M main
gh repo create tendon-isometrics --public --source=. --push
# or, without gh CLI: create an empty repo on github.com, then
# git remote add origin https://github.com/<you>/tendon-isometrics.git
# git push -u origin main
```

Once it's a GitHub repo connected to a Vercel project, every future `git push` auto-deploys.

## Editing exercises later

Everything content-related lives in `data.js` (one JS array of region → exercises
objects). No other file needs to change to add/edit/remove an exercise.
