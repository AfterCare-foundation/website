# Architecture Plan

Running record of decisions for initiatives that go beyond the static
one-pager — new services, new pages, anything with infrastructure or
scope big enough to need a paper trail before building. Update in place as
things move from idea → decided → built, rather than creating a new doc per
feature.

---

## 1. Stretch-goal voting (votes backend)

**Status: roadmap content shipped (static, no voting yet); backend
decided but paused — not yet built.**

The "What's next" section now lives in `index.html` between the trust-bullet
cards and the support/donate section — a continuation of the "How it
works" numbered steps (items 8 and 9, same `.step`/`.step-num` styling,
own mini connector line), listing the two ideas below with a line noting
"Community voting on what we build next is coming soon." No vote buttons,
no counts — purely the static roadmap half of the original idea, shippable
with zero backend. The interactive half (the actual voting/tallying) is
still the paused, not-yet-built piece described below.

### The idea

A way for visitors to vote on stretch-goal features for after launch.
Example options floated so far (not final — just what's been named in
conversation, and now what's listed in the shipped "What's next" section):

- App discrete mode
- Special edition collectible cards

Goal is to show live-ish aggregate counts ("342 votes") to make the roadmap
feel like something the community is actually shaping, not just a static
list.

### The core tension

The product's entire pitch is "no traceable data." A voting feature that
fingerprints visitors (IP logging, accounts) to prevent ballot-stuffing
would directly contradict that promise on the same page that makes it.
Resolved as follows:

- **No accounts, no IP storage — not even hashed IPs.**
- **Anti-abuse is client-side only**: a `localStorage` flag remembers
  "you already voted for X" in that browser. Doesn't stop a determined
  abuser (clearing storage, incognito, another device), but requires zero
  tracking of anyone. Framed on-page as a "community temperature check,"
  not a scientific poll.
- **One narrow server-side backstop, explicitly agreed**: an in-memory
  rate limit (requests per IP over a short rolling window) purely to blunt
  a trivial scripted loop of raw POST requests with no browser involved.
  Never written to disk, a log, or a database — lives only in the running
  process's RAM and is forgotten on every restart. This is a limiter, not
  a tracker: it never persists or associates a vote with an identity.

### Why this needs real infrastructure

The site today is 100% static (nginx serving files, no backend at all —
see `Procfile`/`.buildpacks`/`nginx.conf`). GitHub Pages and similar
static-only hosts are architecturally incapable of running this — there's
no server process to increment or read a counter from, regardless of how
minimal the logic is. Any version of live counts needs a real running
process plus somewhere persistent to store the tallies.

### Decided shape

| Decision | Choice | Why |
|---|---|---|
| Where it lives | **Standalone tiny service**, separate from this repo | This repo's own README states it's website-assets-only ("the service itself lives in its own repo"). A same-repo nginx+Node multi-buildpack setup was considered and rejected — Scalingo's multi-buildpack + nginx-buildpack combo could not be confirmed (via docs/search) to run both processes in one shared container/localhost; that uncertainty made it the riskier of the two paths for something this small. |
| Storage | **Redis add-on** | A handful of counters is exactly what `INCR` is for — atomic, no schema, trivial to query. |
| Runtime | **Node.js**, minimal dependencies | No constraint from the real AfterCare app's stack was available (that repo isn't accessible here) — picked for being small and easy to read/maintain, not for any specific framework reason. |
| Hosting for the standalone service | **Not yet chosen** — Railway, Render, Fly.io, or a second small Scalingo app were named as candidates, all viable, none picked | Revisit when work resumes; any of them avoids the shared-container question entirely by design. |
| Abuse handling | In-memory, non-persisted rate limit (server) + `localStorage` dedup (client) | See "core tension" above. |

### API shape (sketched, not built)

Two endpoints, nothing else:

- `GET /votes` → current tallies for every option, e.g.
  `{"discrete-mode": 42, "collectible-cards": 17}`
- `POST /votes/:option` → increments that option's counter, returns the
  updated tallies

CORS: the standalone service will be on a different origin from the
website, so the API needs to allow the site's origin explicitly (no reverse
proxy / same-origin trick available once it's a separate service).

### Open items before building

1. Pick the hosting platform for the standalone service.
2. Finalize the full list of stretch-goal options (only two named/shipped
   so far — confirm whether there are more, and lock exact wording).
3. Design the voting UI itself (vote buttons/counts) and how it slots into
   the now-shipped static "What's next" section — layout only needs to
   change to add interactivity, not to be built from scratch.
4. Decide the exact rate-limit window/threshold for the server-side
   backstop (e.g. N requests per IP per minute) — not yet specified.

---

## 2. Donate / crowdfunding section

**Status: built.** Lives in `index.html` between the trust-bullet cards and
the footer (`.support` section).

Kickstarter/tip-jar-style tiers, styled to match the trust-card grid:

| Tier | Amount | Framing |
|---|---|---|
| Tip Jar | $5 | Casual, low-commitment |
| Supporter | $25 | Mid-tier |
| Founding Supporter | $100+ | Top tier — gradient-accented card, "Most impact" badge |

A line beneath the tiers points organizations to
`contact.aftercare@protonmail.com` for sponsorship instead of the
individual-tier flow — same split as the sponsors/investors subpage below
(individuals/community → tiers, organizations → direct contact).

**Deliberate interim choice — no real payment processor wired up.**
Real donation processing (Stripe, Ko-fi, Open Collective, etc.) is a
heavier decision than it looks: it implies a payment processor, likely a
registered entity to receive funds, and real compliance/refund handling —
not something to pick without the team weighing in. Rather than ship a
dead `href="#"` placeholder, each tier's "Chip in" button is currently a
pre-filled `mailto:contact.aftercare@protonmail.com` link (subject line
varies per tier) — genuinely functional today, just manual instead of
self-serve.

**Follow-up, whenever there's a real answer**: swap the three `mailto:`
hrefs in `.tier-btn` for real checkout links once a donation platform is
chosen. No other changes needed — the section, copy, and styling are
already final pending that one decision.

---

## 3. Sponsors / investors subpage

**Status: fully specified, not yet started — independent of the other two,
no backend needed.**

A static subpage (same pattern as `connect/index.html` — no build step, no
backend) stating:

- The project is fully not-for-profit.
- The team currently volunteers their time.
- There are still real operational expenses.
- Contact: `contact.aftercare@protonmail.com`

Open items: where it lives in the site structure (e.g. `/sponsors/`), exact
page copy beyond the core facts above, and whether it's linked from the
main page (footer link, nav) or left unlinked/only shared directly.
