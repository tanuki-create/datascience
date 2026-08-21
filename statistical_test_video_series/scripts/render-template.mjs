function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function cueLines(term) {
  const sentences = String(term.narration)
    .replace(/\s+/g, " ")
    .split(/(?<=[。！？])/)
    .map((line) => line.trim())
    .filter(Boolean);
  const lines = sentences.length ? sentences : [term.hook, term.key_takeaway];
  const duration = Number(term.duration || 24);
  const slot = Math.max(2.2, (duration - 2) / Math.max(1, lines.length));
  return lines.map((text, index) => ({
    start: Number((1 + slot * index).toFixed(2)),
    text,
  }));
}

function plotType(term) {
  if (term.id.includes("one_sample")) return "one-sample";
  if (term.id.includes("independent")) return "two-sample";
  if (term.id.includes("paired")) return "paired";
  if (term.id.includes("mann")) return "rank";
  if (term.id.includes("ks")) return "ks";
  if (term.id.includes("anova")) return "anova";
  return "two-sample";
}

function dots(type) {
  const positions = {
    "one-sample": [
      [130, 352, "b"], [172, 336, "b"], [214, 360, "b"], [256, 326, "b"], [298, 344, "b"],
      [340, 318, "b"], [382, 352, "b"], [424, 334, "b"], [466, 358, "b"], [508, 322, "b"],
      [550, 346, "b"], [592, 330, "b"], [634, 356, "b"], [676, 338, "b"], [718, 350, "b"],
    ],
    "two-sample": [
      [120, 392, "b"], [168, 370, "b"], [216, 404, "b"], [264, 354, "b"], [312, 384, "b"], [360, 364, "b"],
      [520, 310, "m"], [568, 292, "m"], [616, 326, "m"], [664, 280, "m"], [712, 304, "m"], [760, 286, "m"],
    ],
    paired: [
      [170, 398, "b"], [250, 372, "b"], [330, 414, "b"], [410, 348, "b"], [490, 386, "b"], [570, 360, "b"],
      [170, 338, "m"], [250, 330, "m"], [330, 362, "m"], [410, 300, "m"], [490, 338, "m"], [570, 316, "m"],
    ],
    rank: [
      [100, 398, "b"], [160, 384, "m"], [220, 372, "b"], [280, 358, "m"], [340, 346, "b"], [400, 334, "m"],
      [460, 318, "m"], [520, 306, "b"], [580, 292, "m"], [640, 278, "m"], [700, 266, "b"], [760, 252, "m"],
    ],
    ks: [
      [130, 392, "b"], [190, 360, "b"], [250, 324, "b"], [310, 304, "b"], [370, 286, "b"],
      [520, 372, "m"], [580, 336, "m"], [640, 296, "m"], [700, 250, "m"], [760, 210, "m"],
    ],
    anova: [
      [120, 390, "b"], [168, 364, "b"], [216, 382, "b"], [264, 356, "b"],
      [390, 320, "a"], [438, 294, "a"], [486, 310, "a"], [534, 282, "a"],
      [660, 250, "m"], [708, 224, "m"], [756, 244, "m"], [804, 210, "m"],
    ],
  };
  return positions[type]
    .map(
      ([x, y, c], index) =>
        `<span class="dot ${c}" style="left:${x}px; top:${y}px" data-dot="${index + 1}"></span>`,
    )
    .join("");
}

function plotDecor(type) {
  if (type === "one-sample") {
    return `<div class="target-line"></div><div class="target-label">仮説の平均 μ0</div>`;
  }
  if (type === "paired") {
    return `<div class="pair-lines">${[170, 250, 330, 410, 490, 570].map((x) => `<span style="left:${x + 10}px"></span>`).join("")}</div>`;
  }
  if (type === "ks") {
    return `<div class="ecdf blue"></div><div class="ecdf magenta"></div><div class="ks-gap">最大差 D</div>`;
  }
  if (type === "anova") {
    return `<div class="group-labels"><span>群A</span><span>群B</span><span>群C</span></div>`;
  }
  if (type === "rank") {
    return `<div class="rank-axis">小さい順位 → 大きい順位</div>`;
  }
  return `<div class="mean-bars"><span></span><span></span></div>`;
}

