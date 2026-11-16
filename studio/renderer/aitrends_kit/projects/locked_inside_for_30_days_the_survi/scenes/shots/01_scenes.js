// scenes/shots/01_scenes.js — Deterministic shots for aiTrends Studio
import { E, V, registerShot, mood, layer, blurLayer, veil, ease, prog, clamp, lerp, shake, seg, circle, ring, rr, poly, glow, alpha, shade, linGrad, FONTS, text } from '/engine/core.js';
import { drawFigure, POSES, posesAt, breathe, bigFace, headPos } from '/engine/rig2d.js';
import * as FX from '/engine/fx2d.js';
import * as UI from '/engine/ui2d.js';
import { bedroom, classroom, cityStreet, ruinsWasteland, spaceVoid, cafe, lab } from '../sets/universal_sets.js';
import { HERO, SECONDARY, FRIEND, DOC, CAST } from '../cast.js';

const SETS = { bedroom, classroom, cityStreet, ruinsWasteland, spaceVoid, cafe, lab };
function getSet(name) { return SETS[name] || SETS.bedroom; }

// s001 — Cold Hook Opening Shot
registerShot('s001', {
  draw(g, t, info) {
    const cam = { z: 1 + 0.07 * ease.inOut(t / info.dur), x: -35 * ease.inOut(t / info.dur) };
    const { GY, CX, M } = getSet('bedroom')(g, t, cam, { mood: 'interiorWarm' });
    const rim = { color: M.rim, dir: [0, -1], w: 4 };
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
    });
    FX.dust(g, t, { count: 35, color: '#ffe4c4', a: 0.35 });
  }
});

// s002 — Narrative Beat
registerShot('s002', {
  draw(g, t, info) {
    const cam = { z: 1 + 0.05 * ease.inOut(t / info.dur), x: 25 * Math.sin(t * 0.8) };
    const { GY, CX, M } = getSet('bedroom')(g, t, cam, { mood: 'interiorWarm' });
    const rim = { color: M.rim, dir: [0, -1], w: 4 };
    layer(g, cam, 1, (g) => {
      drawFigure(g, {
        x: CX,
        y: GY,
        s: V(1.4, 1.55),
        facing: 1,
        outfit: HERO,
        pose: breathe(POSES.point || POSES.stand, t),
        expr: 'neutral',
        rim: rim
      });
    });
    FX.dust(g, t, { count: 30, color: '#ffdfb8', a: 0.3 });
  }
});

// s003 — Narrative Beat
registerShot('s003', {
  draw(g, t, info) {
    const cam = { z: 1 + 0.05 * ease.inOut(t / info.dur), x: 25 * Math.sin(t * 0.8) };
    const { GY, CX, M } = getSet('bedroom')(g, t, cam, { mood: 'interiorWarm' });
    const rim = { color: M.rim, dir: [0, -1], w: 4 };
    layer(g, cam, 1, (g) => {
      drawFigure(g, {
        x: CX,
        y: GY,
        s: V(1.4, 1.55),
        facing: 1,
        outfit: HERO,
        pose: breathe(POSES.shrug || POSES.stand, t),
        expr: 'neutral',
        rim: rim
      });
    });
    FX.dust(g, t, { count: 30, color: '#ffdfb8', a: 0.3 });
  }
});

// s004 — BigFace Dramatic Reaction
registerShot('s004', {
  draw(g, t, info) {
    blurLayer(g, 15, (g) => getSet('bedroom')(g, t, { z: 1.45, x: -60 }, { mood: 'interiorWarm' }));
    veil(g, '#100a14', 0.38);
    const M = mood('interiorWarm');
    const r = V(290, 320) * (1 + 0.04 * ease.inOut(t / info.dur));
    bigFace(g, E.W / 2, E.H * V(0.6, 0.55), r, {
      outfit: HERO,
      expr: 'shocked',
      look: [0.1, -0.1],
      rimColor: M.rim,
      rimSide: -1,
      tilt: Math.sin(t * 1.5) * 0.02
    });
    FX.dust(g, t, { count: 25, color: '#ffdfb8', a: 0.3 });
  }
});

// s005 — Narrative Beat
registerShot('s005', {
  draw(g, t, info) {
    const cam = { z: 1 + 0.05 * ease.inOut(t / info.dur), x: 25 * Math.sin(t * 0.8) };
    const { GY, CX, M } = getSet('ruinsWasteland')(g, t, cam, { mood: 'dusk' });
    const rim = { color: M.rim, dir: [0, -1], w: 4 };
    layer(g, cam, 1, (g) => {
      drawFigure(g, {
        x: CX,
        y: GY,
        s: V(1.4, 1.55),
        facing: 1,
        outfit: HERO,
        pose: breathe(POSES.handsOnHead || POSES.stand, t),
        expr: 'shocked',
        rim: rim
      });
    });
    FX.dust(g, t, { count: 30, color: '#ffdfb8', a: 0.3 });
  }
});

// s006 — Climax & CTA End Screen
registerShot('s006', {
  draw(g, t, info) {
    UI.endScreen(g, t, {
      question: 'Aap aise scenario me akele rehna pasand karen?',
      cast: CAST,
      rim: '#ffb070'
    });
  }
});
