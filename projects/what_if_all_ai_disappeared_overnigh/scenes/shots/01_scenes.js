// scenes/shots/01_scenes.js — Universal Dynamic Story Engine for aiTrends Studio
import { E, V, registerShot, mood, layer, blurLayer, veil, ease, prog, clamp, lerp, shake, seg, circle, ring, rr, poly, glow, alpha, shade, linGrad, radGrad, FONTS, text, measure } from '/engine/core.js';
import { drawFigure, POSES, posesAt, breathe, bigFace, headPos } from '/engine/rig2d.js';
import { drawBeanCharacter, drawShadowDemon, drawFatigueFigure, drawMotivationMeter, drawDayBanner, drawDisciplineGraph, drawInSceneText } from '/engine/dayone_rig.js';
import * as FX from '/engine/fx2d.js';
import * as UI from '/engine/ui2d.js';
import { bedroom, classroom, cityStreet, ruinsWasteland, spaceVoid, natureForest, highTechServer, cafe, lab, dayoneBedroom, dayoneRunningStreet, dayoneGym, dayoneStudyDesk, dayoneSunrise } from '../sets/universal_sets.js';
import { HERO, SECONDARY, FRIEND, DOC, CAST } from '../cast.js';

const SETS = { bedroom, classroom, cityStreet, ruinsWasteland, spaceVoid, natureForest, highTechServer, cafe, lab, dayoneBedroom, dayoneRunningStreet, dayoneGym, dayoneStudyDesk, dayoneSunrise };
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
  preloadImg('s006', '/project/images/scene_006.png')
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

// s001 — Day One Films Shot (Instant Shock: AI Disappears)
registerShot('s001', {
  draw(g, t, info) {
    const cam = { z: 1.0, x: 0 };
    const hasBg = drawSceneBackground(g, SCENE_IMAGES['s001'], t, info.dur, 'zoom_in');
    if (!hasBg) {
      getSet('bedroom')(g, t, cam, { mood: 'interiorWarm', clockTime: '' });
    }
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    layer(g, cam, 1, (g) => {
      
      
      drawBeanCharacter(g, {
        x: CX ,
        y: GY,
        s: V(1.35, 1.48),
        facing: 1,
        pose: 'hands_on_head',
        expr: 'shocked',
        aura: 0.0,
        darkBags: false,
        t: t
      });
      
      
    });
    
    
    FX.dust(g, t, { count: 25, color: '#fed7aa', a: 0.3 });
  }
});

// s002 — Day One Films Shot (Immediate Escalation: Global Effect)
registerShot('s002', {
  draw(g, t, info) {
    const cam = { z: 1.0, x: 0 };
    const hasBg = drawSceneBackground(g, SCENE_IMAGES['s002'], t, info.dur, 'pan_right');
    if (!hasBg) {
      getSet('cityStreet')(g, t, cam, { mood: 'dusk', clockTime: '' });
    }
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    layer(g, cam, 1, (g) => {
      
      
      drawBeanCharacter(g, {
        x: CX ,
        y: GY,
        s: V(1.35, 1.48),
        facing: 1,
        pose: 'panicking',
        expr: 'screaming',
        aura: 0.0,
        darkBags: false,
        t: t
      });
      
      
    });
    
    
    FX.dust(g, t, { count: 25, color: '#fed7aa', a: 0.3 });
  }
});

// s003 — Day One Films Shot (Compounding Chaos: Supply Chain Collapse)
registerShot('s003', {
  draw(g, t, info) {
    const cam = { z: 1.0, x: 0 };
    const hasBg = drawSceneBackground(g, SCENE_IMAGES['s003'], t, info.dur, 'zoom_out');
    if (!hasBg) {
      getSet('classroom')(g, t, cam, { mood: 'coolDay', clockTime: '' });
    }
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    layer(g, cam, 1, (g) => {
      
      
      drawBeanCharacter(g, {
        x: CX ,
        y: GY,
        s: V(1.35, 1.48),
        facing: 1,
        pose: 'hands_on_head',
        expr: 'jaw_drop',
        aura: 0.0,
        darkBags: false,
        t: t
      });
      
      
    });
    
    
    FX.dust(g, t, { count: 25, color: '#fed7aa', a: 0.3 });
  }
});

// s004 — Day One Films Shot (Hidden Science: AI's Invisible Role)
registerShot('s004', {
  draw(g, t, info) {
    const cam = { z: 1.0, x: 0 };
    const hasBg = drawSceneBackground(g, SCENE_IMAGES['s004'], t, info.dur, 'pan_left');
    if (!hasBg) {
      getSet('highTechServer')(g, t, cam, { mood: 'cyberpunk', clockTime: '' });
    }
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    layer(g, cam, 1, (g) => {
      
      
      drawBeanCharacter(g, {
        x: CX ,
        y: GY,
        s: V(1.35, 1.48),
        facing: 1,
        pose: 'explaining',
        expr: 'thinking',
        aura: 0.0,
        darkBags: false,
        t: t
      });
      
      
    });
    
    
    FX.dust(g, t, { count: 25, color: '#fed7aa', a: 0.3 });
  }
});

// s005 — Day One Films Shot (Extreme Climax: System Overload)
registerShot('s005', {
  draw(g, t, info) {
    const cam = { z: 1.0, x: 0 };
    const hasBg = drawSceneBackground(g, SCENE_IMAGES['s005'], t, info.dur, 'zoom_in');
    if (!hasBg) {
      getSet('ruinsWasteland')(g, t, cam, { mood: 'dusk', clockTime: '' });
    }
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    layer(g, cam, 1, (g) => {
      
      
      drawBeanCharacter(g, {
        x: CX ,
        y: GY,
        s: V(1.35, 1.48),
        facing: 1,
        pose: 'slouching',
        expr: 'deadpan',
        aura: 0.0,
        darkBags: false,
        t: t
      });
      
      
    });
    
    
    FX.dust(g, t, { count: 25, color: '#fed7aa', a: 0.3 });
  }
});

// s006 — Day One Films Shot (Mind-Blowing Dilemma Question)
registerShot('s006', {
  draw(g, t, info) {
    const cam = { z: 1.0, x: 0 };
    const hasBg = drawSceneBackground(g, SCENE_IMAGES['s006'], t, info.dur, 'zoom_out');
    if (!hasBg) {
      getSet('spaceVoid')(g, t, cam, { mood: 'midnight', clockTime: '' });
    }
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    layer(g, cam, 1, (g) => {
      
      
      drawBeanCharacter(g, {
        x: CX ,
        y: GY,
        s: V(1.35, 1.48),
        facing: 1,
        pose: 'look_up',
        expr: 'thinking',
        aura: 0.0,
        darkBags: false,
        t: t
      });
      
      
    });
    
    
    FX.dust(g, t, { count: 25, color: '#fed7aa', a: 0.3 });
  }
});
