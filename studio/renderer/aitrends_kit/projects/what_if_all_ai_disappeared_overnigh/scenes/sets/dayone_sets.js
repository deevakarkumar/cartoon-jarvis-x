// scenes/sets/dayone_sets.js — Signature Atmospheric Sets for Day One Films Style
// Implements:
// 1. dayoneBedroom (Midnight dark room with glowing red LED clock 05:00)
// 2. dayoneRunningStreet (Night asphalt road, streetlamps with amber light pools, crescent moon)
// 3. dayoneGym (Moody warehouse gym, dumbbell rack, 'NO EXCUSES' wall poster)
// 4. dayoneStudyDesk (Desk lamp cone, stacked books, schedule whiteboard)
// 5. dayoneSunrise (Day 62 breakthrough, cobalt-rose-apricot dawn horizon)

import { E, V, mood, layer, backdrop, rr, seg, circle, ring, poly, linGrad, radGrad, glow, alpha, shade, mix, text, FONTS } from '/engine/core.js';
import * as FX from '/engine/fx2d.js';

export const standardGround = () => E.H * V(0.82, 0.68);

// -------------------------------------------------------------
// 1. DAY ONE BEDROOM (Midnight Noir + Red LED Alarm 05:00)
// -------------------------------------------------------------
export function dayoneBedroom(g, t, cam, o = {}) {
  const GY = standardGround(), CX = E.W / 2;
  const clockTime = o.clockTime || '05:00';
  const isAlarmRinging = (clockTime === '05:00' || clockTime === '05:07');

  // Deep Obsidian / Midnight Black Atmosphere
  layer(g, cam, 0.15, (g) => {
    backdrop(g, ['#08090e', '#0e111a', '#141824']);
    // Cold moon in window
    FX.moon(g, CX + V(380, 240), GY - V(520, 920), 40, '#e2e8f0');
    FX.stars(g, t, { count: 40, area: [-E.W, 0, E.W * 3, GY - 200] });
  });

  layer(g, cam, 0.5, (g) => {
    const top = GY - V(620, 940), left = CX - 1600, w = 3200;
    // Dark room back wall
    g.fillStyle = linGrad(g, 0, top, 0, GY, ['#10131d', '#0a0c13', '#06070a']);
    g.fillRect(left, top, w, GY - top + 4);

    // Bedroom window on left with cool blue moonlight beam
    const wx = CX - V(480, 360), wy = GY - V(540, 820), ww = V(420, 340), wh = V(320, 360);
    FX.windowFrame(g, { x: wx, y: wy, w: ww, h: wh, cols: 2, rows: 2, frame: '#06070b', bar: 8 }, (g, x, y, w, h) => {
      g.fillStyle = linGrad(g, 0, y, 0, y + h, ['#0a0f1d', '#18243c']);
      g.fillRect(x, y, w, h);
      FX.moon(g, x + w * 0.7, y + h * 0.35, 30, '#ffffff');
    });

    // Nightstand beside bed
    const nx = CX + V(260, 200), ny = GY;
    rr(g, nx - 50, ny - 150, 100, 150, 6);
    g.fillStyle = '#0f1118';
    g.fill();

    // Red LED Digital Alarm Clock
    const clkW = 70, clkH = 36;
    const clkX = nx - clkW / 2, clkY = ny - 190;
    rr(g, clkX, clkY, clkW, clkH, 5);
    g.fillStyle = '#050608';
    g.fill();
    g.strokeStyle = '#1a1d26';
    g.lineWidth = 2;
    g.stroke();

    // Glowing Red 7-segment digital time
    const alarmPulse = isAlarmRinging ? (1.0 + Math.sin(t * 14) * 0.15) : 1.0;
    glow(g, nx, clkY + clkH / 2, 45 * alarmPulse, '#ff2222', 0.85);
    text(g, clockTime, nx, clkY + clkH / 2 + 6, {
      size: 20 * alarmPulse,
      color: '#ff2222',
      font: FONTS.ui,
      weight: 900,
      align: 'center'
    });

    // Ringing shock vibration brackets (( 05:00 ))
    if (isAlarmRinging) {
      g.strokeStyle = 'rgba(255, 34, 34, 0.6)';
      g.lineWidth = 2.5;
      const shk = Math.sin(t * 24) * 3;
      // Left bracket
      g.beginPath();
      g.arc(clkX - 10 + shk, clkY + clkH / 2, 18, Math.PI * 0.65, Math.PI * 1.35);
      g.stroke();
      // Right bracket
      g.beginPath();
      g.arc(clkX + clkW + 10 - shk, clkY + clkH / 2, 18, -Math.PI * 0.35, Math.PI * 0.35);
      g.stroke();
    }
  });

  layer(g, cam, 0.85, (g) => {
    // Dark bedroom floor
    g.fillStyle = linGrad(g, 0, GY, 0, GY + 450, ['#0d0e14', '#06070a']);
    g.fillRect(-E.W, GY, E.W * 3, E.H * 2);
    FX.floorLines(g, GY, GY + 500, 'rgba(0,0,0,.45)', 0.08);

    // Bed frame
    const bx = CX - V(380, 280);
    rr(g, bx - 80, GY - 70, 240, 70, 6);
    g.fillStyle = '#141824';
    g.fill();

    // Red LED light reflection on floor
    FX.pool(g, CX + V(260, 200), GY + 15, 120, 24, '#ff2222', 0.22);
  });

  FX.dust(g, t, { count: 25, color: '#8899b8', a: 0.2 });
  return { GY, CX };
}

