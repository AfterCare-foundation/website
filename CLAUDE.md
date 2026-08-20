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

## Stack

Plain static HTML/CSS/vanilla JS, no build step. Deployed to Scalingo (EU
hosting) via the nginx buildpack — see `Procfile`, `.buildpacks`,
`nginx.conf`.

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
