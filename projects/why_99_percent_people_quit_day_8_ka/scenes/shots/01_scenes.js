// scenes/shots/01_scenes.js — Universal Dynamic Story Engine for aiTrends Studio
import { E, V, registerShot, mood, layer, blurLayer, veil, ease, prog, clamp, lerp, shake, seg, circle, ring, rr, poly, glow, alpha, shade, linGrad, radGrad, FONTS, text, measure } from '/engine/core.js';
import { drawFigure, POSES, posesAt, breathe, bigFace, headPos } from '/engine/rig2d.js';
import { drawBeanCharacter, drawShadowDemon, drawFatigueFigure, drawMotivationMeter, drawDayBanner, drawDisciplineGraph, drawInSceneText } from '/engine/dayone_rig.js';
import * as FX from '/engine/fx2d.js';
import * as UI from '/engine/ui2d.js';
import { bedroom, classroom, cityStreet, ruinsWasteland, spaceVoid, natureForest, highTechServer, cafe, lab, dayoneBedroom, dayoneRunningStreet, dayoneGym, dayoneStudyDesk, dayoneSunrise, studioTech, holoGlassCard, holoBarChart, holoCircularGauge, holoComparisonSplit, holoStageBadge } from '../sets/universal_sets.js';
import { HERO, SECONDARY, FRIEND, DOC, CAST } from '../cast.js';

const SETS = { bedroom, classroom, cityStreet, ruinsWasteland, spaceVoid, natureForest, highTechServer, cafe, lab, dayoneBedroom, dayoneRunningStreet, dayoneGym, dayoneStudyDesk, dayoneSunrise, studioTech };
function getSet(name) { return SETS[name] || SETS.bedroom; }

// Universal Image Preloader
const SCENE_IMAGES = {};
async function preloadImg(id, url) {
  return new Promise((resolve) => {
    const img = new Image();
    const timer = setTimeout(() => {
      console.warn('Image timeout for ' + id + ': ' + url);
      resolve(null);
    }, 8000);
    img.crossOrigin = 'anonymous';
    img.onload = () => { clearTimeout(timer); SCENE_IMAGES[id] = img; resolve(img); };
    img.onerror = () => { clearTimeout(timer); console.warn('Image load error for ' + id + ': ' + url); resolve(null); };
    img.src = url;
  });
}

// Top-level await preloads all scene illustrations before Playwright captures frames
await Promise.all([
  preloadImg('s001', '/project/images/scene_001.png'),
  preloadImg('s002', '/project/images/scene_002.png'),
  preloadImg('s003', '/project/images/scene_003.png'),
  preloadImg('s004', '/project/images/scene_004.png'),
  preloadImg('s005', '/project/images/scene_005.png'),
  preloadImg('s006', '/project/images/scene_006.png'),
  preloadImg('s007', '/project/images/scene_007.png'),
  preloadImg('s008', '/project/images/scene_008.png'),
  preloadImg('s009', '/project/images/scene_009.png'),
  preloadImg('s010', '/project/images/scene_010.png'),
  preloadImg('s011', '/project/images/scene_011.png'),
  preloadImg('s012', '/project/images/scene_012.png'),
  preloadImg('s013', '/project/images/scene_013.png'),
  preloadImg('s014', '/project/images/scene_014.png'),
  preloadImg('s015', '/project/images/scene_015.png'),
  preloadImg('s016', '/project/images/scene_016.png')
]);

// Universal Ken Burns Canvas Drawing Function
function drawSceneBackground(g, img, t, dur, cameraMode = 'zoom_in') {
  if (!img || !img.complete || img.naturalWidth === 0) return false;
  g.save();
  const p = clamp(t / Math.max(0.1, dur));
  let scale = 1.0;
  let tx = 0, ty = 0;
  if (cameraMode === 'zoom_in') {
    scale = 1.0 + 0.12 * ease.inOut(p);
  } else if (cameraMode === 'zoom_out') {
    scale = 1.12 - 0.12 * ease.inOut(p);
  } else if (cameraMode === 'pan_right') {
    scale = 1.08;
    tx = -35 * ease.inOut(p);
  } else if (cameraMode === 'pan_left') {
    scale = 1.08;
    tx = 35 * ease.inOut(p);
  } else {
    scale = 1.05 + 0.05 * Math.sin(p * Math.PI);
  }
  const cx = E.W / 2;
  const cy = E.H / 2;
  g.translate(cx, cy);
  g.scale(scale, scale);
  g.translate(-cx + tx, -cy + ty);
  g.drawImage(img, 0, 0, E.W, E.H);
  // Cinematic dusk atmosphere vignette
  const vig = g.createRadialGradient(cx, cy, E.W * 0.35, cx, cy, E.W * 0.85);
  vig.addColorStop(0, 'rgba(0, 0, 0, 0)');
  vig.addColorStop(1, 'rgba(10, 8, 20, 0.40)');
  g.fillStyle = vig; g.fillRect(0, 0, E.W, E.H);
  g.restore();
  return true;
}

