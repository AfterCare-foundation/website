# AfterCare website

Public site for [AfterCare](https://www.after-care.eu/), an anonymous STI-exposure notification app. Live at [https://www.after-care.eu/](https://www.after-care.eu/).

This repository is the site: the pages, styles, scripts, and images. The product itself is separate:

- [app](https://github.com/AfterCare-foundation/app) — the notifications app
- [backend](https://github.com/AfterCare-foundation/backend) — the notifications server

## Pages

| Path | What it is |
| --- | --- |
| `/` | Marketing page |
| `/privacy/` | Privacy policy |
| `/funding/` | How the project is funded |
| `/connect/` | Redirects to `/` |

## Stack

Static HTML, CSS, and vanilla JavaScript. No build step and no shared templates: `index.html`, `privacy/index.html`, and `funding/index.html` each carry their own markup and styles.

Hosted in the EU on [Scalingo](https://scalingo.com/), served by the nginx buildpack. See `Procfile`, `.buildpacks`, and `nginx.conf`. `notes/` and `data/` are not deployed (`.slugignore`).

## Preview

Open `index.html` in a browser. Nothing to install or build.

## Privacy

A visitor's browser must not call Google, Meta, or any other third party just by loading a page. No analytics, tag managers, embedded players, or CDN-hosted fonts and scripts. Fonts used here are self-hosted in this repo. New services (hosting, email, forms, error logging) should be EU-hosted.

## License

[AGPL-3.0](LICENSE).