// -------------------------------------------------------------
// 2. DAY ONE RUNNING STREET (Night Asphalt + Streetlights + Moon)
// -------------------------------------------------------------
export function dayoneRunningStreet(g, t, cam, o = {}) {
  const GY = standardGround(), CX = E.W / 2;

  layer(g, cam, 0.12, (g) => {
    backdrop(g, ['#070912', '#0e1220', '#181e32']);
    // Slanted crescent moon
    FX.moon(g, CX + V(440, 260), GY - V(520, 940), 42, '#f8fafc');
    // Distant city silhouette
    FX.skyline(g, { x: -E.W, y: GY - V(320, 580), w: E.W * 3, minH: 70, maxH: V(220, 360), color: '#090b12', lit: 0.12, seed: 7 });
  });

  layer(g, cam, 0.55, (g) => {
    // Overhead streetlamps casting warm amber cones of light
    const lampPositions = [CX - V(380, 260), CX + V(320, 220)];
    for (const lx of lampPositions) {
      // Tall dark lamp pole
      rr(g, lx - 4, GY - 360, 8, 360, 3);
      g.fillStyle = '#0d0f17';
      g.fill();
      // Lamp head
      poly(g, [[lx - 32, GY - 360], [lx + 32, GY - 360], [lx + 16, GY - 380], [lx - 16, GY - 380]], '#161a26');
      // Glowing warm bulb
      circle(g, lx, GY - 355, 12, '#ffdd88');
      glow(g, lx, GY - 355, 60, '#ffbb44', 0.65);
      // Light cone casting downward
      FX.lightCone(g, lx, GY - 350, { angle: Math.PI / 2, spread: 0.85, len: 360, color: '#ffe4a0', a: 0.18 });
    }
  });

  layer(g, cam, 0.9, (g) => {
    // Dark asphalt roadway
    g.fillStyle = linGrad(g, 0, GY, 0, GY + 500, ['#131620', '#0a0c12']);
    g.fillRect(-E.W, GY, E.W * 3, E.H * 2);
    FX.floorLines(g, GY, GY + 500, 'rgba(0,0,0,.4)', 0.08);

    // Dashed road centerlines (running perspective)
    g.save();
    g.strokeStyle = 'rgba(255, 255, 255, 0.45)';
    g.lineWidth = 6;
    g.setLineDash([40, 35]);
    seg(g, [[-E.W, GY + 140], [E.W * 2, GY + 140]], 6, 'rgba(255, 255, 255, 0.45)');
    g.restore();

    // Amber streetlamp pools on asphalt
    FX.pool(g, CX - V(380, 260), GY + 30, 280, 48, '#ffcc66', 0.32);
    FX.pool(g, CX + V(320, 220), GY + 30, 280, 48, '#ffcc66', 0.32);
  });

  FX.dust(g, t, { count: 30, color: '#ffdca8', a: 0.25 });
  return { GY, CX };
}