// Universal procedural prop generator
function drawTopicProp(g, type, x, y, scale = 1, t = 0, opts = {}) {
  g.save();
  g.translate(x, y);
  g.scale(scale, scale);
  const p = (type || '').toLowerCase();
  if (p.includes('dna') || p.includes('genetic') || p.includes('strand')) {
    const steps = 9, h = 90; glow(g, 0, 0, 75, '#38bdf8', 0.45);
    for (let i = 0; i < steps; i++) {
      const u = (i / (steps - 1)) * 2 - 1, py = u * (h / 2), phase = t * 3.2 + i * 0.7;
      const x1 = Math.sin(phase) * 32, x2 = -x1, rungColor = i % 2 === 0 ? '#38bdf8' : '#ec4899';
      seg(g, [[x1, py], [x2, py]], 3.5, alpha(rungColor, 0.75));
      circle(g, x1, py, 5, '#38bdf8'); circle(g, x2, py, 5, '#ec4899');
    }
  } else if (p.includes('earth') || p.includes('planet') || p.includes('globe') || p.includes('world')) {
    glow(g, 0, 0, 85, '#38bdf8', 0.55); circle(g, 0, 0, 38, '#1e3a8a'); ring(g, 0, 0, 39, 4, 'rgba(125,211,252,0.85)');
    poly(g, [[-20, -18], [-6, -26], [8, -16], [2, -2], [-14, -4]], '#10b981');
    poly(g, [[-12, 6], [16, 2], [22, 22], [4, 26], [-6, 16]], '#10b981');
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
  } else if (p.includes('clock') || p.includes('alarm') || p.includes('time')) {
    circle(g, 0, 0, 28, '#1e293b'); ring(g, 0, 0, 30, 4, '#f59e0b');
    const ang = t * 7; seg(g, [[0, 0], [Math.sin(ang) * 20, -Math.cos(ang) * 20]], 3.5, '#f59e0b');
    glow(g, 0, 0, 42, '#fbbf24', 0.55);
  } else if (p.includes('money') || p.includes('gold') || p.includes('cash')) {
    circle(g, 0, 0, 26, '#f59e0b'); ring(g, 0, 0, 26, 3.5, '#fbbf24');
    text(g, '$', 0, 9, { size: 28, color: '#78350f', font: FONTS.ui, weight: 900 });
    glow(g, 0, 0, 45, '#fbbf24', 0.65);
  } else if (p.includes('dumbbell') || p.includes('gym')) {
    g.fillStyle = '#94a3b8'; g.fillRect(-36, -5, 72, 10);
    rr(g, -48, -26, 14, 52, 5); g.fillStyle = '#334155'; g.fill();
    rr(g, 34, -26, 14, 52, 5); g.fillStyle = '#334155'; g.fill();
  } else {
    circle(g, 0, 0, 24, '#6366f1'); ring(g, 0, 0, 27, 3, '#a5b4fc');
    glow(g, 0, 0, 45, '#818cf8', 0.65); text(g, '★', 0, 8, { size: 22, color: '#ffffff', font: FONTS.ui, weight: 900 });
  }
  g.restore();
}

