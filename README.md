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

Hosted in the EU on [Scalingo](https://scalingo.com/), served by the nginx buildpack. See `Procfile`, `.buildpacks`, and `nginx.conf`. `data/` is not deployed (`.slugignore`).

## Preview

Open `index.html` in a browser. Nothing to install or build.

## Privacy

A visitor's browser must not call Google, Meta, or any other third party just by loading a page. No analytics, tag managers, embedded players, or CDN-hosted fonts and scripts. Fonts used here are self-hosted in this repo. New services (hosting, email, forms, error logging) should be EU-hosted.

## License

The code in this repository is licensed under [AGPL-3.0](LICENSE). Some third-party material in the repo is **not** covered by the AGPL and keeps its own terms:

| What | Where | Terms |
| --- | --- | --- |
| Stock photos behind the "Why AfterCare" cards (hands, banana, phone call), original and recoloured versions | `visual-assets/why-*.webp` | Sourced from [Pixabay](https://pixabay.com/) under the [Pixabay Content License](https://pixabay.com/service/license-summary/). Modification is allowed. The photos may not be redistributed as standalone files or sold on their own. If you reuse this site, use your own images. |
| Surveillance data on reported STI cases in Europe | `data/ecdc-sti/` (and the charts built from it, `visual-assets/chart-sti-*.png`) | Downloaded from the [ECDC Surveillance Atlas of Infectious Diseases](https://www.ecdc.europa.eu/en/surveillance-atlas-infectious-diseases). Dataset provided by ECDC based on data provided by public health authorities, scientific institutes or health care providers in the relevant reporting countries and/or by WHO. The charts were generated from this data by `data/generate-charts.py`, so they are adapted works. ECDC allows reuse, commercial or not, if the source is acknowledged and any adaptation is stated; see the [ECDC intellectual property notices](https://www.ecdc.europa.eu/en/ecdc-intellectual-property-notices). |
| Poppins typeface | `assets/fonts/`, `data/fonts/` | [SIL Open Font License 1.1](https://openfontlicense.org/). |

The AfterCare name and logo are not licensed for reuse.