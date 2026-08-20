# The Tear Test

**Panel review · UXD & copy audit of the AfterCare coming-soon page**

Nine composite expert personas — not real individuals — walk the page end to
end: once as a stranger who just found a card, once as a research
participant watching a moderator demo it. Method: a full top-to-bottom pass
of the live page content and markup, cross-checked against the repo
(license, assets, source) rather than assumed.

Convened for: public-beta readiness + research-interview prep.

---

## The panel

| Name | Credential | Lens |
|---|---|---|
| Dr. Naomi Reyes | Public health physician, ex-partner-notification program lead | Medical accuracy |
| Priya Chandrasekaran | UX researcher, sensitive-topic & health-stigma studies | Research validity |
| Jonah Kessler | Product designer, trust-heavy onboarding flows | First impression |
| Elena Marchetti | Content strategist & UX writer, health tech | Voice & clarity |
| Marcus Webb | Privacy & digital-trust engineer | Trust signals |
| Yuki Tanaka | Visual & brand designer, iOS-native craft | Visual polish |
| Ade Osei | Accessibility specialist, WCAG & assistive tech | Inclusive access |
| Ruth Calloway *(wildcard)* | Ritual & physical-object designer — live-event ticketing, tabletop games | The object itself |
| Dante Ruiz *(wildcard)* | Nightlife harm-reduction peer educator | The real room |

---

## Two journeys, one page

**Track A — cold visitor, off a card or a link**
A0 hears about / sees a card at a venue → A1 lands on the hero → A2 the
3-second read (legit? for me?) → A3 scrolls through how it works → A4 trust
bullets, objection handling → A5 exit, no live app yet.

**Track B — research-interview demo**
B0 moderator intro → B1 card handed over → B2 physical tear, live → B3 site
shown alongside it → B4 debrief & questions.

---

## Section-by-section audit

### Hero

> "You found the card." · "In testing phase" · "The hardest conversation,
> made unnecessary." · "Tear a card in half with someone… anonymously, no
> name required." · "Coming soon."

**Working well:** the headline is genuinely differentiated and emotionally
accurate — not a generic app tagline.

- **Jonah Kessler (first impression):** the hero passes the 3-second test
  emotionally but leans on the kicker's assumption the reader is already
  holding a card. The sub-copy carries the literal explanation on its own —
  worth checking it lands with the kicker mentally subtracted.
- **Marcus Webb (trust signals):** "In testing phase" and "Coming Soon"
  weren't quite the same claim about availability. **Resolved:** eyebrow
  changed to "In development."
- **Yuki Tanaka (visual polish):** the hero mockup's source file is only
  96×185px, displayed up to 300px+ wide — will read soft on any retina
  display, including the laptops/iPads this page is shown on during
  interviews. Needs a higher-resolution export from the original design
  file; not fixable from the page alone. *(Open — needs a new asset.)*
- **Priya Chandrasekaran (research validity):** the copy's implicit
  card-first sequence may or may not match how a moderator runs the
  session. **Resolved:** confirmed card-first is the intended order: no
  copy change needed.
- **Ruth Calloway (the object itself):** "You found the card" is a good
  instinct — discovery, chance, a found-object narrative that matches how
  these will actually circulate. Worth protecting rather than diluting.
- **Dante Ruiz (the real room):** nothing on the page (until a trust bullet,
  much further down) says where a card actually comes from. Anyone who
  reaches this URL without ever having seen one has no anchor for what "the
  venue" means. *(Open.)*

### How it works — Tear → Keep → Scan → Claim → Connected → Notified

> 1. Tear — "Split a card in half — one side each." 2. Keep — "Hang onto
> your half." 3. Scan — "Scan it in the app, whenever you're ready." 4.
> Claim — "Make it yours — no name required." 5. Connected — "Linked,
> anonymously, once you both claim." 6. Notified *(added)* — "If either of
> you tests positive later, the other finds out — anonymously, no names
> exchanged."

**Working well:** clear, well-paced, honest verbs. The connecting line and
step numbering read as one continuous sequence.

- **Dr. Naomi Reyes (medical accuracy) — biggest finding:** the sequence
  stopped at "Connected" and never showed the actual later moment — the
  entire premise of the product. **Resolved:** added step 6, "Notified,"
  mirroring the mini-phone visual pattern of steps 3–5.
- **Dr. Naomi Reyes:** smaller accuracy note — "Connected" could be misread
  as the meaningful event itself. **Resolved:** added a clarifying line
  after the sequence: "Connecting shares nothing on its own — only a later
  positive test ever triggers a notification."
- **Elena Marchetti (voice & clarity):** "It's a match!" borrows dating-app
  vernacular on purpose — panel debate below.
- **Ruth Calloway:** the tear mechanic is the strongest, most ownable idea
  on the page. A reader who's never encountered this pattern before has to
  infer what kind of object this is from "tear a card in half" alone — one
  concrete comparison (a claim ticket, a broken token) would help
  unfamiliar readers form the mental model faster. *(Open, not yet acted
  on.)*
