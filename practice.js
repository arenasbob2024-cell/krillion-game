/* Practice dive for the Krillion Game Guide.
   Runs entirely in the browser against our own prompt bank. No network calls. */
(function () {
  "use strict";

  var DATA = window.KR_PRACTICE;
  if (!DATA) return;

  var QUESTIONS = DATA.prompts;
  var TIER_NAMES = DATA.tiers;
  var TIER_POINTS = DATA.points;
  var ROUND_SIZE = 7;
  var SECONDS = 25;
  var MAX_SCORE = ROUND_SIZE * 100;

  var el = {
    start: document.getElementById("startPane"),
    play: document.getElementById("playPane"),
    end: document.getElementById("endPane"),
    startBtn: document.getElementById("startBtn"),
    promptNo: document.getElementById("promptNo"),
    cat: document.getElementById("cat"),
    prompt: document.getElementById("promptText"),
    form: document.getElementById("answerForm"),
    input: document.getElementById("answerInput"),
    submit: document.getElementById("submitBtn"),
    timerFill: document.getElementById("timerFill"),
    timerText: document.getElementById("timerText"),
    feedback: document.getElementById("feedback"),
    depthFill: document.getElementById("depthFill"),
    depthLabel: document.getElementById("depthLabel"),
    resultScore: document.getElementById("resultScore"),
    resultDepth: document.getElementById("resultDepth"),
    resultDetail: document.getElementById("resultDetail"),
    tierList: document.getElementById("tierList"),
    shareBtn: document.getElementById("shareBtn"),
    againBtn: document.getElementById("againBtn")
  };
  if (!el.start || !el.play) return;

  var state = {
    queue: [],
    idx: 0,
    score: 0,
    results: [],
    timerId: null,
    remaining: SECONDS,
    locked: true,
    startedAt: 0,
    roundId: 0
  };

  function shuffle(list) {
    var a = list.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function normalize(s) {
    return String(s || "")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/&/g, " and ")
      .replace(/[^a-z0-9 ]/g, " ")
      .replace(/\s+/g, " ")
      .trim()
      .replace(/^the /, "");
  }

  function levenshtein(a, b) {
    if (a === b) return 0;
    if (Math.abs(a.length - b.length) > 2) return 99;
    var prev = [], cur = [], i, j;
    for (j = 0; j <= b.length; j++) prev[j] = j;
    for (i = 1; i <= a.length; i++) {
      cur[0] = i;
      for (j = 1; j <= b.length; j++) {
        cur[j] = Math.min(
          prev[j] + 1,
          cur[j - 1] + 1,
          prev[j - 1] + (a.charAt(i - 1) === b.charAt(j - 1) ? 0 : 1)
        );
      }
      prev = cur.slice();
    }
    return prev[b.length];
  }

  function findAnswer(q, raw) {
    var n = normalize(raw);
    if (!n) return null;
    var i, j, entry, alias;
    for (i = 0; i < q.answers.length; i++) {
      entry = q.answers[i];
      for (j = 0; j < entry.a.length; j++) {
        if (normalize(entry.a[j]) === n) return entry;
      }
    }
    if (n.length >= 7) {
      for (i = 0; i < q.answers.length; i++) {
        entry = q.answers[i];
        for (j = 0; j < entry.a.length; j++) {
          alias = normalize(entry.a[j]);
          if (alias.length >= 7 && levenshtein(alias, n) <= 1) return entry;
        }
      }
    }
    return null;
  }

  function updateDepth(points) {
    var pct = Math.min(100, Math.round(points / MAX_SCORE * 100));
    el.depthFill.style.width = pct + "%";
    el.depthLabel.textContent = Math.round(points * 10).toLocaleString() + " m / 7,000 m";
  }

  function clearTimer() {
    if (state.timerId) { clearInterval(state.timerId); state.timerId = null; }
  }

  function startTimer() {
    clearTimer();
    state.remaining = SECONDS * 1000;
    var last = performance.now();
    el.timerFill.style.width = "100%";
    el.timerText.textContent = SECONDS.toFixed(1) + "s";
    state.timerId = setInterval(function () {
      var now = performance.now();
      state.remaining -= (now - last);
      last = now;
      var secs = Math.max(0, state.remaining / 1000);
      el.timerFill.style.width = (secs / SECONDS * 100) + "%";
      el.timerText.textContent = secs.toFixed(1) + "s";
      if (secs <= 0) {
        clearTimer();
        onTimeout();
      }
    }, 100);
  }

  function setFeedback(html, cls) {
    el.feedback.className = cls || "";
    el.feedback.innerHTML = html;
  }

  function showPrompt() {
    var q = state.queue[state.idx];
    state.locked = false;
    el.promptNo.textContent = "Prompt " + (state.idx + 1) + " / " + ROUND_SIZE;
    el.cat.textContent = q.cat;
    el.prompt.textContent = q.q;
    el.input.value = "";
    el.input.disabled = false;
    el.submit.disabled = false;
    setFeedback("", "");
    el.input.focus();
    startTimer();
  }

  function lockPrompt() {
    state.locked = true;
    el.input.disabled = true;
    el.submit.disabled = true;
    clearTimer();
  }

  function record(points, tierIndex) {
    state.score += points;
    state.results.push({ points: points, tier: tierIndex });
    updateDepth(state.score);
  }

  function scheduleNext(delay) {
    var rid = state.roundId;
    setTimeout(function () {
      if (rid === state.roundId) next();
    }, delay);
  }

  function onValid(entry) {
    var points = TIER_POINTS[entry.t];
    var tier = TIER_NAMES[entry.t];
    record(points, entry.t);
    setFeedback(
      '<span class="fb-good">' + tier + " · +" + points + " pts · " +
      (points * 10).toLocaleString() + " m deeper</span>" +
      '<div class="answers">Accepted answer: ' + entry.a[0] + "</div>",
      ""
    );
    lockPrompt();
    scheduleNext(1700);
  }

  function onTimeout() {
    if (state.locked) return;
    var q = state.queue[state.idx];
    lockPrompt();
    record(0, -1);
    var samples = q.answers.slice(0, 3).map(function (a) { return a.a[0]; }).join(", ");
    setFeedback(
      '<span class="fb-bad">Time. 0 points for this prompt.</span>' +
      '<div class="answers">Some answers our bank accepts: ' + samples + " …</div>",
      ""
    );
    scheduleNext(2600);
  }

  function next() {
    state.idx += 1;
    if (state.idx >= ROUND_SIZE) {
      finish();
      return;
    }
    showPrompt();
  }

  function finish() {
    el.play.hidden = true;
    el.end.hidden = false;
    var depth = state.score * 10;
    el.resultScore.textContent = state.score + " / 700 pts";
    el.resultDepth.textContent = "Depth reached: " + depth.toLocaleString() + " m";
    var pct = Math.round(state.score / MAX_SCORE * 100);
    var tierCounts = {};
    state.results.forEach(function (r) {
      if (r.tier >= 0) tierCounts[r.tier] = (tierCounts[r.tier] || 0) + 1;
    });
    var detail = "That is " + pct + "% of the 7,000 m trench floor.";
    el.resultDetail.textContent = detail;

    el.tierList.innerHTML = "";
    TIER_NAMES.forEach(function (name, i) {
      if (tierCounts[i]) {
        var s = document.createElement("span");
        s.textContent = name + " × " + tierCounts[i];
        el.tierList.appendChild(s);
      }
    });
    var misses = state.results.filter(function (r) { return r.tier === -1; }).length;
    if (misses) {
      var m = document.createElement("span");
      m.textContent = "No answer × " + misses;
      el.tierList.appendChild(m);
    }

    try {
      var best = parseInt(localStorage.getItem("krb_best") || "0", 10) || 0;
      if (state.score > best) localStorage.setItem("krb_best", String(state.score));
    } catch (e) { /* storage can be blocked */ }

    var bestNow = 0;
    try { bestNow = parseInt(localStorage.getItem("krb_best") || "0", 10) || 0; } catch (e) {}
    if (bestNow) {
      var b = document.createElement("span");
      b.textContent = "Your best: " + bestNow + " pts";
      el.tierList.appendChild(b);
    }
  }

  function startRound() {
    state.roundId += 1;
    clearTimer();
    state.queue = shuffle(QUESTIONS).slice(0, ROUND_SIZE);
    state.idx = 0;
    state.score = 0;
    state.results = [];
    state.startedAt = Date.now();
    updateDepth(0);
    el.start.hidden = true;
    el.end.hidden = true;
    el.play.hidden = false;
    showPrompt();
  }

  el.startBtn.addEventListener("click", startRound);
  el.againBtn.addEventListener("click", startRound);

  el.form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    if (state.locked) return;
    var raw = el.input.value.trim();
    if (!raw) return;
    var q = state.queue[state.idx];
    var entry = findAnswer(q, raw);
    if (entry) {
      onValid(entry);
    } else {
      setFeedback(
        '<span class="fb-miss">Not in our practice answer set.</span> ' +
        "Try another valid answer — the timer is still running. " +
        '<div class="answers">Our bank is small, so a valid answer can be missing.</div>',
        ""
      );
      el.input.select();
    }
  });

  el.shareBtn.addEventListener("click", function () {
    var text = "Krillion practice dive: " + state.score + "/700 pts · " +
      (state.score * 10).toLocaleString() + " m / 7,000 m. " +
      "7 prompts, 25 seconds each. Practice tool: " + location.origin + "/practice/";
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () {
        el.shareBtn.textContent = "Copied!";
        setTimeout(function () { el.shareBtn.textContent = "Copy result"; }, 1800);
      }, function () { window.prompt("Copy your result:", text); });
    } else {
      window.prompt("Copy your result:", text);
    }
  });

  updateDepth(0);
})();