// s001 — Cold Hook Opening Shot
registerShot('s001', {
  draw(g, t, info) {
    const cam = { z: 1.05 + 0.05 * ease.inOut(t / info.dur), x: -15 * ease.inOut(t / info.dur) };
    const hasBg = drawSceneBackground(g, SCENE_IMAGES['s001'], t, info.dur, 'zoom_in');
    if (!hasBg) {
      getSet('classroom')(g, t, cam, { mood: 'coolDay' });
    }
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    const rim = { color: '#ffb070', dir: [0, -1], w: 4.5 };
    layer(g, cam, 1, (g) => {
      drawFigure(g, {
        x: CX,
        y: GY,
        s: V(1.35, 1.48),
        facing: 1,
        outfit: HERO,
        pose: breathe(POSES.point || POSES.stand, t),
        expr: 'shocked',
        rim: rim
      });
      drawTopicProp(g, 'target_bullseye', CX + V(30, 22), GY - V(140, 150), 1.2, t);
    });
    UI.titleCard(g, t, {
      lines: ['WHY 99 PERCENT', 'PEOPLE QUIT DAY 8 KA SHOCKING SACH!'],
      dur: Math.min(3.4, info.dur * 0.75),
      y: E.H * V(0.36, 0.30)
    });
    UI.badge(g, { str: 'FOCUS', color: '#ffd54f', x: E.W - V(90, 70), y: V(120, 160) });
    FX.dust(g, t, { count: 35, color: '#ffe4c4', a: 0.3 });
  }
});

// s002 — Narrative Scene 2 (Solo Hero)
registerShot('s002', {
  draw(g, t, info) {
    const cam = { z: 1.0, x: 0 };
    const hasBg = drawSceneBackground(g, SCENE_IMAGES['s002'], t, info.dur, 'pan_right');
    if (!hasBg) {
      getSet('cityStreet')(g, t, cam, { mood: 'dusk' });
    }
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    const rim = { color: '#ffb070', dir: [0, -1], w: 4.5 };
    layer(g, cam, 1, (g) => {
      drawFigure(g, {
        x: CX,
        y: GY,
        s: V(1.4, 1.55),
        facing: 1,
        outfit: HERO,
        pose: breathe(POSES.think || POSES.stand, t),
        expr: 'thinking',
        rim: rim
      });
      drawTopicProp(g, 'dna_strand', CX + V(30, 22), GY - V(140, 150), 1.2, t);
    });
    UI.badge(g, { str: 'BEAT 02', color: '#7ee787', x: E.W - V(90, 70), y: V(120, 160) });
    FX.dust(g, t, { count: 30, color: '#ffdfb8', a: 0.3 });
  }
});

// s003 — Style 2A Modern Studio Tech Shot (studio_analytics)
registerShot('s003', {
  draw(g, t, info) {
    const cam = { z: 1.0, x: 0 };
    studioTech(g, t, cam, { theme: 'light' });
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    layer(g, cam, 1, (g) => {
      drawBeanCharacter(g, {
        x: CX - V(360, 240),
        y: GY,
        s: V(1.35, 1.48),
        facing: 1,
        pose: 'pointing',
        expr: 'motivated',
        t: t
      });
      holoBarChart(g, CX - V(80, 20), GY - V(460, 480), V(480, 400), V(380, 340), [{"label": "Day 1 Starters", "value": 94, "color": "#06b6d4"}, {"label": "Week 2 Drop", "value": 38, "color": "#f59e0b"}, {"label": "Top Masters", "value": 6, "color": "#10b981"}], { title: 'GLOBAL RETENTION METRIC', t, progress: Math.min(1.0, t / 1.5) });
      
      
      
    });
    holoStageBadge(g, V(60, 40), V(60, 110), 1, 'THE BIG PARADOX');
    FX.dust(g, t, { count: 20, color: '#38bdf8', a: 0.25 });
  }
});

// s004 — Narrative Scene 4 (Solo Hero)
registerShot('s004', {
  draw(g, t, info) {
    const cam = { z: 1.0, x: 0 };
    const hasBg = drawSceneBackground(g, SCENE_IMAGES['s004'], t, info.dur, 'pan_left');
    if (!hasBg) {
      getSet('cityStreet')(g, t, cam, { mood: 'dusk' });
    }
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    const rim = { color: '#ffb070', dir: [0, -1], w: 4.5 };
    layer(g, cam, 1, (g) => {
      drawFigure(g, {
        x: CX,
        y: GY,
        s: V(1.4, 1.55),
        facing: 1,
        outfit: HERO,
        pose: breathe(POSES.ready || POSES.stand, t),
        expr: 'motivated',
        rim: rim
      });
      drawTopicProp(g, 'dna_strand', CX + V(30, 22), GY - V(140, 150), 1.2, t);
    });
    UI.badge(g, { str: 'BEAT 04', color: '#7ee787', x: E.W - V(90, 70), y: V(120, 160) });
    FX.dust(g, t, { count: 30, color: '#ffdfb8', a: 0.3 });
  }
});

