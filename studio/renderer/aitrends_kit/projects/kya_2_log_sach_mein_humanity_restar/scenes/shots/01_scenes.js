// scenes/shots/01_scenes.js — Universal High-Retention Shots for aiTrends Studio
import { E, V, registerShot, mood, layer, blurLayer, veil, ease, prog, clamp, lerp, shake, seg, circle, ring, rr, poly, glow, alpha, shade, linGrad, radGrad, FONTS, text, measure } from '/engine/core.js';
import { drawFigure, POSES, posesAt, breathe, bigFace, headPos } from '/engine/rig2d.js';
import * as FX from '/engine/fx2d.js';
import * as UI from '/engine/ui2d.js';
import { bedroom, classroom, cityStreet, ruinsWasteland, spaceVoid, natureForest, highTechServer, cafe, lab } from '../sets/universal_sets.js';
import { HERO, SECONDARY, FRIEND, DOC, CAST } from '../cast.js';

const SETS = { bedroom, classroom, cityStreet, ruinsWasteland, spaceVoid, natureForest, highTechServer, cafe, lab };
function getSet(name) { return SETS[name] || SETS.bedroom; }

// Universal procedural prop generator for any topic
function drawTopicProp(g, type, x, y, scale = 1, t = 0, opts = {}) {
  g.save();
  g.translate(x, y);
  g.scale(scale, scale);
  const p = (type || '').toLowerCase();
  if (p.includes('dna') || p.includes('genetic') || p.includes('strand')) {
    const steps = 9, h = 90;
    glow(g, 0, 0, 75, '#38bdf8', 0.45);
    for (let i = 0; i < steps; i++) {
      const u = (i / (steps - 1)) * 2 - 1;
      const py = u * (h / 2);
      const phase = t * 3.2 + i * 0.7;
      const x1 = Math.sin(phase) * 32, x2 = -x1;
      const rungColor = i % 2 === 0 ? '#38bdf8' : '#ec4899';
      seg(g, [[x1, py], [x2, py]], 3.5, alpha(rungColor, 0.75));
      circle(g, x1, py, 5, '#38bdf8');
      circle(g, x2, py, 5, '#ec4899');
    }
  } else if (p.includes('earth') || p.includes('planet') || p.includes('globe') || p.includes('world')) {
    glow(g, 0, 0, 85, '#38bdf8', 0.55);
    circle(g, 0, 0, 38, '#1e3a8a');
    ring(g, 0, 0, 39, 4, 'rgba(125,211,252,0.85)');
    poly(g, [[-20, -18], [-6, -26], [8, -16], [2, -2], [-14, -4]], '#10b981');
    poly(g, [[-12, 6], [16, 2], [22, 22], [4, 26], [-6, 16]], '#10b981');
    poly(g, [[-26, 4], [-18, 18], [-28, 22]], '#059669');
    g.strokeStyle = 'rgba(255,255,255,0.45)'; g.lineWidth = 3;
    g.beginPath(); g.arc(0, 0, 26, 0.8 + t * 0.2, 2.2 + t * 0.2); g.stroke();
  } else if (p.includes('phone') || p.includes('mobile') || p.includes('screen')) {
    const pw = 48, ph = 96;
    rr(g, -pw/2 - 2, -ph/2 - 2, pw + 4, ph + 4, 10); g.fillStyle = '#1c1b22'; g.fill();
    rr(g, -pw/2, -ph/2, pw, ph, 8); g.fillStyle = '#0a0f1d'; g.fill();
    glow(g, 0, 0, 80, '#38bdf8', 0.6);
    for (let r = 0; r < 3; r++) {
      for (let c = 0; c < 2; c++) {
        rr(g, -16 + c * 20, -34 + r * 20, 13, 13, 3);
        g.fillStyle = c === 0 ? '#38bdf8' : '#fbbf24'; g.fill();
      }
    }
    circle(g, pw/2 - 7, -ph/2 + 7, 4.5, '#ef4444');
    if (opts.cone) FX.lightCone(g, 0, 0, { angle: -Math.PI / 2, spread: 0.9, len: 220, color: '#38bdf8', a: 0.35 });
  } else if (p.includes('laptop') || p.includes('computer')) {
    rr(g, -45, -48, 90, 54, 5); g.fillStyle = '#1e293b'; g.fill();
    glow(g, 0, -20, 65, '#38bdf8', 0.55);
    for (let i = 0; i < 4; i++) { g.fillStyle = i % 2 === 0 ? '#38bdf8' : '#34d399'; g.fillRect(-34, -40 + i * 10, 40 + (i * 7) % 25, 3.5); }
    poly(g, [[-54, 8], [54, 8], [45, 20], [-45, 20]], '#334155');
  } else if (p.includes('dumbbell') || p.includes('weight') || p.includes('gym')) {
    g.fillStyle = '#94a3b8'; g.fillRect(-36, -5, 72, 10);
    rr(g, -48, -26, 14, 52, 5); g.fillStyle = '#334155'; g.fill();
    rr(g, 34, -26, 14, 52, 5); g.fillStyle = '#334155'; g.fill();
    glow(g, 0, 0, 40, '#f59e0b', 0.45);
  } else if (p.includes('coffee') || p.includes('cup') || p.includes('mug')) {
    poly(g, [[-18, -20], [18, -20], [13, 20], [-13, 20]], '#e2e8f0');
    g.strokeStyle = '#e2e8f0'; g.lineWidth = 4.5; g.beginPath(); g.arc(16, 0, 11, -Math.PI/2, Math.PI/2); g.stroke();
    glow(g, 0, 0, 35, '#ffcf80', 0.35);
  } else if (p.includes('brain')) {
    circle(g, -12, -7, 18, '#ec4899'); circle(g, 12, -7, 18, '#ec4899'); circle(g, 0, 7, 16, '#db2777');
    glow(g, 0, 0, 50, '#f472b6', 0.7);
    for (let i = 0; i < 5; i++) {
      if (Math.sin(t * 8 + i * 2) > 0.3) circle(g, -15 + i * 8, -10 + (i % 3) * 10, 2.5, '#ffffff');
    }
  } else if (p.includes('heart')) {
    poly(g, [[0, 18], [-22, -4], [-13, -22], [0, -11], [13, -22], [22, -4]], '#ef4444');
    glow(g, 0, 0, 45, '#f87171', 0.65);
    seg(g, [[-18, 0], [-8, 0], [-3, -12], [3, 14], [8, -4], [18, 0]], 3, '#fef08a');
  } else if (p.includes('clock') || p.includes('stopwatch') || p.includes('time')) {
    circle(g, 0, 0, 28, '#1e293b'); ring(g, 0, 0, 30, 4, '#f59e0b');
    const ang = t * 7; seg(g, [[0, 0], [Math.sin(ang) * 20, -Math.cos(ang) * 20]], 3.5, '#f59e0b');
    glow(g, 0, 0, 42, '#fbbf24', 0.55);
  } else if (p.includes('money') || p.includes('gold') || p.includes('coin')) {
    circle(g, 0, 0, 26, '#f59e0b'); ring(g, 0, 0, 26, 3.5, '#fbbf24');
    text(g, '$', 0, 9, { size: 28, color: '#78350f', font: FONTS.ui, weight: 900 });
    glow(g, 0, 0, 45, '#fbbf24', 0.65);
  } else if (p.includes('danger') || p.includes('skull') || p.includes('toxic')) {
    poly(g, [[0, -32], [32, 22], [-32, 22]], '#f59e0b');
    poly(g, [[0, -22], [22, 16], [-22, 16]], '#18181b');
    glow(g, 0, 0, 50, '#ef4444', 0.6);
    text(g, '!', 0, 12, { size: 26, color: '#f59e0b', font: FONTS.ui, weight: 900 });
  } else if (p.includes('fire') || p.includes('flame') || p.includes('sun')) {
    poly(g, [[0, -36], [22, 8], [14, 30], [-14, 30], [-22, 8]], '#ef4444');
    poly(g, [[0, -20], [12, 10], [6, 26], [-6, 26], [-12, 10]], '#f59e0b');
    circle(g, 0, 16, 8, '#fef08a');
    glow(g, 0, 0, 60, '#f97316', 0.8);
  } else if (p.includes('atom') || p.includes('science')) {
    circle(g, 0, 0, 10, '#38bdf8'); glow(g, 0, 0, 40, '#38bdf8', 0.7);
    g.strokeStyle = '#a855f7'; g.lineWidth = 2.5;
    for (let a = 0; a < 3; a++) {
      g.save(); g.rotate(a * Math.PI / 3 + t * 0.8);
      g.beginPath(); g.ellipse(0, 0, 32, 12, 0, 0, Math.PI * 2); g.stroke();
      circle(g, Math.cos(t * 4 + a) * 32, Math.sin(t * 4 + a) * 12, 3.5, '#ffffff');
      g.restore();
    }
  } else {
    circle(g, 0, 0, 26, '#6366f1'); ring(g, 0, 0, 30, 3.5, '#a5b4fc');
    glow(g, 0, 0, 55, '#818cf8', 0.75);
    text(g, '★', 0, 9, { size: 26, color: '#ffffff', font: FONTS.ui, weight: 900 });
  }
  g.restore();
}

