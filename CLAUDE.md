# AfterCare Website — Project Rules

This repo holds the public marketing/teaser site for AfterCare, an anonymous
STI-exposure-notification app. Privacy-first is the product's core promise,
so the site itself has to hold that standard, not just describe it.

## No big-tech telemetry, no third-party CDNs

Do not add anything that causes a visitor's browser to make a request to
Google, Meta, or similar third parties as a side effect of loading this
page — no Google Fonts (`fonts.googleapis.com`/`fonts.gstatic.com`), no
Google Analytics/Tag Manager, no Facebook/Meta Pixel, no embedded YouTube
players, no CDN-hosted JS libraries (jsDelivr, unpkg, cdnjs, etc.).

**Why:** loading Google Fonts from Google's own CDN sends the visitor's IP
to Google before they've consented to anything — German courts (e.g. LG
München, 2022) have ruled this a GDPR violation on its own, independent of
the font's license. The same logic applies to any other third-party-hosted
asset or tracking snippet.

**How to apply:**
- Fonts: use the system font stack (`-apple-system, "Segoe UI", Helvetica,
  Arial, sans-serif`) unless there's a strong reason not to. If a custom
  webfont is ever truly needed, self-host the font files from this repo —
  never link to a third-party font CDN.
- Analytics: if/when analytics are wanted, use a self-hosted or EU-hosted,
  cookie-free option (e.g. self-hosted Plausible), not Google Analytics.
- Any new dependency (font, script, widget, icon set) must be self-hosted —
  vendor the files into this repo rather than pointing at someone else's
  CDN.
- This extends past fonts/analytics to infrastructure generally: if a new
  service is ever needed (hosting, email delivery, form handling, error
  logging, etc.), default to an EU-hosted/operated provider — consistent
  with the Scalingo EU choice already made for hosting — and avoid
  China-, Russia-, and North-Korea-linked infrastructure outright. A
  non-EU provider is a fallback only when there's genuinely no viable
  alternative, not a first choice.

## Stack

Plain static HTML/CSS/vanilla JS, no build step. Deployed to Scalingo (EU
hosting) via the nginx buildpack — see `Procfile`, `.buildpacks`,
`nginx.conf`.

## Each page is a self-contained HTML file — nothing is shared by a build step

There's no templating, no includes, no bundler. `index.html`,
`privacy/index.html`, `funding/index.html`, and `connect/index.html` each
carry their own full `<head>`, inline `<style>`, and (where used) inline
`<script>`. Notably, the `:root` color tokens (`--bg`, `--purple`, `--teal`,
`--white`, `--gray`, etc.) are hand-copied into each page's own `<style>`
block, not read from one shared file — there is no `global.css` or
equivalent to make that automatic.

**Why:** this is a deliberate no-build-step stack (see Stack above), so
there's no tool to catch drift the way a bundler or CSS-variable import
would. Consistency across pages is a manual discipline, not something the
architecture enforces.

**How to apply:**
- Changing a color token (e.g. retiring `--purple` for a new accent)? Grep
  for that variable across `index.html`, `privacy/index.html`, and
  `funding/index.html` and update all of them in the same change — don't
  edit just the page you're looking at.
- Adding a new page? Follow the existing pattern: its own folder with an
  `index.html` (see `funding/` or `privacy/`), the same `:root` token block
  copied in, relative-path links (`../`, `../visual-assets/...`) rather
  than root-absolute (`/...`) — every existing internal link uses the
  relative form — and a "← Back to AfterCare" link home.
- If duplication across three-plus pages ever becomes painful enough to
  justify it, introducing a shared `assets/tokens.css` (still no build
  step — just a linked stylesheet) is a reasonable escape hatch. Don't
  reach for a static-site generator or bundler for this alone; that's a
  much bigger shift than the problem warrants.

## Verifying changes: headless browser tooling defaults to Firefox

When a code change needs an actual rendered check — a screenshot, or
headless browser automation via Playwright/Puppeteer/etc. — install and
drive Firefox, not Chromium. Don't silently reach for Chromium as the
path of least resistance just because a tool defaults to it.

**Why:** this project already avoids Google-linked infrastructure for
everything the *visitor's* browser touches (see "No big-tech telemetry,
no third-party CDNs" above). The same preference extends to our own dev
tooling — Chromium is a Google-controlled project; Firefox is not.

**How to apply:**
- `npx playwright install firefox` (not `chromium`) when a headless
  browser is needed to verify a visual change.
- If Firefox isn't available or installable in the environment either,
  say so and fall back to a manual eyeball check (open the file in a real
  browser, or describe the change precisely) rather than defaulting to
  Chromium to get unblocked.

## Commit and deploy discipline

Treat `main` as production, not a scratchpad — Scalingo deploys straight
from this repo (Stack above), so there's no staging environment or CI gate
between a push and the live public site.

**How to apply:**
- Batch a logical change into one commit rather than splitting one reason
  for changing across several, and don't bundle unrelated changes into one
  commit.
- Only commit/push when actually asked to, or when it's the clearly agreed
  next step — not proactively after every edit.
- Before pushing a non-trivial change, sanity-check the "no third-party
  requests" rule above still holds — grep the changed file(s) for `http`
  or a bare domain to catch an accidentally-introduced external `src`/
  `href` — and open the changed page(s) to eyeball the result, since
  there's no build or test suite to catch a broken tag or dead link.
- If you take a screenshot to verify a visual change, save it to the
  scratchpad/temp directory, not into this repo, and don't leave it lying
  around once you've looked at it. If a capture is genuinely worth keeping
  as a reference, move it deliberately into `visual-assets/` — don't let
  one-off verification shots and real design assets pile up together.
- Dev happens on Windows here — if a helper script (a link checker, an
  image-optimization pass, etc.) is ever added to this repo, make sure any
  documented commands work in PowerShell, not just bash (e.g. don't
  document `a && b` as the only form — PowerShell 5.1 doesn't support
  `&&`/`||` chaining).


### Standing Protocol — Multi-Instance Collaboration
This repo is routinely worked on by more than one Claude Code instance at once —
a teammate's parallel session, another window on a different machine. Treat
that as the normal case, not an anomaly:
  - Before merging or pushing, `git fetch` and check for divergent remote
    history — that's expected here, not a sign something went wrong.
  - Default to **merging** another instance's committed work, not force-pushing
    over it or rebasing it away. Resolve conflicts by combining intent from
    both sides, not by unilaterally picking one.
  - If a file has *uncommitted* changes that don't match anything you just did,
    assume another live session owns them. Don't stash, edit, revert, or commit
    over them without asking first. `git stash` is fine to *unblock* your own
    work as long as the stashed content is restored unchanged afterward.
  - When changes genuinely can't be reconciled automatically — two different
    fixes to the same function, two different values for the same data field —
    stop and surface the conflict to the user with both versions shown, rather
    than guessing which one should win.


## Deliverables stay local — don't use the Artifact tool here

Don't publish reports, audits, reviews, or plans via the Artifact tool
(claude.ai) for this project. Write them as local Markdown files in the repo
instead.

**Why:** publishing to claude.ai forces a context switch out of VS Code into
a browser to log in, and separates the deliverable from the repo it's
actually about.

**How to apply:**
- Write reports/audits/plans/reviews as local `.md` files in the repo (e.g.
  under a `notes/` folder) rather than calling the Artifact tool.
- This is about the default for internal working deliverables. If the user
  explicitly asks for something to be published as a shareable web
  page/link, that's a distinct, explicit request — not the default.