// -------------------------------------------------------------
// 3. DAY ONE GYM (Moody Warehouse + Dumbbell Rack + 'NO EXCUSES')
// -------------------------------------------------------------
export function dayoneGym(g, t, cam, o = {}) {
  const GY = standardGround(), CX = E.W / 2;

  layer(g, cam, 0.15, (g) => {
    backdrop(g, ['#0a0c13', '#111420', '#171c2b']);
  });

  layer(g, cam, 0.5, (g) => {
    const top = GY - V(640, 960), left = CX - 1600, w = 3200;
    // Industrial dark concrete gym wall
    g.fillStyle = linGrad(g, 0, top, 0, GY, ['#141724', '#0c0e17']);
    g.fillRect(left, top, w, GY - top + 4);

    // Bold Motivational Wall Poster ("NO EXCUSES")
    const pw = 420, ph = 140;
    const px = CX - pw / 2, py = GY - V(460, 720);
    rr(g, px, py, pw, ph, 10);
    g.fillStyle = '#080a10';
    g.fill();
    g.strokeStyle = '#222838';
    g.lineWidth = 3;
    g.stroke();

    text(g, 'NO EXCUSES', CX, py + 65, {
      size: 42,
      color: '#ffffff',
      font: FONTS.ui,
      weight: 900,
      align: 'center'
    });
    text(g, 'EVERY SINGLE DAY · ZERO COMPROMISE', CX, py + 105, {
      size: 14,
      color: '#ef4444',
      font: FONTS.ui,
      weight: 800,
      align: 'center'
    });

    // Heavy Cast Iron Dumbbell Rack on left
    const rx = CX - V(480, 360), ry = GY;
    // Rack stand
    seg(g, [[rx - 90, ry - 180], [rx + 90, ry - 180]], 12, '#1e2433');
    seg(g, [[rx - 70, ry - 180], [rx - 85, ry]], 10, '#121620');
    seg(g, [[rx + 70, ry - 180], [rx + 85, ry]], 10, '#121620');
    // Dumbbells lined up on rack
    for (let d = -2; d <= 2; d++) {
      const dx = rx + d * 32;
      const dy = ry - 180;
      g.fillStyle = '#475569';
      g.fillRect(dx - 10, dy - 2, 20, 5);
      rr(g, dx - 13, dy - 12, 6, 25, 2); g.fillStyle = '#0f172a'; g.fill();
      rr(g, dx + 7, dy - 12, 6, 25, 2); g.fill();
    }
  });

  layer(g, cam, 0.85, (g) => {
    // Rubberized gym flooring
    g.fillStyle = linGrad(g, 0, GY, 0, GY + 450, ['#10131d', '#08090f']);
    g.fillRect(-E.W, GY, E.W * 3, E.H * 2);
    FX.floorLines(g, GY, GY + 500, 'rgba(0,0,0,.5)', 0.08);

    // Overhead industrial spotlight pool
    FX.pool(g, CX, GY + 25, 360, 55, '#f8fafc', 0.22);
  });

  FX.dust(g, t, { count: 35, color: '#e2e8f0', a: 0.2 });
  return { GY, CX };
}