// s001 — Cold Hook Opening Shot (Solo Hero)
registerShot('s001', {
  draw(g, t, info) {
    const cam = { z: 1 + 0.12 * ease.inOut(t / info.dur), x: -30 * ease.inOut(t / info.dur) };
    const { GY, CX, M } = getSet('ruinsWasteland')(g, t, cam, { mood: 'dusk' });
    const rim = { color: M.rim, dir: [0, -1], w: 4.5 };
    layer(g, cam, 1, (g) => {
      drawFigure(g, {
        x: CX - V(40, 20),
        y: GY,
        s: V(1.4, 1.55),
        facing: 1,
        outfit: HERO,
        pose: breathe(POSES.handsOnHead || POSES.stand, t),
        expr: 'shocked',
        rim: rim
      });
      drawTopicProp(g, 'skull_danger', CX - V(40, 20) + V(25, 22), GY - V(140, 150), 1.3, t, { cone: true });
    });
    UI.titleCard(g, t, {
      lines: ['KYA 2 LOG', 'SACH MEIN HUMANITY RESTART KAR SAKTE HAIN?'],
      dur: Math.min(3.4, info.dur * 0.75),
      y: E.H * V(0.36, 0.30)
    });
    UI.badge(g, { str: 'POPULATION: 2', color: '#ffd54f', x: E.W - V(90, 70), y: V(120, 160) });
    FX.dust(g, t, { count: 40, color: '#ffe4c4', a: 0.35 });
  }
});

