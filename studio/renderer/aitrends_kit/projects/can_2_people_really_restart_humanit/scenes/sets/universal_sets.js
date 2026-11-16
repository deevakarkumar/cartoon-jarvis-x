// scenes/sets/universal_sets.js — Cinematic flat-shaded vector sets for aiTrends Studio
// Supports: bedroom, classroom, cityStreet, ruinsWasteland, spaceVoid, cafe, lab
import { E, V, mood, layer, backdrop, rr, seg, circle, ring, poly, linGrad, radGrad, glow, alpha, shade, mix, text, FONTS } from '/engine/core.js';
import * as FX from '/engine/fx2d.js';

export const standardGround = () => E.H * V(0.82, 0.68);

// 1. COZY BEDROOM (Dusk / Night)
export function bedroom(g, t, cam, o = {}) {
  const M = mood(o.mood || 'interiorWarm'), GY = standardGround(), CX = E.W / 2;
  const wall = shade(M.wall, -0.35), wallDark = shade(M.wall, -0.65);

  layer(g, cam, 0.15, (g) => {
    backdrop(g, M.sky);
    FX.moon(g, CX + V(380, 220), GY - V(520, 920), 44, '#f0f4ff');
    FX.stars(g, t, { count: 60, area: [-E.W, 0, E.W * 3, GY - 200] });
    FX.clouds(g, { y: GY - V(700, 1200), h: 140, color: '#e8d8c8', a: 0.14, seed: 4 });
  });

  layer(g, cam, 0.5, (g) => {
    const top = GY - V(620, 940), left = CX - 1600, w = 3200;
    g.fillStyle = linGrad(g, 0, top, 0, GY, [shade(wall, 0.08), wall, wallDark]);
    g.fillRect(left, top, w, GY - top + 4);

    // Large bedroom window overlooking the dusk sky
    const wx = CX - V(320, 280), wy = GY - V(540, 800), ww = V(520, 480), wh = V(340, 400);
    FX.windowFrame(g, { x: wx, y: wy, w: ww, h: wh, cols: 2, rows: 2, frame: wallDark, bar: 9, blinds: 4 }, (g, x, y, w, h) => {
      g.fillStyle = linGrad(g, 0, y, 0, y + h, M.sky);
      g.fillRect(x, y, w, h);
      FX.moon(g, x + w * 0.65, y + h * 0.35, 34, '#ffffff');
      FX.skyline(g, { x, y: y + h, w, maxH: h * 0.5, color: alpha(shade(wallDark, 0.2), 0.8), lit: 0.2, seed: 12 });
    });

    // Nightstand with warm lamp & alarm clock
    const nx = CX + V(280, 240), ny = GY;
    rr(g, nx - 60, ny - 160, 120, 160, 6); g.fillStyle = shade(wallDark, -0.2); g.fill();
    // Warm bedside lamp
    rr(g, nx - 8, ny - 240, 16, 80, 3); g.fillStyle = '#b89860'; g.fill();
    poly(g, [[nx - 36, ny - 240], [nx + 36, ny - 240], [nx + 24, ny - 290], [nx - 24, ny - 290]], '#ffe0a0');
    glow(g, nx, ny - 260, 90, '#ffcf80', 0.5);
    FX.lightCone(g, nx, ny - 240, { angle: Math.PI / 2, spread: 0.75, len: 320, color: '#ffe6a8', a: 0.24 });

    // Alarm clock with glowing digital face
    rr(g, nx - 42, ny - 188, 54, 28, 4); g.fillStyle = '#0e0b12'; g.fill();
    text(g, '07:00', nx - 15, ny - 174, { size: 14, color: '#ff4433', font: FONTS.ui, weight: 900 });
  });

  layer(g, cam, 0.85, (g) => {
    // Wooden floor
    g.fillStyle = linGrad(g, 0, GY, 0, GY + 450, [shade(M.floor, -0.15), shade(M.dark, -0.3)]);
    g.fillRect(-E.W, GY, E.W * 3, E.H * 2);
    FX.floorLines(g, GY, GY + 500, 'rgba(0,0,0,.25)', 0.08);

    // Cozy bed on left
    const bx = CX - V(520, 440);
    FX.bed(g, { x: bx, y: GY, w: V(380, 340), color: '#3d4d75', frame: '#181422', pillow: '#ece6f0' });

    // Warm light pools
    FX.pool(g, CX + V(280, 240), GY + 20, 180, 36, '#ffcf80', 0.26);
    FX.pool(g, CX - V(100, 80), GY + 25, 260, 44, M.practical, 0.15);
  });

  FX.dust(g, t, { count: 35, color: '#ffe4c4', a: 0.3 });
  return { GY, CX, M };
}

