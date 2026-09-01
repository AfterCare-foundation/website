// Shared accessibility widget behavior — linked identically from index.html,
// privacy/index.html, and funding/index.html (see a11y-panel.css's own
// top-of-file note on why this is linked rather than tripled).
//
// This only wires up the interactive controls and keeps them in sync with
// whatever each page's own inline pre-paint <script> already applied to
// <html>'s data-* attributes — that script runs synchronously before first
// paint so a returning visitor never sees a flash of the wrong theme/size/
// contrast/motion; this file only needs to run once the DOM exists.
(function () {
  var TEXT_SIZES = ["md", "lg", "xl"];
  var root = document.documentElement;

  var widget = document.getElementById("a11yWidget");
  var toggle = document.getElementById("a11yToggle");
  var panel = document.getElementById("a11yPanel");
  var themeToggle = document.getElementById("a11yThemeToggle");
  var decreaseBtn = document.getElementById("a11yTextDecrease");
  var resetTextBtn = document.getElementById("a11yTextReset");
  var increaseBtn = document.getElementById("a11yTextIncrease");
  var contrastToggle = document.getElementById("a11yContrastToggle");
  var motionToggle = document.getElementById("a11yMotionToggle");
  var resetAllBtn = document.getElementById("a11yReset");

  function currentTextSize() {
    var size = root.dataset.textSize;
    return TEXT_SIZES.indexOf(size) !== -1 ? size : "md";
  }

  function updateStepperState() {
    var size = currentTextSize();
    var i = TEXT_SIZES.indexOf(size);
    if (decreaseBtn) decreaseBtn.disabled = i === 0;
    if (increaseBtn) increaseBtn.disabled = i === TEXT_SIZES.length - 1;
    if (resetTextBtn)
      resetTextBtn.setAttribute("aria-pressed", String(size === "md"));
  }

  function setTextSize(size) {
    if (size === "md") delete root.dataset.textSize;
    else root.dataset.textSize = size;
    try {
      localStorage.setItem("ac-text-size", size);
    } catch (e) {}
    updateStepperState();
  }

  function updateMetaColors() {
    var isLight = root.dataset.theme === "light";
    var themeColorMeta = document.querySelector('meta[name="theme-color"]');
    var colorSchemeMeta = document.querySelector('meta[name="color-scheme"]');
    if (themeColorMeta)
      themeColorMeta.setAttribute("content", isLight ? "#f5f6fa" : "#0a0a10");
    if (colorSchemeMeta)
      colorSchemeMeta.setAttribute("content", isLight ? "light" : "dark");
  }

  function setTheme(light) {
    if (light) {
      root.dataset.theme = "light";
      try {
        localStorage.setItem("ac-theme", "light");
      } catch (e) {}
    } else {
      delete root.dataset.theme;
      try {
        localStorage.setItem("ac-theme", "dark");
      } catch (e) {}
    }
    if (themeToggle) themeToggle.checked = !light;
    updateMetaColors();
  }

  function setContrast(high) {
    if (high) {
      root.dataset.contrast = "high";
      try {
        localStorage.setItem("ac-contrast", "high");
      } catch (e) {}
    } else {
      delete root.dataset.contrast;
      try {
        localStorage.removeItem("ac-contrast");
      } catch (e) {}
    }
    if (contrastToggle) contrastToggle.checked = high;
  }

  function setMotion(reduced) {
    if (reduced) {
      root.dataset.motion = "reduced";
      try {
        localStorage.setItem("ac-motion", "reduced");
      } catch (e) {}
    } else {
      delete root.dataset.motion;
      try {
        localStorage.removeItem("ac-motion");
      } catch (e) {}
    }
    if (motionToggle) motionToggle.checked = reduced;
  }

  // Sync the controls' own visible state to whatever the pre-paint script
  // already applied — never needs to re-run per navigation since this is a
  // plain multi-page site (no client-side router), just once on load.
  if (themeToggle) themeToggle.checked = root.dataset.theme !== "light";
  if (contrastToggle) contrastToggle.checked = root.dataset.contrast === "high";
  if (motionToggle) motionToggle.checked = root.dataset.motion === "reduced";
  updateStepperState();

  if (themeToggle)
    themeToggle.addEventListener("change", function () {
      setTheme(!themeToggle.checked);
    });
  if (decreaseBtn)
    decreaseBtn.addEventListener("click", function () {
      var i = TEXT_SIZES.indexOf(currentTextSize());
      setTextSize(TEXT_SIZES[Math.max(0, i - 1)]);
    });
  if (resetTextBtn)
    resetTextBtn.addEventListener("click", function () {
      setTextSize("md");
    });
  if (increaseBtn)
    increaseBtn.addEventListener("click", function () {
      var i = TEXT_SIZES.indexOf(currentTextSize());
      setTextSize(TEXT_SIZES[Math.min(TEXT_SIZES.length - 1, i + 1)]);
    });
  if (contrastToggle)
    contrastToggle.addEventListener("change", function () {
      setContrast(!!contrastToggle.checked);
    });
  if (motionToggle)
    motionToggle.addEventListener("change", function () {
      setMotion(!!motionToggle.checked);
    });

  if (resetAllBtn)
    resetAllBtn.addEventListener("click", function () {
      setTheme(false);
      setTextSize("md");
      setContrast(false);
      setMotion(false);
    });

  // Panel open/close: click pins it open until explicitly closed, layered
  // with a hover reveal for a quick peek without clicking. Escape, an
  // outside click, or tabbing focus out of the widget all close it.
  var pinned = false;
  function closePanel() {
    if (panel) panel.classList.remove("is-open");
    if (toggle) toggle.setAttribute("aria-expanded", "false");
    pinned = false;
  }
  function openPanel() {
    if (panel) panel.classList.add("is-open");
    if (toggle) toggle.setAttribute("aria-expanded", "true");
  }
  if (toggle)
    toggle.addEventListener("click", function (event) {
      event.stopPropagation();
      if (pinned) {
        closePanel();
      } else {
        openPanel();
        pinned = true;
      }
    });
  if (panel)
    panel.addEventListener("click", function (event) {
      event.stopPropagation();
    });
  document.addEventListener("click", closePanel);
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && panel && panel.classList.contains("is-open")) {
      closePanel();
      if (toggle) toggle.focus();
    }
  });
  if (widget)
    widget.addEventListener("focusout", function (event) {
      var next = event.relatedTarget;
      if (!next || !widget.contains(next)) closePanel();
    });
  var hoverCloseTimer;
  if (widget) {
    widget.addEventListener("pointerenter", function () {
      clearTimeout(hoverCloseTimer);
      openPanel();
    });
    widget.addEventListener("pointerleave", function (event) {
      if (pinned) return;
      if (event.pointerType === "touch") return;
      hoverCloseTimer = setTimeout(closePanel, 150);
    });
  }
})();