function beatCards(term) {
  return term.visual_beats
    .slice(0, 4)
    .map(
      (beat, index) => `
        <div class="beat-card">
          <div class="beat-num">${String(index + 1).padStart(2, "0")}</div>
          <div class="beat-text">${escapeHtml(beat.text)}</div>
          <div class="beat-visual">${escapeHtml(beat.visual)}</div>
        </div>`,
    )
    .join("");
}

function assumptionChips(term) {
  return term.assumptions
    .slice(0, 4)
    .map((item) => `<span>${escapeHtml(item)}</span>`)
    .join("");
}

export function renderHtml(term) {
  const duration = Number(term.duration || 24);
  const cues = cueLines(term);
  const type = plotType(term);

  return `<!doctype html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * { box-sizing: border-box; }
      html, body {
        margin: 0;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #f8faf7;
        color: #18201a;
        font-family: sans-serif;
      }
      #root {
        position: relative;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background:
          linear-gradient(90deg, rgba(24, 32, 26, 0.045) 1px, transparent 1px),
          linear-gradient(180deg, rgba(24, 32, 26, 0.045) 1px, transparent 1px),
          #f8faf7;
        background-size: 72px 72px;
      }
      .chrome {
        position: absolute;
        inset: 0;
        padding: 72px 72px 220px;
        pointer-events: none;
      }
      .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        height: 54px;
        color: #435047;
        font-size: 24px;
        font-weight: 850;
      }
      .series-mark { display: flex; align-items: center; gap: 14px; }
      .series-dot { width: 22px; height: 22px; background: #2166ac; border: 4px solid #18201a; }
      .chapter { font-family: monospace; }
      .scene {
        position: absolute;
        inset: 152px 72px 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 30px;
      }
      .scene-title {
        color: #8a285b;
        font-size: 42px;
        font-weight: 950;
      }
      .term {
        font-size: 104px;
        line-height: 1.02;
        font-weight: 950;
        letter-spacing: 0;
      }
      .short-name {
        font-family: monospace;
        font-size: 34px;
        color: #435047;
      }
      .hook {
        max-width: 900px;
        font-size: 50px;
        line-height: 1.18;
        font-weight: 900;
      }
      .chips {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
      }
      .chip {
        border: 3px solid #18201a;
        background: #ffffff;
        padding: 12px 16px;
        font-family: monospace;
        font-size: 22px;
        font-weight: 850;
      }
      .plot-card {
        position: relative;
        height: 590px;
        border: 5px solid #18201a;
        background: #ffffff;
        box-shadow: 12px 12px 0 #c78318;
        overflow: hidden;
      }
      .axis-x, .axis-y {
        position: absolute;
        background: #18201a;
      }
      .axis-x { left: 80px; right: 70px; bottom: 112px; height: 5px; }
      .axis-y { left: 80px; top: 76px; bottom: 112px; width: 5px; }
      .dot {
        position: absolute;
        width: 30px;
        height: 30px;
        border: 4px solid #18201a;
      }
      .dot.b { background: #2166ac; }
      .dot.m { background: #b7357a; }
      .dot.a { background: #c78318; }
      .target-line {
        position: absolute;
        left: 520px;
        top: 78px;
        bottom: 112px;
        border-left: 7px dashed #b83a2d;
      }
      .target-label {
        position: absolute;
        left: 452px;
        top: 44px;
        color: #8a2b22;
        font-family: monospace;
        font-size: 24px;
        font-weight: 900;
      }
      .mean-bars span {
        position: absolute;
        bottom: 104px;
        width: 164px;
        border-top: 10px solid #168a5a;
      }
      .mean-bars span:first-child { left: 136px; }
      .mean-bars span:nth-child(2) { left: 576px; }
      .pair-lines span {
        position: absolute;
        top: 330px;
        height: 62px;
        border-left: 5px solid rgba(24, 32, 26, 0.45);
      }
      .rank-axis {
        position: absolute;
        left: 122px;
        bottom: 54px;
        font-family: monospace;
        font-size: 28px;
        color: #6b430b;
        font-weight: 900;
      }
      .ecdf {
        position: absolute;
        left: 120px;
        right: 110px;
        height: 210px;
        border-left: 8px solid currentColor;
        border-bottom: 8px solid currentColor;
        transform: skewX(-12deg);
      }
      .ecdf.blue { top: 220px; color: #2166ac; }
      .ecdf.magenta { top: 150px; color: #b7357a; }
      .ks-gap {
        position: absolute;
        right: 160px;
        top: 228px;
        padding: 10px 14px;
        background: #fff3d8;
        border: 3px solid #18201a;
        font-size: 30px;
        font-weight: 950;
      }
      .group-labels {
        position: absolute;
        left: 108px;
        right: 150px;
        bottom: 52px;
        display: flex;
        justify-content: space-between;
        font-size: 28px;
        font-weight: 950;
      }
      .hypothesis-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 20px;
      }
      .hypo-card, .formula-card, .lower-card, .takeaway {
        border: 5px solid #18201a;
        background: #ffffff;
        padding: 28px 30px;
      }
      .hypo-card {
        min-height: 150px;
        box-shadow: 10px 10px 0 #2166ac;
      }
      .label {
        font-family: monospace;
        font-size: 22px;
        color: #435047;
        font-weight: 950;
        margin-bottom: 12px;
      }
      .hypo-text {
        font-size: 38px;
        line-height: 1.22;
        font-weight: 900;
      }
      .formula-card {
        box-shadow: 10px 10px 0 #b7357a;
      }
      .formula {
        font-family: monospace;
        font-size: 34px;
        line-height: 1.25;
        font-weight: 950;
        overflow-wrap: anywhere;
      }
      .lower-card {
        box-shadow: 10px 10px 0 #168a5a;
      }
      .lower-text {
        font-size: 38px;
        line-height: 1.25;
        font-weight: 900;
      }
      .assumptions {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 18px;
      }
      .assumptions span {
        background: #eef5ff;
        border: 3px solid #18201a;
        padding: 10px 14px;
        font-size: 24px;
        font-weight: 850;
      }
      .beat-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
      }
      .beat-card {
        min-height: 226px;
        border: 4px solid #18201a;
        background: #ffffff;
        padding: 22px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }
      .beat-card:nth-child(2) { background: #f2f7ff; }
      .beat-card:nth-child(3) { background: #fff5df; }
      .beat-card:nth-child(4) { background: #f1fbf5; }
      .beat-num {
        font-family: monospace;
        font-size: 24px;
        font-weight: 950;
        color: #8a285b;
      }
      .beat-text {
        font-size: 31px;
        line-height: 1.18;
        font-weight: 950;
      }
      .beat-visual {
        color: #435047;
        font-size: 23px;
        line-height: 1.25;
        font-weight: 800;
      }
      .takeaway {
        border-left: 18px solid #168a5a;
        font-size: 46px;
        line-height: 1.18;
        font-weight: 950;
        box-shadow: 10px 10px 0 #18201a;
      }
      .caption-wrap {
        position: absolute;
        left: 76px;
        right: 76px;
        bottom: 82px;
        min-height: 132px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 24px 34px;
        background: #18201a;
        color: #ffffff;
        border: 5px solid #18201a;
      }
      .caption {
        font-size: 34px;
        line-height: 1.28;
        font-weight: 850;
        text-align: center;
      }
      .progress {
        position: absolute;
        left: 0;
        bottom: 0;
        width: 100%;
        height: 18px;
        background: #dfe7df;
      }
      .progress-fill {
        width: 100%;
        height: 100%;
        transform-origin: left center;
        transform: scaleX(0);
        background: linear-gradient(90deg, #2166ac, #b7357a, #c78318, #168a5a);
      }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="${duration}" data-width="1080" data-height="1920">
      <div class="chrome">
        <div class="topbar">
          <div class="series-mark"><span class="series-dot"></span><span>STATISTICAL TESTS</span></div>
          <div class="chapter">${escapeHtml(term.chapter)}</div>
        </div>
      </div>

      <section class="scene scene-1" data-layout-allow-overflow>
        <div class="scene-title">どの検定を選ぶ？</div>
        <h1 class="term">${escapeHtml(term.term)}</h1>
        <div class="short-name">${escapeHtml(term.short_name)}</div>
        <p class="hook">${escapeHtml(term.hook)}</p>
        <div class="chips">${term.keywords.slice(0, 5).map((keyword) => `<span class="chip">${escapeHtml(keyword)}</span>`).join("")}</div>
      </section>

      <section class="scene scene-2" data-layout-allow-overflow>
        <div class="scene-title">データの形を見る</div>
        <div class="plot-card">
          <div class="axis-x"></div><div class="axis-y"></div>
          ${plotDecor(type)}
          ${dots(type)}
        </div>
        <div class="lower-text">${escapeHtml(term.use_when)}</div>
      </section>

      <section class="scene scene-3" data-layout-allow-overflow>
        <div class="scene-title">帰無仮説と統計量</div>
        <div class="hypothesis-grid">
          <div class="hypo-card">
            <div class="label">H0</div>
            <div class="hypo-text">${escapeHtml(term.hypothesis.h0)}</div>
          </div>
          <div class="formula-card">
            <div class="label">TEST STATISTIC</div>
            <div class="formula">${escapeHtml(term.formula)}</div>
          </div>
        </div>
      </section>

      <section class="scene scene-4" data-layout-allow-overflow>
        <div class="scene-title">一個下のレイヤー</div>
        <div class="lower-card">
          <div class="lower-text">${escapeHtml(term.lower_layer)}</div>
          <div class="assumptions">${assumptionChips(term)}</div>
        </div>
      </section>

      <section class="scene scene-5" data-layout-allow-overflow>
        <div class="scene-title">画面ではこう見る</div>
        <div class="beat-grid">${beatCards(term)}</div>
      </section>

      <section class="scene scene-6" data-layout-allow-overflow>
        <div class="short-name">${escapeHtml(term.short_name)}</div>
        <div class="takeaway">${escapeHtml(term.key_takeaway)}</div>
      </section>

      <div class="caption-wrap"><div class="caption" id="caption">${escapeHtml(cues[0]?.text || term.hook)}</div></div>
      <div class="progress"><div class="progress-fill"></div></div>
    </div>

    <script>
      window.__timelines = window.__timelines || {};
      const cues = ${JSON.stringify(cues)};
      const tl = gsap.timeline({ paused: true });
      tl.set(".scene", { x: 1180, y: 0 });
      tl.set(".scene-1", { x: 0, y: 0 });
      tl.set(".dot", { xPercent: -50, yPercent: -50 });
      tl.to(".progress-fill", { scaleX: 1, duration: ${duration}, ease: "none" }, 0);

      function showScene(selector, at, hold) {
        tl.to(".scene", { x: -1180, y: 0, duration: 0.3, ease: "power2.in" }, at);
        tl.fromTo(selector, { x: 1180, y: 0 }, { x: 0, y: 0, duration: 0.45, ease: "power3.out" }, at + 0.22);
        tl.to(selector, { x: 0, y: 0, duration: hold }, at + 0.68);
      }

      tl.from(".term", { y: 60, duration: 0.55, ease: "power3.out" }, 0.1);
      tl.from(".hook", { y: 34, duration: 0.4, ease: "power3.out" }, 0.44);
      tl.from(".chip", { y: 20, duration: 0.28, stagger: 0.05, ease: "power2.out" }, 0.82);
      showScene(".scene-2", 3.3, 2.4);
      tl.from(".dot", { y: 80, scale: 0.2, duration: 0.34, stagger: 0.025, ease: "back.out(1.5)" }, 3.62);
      showScene(".scene-3", 7.0, 2.5);
      tl.from(".hypo-card, .formula-card", { y: 32, duration: 0.34, stagger: 0.08, ease: "power2.out" }, 7.28);
      showScene(".scene-4", 10.8, 2.6);
      tl.from(".assumptions span", { y: 18, duration: 0.25, stagger: 0.05, ease: "power2.out" }, 11.25);
      showScene(".scene-5", 14.8, 3.0);
      tl.from(".beat-card", { y: 34, duration: 0.32, stagger: 0.06, ease: "power2.out" }, 15.08);
      showScene(".scene-6", 19.6, ${(duration - 20.3).toFixed(2)});
      tl.from(".takeaway", { x: -42, duration: 0.42, ease: "power3.out" }, 19.9);

      for (const cue of cues) {
        tl.call(() => {
          document.getElementById("caption").textContent = cue.text;
        }, [], cue.start);
      }

      window.__timelines["main"] = tl;
    </script>
  </body>
</html>`;
}