// 2. SCHOOL CLASSROOM (Dusk / Golden Hour)
export function classroom(g, t, cam, o = {}) {
  const M = mood(o.mood || 'dusk'), GY = standardGround(), CX = E.W / 2;
  const wall = shade(M.wall, -0.3), wallDark = shade(M.wall, -0.6);

  layer(g, cam, 0.15, (g) => {
    backdrop(g, M.sky);
    FX.sun(g, CX - V(480, 300), GY - V(540, 960), 60, '#fff4dc', M.key, 4);
    FX.skyline(g, { x: -E.W, y: GY - V(360, 640), w: E.W * 3, maxH: 220, color: shade(M.sky[1], -0.2), lit: 0.2, seed: 15 });
  });

  layer(g, cam, 0.5, (g) => {
    const top = GY - V(640, 960), left = CX - 1600, w = 3200;
    g.fillStyle = linGrad(g, 0, top, 0, GY, [wall, wallDark]);
    g.fillRect(left, top, w, GY - top + 4);

    // Wide school windows on left
    const wx = CX - V(620, 460), wy = GY - V(520, 780), ww = V(420, 360), wh = V(320, 380);
    FX.windowFrame(g, { x: wx, y: wy, w: ww, h: wh, cols: 3, rows: 2, frame: wallDark, bar: 8 }, (g, x, y, w, h) => {
      g.fillStyle = linGrad(g, 0, y, 0, y + h, M.sky);
      g.fillRect(x, y, w, h);
      FX.godRays(g, x + w / 2, y + 40, { count: 6, len: 1200, a: 0.12, t });
    });

    // Large chalkboard on right with chalk notes
    const bx = CX + V(40, 20), by = GY - V(500, 750), bw = V(520, 440), bh = V(260, 280);
    rr(g, bx - 6, by - 6, bw + 12, bh + 12, 6); g.fillStyle = '#4a3828'; g.fill(); // wooden border
    rr(g, bx, by, bw, bh, 4); g.fillStyle = '#1e3328'; g.fill(); // chalkboard green
    // Dynamic Chalk text & scientific diagrams
    const cTitle = o.chalkTitle || 'RESEARCH & ANALYSIS';
    const cSub = o.chalkSub || 'CASE STUDY · 100% VERIFIED';
    text(g, cTitle, bx + bw / 2, by + 45, { size: 22, color: 'rgba(255,255,255,0.9)', font: FONTS.ui, weight: 900 });
    text(g, cSub, bx + bw / 2, by + 85, { size: 16, color: 'rgba(255,230,180,0.75)', font: FONTS.ui, weight: 800 });
    seg(g, [[bx + 40, by + 125], [bx + bw - 40, by + 125]], 2, 'rgba(255,255,255,0.3)');
    // Draw dynamic scientific chalk curve
    g.strokeStyle = 'rgba(120,220,255,0.6)'; g.lineWidth = 3; g.beginPath();
    g.moveTo(bx + 50, by + 220);
    g.bezierCurveTo(bx + bw * 0.35, by + 220, bx + bw * 0.6, by + 150, bx + bw - 50, by + 160);
    g.stroke();
    text(g, 'DATA METRICS · VERIFIED', bx + bw / 2, by + 245, { size: 16, color: 'rgba(255,255,255,0.7)', font: FONTS.ui, weight: 900 });

    // Classroom wall clock
    FX.clock(g, CX - V(80, 50), GY - V(580, 880), 28, t * 10, { face: '#f2f0ea' });

    // Vending machine on far right
    const vx = CX + V(620, 380), vy = GY;
    rr(g, vx - 50, vy - 280, 100, 280, 8); g.fillStyle = '#222838'; g.fill();
    rr(g, vx - 40, vy - 260, 80, 160, 4); g.fillStyle = '#141a24'; g.fill();
    glow(g, vx, vy - 180, 120, '#58a6ff', 0.25);
    text(g, 'SNACKS', vx, vy - 245, { size: 12, color: '#58a6ff', font: FONTS.ui, weight: 900 });
  });

  layer(g, cam, 0.85, (g) => {
    // School floor
    g.fillStyle = linGrad(g, 0, GY, 0, GY + 450, [shade(M.floor, -0.1), shade(M.dark, -0.25)]);
    g.fillRect(-E.W, GY, E.W * 3, E.H * 2);
    FX.floorLines(g, GY, GY + 500, 'rgba(0,0,0,.22)', 0.08);

    // School desk & chair silhouettes
    for (const sx of [-V(320, 260), V(220, 180)]) {
      FX.chair(g, CX + sx, GY, 1.1, '#1e1826');
      rr(g, CX + sx - 50, GY - 120, 100, 12, 4); g.fillStyle = '#2a2234'; g.fill();
      seg(g, [[CX + sx - 40, GY - 110], [CX + sx - 40, GY]], 5, '#1e1826');
      seg(g, [[CX + sx + 40, GY - 110], [CX + sx + 40, GY]], 5, '#1e1826');
    }

    FX.pool(g, CX - V(400, 300), GY + 20, 320, 50, M.key, 0.25);
  });

  FX.dust(g, t, { count: 40, color: '#ffdca8', a: 0.35 });
  return { GY, CX, M };
}

