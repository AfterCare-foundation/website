# MVP Archive

Content and code cut from the live site to simplify it down to the initial
MVP, kept here in full so any of it can be reintroduced later without
rebuilding from scratch. Nothing here is a description of *what* was built —
it's the actual markup/CSS/JS, verbatim, as it stood right before removal.

---

## 1. Step 4 "Claim" — the search → found → tap sequence

**Cut because:** for the MVP, "Scan" (step 3) transitions directly to
"Connected" (step 5, renumbered to step 4 after this cut) — the intermediate
claim/search UI isn't needed to communicate the flow.

**What it was:** a mini-phone screen that, on arriving at the step, showed a
spinner (already spinning, no tap needed to start it — this was itself the
result of an earlier correction, see conversation history) resolving to a
teal checkmark badge and "Card found," which then revealed "Make this card
yours?" and a "Claim Card" button. The button played a tap/ripple/confirm
animation either when the user scrolled on past the step toward "Connected"
or when they tapped it directly — the latter also auto-scrolled the page to
the "Connected" step. Timing was driven by a `--mp-claim-dur` CSS custom
property so a `.fast`-class speed-up (added when the sequence was still
genuinely mid-flight) could shorten it without cutting to the end state, the
same "speed up, don't skip" treatment step 1's tear animation uses.

Two real bugs were found and fixed on this before it was cut (kept here for
context in case it's rebuilt): the checkmark badge used `inset: 22%` for
sizing, which depends on the parent's `aspect-ratio`-derived height being
resolved before the inset can be computed — real iOS Safari got this wrong
and rendered the checkmark visibly off-center, while desktop Chrome (and its
device simulator) didn't; switching to explicit `top`/`left`/`width`/`height`
percentages fixed it. Separately, `.mp-label`'s `white-space: nowrap` (added
to keep "Card found" on one line) was originally applied to the *shared*
`.mp-label` class, which broke step 6's "Possible exposure" wrapping — it
needed to be scoped to `.mp-label-stack .mp-label` instead.

### HTML (was inside the `<ol class="steps">` list, between "Scan" and
"Connected")

```html
<li class="step scroll-reveal" style="--sd: 3">
  <span class="step-num">4</span>
  <div class="step-body">
    <span class="step-label">Claim</span>
    <span class="step-desc"
      >Make it yours — no name or identifying info required.</span
    >
  </div>
  <div class="step-visual">
    <div class="mini-phone" aria-hidden="true">
      <div class="mp-bar"><span class="mp-island"></span></div>
      <div class="mp-screen">
        <span class="mp-status">
          <span class="mp-spinner-wrap"
            ><span class="mp-spinner"></span
          ></span>
          <span class="mp-checkmark-badge"></span>
          <svg
            class="mp-checkmark"
            viewBox="0 0 24 24"
            fill="none"
            stroke="#2dd4bf"
            stroke-width="2.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M20 6 9 17l-5-5" />
          </svg>
        </span>
        <span class="mp-label-stack">
          <span class="mp-label mp-label-a">Searching</span>
          <span class="mp-label mp-label-b">Card found</span>
        </span>
        <span class="mp-sub mp-claim-reveal"
          >Make this card yours?</span
        >
        <span class="mp-btn mp-claim-reveal mp-claim-btn">
          <span class="mp-tap-ripple"></span>
          <svg
            class="mp-btn-check"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="3"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M5 13l4 4L19 7" />
          </svg>
          Claim Card
        </span>
      </div>
    </div>
  </div>
</li>
```

### CSS (was between `.mp-btn-check`'s neighbor `.mp-sub` and the step 5
"Connected" celebratory-entrance block)

