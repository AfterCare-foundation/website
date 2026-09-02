// Works around Chrome on iOS hiding the top of the page behind its own chrome.
//
// Opening a link from another app (Signal, Telegram) puts Chrome into a state
// where, shortly after first paint, it expands its web view to the full screen
// and overlays its toolbars — without offsetting the page. The top ~110px of
// the document then renders behind the status bar, the "back to <app>" banner
// and the URL bar. Measured on an iPhone (852px screen): 108px swallowed,
// which is enough to eat the hero's kicker and slice the logo in half.
//
// Nothing in the platform reports this. scrollY stays 0, the safe-area insets
// are 0px (it is not a viewport-fit=cover problem), and visualViewport
// .offsetTop is 0 — the browser believes the top of the document is on screen.
// The one detectable symptom is that window.innerHeight jumps to the full
// screen height while documentElement.clientHeight stays at the visible area
// (852 vs 665). Chrome fixes itself on the first scroll, at which point the
// two reconverge — so the offset set here lifts at the same moment Chrome
// shifts the page down by roughly the same amount, and the two cancel out
// instead of the content visibly jumping.
//
// Linked from index.html, privacy/index.html and funding/index.html. Consumed
// by each page's `body` padding and by .a11y-widget in a11y-panel.css, both
// via var(--chrome-top-inset, 0px), so any page that forgets to load this
// simply gets 0 and behaves as before.
(function () {
  var root = document.documentElement;

  // A horizontal scrollbar makes innerHeight exceed clientHeight by ~15px on
  // desktop; only a gap far larger than that means real chrome over the page.
  var MIN_GAP = 60;
  var OFFSET = "110px";

  function sync() {
    // Before first layout clientHeight is 0, which would read as a huge gap.
    if (!root.clientHeight) return;
    var gap = window.innerHeight - root.clientHeight;
    root.style.setProperty(
      "--chrome-top-inset",
      gap > MIN_GAP ? OFFSET : "0px"
    );
  }

  sync();
  window.addEventListener("resize", sync);
  window.addEventListener("orientationchange", sync);
  window.addEventListener("scroll", sync, { passive: true });
  if (window.visualViewport) {
    window.visualViewport.addEventListener("resize", sync);
  }
})();