// 3. CITY STREET AT DUSK / NIGHT
export function cityStreet(g, t, cam, o = {}) {
  const M = mood(o.mood || 'dusk'), GY = standardGround(), CX = E.W / 2;
  const wallDark = shade(M.wall, -0.6);

  layer(g, cam, 0.15, (g) => {
    backdrop(g, M.sky);
    FX.sun(g, CX + V(500, 280), GY - V(480, 880), 55, '#fff6e4', M.key, 4);
    FX.skyline(g, { x: -E.W, y: GY - V(340, 600), w: E.W * 3, minH: 70, maxH: V(240, 380), color: shade(M.wall, -0.4), windowColor: alpha(M.practical, 0.6), lit: 0.25, seed: 9 });
  });

  layer(g, cam, 0.55, (g) => {
    // City buildings in midground
    FX.facade(g, { x: CX - V(700, 480), y: GY, w: V(360, 320), h: V(460, 520), color: '#201b2a', win: M.practical, lit: 0.35, cols: 3, rows: 4, seed: 3 });
    FX.facade(g, { x: CX + V(340, 220), y: GY, w: V(380, 340), h: V(500, 560), color: '#1a1624', win: M.practical, lit: 0.4, cols: 3, rows: 5, seed: 7 });

    // Street trees
    FX.tree(g, CX - V(260, 180), GY, V(1.2, 1.0), '#140f1c');
    FX.tree(g, CX + V(240, 160), GY, V(1.1, 0.95), '#140f1c');

    // Classic glowing street lamp post
    FX.lampPost(g, CX - V(120, 90), GY, V(340, 380), { color: '#120d18', light: M.key, on: true });
    FX.lampPost(g, CX + V(520, 360), GY, V(340, 380), { color: '#120d18', light: M.key, on: true });
  });

  layer(g, cam, 0.9, (g) => {
    // Sidewalk & road
    g.fillStyle = linGrad(g, 0, GY, 0, GY + 500, [shade(M.floor, -0.1), shade(M.dark, -0.3)]);
    g.fillRect(-E.W, GY, E.W * 3, E.H * 2);
    FX.floorLines(g, GY, GY + 500, 'rgba(0,0,0,.26)', 0.08);

    // Lamp light pools
    FX.pool(g, CX - V(80, 60), GY + 25, 220, 40, M.key, 0.35);
    FX.pool(g, CX + V(560, 390), GY + 25, 220, 40, M.key, 0.35);
  });

  FX.dust(g, t, { count: 35, color: '#ffdfb8', a: 0.3 });
  return { GY, CX, M };
}