```css
.mp-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  white-space: nowrap;
  /* em, not % — same circular-sizing issue as .mp-btn-check's own
     width: .mp-btn is inline-flex (shrink-to-fit), so a %-based
     gap between its own children depends on a width the gap
     itself is part of computing. That's what was pushing "Claim
     Card" onto two lines. */
  gap: 0.35em;
  background: linear-gradient(135deg, var(--purple-light), var(--teal));
  color: #05070d;
  border-radius: 999px;
  padding: 6% 12%;
  font-size: clamp(9.5px, 2.6vw, 11px);
  font-weight: 600;
}
/* Muting via a scrim overlay rather than animating the gradient
   itself — background-image (gradient) doesn't interpolate with a
   solid color the way a plain color property does, so it would
   just snap instead of transition. An overlay's opacity animates
   cleanly, and the scale pulse below is what actually reads as
   "just tapped." */
.mp-btn::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: rgba(10, 10, 16, 0.55);
  opacity: 0;
}
/* Fixed em size, not a % — .mp-btn is inline-flex (shrink-to-fit),
   so a %-width child creates a circular sizing dependency: the
   child's width depends on the parent's width, which depends on
   the child's rendered size. In practice that made the button
   render far wider than its content, not narrower. em ties it to
   the button's own font-size instead, which is independent. */
.mp-btn-check {
  position: relative;
  display: inline-block;
  width: 0.85em;
  height: 0.85em;
  opacity: 0;
  transform: scale(0.5);
}
/* ---- step 4 "Claim", two independent triggers:
   (1) .step.content-active — the spinner is already centered and
   spinning as soon as the step settles into view (this is an
   automatic result of scanning back in step 3, not something the
   user waits on a tap for), resolving to "Card found" and only
   then revealing "Make this card yours?" and the button — there's
   nothing to tap until the card the button claims actually exists.
   (2) .step.content-active.tapped — added separately by JS once
   the user has scrolled a meaningful amount past step 4, heading
   on toward step 5 ("Connected"), which is what tapping "Claim
   Card" actually leads to. The tap ripple/press/confirm plays
   then, not on a fixed delay after arrival — the tap is something
   the user does on their way to the outcome, not something that
   just happens to them a few seconds after landing. */
.mp-status {
  position: relative;
  width: 24%;
  aspect-ratio: 1;
}
.mp-spinner-wrap {
  position: absolute;
  inset: 0;
  opacity: 1;
  transform: scale(1);
}
.mp-spinner {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.15);
  border-top-color: var(--teal);
  animation: mp-spin 0.8s linear infinite;
}
@keyframes mp-spin {
  to {
    transform: rotate(360deg);
  }
}
@keyframes mp-spinner-life {
  0%,
  55% {
    opacity: 1;
    transform: scale(1);
  }
  65%,
  100% {
    opacity: 0;
    transform: scale(0.6);
  }
}
.mp-checkmark-badge {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 1.5px solid var(--teal);
  opacity: 0;
  transform: scale(0.5);
}
@keyframes mp-badge-life {
  0%,
  58% {
    opacity: 0;
    transform: scale(0.5);
  }
  68% {
    opacity: 1;
    transform: scale(1.12);
  }
  76%,
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
/* top/left/width/height, not inset: 22% — .mp-status's own size
   comes from aspect-ratio (width: 24%, aspect-ratio: 1), and an
   inset shorthand has to derive this child's width/height by
   subtracting left+right / top+bottom from the containing block's
   resolved size. .mp-btn-check (a plain width/height icon, never
   inset-sized) rendered fine on the same real iPhone that showed
   this one visibly off-center — width/height percentages resolve
   directly against the parent instead, without needing that
   subtraction, so they don't depend on timing between
   aspect-ratio's layout pass and inset resolution the way Safari
   apparently doesn't get right here. */
.mp-checkmark {
  position: absolute;
  top: 22%;
  left: 22%;
  width: 56%;
  height: 56%;
  opacity: 0;
  transform: scale(0.5);
}
/* A stroke-dasharray "draw-on" used to reveal this path, but
   stroke-dashoffset isn't compositor-accelerated in Safari the way
   transform/opacity are — during momentum scroll on iOS it runs on
   the (scroll-busy) main thread and visibly stutters or freezes
   mid-draw, leaving a half-drawn hook instead of a checkmark. Scale
   + fade instead, matching the badge circle's own entrance, so the
   whole mark is complete the instant it's visible. */
@keyframes mp-check-life {
  0%,
  62% {
    opacity: 0;
    transform: scale(0.5);
  }
  70%,
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
.mp-label-stack {
  position: relative;
  display: block;
}
/* nowrap here only — .mp-label-b sits absolutely over .mp-label-a
   (inset: 0, so it takes its width from the stack, not its own
   text), and a wrapped "Card found" would reflow to two lines
   inside that fixed box. Elsewhere .mp-label is a normal static
   child of .mp-screen and should wrap like any other label
   (step 6's longer "Possible exposure" needs to). */
.mp-label-stack .mp-label {
  white-space: nowrap;
}
.mp-label-b {
  position: absolute;
  inset: 0;
  opacity: 0;
}
@keyframes mp-label-a-life {
  0%,
  58% {
    opacity: 1;
  }
  66%,
  100% {
    opacity: 0;
  }
}
@keyframes mp-label-b-life {
  0%,
  62% {
    opacity: 0;
  }
  70%,
  100% {
    opacity: 1;
  }
}
/* Hidden until the card is actually found — reused by both .mp-sub
   and .mp-btn in step 4 specifically (the generic .mp-sub/.mp-btn
   classes stay always-visible everywhere else on the page, e.g.
   step 3's and step 5's own sub-text). */
.mp-claim-reveal {
  opacity: 0;
  transform: translateY(6px);
}
@keyframes mp-claim-reveal-in {
  0%,
  80% {
    opacity: 0;
    transform: translateY(6px);
  }
  94%,
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
.step.content-active .mp-spinner-wrap {
  animation: mp-spinner-life var(--mp-claim-dur) ease both;
}
.step.content-active .mp-checkmark-badge {
  animation: mp-badge-life var(--mp-claim-dur) ease both;
}
.step.content-active .mp-checkmark {
  animation: mp-check-life var(--mp-claim-dur) ease both;
}
.step.content-active .mp-label-a {
  animation: mp-label-a-life var(--mp-claim-dur) ease both;
}
.step.content-active .mp-label-b {
  animation: mp-label-b-life var(--mp-claim-dur) ease both;
}
.step.content-active .mp-claim-reveal {
  animation: mp-claim-reveal-in var(--mp-claim-dur) ease both;
}
/* Screen-recording/demo-mode style tap indicator — a ring that
   pops in on the button and expands outward while fading, right
   where a fingertip would land. */
.mp-tap-ripple {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 90%;
  aspect-ratio: 1;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.9);
  transform: translate(-50%, -50%) scale(0.15);
  opacity: 0;
  pointer-events: none;
}
@keyframes mp-tap-ripple {
  0% {
    transform: translate(-50%, -50%) scale(0.15);
    opacity: 0.9;
  }
  45% {
    transform: translate(-50%, -50%) scale(1.5);
    opacity: 0;
  }
  100% {
    opacity: 0;
  }
}
.step.content-active.tapped .mp-tap-ripple {
  animation: mp-tap-ripple 0.6s ease-out both;
}
/* Immediate feedback (press-pulse, right on the tap) vs. delayed
   confirmation (mute + checkmark, once the claim actually goes
   through) — animating .mp-btn's color, not its background:
   background-image (the gradient) doesn't interpolate with a
   solid color the way a plain color property does, so muting the
   fill is done via the ::after scrim's opacity instead, which
   animates cleanly. The compound .content-active.tapped selector
   (rather than .tapped alone) is what lets this cleanly take over
   .mp-btn's transform from mp-claim-reveal-in above once tapped —
   a more specific selector wins outright for a shared property,
   and by the time .tapped can even be added, the reveal has long
   since finished and settled anyway. */
/* opacity: 1 at every stop isn't decorative — .tapped's higher
   specificity fully replaces .mp-claim-reveal's animation on
   .mp-btn (not just its transform), so without opacity claimed
   here too, .mp-btn would fall back to .mp-claim-reveal's static
   opacity: 0 the instant .tapped is added. */
@keyframes mp-btn-tap {
  0% {
    opacity: 1;
    transform: scale(0.9);
  }
  40%,
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
@keyframes mp-btn-mute {
  0%,
  40% {
    opacity: 0;
  }
  75%,
  100% {
    opacity: 1;
  }
}
@keyframes mp-btn-color {
  0%,
  40% {
    color: #05070d;
  }
  75%,
  100% {
    color: var(--white);
  }
}
@keyframes mp-btn-check-in {
  0%,
  45% {
    opacity: 0;
    transform: scale(0.5);
  }
  80%,
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
.step.content-active.tapped .mp-btn {
  animation:
    mp-btn-tap 0.6s ease both,
    mp-btn-color 0.6s ease both;
}
.step.content-active.tapped .mp-btn::after {
  animation: mp-btn-mute 0.6s ease both;
}
.step.content-active.tapped .mp-btn-check {
  animation: mp-btn-check-in 0.6s ease both;
}
/* the following lived inside the shared reduced-motion media query
   alongside rules for steps 5/6 that are NOT cut — these five were
   the step-4-only entries within it */
.mp-claim-reveal {
  opacity: 1;
  transform: none;
}
.mp-btn::after {
  opacity: 1;
}
.mp-btn-check {
  opacity: 1;
  transform: none;
}
.mp-btn {
  color: var(--white);
}
.mp-spinner {
  animation: none;
}
.mp-spinner-wrap {
  opacity: 0;
}
.mp-checkmark-badge,
.mp-checkmark {
  opacity: 1;
  transform: none;
}
.mp-label-a {
  opacity: 0;
}
.mp-label-b {
  opacity: 1;
}
/* and, separately, on the generic .step class: */
.step {
  /* Drives step 4's search -> found timeline. .fast — added by JS
     when the user scrolls into or past step 4 quickly — shortens
     it the same way --tear-dur does for the torn cards: same
     animation-name/easing/fill-mode, just a faster playback rate,
     not a cut to the end state. */
  --mp-claim-dur: 1.3s;
}
.step.fast {
  --mp-claim-dur: 0.45s;
}
/* and the button's own hover affordance: */
.mp-claim-btn {
  cursor: pointer;
}
```

