function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function jsString(value) {
  return JSON.stringify(String(value ?? ""));
}

function cueLines(term) {
  const sentences = String(term.narration)
    .replace(/\s+/g, " ")
    .split(/(?<=[。！？])/)
    .map((line) => line.trim())
    .filter(Boolean);

  const lines = sentences.length > 0 ? sentences : [term.hook, term.key_takeaway];
  const duration = Number(term.duration || 22);
  const slot = Math.max(2.2, (duration - 2) / Math.max(1, lines.length));

  return lines.map((text, index) => ({
    start: Number((1 + slot * index).toFixed(2)),
    end: Number(Math.min(duration - 0.6, 1 + slot * (index + 1)).toFixed(2)),
    text,
  }));
}

function layerRows(term) {
  const layers = [
    "ユーザー / 攻撃者",
    "ブラウザ",
    "HTTP",
    "Cookie / Header / URL / Origin",
    "アプリケーションコード",
    "DB / ファイル / 外部API / クラウド",
  ];
  const lower = String(term.lower_layer).toLowerCase();
  return layers
    .map((layer) => {
      const hit =
        lower.includes(layer.toLowerCase()) ||
        layer
          .split(/\s*\/\s*/)
          .some((part) => part && lower.includes(part.toLowerCase()));
      return `<div class="layer-row${hit ? " active" : ""}"><span>${escapeHtml(layer)}</span></div>`;
    })
    .join("");
}

function beatCards(term) {
  const beats = term.visual_beats.slice(0, 4);
  return beats
    .map(
      (beat, index) => `
        <div class="beat-card beat-${index + 1}">
          <div class="beat-num">${String(index + 1).padStart(2, "0")}</div>
          <div class="beat-text">${escapeHtml(beat.text)}</div>
          <div class="beat-visual">${escapeHtml(beat.visual)}</div>
        </div>`,
    )
    .join("");
}

