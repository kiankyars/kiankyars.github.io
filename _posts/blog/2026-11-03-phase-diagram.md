---
layout: post
title: Can LLMs predict water's state?
date: 2026-11-03
categories: machine_learning
---

Thinking of how to use left-over API credits, I questioned 28 language models[^models] 1,180,160 times on the state of pure water at different temperatures and pressures, [repo](https://github.com/kiankyars/phase-diagram). Each question followed this format:

> Pure water at equilibrium, at 450.00 kelvin and 2.000 megapascals: solid, liquid, vapor, or supercritical? Do not say anything else.

The questions were independent, with no tools or memory; cost was \$796: \$462 from Ant and \$334 from Oai at batch prices. From the answers I drew the phase diagram of each model against the IAPWS reference equations.

## Results

Scores are balanced accuracy: the average share correct over the four phases. 0.25 is guessing and 1 is perfect. They are measured in kelvin and megapascals on the same 64 × 64 points for every model, you can click a map to explore it below.

<div class="pd-segments" id="atlasCondition"></div>
<div class="pd-key" id="atlasKey"></div>
<div class="pd-atlas" id="atlas"></div>

## Explore one model

Hover over a pixel (or tap it, or use the arrow keys) to see the exact prompt, what the model said and the true phase.

<div class="pd-explorer">
  <select id="model" aria-label="Model"></select>
  <div class="pd-label">Mode</div>
  <div class="pd-segments" id="condition"></div>
  <div class="pd-label">Units in the prompt</div>
  <div class="pd-segments" id="units"></div>
  <div class="pd-label">Show</div>
  <div class="pd-segments" id="view"></div>
  <div class="pd-frame">
    <div class="pd-y" id="yAxis" aria-hidden="true"></div>
    <div class="pd-map" id="bigMap" tabindex="0" aria-label="Phase diagram. Use the arrow keys to move between cells.">
      <canvas id="bigCanvas"></canvas>
      <svg viewBox="0 0 1000 1000" preserveAspectRatio="none" aria-hidden="true"><use href="#pdLines"></use><rect class="pd-cursor-shadow" id="cursorShadow"></rect><rect class="pd-cursor" id="cursor"></rect></svg>
    </div>
    <div class="pd-x" id="xAxis" aria-hidden="true"></div>
  </div>
  <div class="pd-key" id="bigKey"></div>
  <p class="pd-prompt" id="prompt"></p>
  <div class="pd-verdict"><div><small>Model</small><b id="said">–</b></div><div><small>IAPWS</small><b id="truth">–</b></div></div>
</div>

<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><g id="pdLines"></g></defs></svg>

Without reasoning, 84–98% of points sit in the biggest connected patch of their phase; however, balanced accuracy is only 0.63 to 0.83. The big misses are liquid above the critical pressure, which models call supercritical or ice (68% wrong), and vapor below 0 °C (56% wrong).

## Reasoning fixes most of it

<div class="pd-key"><span><i class="pd-dot hollow"></i>Answering instantly</span><span><i class="pd-dot" style="background:var(--text)"></i>Reasoning allowed</span></div>
<div id="effect"></div>

Each line below is where one model stops saying vapor (boiling) or solid (melting). Black lines are the truth.

<div class="pd-segments" id="fanCondition"></div>
<div class="pd-key" style="margin-top:6px"><span><i class="pd-dot" style="background:#d97757"></i>Anthropic</span><span><i class="pd-dot" style="background:#10a37f"></i>OpenAI</span></div>
<div id="fan"></div>
<div class="pd-tip" id="tip" hidden></div>

18 models can answer both ways, and reasoning made all 18 better: balanced accuracy rose by a median of 0.20. Median melting curve error fell from 77 K to 20 K. Boiling curve error fell from 0.58 to 0.006 decades of pressure (a decade is a factor of 10). GPT-5.6 Sol, GPT-6 Astra and GPT-6.1 Sol get the melting curve right at all but one or two of 39 pressures.

Haiku 5.5 gains the most, from 0.63 to 0.96, because instantly it almost never says liquid. Sonnet 5 gains the least, from 0.79 to 0.85, because with reasoning it calls even more hot gas supercritical.

## Do newer models do better?

It depends on the curve. Answering instantly, OpenAI's boiling curve moved toward the truth: the error fell from about 2 decades on GPT-4o mini to about 0.2 on GPT-5.5 and GPT-6 Sol. Their melting curve went the other way. OpenAI's three oldest models put ice 46–193 K too cold above 209 MPa, and its models from GPT-5.4 on put it 65–351 K too hot. Thirteen of the 22 instant models turn hot compressed liquid into ice below 1 GPa, where the true melting pressure is 3 to 12 GPa.

![Accuracy and boundary error by release date](/imgs/2026-11-03-phase-diagram/generations.png)

Over time, balanced accuracy barely moves. Since September 2025, the period both providers cover, neither provider's instant trend is clear, and with reasoning allowed neither shows a clear gain either. Anthropic's older models are retired, so its history only goes back to September 2025, while OpenAI's goes back to July 2024.

## Changing the units changes the answer

![Agreement across units against agreement on a repeat](/imgs/2026-11-03-phase-diagram/units_gap_instant.png)

I asked the same points in six sets of units: kelvin or Celsius, with pascals, megapascals or atmospheres. I also asked two of them, kelvin with megapascals and Celsius with atmospheres, a second time to see how much answers move by chance. Answering instantly, all 22 models change their answers more when only the units change. Sonnet 4.6 agrees with itself on 96% of repeats but only 76% of unit changes. Opus 5 calls hot gas supercritical 85–89% of the time in kelvin and 18–22% in Celsius. With reasoning allowed, the gap is at most 0.06.

Part of this is how the number is written rather than the unit itself: 2 MPa is "2.000 megapascals" but "2.000e6 pascals".

## Models think hardest near the boundaries

![Reasoning tokens spent at each point for four models](/imgs/2026-11-03-phase-diagram/thought_map.png)

Darker cells above took more reasoning tokens, and they trace the true boundaries, cool! Opus 5.5 reasons on 79% of points near a boundary and 20% of the rest, Sonnet 5.5 on 76% and 17%.

## Caveats

- Hot gas below the critical pressure counts as vapor and dense fluid above it counts as liquid. That is the textbook convention, but the prompt doesn't say so. If I accept "supercritical" for vapor above 647 K and liquid above 22 MPa, the best instant score rises from 0.83 to 0.92.
- Reasoning settings differ between models, so the reasoning comparison is not fully controlled.
- The whole experiment was run by Claude Opus 5.5, which is also one of the graded models.

<style>
  .pd-atlas { display: grid; grid-template-columns: repeat(auto-fill, minmax(112px, 1fr)); gap: 14px 10px; margin: 1rem 0 1.5rem; }
  .pd-group { grid-column: 1 / -1; font-weight: 700; color: var(--muted); border-bottom: 1px solid var(--border); padding-bottom: 2px; margin-top: 0.4rem; }
  .pd-tile { all: unset; display: grid; gap: 3px; cursor: pointer; min-width: 0; }
  .pd-tile:focus-visible { outline: 2px solid var(--link); outline-offset: 3px; }
  .pd-tile.ref { cursor: default; }
  .pd-head { display: flex; justify-content: space-between; gap: 4px; font-size: 0.76rem; line-height: 1.2; }
  .pd-head b { font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0; }
  .pd-head span { white-space: nowrap; }
  .pd-tile:not(.ref):hover b, .pd-tile.on b { color: var(--link); }
  .pd-map { position: relative; aspect-ratio: 1; width: 100%; background: var(--border); }
  .pd-map canvas, .pd-map svg { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
  .pd-map canvas { image-rendering: pixelated; }
  .pd-map svg { pointer-events: none; overflow: visible; }
  #pdLines polyline { fill: none; stroke: #111; stroke-width: 1; vector-effect: non-scaling-stroke; stroke-linejoin: round; }
  .pd-explorer { display: grid; gap: 8px; margin: 1rem 0; }
  .pd-explorer select { font: inherit; font-size: 1.15rem; font-weight: 700; padding: 6px 8px; color: var(--text); background: light-dark(#fff, #1c1c1c); border: 1px solid var(--border); max-width: 320px; }
  .pd-label { font-size: 0.72rem; letter-spacing: 0.05em; text-transform: uppercase; color: var(--muted); margin-top: 4px; }
  .pd-segments { display: flex; flex-wrap: wrap; }
  .pd-segments input { position: absolute; opacity: 0; width: 1px; height: 1px; }
  .pd-segments label { font-size: 0.85rem; padding: 5px 10px; border: 1px solid var(--border); margin: 0 -1px -1px 0; cursor: pointer; color: var(--muted); }
  .pd-segments input:checked + label { background: var(--text); border-color: var(--text); color: light-dark(#fff, #111); }
  .pd-segments input:focus-visible + label { outline: 2px solid var(--link); outline-offset: 2px; }
  .pd-segments input:disabled + label { opacity: 0.4; cursor: not-allowed; }
  .pd-frame { display: grid; grid-template-columns: 46px minmax(0, 1fr); grid-template-rows: auto 24px; margin-top: 10px; }
  .pd-y, .pd-x { position: relative; font-size: 0.72rem; color: var(--muted); }
  .pd-y span { position: absolute; right: 6px; transform: translateY(-50%); white-space: nowrap; }
  .pd-x { grid-column: 2; }
  .pd-x span { position: absolute; top: 4px; transform: translateX(-50%); white-space: nowrap; }
  #bigMap { cursor: crosshair; touch-action: none; }
  #bigMap:focus-visible { outline: 2px solid var(--link); outline-offset: 3px; }
  .pd-cursor { fill: none; stroke: #fff; stroke-width: 2; vector-effect: non-scaling-stroke; }
  .pd-cursor-shadow { fill: none; stroke: #000; stroke-width: 4; vector-effect: non-scaling-stroke; }
  .pd-key { display: flex; flex-wrap: wrap; gap: 4px 14px; font-size: 0.8rem; color: var(--muted); }
  .pd-key i { display: inline-block; width: 11px; height: 11px; margin-right: 5px; vertical-align: -1px; }
  .pd-prompt { font-family: ui-monospace, Menlo, monospace; font-size: 0.88rem; min-height: 4.2em; margin: 0.5rem 0 0; }
  .pd-verdict { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .pd-verdict small { display: block; font-size: 0.72rem; letter-spacing: 0.05em; text-transform: uppercase; color: var(--muted); }
  .pd-verdict b { font-size: 1.35rem; }
  .pd-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; vertical-align: -1px; }
  .pd-dot.hollow { box-shadow: inset 0 0 0 2px var(--muted); }
  #effect svg { display: block; width: 100%; height: auto; margin: 0.5rem 0 1rem; }
  #effect text { font-size: 12px; fill: var(--muted); }
  #effect .name { fill: var(--text); font-size: 13px; }
  #effect .grid { stroke: var(--border); }
  #effect .bar { stroke: light-dark(#c3c2b7, #555); stroke-width: 3; stroke-linecap: round; }
  #effect .row:hover .name { fill: var(--link); }
  #fan svg { display: block; width: 100%; height: auto; margin: 0.5rem 0 1rem; }
  #fan text { font-size: 12px; fill: var(--muted); }
  #fan .grid { stroke: var(--border); }
  #fan .line { pointer-events: none; fill: none; stroke-width: 1.4; stroke-linejoin: round; opacity: 0.75; }
  #fan .truth { fill: none; stroke: var(--text); stroke-width: 2.2; pointer-events: none; }
  .pd-tip { position: fixed; z-index: 20; pointer-events: none; background: var(--text); color: light-dark(#fff, #111); font-size: 0.78rem; padding: 5px 8px; line-height: 1.35; }
</style>

<script>
(function () {
  "use strict";
  const PHASES = ["Solid", "Liquid", "Vapor", "Supercritical"];
  const COLORS = [[42, 120, 214], [0, 131, 0], [237, 161, 0], [232, 123, 164]];
  const NONE = [195, 194, 183];
  const RIGHT = [226, 228, 228];
  const CONDITIONS = [["instant", "Answering instantly"], ["reasoned", "Reasoning allowed"]];
  const VIEWS = [["answers", "Answers"], ["errors", "Mistakes only"]];
  const PROVIDER = { anthropic: "Anthropic", openai: "OpenAI" };
  const $ = (id) => document.getElementById(id);
  const svgNS = "http://www.w3.org/2000/svg";
  let D;
  const state = { model: null, condition: "instant", units: null, view: "answers", cell: null, atlas: "instant" };

  const key = (id, condition, units) => `${id}|${condition}|${units}`;
  const current = () => D.maps[key(state.model, state.condition, state.units)];
  const has = (id, condition) => !!D.maps[key(id, condition, D.framings[0].key)];
  const named = (m) => m.label + (m.thinks ? " *" : "");
  const fixed = (x, n) => (x === null || x === undefined ? "–" : x.toFixed(n));

  fetch("/imgs/2026-11-03-phase-diagram/maps.json?v=3").then((r) => r.json()).then((data) => {
    D = data;
    state.units = D.framings[0].key;
    state.model = D.models.find((m) => m.label === "Sonnet 4.6").id;
    buildLines();
    buildAxes();
    for (const host of [$("atlasKey"), $("bigKey")]) legend(host);
    for (const m of D.models) $("model").add(new Option(named(m), m.id));
    $("model").addEventListener("change", () => setModel($("model").value));
    segments($("atlasCondition"), "atlasCondition", CONDITIONS, state.atlas, (v) => { state.atlas = v; renderAtlas(); });
    segments($("view"), "view", VIEWS, state.view, (v) => { state.view = v; renderBig(); });
    hookMap();
    renderAtlas();
    renderEffect();
    segments($("fanCondition"), "fanCondition", CONDITIONS, "instant", renderFan);
    renderFan("instant");
    setModel(state.model);
  });

  /* Each grid level keeps one question per block of the finest grid. */
  const lookups = {};
  function lookup(level) {
    if (lookups[level]) return lookups[level];
    const side = D.side >> level;
    const table = new Int32Array(side * side).fill(-1);
    for (let pid = 0; pid < D.side * D.side; pid++) {
      if (+D.levelOf[pid] >= level) table[(Math.floor(pid / D.side) >> level) * side + ((pid % D.side) >> level)] = pid;
    }
    return (lookups[level] = table);
  }

  const answerPaint = (c) => (c >= "0" && c <= "3" ? COLORS[+c] : NONE);
  function errorPaint(level) {
    const table = lookup(level);
    const side = D.side >> level;
    return (c, i, j) => (c === D.truth[table[i * side + j]] ? RIGHT : answerPaint(c));
  }

  function draw(canvas, cells, side, paint) {
    canvas.width = canvas.height = side;
    const ctx = canvas.getContext("2d");
    const image = ctx.createImageData(side, side);
    for (let i = 0; i < side; i++) {
      for (let j = 0; j < side; j++) image.data.set([...paint(cells[i * side + j], i, j), 255], ((side - 1 - j) * side + i) * 4);
    }
    ctx.putImageData(image, 0, 0);
  }

  function buildLines() {
    const { tMin, tMax, logpMin, logpMax } = D.bounds;
    for (const line of D.curves) {
      const path = document.createElementNS(svgNS, "polyline");
      path.setAttribute("points", line.map(([t, p]) => `${(1000 * (t - tMin)) / (tMax - tMin)},${1000 * (1 - (p - logpMin) / (logpMax - logpMin))}`).join(" "));
      $("pdLines").appendChild(path);
    }
  }

  function buildAxes() {
    const { tMin, tMax, logpMin, logpMax } = D.bounds;
    for (const t of [200, 300, 400, 500, 600, 700, 800]) {
      const tick = document.createElement("span");
      tick.textContent = t === 800 ? "800 K" : t;
      tick.style.left = `${(100 * (t - tMin)) / (tMax - tMin)}%`;
      $("xAxis").appendChild(tick);
    }
    for (const [p, name] of [[0, "1 Pa"], [3, "1 kPa"], [6, "1 MPa"], [9, "1 GPa"]]) {
      const tick = document.createElement("span");
      tick.textContent = name;
      tick.style.top = `${100 * (1 - (p - logpMin) / (logpMax - logpMin))}%`;
      $("yAxis").appendChild(tick);
    }
  }

  function legend(host) {
    host.innerHTML = PHASES.map((name, k) => `<span><i style="background:rgb(${COLORS[k]})"></i>${name}</span>`).join("");
  }

  function segments(host, name, options, chosen, onChange) {
    host.innerHTML = "";
    for (const [value, text, disabled] of options) {
      const input = Object.assign(document.createElement("input"), { type: "radio", name, id: `${name}-${value}`, value, checked: value === chosen, disabled: !!disabled });
      input.addEventListener("change", () => onChange(value));
      const label = document.createElement("label");
      label.htmlFor = input.id;
      label.textContent = text;
      host.append(input, label);
    }
  }

  function tile(name, score, cells, side, onClick) {
    const node = document.createElement(onClick ? "button" : "div");
    node.className = onClick ? "pd-tile" : "pd-tile ref";
    if (onClick) node.type = "button";
    node.innerHTML = `<span class="pd-head"><b>${name}</b><span>${score}</span></span><span class="pd-map"><canvas></canvas><svg viewBox="0 0 1000 1000" preserveAspectRatio="none"><use href="#pdLines"></use></svg></span>`;
    draw(node.querySelector("canvas"), cells, side, answerPaint);
    if (onClick) node.addEventListener("click", onClick);
    return node;
  }

  function renderAtlas() {
    const host = $("atlas");
    host.innerHTML = "";
    for (const provider of ["anthropic", "openai"]) {
      const title = document.createElement("div");
      title.className = "pd-group";
      title.textContent = PROVIDER[provider];
      host.appendChild(title);
      for (const m of D.models.filter((x) => x.provider === provider && has(x.id, state.atlas))) {
        const entry = D.maps[key(m.id, state.atlas, D.framings[0].key)];
        host.appendChild(tile(named(m), fixed(m.atlas[state.atlas], 2), entry.cells, D.side >> entry.level, () => {
          state.condition = state.atlas;
          setModel(m.id);
          $("model").scrollIntoView({ behavior: "smooth", block: "start" });
        }));
      }
    }
    const note = document.createElement("div");
    note.className = "pd-group";
    note.style.border = "0";
    note.style.fontWeight = "400";
    note.textContent = "* Cannot turn reasoning off.";
    host.appendChild(note);
  }

  /* Not every model has every mode or set of units, so those stay disabled. */
  function setModel(id) {
    state.model = id;
    $("model").value = id;
    if (!has(id, state.condition)) state.condition = has(id, "instant") ? "instant" : "reasoned";
    segments($("condition"), "condition", CONDITIONS.map(([v, t]) => [v, t, !has(id, v)]), state.condition, (v) => { state.condition = v; renderUnits(); renderBig(); });
    renderUnits();
    renderBig();
  }

  function renderUnits() {
    const available = (u) => !!D.maps[key(state.model, state.condition, u)];
    if (!available(state.units)) state.units = D.framings[0].key;
    segments($("units"), "units", D.framings.map((f) => [f.key, f.label, !available(f.key)]), state.units, (v) => { state.units = v; renderBig(); });
  }

  function renderBig() {
    const entry = current();
    draw($("bigCanvas"), entry.cells, D.side >> entry.level, state.view === "errors" ? errorPaint(entry.level) : answerPaint);
    readout();
  }

  function number(x, sig = 4) {
    const [mantissa, raw] = x.toExponential(sig - 1).split("e");
    const exponent = +raw;
    if (exponent >= -3 && exponent < 6) return Number(`${mantissa}e${exponent}`).toFixed(Math.max(sig - 1 - exponent, 0));
    return `${mantissa}e${exponent}`;
  }

  /* The prompt, written exactly as the experiment wrote it. */
  function readout() {
    const entry = current();
    const side = D.side >> entry.level;
    const cell = state.cell || { x: 0.39, y: 0.57 };
    const i = Math.min(Math.floor(cell.x * side), side - 1);
    const j = Math.min(Math.floor(cell.y * side), side - 1);
    const pid = lookup(entry.level)[i * side + j];
    const f = D.framings.find((x) => x.key === state.units);
    const T = D.T[pid], p = D.p[pid];
    const temperature = f.t === "K" ? `${T.toFixed(2)} kelvin` : `${(T - 273.15).toFixed(2)} degrees Celsius`;
    const pressure = f.p === "Pa" ? `${number(p)} pascals` : f.p === "MPa" ? `${number(p / 1e6)} megapascals` : `${number(p / 101325)} atmospheres`;
    $("prompt").textContent = `Pure water at equilibrium, at ${temperature} and ${pressure}: solid, liquid, vapor, or supercritical? Do not say anything else.`;
    const said = entry.cells[i * side + j];
    const truth = D.truth[pid];
    $("said").textContent = said >= "0" && said <= "3" ? PHASES[+said] : "No answer";
    $("said").style.color = said === truth ? "rgb(0, 131, 0)" : "";
    $("truth").textContent = PHASES[+truth];
    const size = 1000 / side;
    for (const id of ["cursor", "cursorShadow"]) {
      const rect = $(id);
      rect.setAttribute("x", i * size);
      rect.setAttribute("y", (side - 1 - j) * size);
      rect.setAttribute("width", size);
      rect.setAttribute("height", size);
    }
  }

  /* Each model with and without reasoning, on the same points as the atlas. */
  function renderEffect() {
    const W = 680, left = 120, right = 14, top = 26, rowH = 22;
    const x = (v) => left + ((v - 0.5) / 0.5) * (W - left - right);
    let y = 0, body = "";
    for (const provider of ["anthropic", "openai"]) {
      y += 30;
      body += `<text class="name" x="0" y="${y}" style="font-weight:700">${PROVIDER[provider]}</text>`;
      y += 8;
      for (const m of D.models.filter((v) => v.provider === provider)) {
        y += rowH;
        const a = m.atlas.instant, b = m.atlas.reasoned;
        const color = provider === "anthropic" ? "#d97757" : "#10a37f";
        const tip = `${named(m)}: ${a === undefined ? "no instant mode" : "instant " + a.toFixed(2)}, ${b === undefined ? "no reasoning mode" : "reasoning " + b.toFixed(2)}`;
        body += `<g class="row" data-tip="${tip}"><rect x="0" y="${y - rowH / 2}" width="${W}" height="${rowH}" fill="transparent"></rect><text class="name" x="${left - 10}" y="${y + 4}" text-anchor="end">${named(m)}</text>`;
        if (a !== undefined && b !== undefined) body += `<line class="bar" x1="${x(a)}" x2="${x(b)}" y1="${y}" y2="${y}"></line>`;
        if (a !== undefined) body += `<circle cx="${x(a)}" cy="${y}" r="5.5" style="fill: light-dark(#fff, #111); stroke: var(--muted); stroke-width: 2"></circle>`;
        if (b !== undefined) body += `<circle cx="${x(b)}" cy="${y}" r="5.5" fill="${color}"></circle>`;
        body += `</g>`;
      }
    }
    const H = y + 40;
    let axis = "";
    for (const v of [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]) axis += `<line class="grid" x1="${x(v)}" x2="${x(v)}" y1="${top}" y2="${H - 26}"></line><text x="${x(v)}" y="${H - 10}" text-anchor="middle">${v.toFixed(1)}</text>`;
    $("effect").innerHTML = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Balanced accuracy of each model, instantly and with reasoning allowed">${axis}<text x="${x(0.75)}" y="12" text-anchor="middle">Balanced accuracy, 64 × 64, kelvin and megapascals</text>${body}</svg>`;
    const tipBox = $("tip");
    for (const row of $("effect").querySelectorAll(".row")) {
      row.addEventListener("pointermove", (e) => { tipBox.hidden = false; tipBox.textContent = row.dataset.tip; tipBox.style.left = `${e.clientX + 12}px`; tipBox.style.top = `${e.clientY + 12}px`; });
      row.addEventListener("pointerleave", () => { tipBox.hidden = true; });
    }
  }

  /* Every model's boiling and melting curves, one mode at a time. */
  function renderFan(condition) {
    const { tMin, tMax, logpMin, logpMax } = D.bounds;
    const [W, H, left, bottom] = [680, 560, 52, 26];
    const x = (t) => left + ((t - tMin) / (tMax - tMin)) * (W - left - 8);
    const y = (p) => 8 + (1 - (p - logpMin) / (logpMax - logpMin)) * (H - bottom - 8);
    const pts = (curve) => curve.map(([t, p]) => `${x(t)},${y(p)}`).join(" ");
    let svg = "";
    for (const [p, name] of [[0, "1 Pa"], [3, "1 kPa"], [6, "1 MPa"], [9, "1 GPa"]]) svg += `<line class="grid" x1="${left}" x2="${W - 8}" y1="${y(p)}" y2="${y(p)}"></line><text x="${left - 6}" y="${y(p) + 4}" text-anchor="end">${name}</text>`;
    for (const t of [200, 400, 600, 800]) svg += `<text x="${x(t)}" y="${H - 6}" text-anchor="middle">${t === 800 ? "800 K" : t}</text>`;
    svg += `<g id="fanLines">`;
    for (const m of D.models.filter((v) => v.lines && v.lines[condition])) {
      const color = m.provider === "anthropic" ? "#d97757" : "#10a37f";
      svg += `<g>`;
      for (const curve of Object.values(m.lines[condition])) {
        if (curve.length < 2) continue;
        svg += `<polyline class="line" stroke="${color}" points="${pts(curve)}"></polyline>`;
      }
      svg += `</g>`;
    }
    svg += `</g>`;
    for (const curve of D.curves) svg += `<polyline class="truth" points="${pts(curve)}"></polyline>`;
    $("fan").innerHTML = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Every model's boiling and melting curves">${svg}</svg>`;
  }

  function hookMap() {
    const map = $("bigMap");
    const pick = (e) => {
      const box = map.getBoundingClientRect();
      state.cell = { x: Math.min(Math.max((e.clientX - box.left) / box.width, 0), 0.9999), y: Math.min(Math.max((box.bottom - e.clientY) / box.height, 0), 0.9999) };
      readout();
    };
    map.addEventListener("pointermove", pick);
    map.addEventListener("pointerdown", pick);
    map.addEventListener("keydown", (e) => {
      const step = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, 1], ArrowDown: [0, -1] }[e.key];
      if (!step) return;
      e.preventDefault();
      const side = D.side >> current().level;
      const cell = state.cell || { x: 0.39, y: 0.57 };
      const i = Math.min(Math.max(Math.floor(cell.x * side) + step[0], 0), side - 1);
      const j = Math.min(Math.max(Math.floor(cell.y * side) + step[1], 0), side - 1);
      state.cell = { x: (i + 0.5) / side, y: (j + 0.5) / side };
      readout();
    });
  }
})();
</script>

[^models]: 14 from Anthropic and 14 from OpenAI.