### JS (was a self-contained block, called the same way
`activateMiniPhoneSteps` is)

```js
// Step 4 -> 5: the "Claim Card" tap-confirm plays one of two ways.
// Either the user scrolls on past step 4 toward "Connected" — a
// rect.top geometry check that fires on the very first bit of
// scroll movement away from step 4, not after scroll-snap settles
// with step 5 centered, since the tap-confirm is meant to read as
// "leaving step 4," not "having arrived at step 5." Or they tap
// the button directly, which fires the same tap-confirm
// immediately and carries the page on to step 5 itself, since
// that's what tapping "Claim Card" is actually for.
var initClaimTapTrigger = function () {
  var claimBtn = document.querySelector(".mp-claim-btn");
  if (!claimBtn) return;
  var claimStep = claimBtn.closest(".step");
  var connectedStep = claimStep ? claimStep.nextElementSibling : null;
  var claimTapped = false;
  var fireClaimTap = function () {
    if (claimTapped || !claimStep) return;
    claimTapped = true;
    // .fast speeds up the search -> found sequence (via
    // --mp-claim-dur) if it's still mid-flight — the same
    // "speed up, don't skip" treatment step 1 gets for a fast
    // scroll-past. Only touch --mp-claim-dur while that sequence
    // is still actually running, not on every tap regardless —
    // retargeting a CSS variable that drives animation-duration
    // on an animation that already finished and settled (the
    // common case: reading "Card found" takes longer than the
    // sequence's own ~1.3s) is exactly the kind of edge case
    // engines disagree on, and real iOS Safari held onto a
    // stray composited frame of the spinner there when nothing
    // else did.
    var activatedAt = parseFloat(claimStep.dataset.activatedAt || "");
    var stillMidSequence =
      isNaN(activatedAt) || performance.now() - activatedAt < 1300;
    if (stillMidSequence) {
      claimStep.classList.add("fast");
    }
    claimStep.classList.add("tapped");
  };
  claimBtn.addEventListener("click", function () {
    fireClaimTap();
    if (connectedStep) {
      connectedStep.scrollIntoView({
        behavior: reduceMotion ? "auto" : "smooth",
        block: "center",
      });
    }
  });
  if (claimStep && !reduceMotion) {
    var checkClaimTapScroll = function () {
      if (claimTapped) {
        window.removeEventListener("scroll", checkClaimTapScroll);
        return;
      }
      if (
        claimStep.classList.contains("content-active") &&
        claimStep.getBoundingClientRect().top < -1
      ) {
        fireClaimTap();
        window.removeEventListener("scroll", checkClaimTapScroll);
      }
    };
    window.addEventListener("scroll", checkClaimTapScroll, {
      passive: true,
    });
  }
};
if (document.readyState === "complete") {
  initClaimTapTrigger();
} else {
  window.addEventListener("load", initClaimTapTrigger, {
    once: true,
  });
}
```