// 4. RUINS & WASTELAND (Post-Apocalypse Earth)
export function ruinsWasteland(g, t, cam, o = {}) {
  const M = mood(o.mood || 'dusk'), GY = standardGround(), CX = E.W / 2;

  layer(g, cam, 0.12, (g) => {
    backdrop(g, ['#1c101c', '#441824', '#8c3426']);
    // Massive dying sun on the horizon
    FX.sun(g, CX, GY - V(260, 420), V(85, 95), '#ffcc88', '#ff5522', 5);
    FX.godRays(g, CX, GY - V(260, 420), { count: 9, len: 1600, color: '#ff8844', a: 0.12, t });
  });

  layer(g, cam, 0.45, (g) => {
    // Crumbling broken skyline silhouettes
    FX.skyline(g, { x: -E.W, y: GY - V(180, 320), w: E.W * 3, minH: 50, maxH: V(280, 400), color: '#140a16', lit: 0.02, seed: 19 });
    // Dead pine trees
    FX.pine(g, CX - V(460, 320), GY, 1.2, '#120814');
    FX.pine(g, CX + V(420, 280), GY, 1.0, '#120814');
    FX.fog(g, GY - 80, 90, '#ff6633', 0.14);
  });

  layer(g, cam, 0.85, (g) => {
    // Cracked desolate ground
    g.fillStyle = linGrad(g, 0, GY, 0, GY + 500, ['#1a0f18', '#0c060d']);
    g.fillRect(-E.W, GY, E.W * 3, E.H * 2);
    FX.floorLines(g, GY, GY + 500, 'rgba(0,0,0,.35)', 0.1);

    // Rubble & broken boulders
    for (const [rx, rw, rh] of [[CX - 300, 70, 34], [CX + 280, 90, 42], [CX - 120, 40, 20]]) {
      poly(g, [[rx, GY], [rx + rw * 0.2, GY - rh], [rx + rw * 0.8, GY - rh * 0.8], [rx + rw, GY]], '#120814');
    }

    FX.pool(g, CX, GY + 20, 380, 50, '#ff7733', 0.2);
  });

  FX.dust(g, t, { count: 50, color: '#ffaa77', a: 0.45 });
  return { GY, CX, M };
}

// 5. DEEP SPACE & VOID (Cosmic / Planet Horizon)
export function spaceVoid(g, t, cam, o = {}) {
  const M = mood(o.mood || 'night'), GY = standardGround(), CX = E.W / 2;

  layer(g, cam, 0.1, (g) => {
    backdrop(g, ['#040208', '#0a0614', '#140c24']);
    FX.stars(g, t, { count: 220, area: [-E.W, 0, E.W * 3, E.H] });

    // Glowing Earth in distant cosmos
    const ex = CX + V(380, 220), ey = GY - V(460, 780), er = V(90, 80);
    glow(g, ex, ey, er * 2.2, '#388bfd', 0.4);
    circle(g, ex, ey, er, '#1d428a');
    ring(g, ex, ey, er + 2, 4, 'rgba(120,200,255,.65)');
    // Atmosphere rim
    g.save(); g.beginPath(); g.arc(ex, ey, er, -1.2, 1.2);
    g.strokeStyle = '#7ee787'; g.lineWidth = 6; g.stroke(); g.restore();
  });

  layer(g, cam, 0.85, (g) => {
    // Tech platform or dark ground
    g.fillStyle = linGrad(g, 0, GY, 0, GY + 450, ['#100a1c', '#06030c']);
    g.fillRect(-E.W, GY, E.W * 3, E.H * 2);
    FX.floorLines(g, GY, GY + 500, 'rgba(88,166,255,.18)', 0.08);
    FX.pool(g, CX, GY + 20, 360, 45, '#58a6ff', 0.2);
  });

  FX.dust(g, t, { count: 30, color: '#cfe0ff', a: 0.35 });
  return { GY, CX, M };
}

// 6. CAFE & LAB (Imports from existing or provided sets)
export { cafe } from './cafe.js';
export { lab } from './lab.js';