// s005 — Style 2A Modern Studio Tech Shot (studio_disruption)
registerShot('s005', {
  draw(g, t, info) {
    const cam = { z: 1.0, x: 0 };
    studioTech(g, t, cam, { theme: 'light' });
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    layer(g, cam, 1, (g) => {
      drawBeanCharacter(g, {
        x: CX - V(360, 240),
        y: GY,
        s: V(1.35, 1.48),
        facing: 1,
        pose: 'explaining',
        expr: 'motivated',
        t: t
      });
      
      
      holoComparisonSplit(g, CX - V(340, 280), GY - V(450, 480), V(700, 580), V(360, 340), {"title": "99% AMATEUR TRAP", "points": ["Wait for inspiration", "Emotional inconsistency", "Quit at first resistance"]}, {"title": "1% MASTER PROTOCOL", "points": ["Non-negotiable daily habits", "Systems over feelings", "Compounding focus"]}, { t });
      
    });
    holoStageBadge(g, V(60, 40), V(60, 110), 2, 'DISRUPTING ASSUMPTIONS');
    FX.dust(g, t, { count: 20, color: '#38bdf8', a: 0.25 });
  }
});

// s006 — Narrative Scene 6 (Solo Hero)
registerShot('s006', {
  draw(g, t, info) {
    const cam = { z: 1.0, x: 0 };
    const hasBg = drawSceneBackground(g, SCENE_IMAGES['s006'], t, info.dur, 'zoom_out');
    if (!hasBg) {
      getSet('cityStreet')(g, t, cam, { mood: 'dusk' });
    }
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    const rim = { color: '#ffb070', dir: [0, -1], w: 4.5 };
    layer(g, cam, 1, (g) => {
      drawFigure(g, {
        x: CX,
        y: GY,
        s: V(1.4, 1.55),
        facing: 1,
        outfit: HERO,
        pose: breathe(POSES.sit || POSES.stand, t),
        expr: 'exhausted',
        rim: rim
      });
      drawTopicProp(g, 'lightbulb_idea', CX + V(30, 22), GY - V(140, 150), 1.2, t);
    });
    UI.badge(g, { str: 'BEAT 06', color: '#7ee787', x: E.W - V(90, 70), y: V(120, 160) });
    FX.dust(g, t, { count: 30, color: '#ffdfb8', a: 0.3 });
  }
});

// s007 — Narrative Scene 7 (Solo Hero)
registerShot('s007', {
  draw(g, t, info) {
    const cam = { z: 1.0, x: 0 };
    const hasBg = drawSceneBackground(g, SCENE_IMAGES['s007'], t, info.dur, 'zoom_in');
    if (!hasBg) {
      getSet('lab')(g, t, cam, { mood: 'coolDay' });
    }
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    const rim = { color: '#ffb070', dir: [0, -1], w: 4.5 };
    layer(g, cam, 1, (g) => {
      drawFigure(g, {
        x: CX,
        y: GY,
        s: V(1.4, 1.55),
        facing: 1,
        outfit: HERO,
        pose: breathe(POSES.sad || POSES.stand, t),
        expr: 'shocked',
        rim: rim
      });
      drawTopicProp(g, 'dna_strand', CX + V(30, 22), GY - V(140, 150), 1.2, t);
    });
    UI.badge(g, { str: 'BEAT 07', color: '#7ee787', x: E.W - V(90, 70), y: V(120, 160) });
    FX.dust(g, t, { count: 30, color: '#ffdfb8', a: 0.3 });
  }
});