Note: `activateMiniPhoneSteps` (which stays live) also had a comment
referencing "step 4's search -> found" as an example of a sequence that
*does* need the scrollend settle-wait, contrasted against step 6's
single-shot banner drop that doesn't. That comment was reworded on removal
to stop pointing at a step that no longer exists — the underlying logic
(the scrollend-wait vs. IntersectionObserver-only branch) is unchanged.

---

## 2. Stretch goals section

**Cut because:** roadmap/stretch-goal content isn't essential to the MVP's
core pitch — it can come back once there's a real community-voting
mechanism to attach it to (see the votes-backend plan in
[architecture-plan.md](architecture-plan.md), section 1 — still paused,
not built).

```html
<section class="how stretch-goals" id="stretch-goals">
  <div class="how-title scroll-reveal" style="--sd: 8">Stretch goals:</div>
  <p class="support-copy scroll-reveal" style="--sd: 8">
    Ideas we're considering once AfterCare is past testing. Community voting
    on what we build next is coming soon.
  </p>
  <ol class="steps">
    <li class="step scroll-reveal" style="--sd: 8">
      <span class="step-num">1</span>
      <div class="step-body">
        <span class="step-label">Discrete mode</span>
        <span class="step-desc"
          >A low-profile app icon and discrete mode to avoid prying
          eyes</span
        >
      </div>
    </li>
    <li class="step scroll-reveal" style="--sd: 9">
      <span class="step-num">2</span>
      <div class="step-body">
        <span class="step-label">Collectible cards</span>
        <span class="step-desc"
          >Special-edition card designs for events and venues.</span
        >
      </div>
    </li>
    <li class="step scroll-reveal" style="--sd: 10">
      <span class="step-num">3</span>
      <div class="step-body">
        <span class="step-label">Clinic integration</span>
        <span class="step-desc"
          >Clinic verified STI notifications from partner clinics.</span
        >
      </div>
    </li>
  </ol>
</section>
```