// -------------------------------------------------------------
// 4. DAY ONE STUDY DESK (Desk Lamp + Books + Schedule Board)
// -------------------------------------------------------------
export function dayoneStudyDesk(g, t, cam, o = {}) {
  const GY = standardGround(), CX = E.W / 2;

  layer(g, cam, 0.15, (g) => {
    backdrop(g, ['#090a10', '#10131c', '#181b28']);
  });

  layer(g, cam, 0.5, (g) => {
    const top = GY - V(620, 940), left = CX - 1600, w = 3200;
    // Dark room wall
    g.fillStyle = linGrad(g, 0, top, 0, GY, ['#131622', '#0a0c12']);
    g.fillRect(left, top, w, GY - top + 4);

    // Wall Whiteboard with Daily Schedule ("5:00 RUN", "6:30 GYM", "20:00 STUDY")
    const bw = 380, bh = 240;
    const bx = CX + V(220, 160), by = GY - V(520, 780);
    rr(g, bx - 6, by - 6, bw + 12, bh + 12, 6);
    g.fillStyle = '#1e2433';
    g.fill();
    rr(g, bx, by, bw, bh, 4);
    g.fillStyle = '#f8fafc'; // Whiteboard face
    g.fill();

    text(g, 'DAILY DISCIPLINE', bx + bw / 2, by + 38, { size: 18, color: '#0f172a', font: FONTS.ui, weight: 900, align: 'center' });
    seg(g, [[bx + 30, by + 52], [bx + bw - 30, by + 52]], 2, '#cbd5e1');

    text(g, '• 05:00 — 5KM RUN', bx + 35, by + 90, { size: 17, color: '#ef4444', font: FONTS.ui, weight: 800, align: 'left' });
    text(g, '• 06:30 — HEAVY GYM', bx + 35, by + 135, { size: 17, color: '#1e293b', font: FONTS.ui, weight: 800, align: 'left' });
    text(g, '• 20:00 — DEEP STUDY', bx + 35, by + 180, { size: 17, color: '#1e293b', font: FONTS.ui, weight: 800, align: 'left' });

    // Minimalist Angled Desk Lamp casting warm conical light
    const lx = CX - V(260, 200), ly = GY - 280;
    // Lamp base
    rr(g, lx - 20, GY - 80, 40, 10, 4); g.fillStyle = '#0f172a'; g.fill();
    // Angled stem
    seg(g, [[lx, GY - 80], [lx + 25, GY - 180], [lx + 50, ly]], 5, '#1e293b');
    // Lamp shade
    poly(g, [[lx + 30, ly], [lx + 70, ly], [lx + 85, ly + 25], [lx + 15, ly + 25]], '#ffedd5');
    glow(g, lx + 50, ly + 25, 45, '#fbbf24', 0.6);
    // Light cone shining on desk
    FX.lightCone(g, lx + 50, ly + 25, { angle: Math.PI / 2 + 0.15, spread: 0.8, len: 260, color: '#fef08a', a: 0.28 });
  });

  layer(g, cam, 0.85, (g) => {
    // Dark wooden floor
    g.fillStyle = linGrad(g, 0, GY, 0, GY + 450, ['#0d0e14', '#06070a']);
    g.fillRect(-E.W, GY, E.W * 3, E.H * 2);

    // Warm lamp pool on desk
    FX.pool(g, CX - V(200, 150), GY + 15, 240, 40, '#fef08a', 0.35);
  });

  FX.dust(g, t, { count: 30, color: '#fef08a', a: 0.25 });
  return { GY, CX };
}

// -------------------------------------------------------------
// 5. DAY ONE SUNRISE (Day 62 Breakthrough Dawn)
// -------------------------------------------------------------
export function dayoneSunrise(g, t, cam, o = {}) {
  const GY = standardGround(), CX = E.W / 2;

  layer(g, cam, 0.12, (g) => {
    // 3-Tone Dawn Horizon: Deep Cobalt Blue -> Dusty Rose -> Radiant Apricot Gold
    backdrop(g, ['#131a38', '#40294b', '#a24857', '#e88958', '#fed7aa']);

    // Rising Golden Sun Disc on Horizon
    const sunY = GY - V(260, 420);
    glow(g, CX, sunY, 140, '#ffedd5', 0.95);
    glow(g, CX, sunY, 260, '#fbbf24', 0.6);
    circle(g, CX, sunY, 70, '#fffbeb');

    // Soft morning god rays
    FX.godRays(g, CX, sunY, { count: 8, len: 1400, color: '#fde68a', a: 0.18, t });
  });

  layer(g, cam, 0.55, (g) => {
    // Quiet distant road horizon
    FX.fog(g, GY - 70, 80, '#fde68a', 0.2);
  });

  layer(g, cam, 0.9, (g) => {
    // Warm morning road
    g.fillStyle = linGrad(g, 0, GY, 0, GY + 500, ['#27212b', '#130f17']);
    g.fillRect(-E.W, GY, E.W * 3, E.H * 2);
    FX.floorLines(g, GY, GY + 500, 'rgba(0,0,0,.35)', 0.08);

    // Warm sunrise pool along the road
    FX.pool(g, CX, GY + 25, 480, 60, '#fed7aa', 0.35);
  });

  FX.dust(g, t, { count: 45, color: '#fed7aa', a: 0.4 });
  return { GY, CX };
}
