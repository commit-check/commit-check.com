/*
 * Landing page demos: the commit-msg terminal in the hero and the tabbed
 * GitHub Action window.
 *
 * Loaded on every page through extra_javascript, and a no-op on every page
 * but the home page. Instant navigation swaps the page content without a
 * reload, so setup runs from the theme's document$ observable on each page
 * view, and whatever the previous view started is stopped first.
 *
 * The demos are plain HTML: index.md documents the data-* timeline
 * attributes, landing.css says what each state looks like, and this file only
 * moves the clock. Nothing animates under prefers-reduced-motion, or while a
 * demo is scrolled out of view.
 */
(function () {
  "use strict";

  var stops = [];

  function prefersReducedMotion() {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function each(root, selector, fn) {
    Array.prototype.forEach.call(root.querySelectorAll(selector), fn);
  }

  function prepare(root) {
    each(root, "[data-type]", function (el) {
      if (el.dataset.full === undefined) el.dataset.full = el.textContent;
    });
  }

  /* Put a timeline at `t` milliseconds. */
  function render(root, t) {
    each(root, "[data-on]", function (el) {
      el.classList.toggle("is-on", t >= Number(el.dataset.on));
    });
    each(root, "[data-from]", function (el) {
      el.classList.toggle("is-on", t >= Number(el.dataset.from));
    });
    each(root, "[data-until]", function (el) {
      el.classList.toggle("is-gone", t >= Number(el.dataset.until));
    });
    each(root, "[data-hl]", function (el) {
      el.classList.toggle("is-hl", t >= Number(el.dataset.hl));
    });
    each(root, "[data-type]", function (el) {
      var full = el.dataset.full;
      var speed = Number(el.dataset.speed || 50);
      var n = Math.floor((t - Number(el.dataset.type)) / speed);
      var text = full.slice(0, Math.max(0, Math.min(full.length, n)));
      if (el.textContent !== text) el.textContent = text;
    });
  }

  /* Back to the final frame, as if the script had never run. */
  function rest(root) {
    root.classList.remove("is-live");
    each(root, "[data-type]", function (el) {
      el.textContent = el.dataset.full;
    });
  }

  /* Runs `onFrame(now)` on every animation frame while `el` is on screen. */
  function whileVisible(el, onShow, onFrame) {
    var raf = null;
    function frame(now) {
      onFrame(now);
      raf = requestAnimationFrame(frame);
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting && raf === null) {
          onShow(performance.now());
          raf = requestAnimationFrame(frame);
        } else if (!entry.isIntersecting && raf !== null) {
          cancelAnimationFrame(raf);
          raf = null;
        }
      });
    }, { threshold: 0.25 });
    io.observe(el);
    return function () {
      io.disconnect();
      if (raf !== null) cancelAnimationFrame(raf);
    };
  }

  /* A timeline that plays on a loop: the hero terminal. */
  function setupLoop(root) {
    var loop = Number(root.dataset.loop);
    var start = 0;
    prepare(root);
    root.classList.add("is-live");
    render(root, 0);
    stops.push(whileVisible(root, function (now) {
      start = now;
    }, function (now) {
      render(root, (now - start) % loop);
    }));
  }

  /* The tabbed Action demo. */
  function setupDemo(demo, motion) {
    var tabs = Array.prototype.slice.call(demo.querySelectorAll('[role="tab"]'));
    var panels = tabs.map(function (tab) {
      return document.getElementById(tab.getAttribute("aria-controls"));
    });
    var cycle = Number(demo.dataset.cycle);
    var current = 0;
    var start = performance.now();
    // Cycles through the tabs until the reader picks one, then stays put.
    var autoplay = motion;
    var hovering = false;

    function select(index, focus) {
      tabs.forEach(function (tab, i) {
        var on = i === index;
        tab.setAttribute("aria-selected", on ? "true" : "false");
        tab.tabIndex = on ? 0 : -1;
        tab.style.setProperty("--p", "0");
        panels[i].hidden = !on;
        rest(panels[i]);
      });
      current = index;
      start = performance.now();
      if (motion) {
        panels[index].classList.add("is-live");
        render(panels[index], 0);
      }
      if (focus) tabs[index].focus();
    }

    function choose(index, focus) {
      autoplay = false;
      select(index, focus);
    }

    tabs.forEach(function (tab, i) {
      tab.addEventListener("click", function () {
        choose(i, false);
      });
    });

    demo.querySelector('[role="tablist"]').addEventListener("keydown", function (event) {
      var last = tabs.length - 1;
      var next = {
        ArrowRight: current === last ? 0 : current + 1,
        ArrowLeft: current === 0 ? last : current - 1,
        Home: 0,
        End: last
      }[event.key];
      if (next === undefined) return;
      event.preventDefault();
      choose(next, true);
    });

    demo.addEventListener("pointerenter", function () { hovering = true; });
    demo.addEventListener("pointerleave", function () { hovering = false; });
    demo.addEventListener("focusin", function () { hovering = true; });
    demo.addEventListener("focusout", function () { hovering = false; });

    panels.forEach(prepare);
    demo.classList.add("is-ready");
    select(0, false);

    if (!motion) return;

    stops.push(whileVisible(demo, function (now) {
      start = now;
    }, function (now) {
      var t = now - start;
      render(panels[current], t);
      if (!autoplay) return;
      tabs[current].style.setProperty("--p", String(Math.min(1, t / cycle)));
      if (t >= cycle && !hovering) select((current + 1) % tabs.length, false);
    }));
  }

  function setupCopy(button) {
    button.addEventListener("click", function () {
      var source = button.dataset.copyFrom
        ? document.getElementById(button.dataset.copyFrom).textContent
        : button.dataset.copy;
      if (!navigator.clipboard) return;
      navigator.clipboard.writeText(source).then(function () {
        var label = button.getAttribute("aria-label");
        var text = button.textContent;
        button.classList.add("is-done");
        if (label) button.setAttribute("aria-label", "Copied");
        if (!label) button.textContent = "Copied";
        setTimeout(function () {
          button.classList.remove("is-done");
          if (label) button.setAttribute("aria-label", label);
          if (!label) button.textContent = text;
        }, 1600);
      });
    });
  }

  function init() {
    stops.forEach(function (stop) { stop(); });
    stops = [];

    var motion = !prefersReducedMotion() && "IntersectionObserver" in window;
    if (motion) each(document, ".cc-term .cc-tl[data-loop]", setupLoop);
    each(document, ".cc-demo", function (demo) { setupDemo(demo, motion); });
    each(document, ".cc-copy", setupCopy);
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(init);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