// s008 — Style 2A Modern Studio Tech Shot (studio_resistance_gauge)
registerShot('s008', {
  draw(g, t, info) {
    const cam = { z: 1.0, x: 0 };
    studioTech(g, t, cam, { theme: 'dark_studio' });
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    layer(g, cam, 1, (g) => {
      drawBeanCharacter(g, {
        x: CX - V(360, 240),
        y: GY,
        s: V(1.35, 1.48),
        facing: 1,
        pose: 'thinking',
        expr: 'motivated',
        t: t
      });
      
      holoCircularGauge(g, CX + V(160, 100), GY - V(280, 300), V(110, 95), 91, { label: 'RESISTANCE PEAK', unit: '%', t });
      
      
    });
    holoStageBadge(g, V(60, 40), V(60, 110), 3, 'UNVEILING THE MECHANISM');
    FX.dust(g, t, { count: 20, color: '#38bdf8', a: 0.25 });
  }
});

// s009 — Narrative Scene 9 (Solo Hero)
registerShot('s009', {
  draw(g, t, info) {
    const cam = { z: 1.0, x: 0 };
    const hasBg = drawSceneBackground(g, SCENE_IMAGES['s009'], t, info.dur, 'zoom_out');
    if (!hasBg) {
      getSet('classroom')(g, t, cam, { mood: 'coolDay' });
    }
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    const rim = { color: '#ffb070', dir: [0, -1], w: 4.5 };
    layer(g, cam, 1, (g) => {
      drawFigure(g, {
        x: CX,
        y: GY,
        s: V(1.4, 1.55),
        facing: 1,
        outfit: HERO,
        pose: breathe(POSES.stand || POSES.stand, t),
        expr: 'disciplined',
        rim: rim
      });
      drawTopicProp(g, 'dna_strand', CX + V(30, 22), GY - V(140, 150), 1.2, t);
    });
    UI.badge(g, { str: 'BEAT 09', color: '#7ee787', x: E.W - V(90, 70), y: V(120, 160) });
    FX.dust(g, t, { count: 30, color: '#ffdfb8', a: 0.3 });
  }
});

// s010 — Narrative Scene 10 (Solo Hero)
registerShot('s010', {
  draw(g, t, info) {
    const cam = { z: 1.0, x: 0 };
    const hasBg = drawSceneBackground(g, SCENE_IMAGES['s010'], t, info.dur, 'pan_left');
    if (!hasBg) {
      getSet('classroom')(g, t, cam, { mood: 'coolDay' });
    }
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    const rim = { color: '#ffb070', dir: [0, -1], w: 4.5 };
    layer(g, cam, 1, (g) => {
      drawFigure(g, {
        x: CX,
        y: GY,
        s: V(1.4, 1.55),
        facing: 1,
        outfit: HERO,
        pose: breathe(POSES.holdFront || POSES.stand, t),
        expr: 'disciplined',
        rim: rim
      });
      drawTopicProp(g, 'dna_strand', CX + V(30, 22), GY - V(140, 150), 1.2, t);
    });
    UI.badge(g, { str: 'BEAT 010', color: '#7ee787', x: E.W - V(90, 70), y: V(120, 160) });
    FX.dust(g, t, { count: 30, color: '#ffdfb8', a: 0.3 });
  }
});

// s011 — Style 2A Modern Studio Tech Shot (studio_truth_revelation)
registerShot('s011', {
  draw(g, t, info) {
    const cam = { z: 1.0, x: 0 };
    studioTech(g, t, cam, { theme: 'light' });
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    layer(g, cam, 1, (g) => {
      drawBeanCharacter(g, {
        x: CX - V(360, 240),
        y: GY,
        s: V(1.35, 1.48),
        facing: 1,
        pose: 'pointing',
        expr: 'disciplined',
        t: t
      });
      
      
      
      holoGlassCard(g, CX - V(120, 40), GY - V(420, 440), V(440, 360), V(280, 260), { title: 'THE MATHEMATICAL TRUTH', subtitle: 'Small daily disciplines repeated consistently create massive exponential advantage.', t });
    });
    holoStageBadge(g, V(60, 40), V(60, 110), 4, 'ULTIMATE TRUTH REVELATION');
    FX.dust(g, t, { count: 20, color: '#38bdf8', a: 0.25 });
  }
});