// s002 — Macro Insert of Core Subject
registerShot('s002', {
  draw(g, t, info) {
    g.fillStyle = linGrad(g, 0, 0, 0, E.H, ['#0d0a14', '#171122']);
    g.fillRect(-E.W, -E.H, E.W * 3, E.H * 3);
    const CX = E.W / 2, CY = E.H * V(0.48, 0.44);
    glow(g, CX, CY, V(340, 300), '#38bdf8', 0.45);
    FX.dust(g, t, { count: 25, color: '#ffdfb8', a: 0.3 });
    // Giant Macro Prop
    drawTopicProp(g, 'question_mark', CX, CY, V(4.2, 3.8), t, { cone: true });
    // Focus marquee box
    const mw = V(360, 300), mh = V(480, 420);
    g.strokeStyle = '#7fd4ff'; g.lineWidth = 4; g.setLineDash([16, 12]);
    g.strokeRect(CX - mw/2, CY - mh/2, mw, mh);
    g.setLineDash([]);
    UI.badge(g, { str: 'THE RULES', x: E.W - V(90, 70), y: V(120, 160) });
    // Pip's arm entering with rim light
    drawFigure(g, {
      x: CX + V(300, 220),
      y: E.H * 1.18,
      s: V(2.4, 2.6),
      facing: -1,
      outfit: HERO,
      pose: POSES.phone,
      expr: 'neutral',
      rim: { color: '#ffb070', dir: [0, -1], w: 6 }
    });
  }
});