No dedicated CSS — it reused `.how`, `.how-title`, `.support-copy`, `.steps`,
and `.step`, all shared with the main "How it works" section (which stays
live) or with the donate section below (which doesn't).

---

## 3. "Support the project" / donate section

**Cut because:** there's no real payment processor wired up yet (see
[architecture-plan.md](architecture-plan.md), section 2) — every "Chip in"
button just showed a "coming soon" toast. Cutting it for the MVP rather than
shipping a section whose only working feature is a placeholder.

**Follow-up needed elsewhere:** `funding/index.html` had a line — "Chip in
from the home page — donations already work today" — pointing at
`../#support`. That's no longer true once this section is gone; the line was
removed from `funding/index.html` as part of this same cut.

### HTML

```html
<section class="support" id="support">
  <div class="how-title scroll-reveal" style="--sd: 11">
    Support the project
  </div>
  <p class="support-copy scroll-reveal" style="--sd: 11">
    AfterCare is free and volunteer-run — no investors yet, and no ad
    revenue, <b>ever</b>. Made by the community, for the community. Still,
    developing, hosting a server, printing, and distributing cards costs
    real money. If this is worth something to you, a small contribution
    helps keep it going.
  </p>
  <div class="support-toggle-wrap scroll-reveal" style="--sd: 11">
    <button
      type="button"
      class="support-toggle"
      id="supportToggle"
      aria-expanded="false"
      aria-controls="donate-tiers"
    >
      <span>I want to donate</span>
      <svg
        class="support-toggle-icon"
        width="16"
        height="16"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2.5"
        stroke-linecap="round"
        stroke-linejoin="round"
        aria-hidden="true"
      >
        <polyline points="6 9 12 15 18 9"></polyline>
      </svg>
    </button>
    <p class="support-soon">One-click donations coming soon.</p>
  </div>
  <div class="tiers-wrap" id="donate-tiers" inert>
    <div class="tiers-inner">
      <ul class="tiers">
        <li class="tier">
          <span class="tier-name">Tip Jar</span>
          <span class="tier-amount">€5</span>
          <span class="tier-desc">Buy the team a coffee.</span>
          <button type="button" class="tier-btn">Chip in</button>
        </li>
        <li class="tier">
          <span class="tier-name">Supporter</span>
          <span class="tier-amount">€25</span>
          <span class="tier-desc">Help cover a month of hosting.</span>
          <button type="button" class="tier-btn">Chip in</button>
        </li>
        <li class="tier tier-founding">
          <span class="tier-badge">Most impact</span>
          <span class="tier-name">Founding Supporter</span>
          <span class="tier-amount">€100+</span>
          <span class="tier-desc"
            >Be one of the people who got this off the ground. Choose to
            have your name — or an anonymous handle — commemorated on our
            upcoming founder's wall.</span
          >
          <button type="button" class="tier-btn">Chip in</button>
        </li>
      </ul>
      <p class="support-note">
        Representing an organization?
        <a href="mailto:contact.aftercare@protonmail.com">Get in touch</a>
        about sponsorship.
      </p>
    </div>
  </div>
</section>
```