- **Dante Ruiz:** "Scan it in the app, whenever you're ready" is exactly
  right — no real-time pressure in a dim, loud room. Separately (a product
  question, not a page fix): confirm the real scanner has a manual
  code-entry fallback for bad lighting / wet hands / a cracked screen.
- **Priya Chandrasekaran:** the tear animation played once per pageload,
  which is real friction for a moderator demoing to many participants in
  one session. **Resolved:** click now always replays the tear (no longer
  `{once: true}`).
- **Marcus Webb:** the QR graphic is literally `qr-placeholder.png`. Fine
  for a teaser, but a dead end if a participant is invited to actually scan
  it. *(Open — confirm whether sessions rely on this exact page for that.)*

> **Panel debate — resolved:** does "It's a match!" trivialize a
> health-safety moment with dating-app tone right where it matters most?
> Consensus: no, keep it. The product's thesis is making this feel as
> ordinary as a swipe, not an ordeal — and that step is pairing two people,
> not disclosing a result. Gravity belongs at the "Notified" moment, which
> is why step 6 exists now.

### Trust bullets

> "Privacy first — no traceable data" · "Anonymous — no names, no emails" ·
> "Free — pick up a card at the venue" · "Open source — anyone can read the
> code"

**Working well:** four claims, parallel construction, genuinely scannable —
no phrasing changes needed.

- **Marcus Webb — verified:** the repo is AGPLv3-licensed, a license
  written specifically for network services, whose own license text
  recommends exactly this: *"its interface could display a 'Source' link
  that leads users to an archive of the code."* The "Open source" bullet
  currently links nowhere. *(Open — needs the repo URL and a decision on
  whether to expose it pre-launch.)*
- **Dr. Naomi Reyes:** "Free — pick up a card at the venue" implicitly
  limits access to people who can attend specific venues. If there's any
  other path into the beta, say so. *(Open — needs accurate info.)*
- **Ade Osei (inclusive access):** the trust icons (white, larger, thicker)
  read clearly against the dark background and are correctly
  `aria-hidden`, with text carrying the meaning. No issue.

### Footer & exit

> "AfterCare · privacy-first, always"

- **Jonah Kessler:** no call-to-action anywhere after the trust bullets —
  the page simply ends.
- **Ade Osei:** footer text sat around 28% white opacity on near-black —
  borderline WCAG AA contrast. **Resolved:** bumped kicker/microcopy to
  55% and footer to 40%.

> **Panel debate — resolved:** the obvious fix for "nothing to do here" is
> an email waitlist, which directly contradicts "Anonymous — no names, no
> emails." Options were: (a) no capture, stay fully consistent; (b) a
> genuinely anonymous mechanism (Signal/social link, no-PII push opt-in);
> (c) a narrowly-scoped "launch updates only" email opt-in. **Decision: (a)
> — no capture, stay consistent with the privacy promise.** No CTA added.

---

## Using this page in research interviews

- **Priya Chandrasekaran:** script the demo order deliberately rather than
  letting it vary by moderator. **Resolved:** confirmed card-first, matches
  existing copy.
- **Dante Ruiz:** if sessions happen on-site near venues, test the live
  page on the actual venue wifi/cell signal beforehand — the page is light,
  the room's connectivity is the real risk.
- **Ade Osei:** the decorative torn-card and mini-phone visuals are
  correctly `aria-hidden` for a sighted demo, but that means a
  screen-reader-only pass conveys none of the "how it works" visuals, text
  only. Worth a moderator listen-through before sessions involving
  assistive tech.
- **Yuki Tanaka:** the ambient background motion (drifting blobs, cursor
  glow) is nice for solo browsing; in a moderated 1:1 session it's worth a
  conscious call rather than an accident.

---

## What shipped vs. what's still open

| Item | Status |
|---|---|
| Reconcile "Coming Soon" vs. "In testing phase" | ✅ Done — eyebrow now "In development" |
| Close the loop on the notification promise | ✅ Done — added step 6, "Notified" |
| Interest-capture approach | ✅ Decided — none, stay consistent with the privacy promise |
| Research-demo order | ✅ Confirmed — card-first, no copy change needed |
| Replayable tear animation for repeat demos | ✅ Done |
| Text contrast (kicker/microcopy/footer) | ✅ Done |
| "Connecting ≠ sharing health info yet" clause | ✅ Done |
| Link "Open source" bullet to the real repo | ⬜ Open — needs the URL + a go/no-go on exposing it pre-launch |
| Clarify access beyond "pick up a card at the venue" | ⬜ Open — needs accurate info |
| Higher-resolution hero mockup export | ⬜ Open — needs a new asset, not a code fix |
| A concrete comparison for the tear mechanic (claim ticket / broken token) | ⬜ Open — not yet acted on |
| QR placeholder — confirm it's not expected to scan-through during interviews | ⬜ Open |