// s003 — Narrative Escalation Beat (Dual Characters)
registerShot('s003', {
  draw(g, t, info) {
    const cam = { z: 1.08 + 0.04 * ease.inOut(t / info.dur), x: 20 * Math.sin(t * 1.2) };
    const { GY, CX, M } = getSet('cityStreet')(g, t, cam, { mood: 'dusk' });
    const rim = { color: M.rim, dir: [0, -1], w: 4.5 };
    layer(g, cam, 1, (g) => {
      drawFigure(g, {
        x: CX - V(130, 95),
        y: GY,
        s: V(1.35, 1.48),
        facing: 1,
        outfit: HERO,
        pose: breathe(POSES.cheer || POSES.explain, t),
        expr: 'happy',
        rim: rim
      });
      drawFigure(g, {
        x: CX + V(130, 95),
        y: GY,
        s: V(1.35, 1.48),
        facing: -1,
        outfit: SECONDARY,
        pose: breathe(POSES.point || POSES.think, t + 0.5),
        expr: 'thinking',
        rim: { color: M.key, dir: [0, -1], w: 4 }
      });
      drawTopicProp(g, 'campfire', CX, GY - V(150, 170), 1.2, t);
    });
    UI.badge(g, { str: 'SURVIVAL MODE', color: '#7ee787', x: E.W - V(90, 70), y: V(120, 160) });
    FX.dust(g, t, { count: 35, color: '#ffdfb8', a: 0.35 });
  }
});

// s004 — The Science Turn (Technical Blueprint & Data Card)
registerShot('s004', {
  draw(g, t, info) {
    // 1. Deep Technical Blueprint Grid
    UI.blueprint(g, { grid: 48, a: 0.16 });
    // 2. Animated Data Card with metric progression
    UI.dataCard(g, t, {
      title: 'GENETIC BOTTLENECK RISK',
      subtitle: 'REPRODUCTIVE VIABILITY RATE',
      from: 1.0,
      to: 98.5,
      decimals: 1,
      unit: ' %',
      dur: 2.2,
      labels: [
        [0, 'Gen 1 (1%)'],
        [0.5, 'Gen 3 (50%)'],
        [1.0, 'Gen 5 (98.5%)']
      ]
    });
    // 3. Dynamic Comparison Bars
    UI.compareBars(g, t, {
      rows: [{"label": "SAFE POPULATION", "v": 0.95, "color": "#7ee787"}, {"label": "JUST 2 HUMANS", "v": 0.05, "color": "#ff5555"}],
      x: V(220, 120),
      y: E.H - V(180, 480),
      w: V(700, 840)
    });
    // 4. Technical Line-Art Stick Figure showing physiological/system strain
    UI.lineFigure(g, {
      x: E.W * 0.82,
      y: E.H * V(0.68, 0.74),
      s: V(1.2, 1.3),
      pose: POSES.facepalm,
      color: '#ffb070'
    });
  }
});

// s005 — Emergency Alert & Friction Wall (Dual Characters)
registerShot('s005', {
  draw(g, t, info) {
    const cam = { z: 1.12 + 0.05 * Math.sin(t * 4), x: shake(t, 18), y: shake(t, 10) };
    const { GY, CX, M } = getSet('lab')(g, t, cam, { mood: 'interiorWarm' });
    // Emergency Red Strobe Warning
    const redPulse = (Math.sin(t * 12) > 0 ? 0.35 : 0.10);
    veil(g, '#ff1a1a', redPulse);
    UI.readout(g, {
      label: 'GENETIC FAILURE',
      value: 'CRITICAL INBREEDING DEPRESSION',
      color: '#ff4444',
      x: V(140, 90),
      y: V(160, 220)
    });
    layer(g, cam, 1, (g) => {
      drawFigure(g, {
        x: CX - V(120, 80),
        y: GY,
        s: V(1.35, 1.48),
        facing: 1,
        outfit: HERO,
        pose: breathe(POSES.handsOnHead, t),
        expr: 'shocked',
        rim: { color: '#ff4444', dir: [0, -1], w: 6 }
      });
      drawFigure(g, {
        x: CX + V(120, 80),
        y: GY,
        s: V(1.35, 1.48),
        facing: -1,
        outfit: SECONDARY,
        pose: breathe(POSES.panicking || POSES.facepalm, t + 0.3),
        expr: 'screaming',
        rim: { color: '#ff4444', dir: [0, -1], w: 6 }
      });
    });
    FX.dust(g, t, { count: 40, color: '#ff7777', a: 0.4 });
  }
});

// s006 — Climax & CTA End Screen
registerShot('s006', {
  draw(g, t, info) {
    UI.endScreen(g, t, {
      question: 'Kya aapko lagta hai ki 2 log survive kar p?',
      cast: CAST,
      rim: '#ffb070'
    });
  }
});