Note: that last `<p class="support-note">` used a class shared with the
still-live "doctor or researcher" contact line further down the page —
`.support-note`/`.support-note a` CSS was **not** removed, since it's still
in use.

### CSS

```css
.support {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: clamp(320px, 92vw, 640px);
  margin: 0 auto;
  padding: 48px 20px 8px;
}
.support-copy {
  text-align: center;
  color: var(--gray);
  font-size: 13.5px;
  line-height: 1.6;
  max-width: 46ch;
  margin: 14px auto 38px;
}
.support-toggle-wrap {
  text-align: center;
  margin-top: 22px;
}
.support-toggle {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 22px;
  border: none;
  border-radius: 999px;
  background: linear-gradient(135deg, var(--purple-light), var(--teal));
  color: #05070d;
  font-family: inherit;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition:
    transform 0.15s ease,
    box-shadow 0.2s ease;
}
.support-toggle:hover {
  box-shadow: 0 8px 24px -8px rgba(96, 165, 250, 0.5);
}
.support-soon {
  margin: 10px 0 0;
  font-size: 11.5px;
  color: rgba(244, 244, 246, 0.4);
}
.support-toggle:active {
  transform: scale(0.96);
}
.support-toggle-icon {
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.support-toggle[aria-expanded="true"] .support-toggle-icon {
  transform: rotate(180deg);
}
/* Height/opacity reveal via the grid-rows trick (0fr -> 1fr) — no
   JS measurement needed, works regardless of content height. The
   inner wrapper's overflow:hidden is what actually clips the
   content while the row is collapsed. */
.tiers-wrap {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.tiers-wrap.is-open {
  grid-template-rows: 1fr;
}
.tiers-inner {
  overflow: hidden;
  min-height: 0;
  opacity: 0;
  transform: translateY(-8px);
  transition:
    opacity 0.3s ease,
    transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.tiers-wrap.is-open .tiers-inner {
  opacity: 1;
  transform: translateY(0);
}
@media (prefers-reduced-motion: reduce) {
  .tiers-wrap,
  .tiers-inner,
  .support-toggle-icon {
    transition: none;
  }
}
.tiers {
  list-style: none;
  margin: 28px auto 0;
  padding: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.tier {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 6px;
  padding: 20px 14px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  position: relative;
}
.tier-founding {
  grid-column: 1 / -1;
  background: linear-gradient(
    135deg,
    rgba(96, 165, 250, 0.1),
    rgba(45, 212, 191, 0.08)
  );
  border: 1px solid rgba(96, 165, 250, 0.3);
}
.tier-badge {
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #05070d;
  background: linear-gradient(135deg, var(--purple-light), var(--teal));
  padding: 3px 10px;
  border-radius: 999px;
}
.tier-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--white);
  margin-top: 6px;
}
.tier-amount {
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(120deg, var(--purple-light), var(--teal));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.tier-desc {
  font-size: 12px;
  color: var(--gray);
  line-height: 1.4;
}
.tier-btn {
  margin-top: 8px;
  display: inline-block;
  font-family: inherit;
  font-size: 12.5px;
  font-weight: 600;
  color: var(--gray);
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 999px;
  padding: 8px 18px;
  text-decoration: none;
  cursor: pointer;
  transition:
    background 0.2s ease,
    color 0.2s ease,
    transform 0.15s ease;
}
.tier-btn:active {
  transform: scale(0.96);
}
.tier-btn:hover,
.tier-btn:focus-visible {
  color: var(--white);
}
.tier-btn:hover,
.tier-btn:focus-visible {
  background: rgba(255, 255, 255, 0.14);
}
.tier-btn:active {
  transform: scale(0.96);
}
.tier-founding .tier-btn {
  background: linear-gradient(135deg, var(--purple-light), var(--teal));
  color: #05070d;
  border: none;
}
/* and, at the 1024px+ breakpoint: */
@media (min-width: 1024px) {
  .support {
    max-width: 900px;
  }
  .tiers {
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
  }
  .tier-founding {
    grid-column: auto;
  }
  .tier {
    padding: 24px 16px;
  }
}
```

### JS

```js
var tierBtns = document.querySelectorAll(".tier-btn");
tierBtns.forEach(function (btn) {
  btn.addEventListener("click", function () {
    showToast("One-click donations are coming soon.");
  });
});
```

`showToast`/`toastEl` and the `.toast` CSS stayed live — the share button's
clipboard-copy fallback still uses them.

The toggle open/close handler (grid-rows expand, `aria-expanded`, `inert`
toggling on `#donate-tiers`):

```js
var supportToggle = document.getElementById("supportToggle");
var tiersWrap = document.getElementById("donate-tiers");
if (supportToggle && tiersWrap) {
  supportToggle.addEventListener("click", function () {
    var isOpen = supportToggle.getAttribute("aria-expanded") === "true";
    var next = !isOpen;
    supportToggle.setAttribute("aria-expanded", String(next));
    tiersWrap.classList.toggle("is-open", next);
    if (next) {
      tiersWrap.removeAttribute("inert");
    } else {
      tiersWrap.setAttribute("inert", "");
    }
  });
}
```