export function renderHtml(term) {
  const duration = Number(term.duration || 22);
  const cues = cueLines(term);
  const keywords = term.keywords.slice(0, 5);

  return `<!doctype html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {
        box-sizing: border-box;
      }
      html,
      body {
        margin: 0;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #f7f9f6;
        color: #17211a;
        font-family: sans-serif;
      }
      #root {
        position: relative;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background:
          linear-gradient(90deg, rgba(23, 33, 26, 0.045) 1px, transparent 1px),
          linear-gradient(180deg, rgba(23, 33, 26, 0.045) 1px, transparent 1px),
          #f7f9f6;
        background-size: 72px 72px;
      }
      .chrome {
        position: absolute;
        inset: 0;
        padding: 78px 76px 220px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        pointer-events: none;
      }
      .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 54px;
        font-size: 24px;
        letter-spacing: 0;
        color: #414a42;
      }
      .series-mark {
        display: flex;
        align-items: center;
        gap: 14px;
        font-weight: 800;
      }
      .series-dot {
        width: 22px;
        height: 22px;
        background: #e6462e;
        border: 4px solid #17211a;
      }
      .chapter {
        font-family: monospace;
        font-size: 22px;
      }
      .scene {
        position: absolute;
        inset: 156px 72px 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 34px;
      }
      .scene-title {
        font-size: 44px;
        font-weight: 900;
        color: #a92f20;
      }
      .term {
        font-size: 142px;
        line-height: 0.9;
        font-weight: 950;
        letter-spacing: 0;
      }
      .hook {
        font-size: 52px;
        line-height: 1.23;
        font-weight: 850;
        max-width: 900px;
      }
      .chips {
        display: flex;
        flex-wrap: wrap;
        gap: 14px;
      }
      .chip {
        border: 3px solid #17211a;
        background: #ffffff;
        padding: 12px 18px;
        font-family: monospace;
        font-size: 22px;
        font-weight: 800;
      }
      .definition-box {
        border: 5px solid #17211a;
        background: #ffffff;
        padding: 34px;
        display: flex;
        flex-direction: column;
        gap: 20px;
        box-shadow: 12px 12px 0 #f2b84b;
      }
      .label {
        font-family: monospace;
        font-size: 22px;
        font-weight: 900;
        color: #414a42;
        text-transform: uppercase;
      }
      .definition-main {
        font-size: 46px;
        line-height: 1.22;
        font-weight: 900;
      }
      .definition-sub {
        font-size: 34px;
        line-height: 1.35;
        color: #273128;
        font-weight: 750;
      }
      .layer-stack {
        display: flex;
        flex-direction: column;
        gap: 14px;
      }
      .layer-row {
        height: 96px;
        border: 4px solid #17211a;
        background: #ffffff;
        display: flex;
        align-items: center;
        padding: 0 30px;
        font-size: 31px;
        font-weight: 850;
      }
      .layer-row.active {
        background: #0b6f78;
        color: #ffffff;
        box-shadow: 10px 10px 0 #17211a;
        transform: translateX(18px);
      }
      .lower-note {
        font-size: 42px;
        line-height: 1.24;
        font-weight: 900;
      }
      .beat-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 22px;
      }
      .beat-card {
        min-height: 240px;
        border: 4px solid #17211a;
        background: #ffffff;
        padding: 24px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }
      .beat-card:nth-child(2) {
        background: #effbf8;
      }
      .beat-card:nth-child(3) {
        background: #fff7df;
      }
      .beat-card:nth-child(4) {
        background: #fff0ec;
      }
      .beat-num {
        font-family: monospace;
        font-size: 24px;
        font-weight: 900;
        color: #a92f20;
      }
      .beat-text {
        font-size: 31px;
        line-height: 1.2;
        font-weight: 900;
      }
      .beat-visual {
        font-size: 23px;
        line-height: 1.25;
        color: #414a42;
        font-weight: 750;
      }
      .takeaway {
        border-left: 18px solid #1e9f70;
        background: #ffffff;
        padding: 30px 34px;
        font-size: 45px;
        line-height: 1.18;
        font-weight: 950;
        box-shadow: 10px 10px 0 #17211a;
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
        background: #17211a;
        color: #ffffff;
        border: 5px solid #17211a;
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
        height: 18px;
        width: 100%;
        background: #dfe7df;
      }
      .progress-fill {
        height: 100%;
        width: 100%;
        transform-origin: left center;
        transform: scaleX(0);
        background: linear-gradient(90deg, #e6462e, #f2b84b, #1e9f70, #0b6f78);
      }
      .diagram-line {
        height: 6px;
        background: #17211a;
        width: 100%;
      }
      .term-mini {
        font-family: monospace;
        font-size: 28px;
        color: #414a42;
      }
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="${duration}"
      data-width="1080"
      data-height="1920"
    >
      <div class="chrome">
        <div class="topbar">
          <div class="series-mark"><span class="series-dot"></span><span>WEB SECURITY TERMS</span></div>
          <div class="chapter">${escapeHtml(term.chapter)}</div>
        </div>
      </div>

      <section class="scene scene-1" data-layout-allow-overflow>
        <div class="scene-title">まず、出どころを見る</div>
        <h1 class="term">${escapeHtml(term.term)}</h1>
        <p class="hook">${escapeHtml(term.hook)}</p>
        <div class="chips">
          ${keywords.map((keyword) => `<span class="chip">${escapeHtml(keyword)}</span>`).join("")}
        </div>
      </section>

      <section class="scene scene-2" data-layout-allow-overflow>
        <div class="definition-box">
          <div class="label">ABBREVIATION / NAME</div>
          <div class="definition-main">${escapeHtml(term.expanded || term.term)}</div>
          <div class="diagram-line"></div>
          <div class="label">WORD ORIGIN</div>
          <div class="definition-sub">${escapeHtml(term.origin)}</div>
        </div>
      </section>

      <section class="scene scene-3" data-layout-allow-overflow>
        <div class="scene-title">一個下のレイヤー</div>
        <div class="layer-stack">${layerRows(term)}</div>
        <div class="lower-note">${escapeHtml(term.lower_layer)}</div>
      </section>

      <section class="scene scene-4" data-layout-allow-overflow>
        <div class="scene-title">画面ではこう見せる</div>
        <div class="beat-grid">${beatCards(term)}</div>
      </section>

      <section class="scene scene-5" data-layout-allow-overflow>
        <div class="term-mini">${escapeHtml(term.term)}</div>
        <div class="takeaway">${escapeHtml(term.key_takeaway)}</div>
      </section>

      <div class="caption-wrap">
        <div class="caption" id="caption">${escapeHtml(cues[0]?.text || term.hook)}</div>
      </div>
      <div class="progress"><div class="progress-fill"></div></div>
    </div>

    <script>
      window.__timelines = window.__timelines || {};
      const cues = ${JSON.stringify(cues)};
      const tl = gsap.timeline({ paused: true });
      tl.set(".scene", { x: 1180, y: 0 });
      tl.set(".scene-1", { x: 0, y: 0 });
      tl.to(".progress-fill", { scaleX: 1, duration: ${duration}, ease: "none" }, 0);

      function showScene(selector, at, hold) {
        tl.to(".scene", { x: -1180, y: 0, duration: 0.32, ease: "power2.in" }, at);
        tl.fromTo(selector, { x: 1180, y: 0 }, { x: 0, y: 0, duration: 0.46, ease: "power3.out" }, at + 0.25);
        tl.to(selector, { x: 0, y: 0, duration: hold }, at + 0.72);
      }

      tl.from(".term", { y: 70, duration: 0.55, ease: "power3.out" }, 0.1);
      tl.from(".hook", { y: 42, duration: 0.45, ease: "power3.out" }, 0.45);
      tl.from(".chip", { y: 22, duration: 0.3, stagger: 0.06, ease: "power2.out" }, 0.82);
      showScene(".scene-2", 3.4, 2.6);
      tl.from(".definition-box", { scale: 0.96, duration: 0.38, ease: "power2.out" }, 3.65);
      showScene(".scene-3", 7.3, 3.1);
      tl.from(".layer-row", { x: -36, duration: 0.28, stagger: 0.06, ease: "power2.out" }, 7.6);
      showScene(".scene-4", 12.0, 3.6);
      tl.from(".beat-card", { y: 36, duration: 0.34, stagger: 0.08, ease: "power2.out" }, 12.28);
      showScene(".scene-5", 17.2, ${Math.max(2.2, duration - 18.2).toFixed(2)});
      tl.from(".takeaway", { x: -42, duration: 0.44, ease: "power3.out" }, 17.48);

      for (const cue of cues) {
        tl.call(() => {
          document.getElementById("caption").textContent = ${jsString("")} + cue.text;
        }, [], cue.start);
      }

      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
`;
}