// s012 — Narrative Scene 12 (Solo Hero)
registerShot('s012', {
  draw(g, t, info) {
    const cam = { z: 1.0, x: 0 };
    const hasBg = drawSceneBackground(g, SCENE_IMAGES['s012'], t, info.dur, 'zoom_out');
    if (!hasBg) {
      getSet('cityStreet')(g, t, cam, { mood: 'dusk' });
    }
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    const rim = { color: '#ffb070', dir: [0, -1], w: 4.5 };
    layer(g, cam, 1, (g) => {
      drawFigure(g, {
        x: CX,
        y: GY,
        s: V(1.4, 1.55),
        facing: 1,
        outfit: HERO,
        pose: breathe(POSES.reach || POSES.stand, t),
        expr: 'disciplined',
        rim: rim
      });
      drawTopicProp(g, 'trophy_cup', CX + V(30, 22), GY - V(140, 150), 1.2, t);
    });
    UI.badge(g, { str: 'BEAT 012', color: '#7ee787', x: E.W - V(90, 70), y: V(120, 160) });
    FX.dust(g, t, { count: 30, color: '#ffdfb8', a: 0.3 });
  }
});

// s013 — Narrative Scene 13 (Solo Hero)
registerShot('s013', {
  draw(g, t, info) {
    const cam = { z: 1.0, x: 0 };
    const hasBg = drawSceneBackground(g, SCENE_IMAGES['s013'], t, info.dur, 'zoom_in');
    if (!hasBg) {
      getSet('cityStreet')(g, t, cam, { mood: 'dusk' });
    }
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    const rim = { color: '#ffb070', dir: [0, -1], w: 4.5 };
    layer(g, cam, 1, (g) => {
      drawFigure(g, {
        x: CX,
        y: GY,
        s: V(1.4, 1.55),
        facing: 1,
        outfit: HERO,
        pose: breathe(POSES.cheer || POSES.stand, t),
        expr: 'happy',
        rim: rim
      });
      drawTopicProp(g, 'dna_strand', CX + V(30, 22), GY - V(140, 150), 1.2, t);
    });
    UI.badge(g, { str: 'BEAT 013', color: '#7ee787', x: E.W - V(90, 70), y: V(120, 160) });
    FX.dust(g, t, { count: 30, color: '#ffdfb8', a: 0.3 });
  }
});

// s014 — Style 2A Modern Studio Tech Shot (the_mastery_level)
registerShot('s014', {
  draw(g, t, info) {
    const cam = { z: 1.0, x: 0 };
    studioTech(g, t, cam, { theme: 'light' });
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    layer(g, cam, 1, (g) => {
      drawBeanCharacter(g, {
        x: CX - V(360, 240),
        y: GY,
        s: V(1.35, 1.48),
        facing: 1,
        pose: 'standing',
        expr: 'disciplined',
        t: t
      });
      
      
      
      
    });
    
    FX.dust(g, t, { count: 20, color: '#38bdf8', a: 0.25 });
  }
});

// s015 — Style 2A Modern Studio Tech Shot (the_core_philosophy)
registerShot('s015', {
  draw(g, t, info) {
    const cam = { z: 1.0, x: 0 };
    studioTech(g, t, cam, { theme: 'light' });
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    layer(g, cam, 1, (g) => {
      drawBeanCharacter(g, {
        x: CX - V(360, 240),
        y: GY,
        s: V(1.35, 1.48),
        facing: 1,
        pose: 'cheer',
        expr: 'motivated',
        t: t
      });
      
      
      
      
    });
    
    FX.dust(g, t, { count: 20, color: '#38bdf8', a: 0.25 });
  }
});

// s016 — Style 2A Modern Studio Tech Shot (the_challenge_cta)
registerShot('s016', {
  draw(g, t, info) {
    const cam = { z: 1.0, x: 0 };
    studioTech(g, t, cam, { theme: 'dark_studio' });
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    layer(g, cam, 1, (g) => {
      drawBeanCharacter(g, {
        x: CX - V(360, 240),
        y: GY,
        s: V(1.35, 1.48),
        facing: 1,
        pose: 'pointing',
        expr: 'disciplined',
        t: t
      });
      
      
      
      
    });
    holoStageBadge(g, V(60, 40), V(60, 110), 5, 'COMMUNITY DEBATE');
    FX.dust(g, t, { count: 20, color: '#38bdf8', a: 0.25 });
  }
});
