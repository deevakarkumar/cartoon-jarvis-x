// scenes/sets/style2a_sets.js — Style 2A (Modern Studio Tech) for aiTrends & Stickman Video Director
// Inspired by kaomei/stickman-video-director Style 2A:
// "A modern bright white studio space with subtle light-gray perspective grid lines on the floor plane.
// High-key studio lighting, clean white negative space, sleek glowing cyan and electric blue glass holographic UI elements."

import { E, V, mood, layer, backdrop, rr, seg, circle, ring, poly, linGrad, radGrad, glow, alpha, shade, mix, text, FONTS } from '/engine/core.js';
import * as FX from '/engine/fx2d.js';

export const standardGround = () => E.H * V(0.82, 0.68);

// -------------------------------------------------------------
// 1. STYLE 2A STUDIO TECH SET (Floor Grid + High-Key Horizon)
// -------------------------------------------------------------
export function studioTech(g, t, cam, o = {}) {
  const GY = standardGround(), CX = E.W / 2;
  const gridAlpha = o.gridAlpha ?? 0.35;
  const theme = o.theme || 'light'; // 'light' or 'dark_studio'

  if (theme === 'light') {
    // High-Key Modern White Minimalist Studio
    layer(g, cam, 0.1, (g) => {
      // Soft high-key studio wall
      g.fillStyle = linGrad(g, 0, 0, 0, GY, ['#ffffff', '#f8fafc', '#edf2f7']);
      g.fillRect(-E.W, -E.H, E.W * 3, GY + E.H);

      // Subtle cyan studio ambient rim
      glow(g, CX, GY * 0.3, 400, '#06b6d4', 0.08);
      glow(g, CX + V(400, 200), GY * 0.5, 300, '#3b82f6', 0.06);
    });

    layer(g, cam, 0.4, (g) => {
      // Horizon gradient blend
      g.fillStyle = linGrad(g, 0, GY - 10, 0, GY + 10, ['rgba(237,242,247,0)', 'rgba(203,213,225,0.7)']);
      g.fillRect(-E.W, GY - 10, E.W * 3, 20);

      // Floor plane
      g.fillStyle = linGrad(g, 0, GY, 0, E.H, ['#f1f5f9', '#e2e8f0', '#cbd5e1']);
      g.fillRect(-E.W, GY, E.W * 3, E.H * 2);

      // PERSPECTIVE GRID: Horizontal Depth Lines (exponential spacing)
      g.strokeStyle = `rgba(148, 163, 184, ${gridAlpha * 0.9})`;
      g.lineWidth = 1.5;
      const hLines = [GY + 15, GY + 45, GY + 90, GY + 155, GY + 245, GY + 365, GY + 520, GY + 720];
      for (const y of hLines) {
        if (y < E.H + 200) {
          g.beginPath();
          g.moveTo(-E.W, y);
          g.lineTo(E.W * 2, y);
          g.stroke();
        }
      }

      // PERSPECTIVE GRID: Longitudinal Vanishing Lines (radiating from CX, GY - 150)
      const VP_Y = GY - 120;
      const VP_X = CX;
      g.strokeStyle = `rgba(148, 163, 184, ${gridAlpha * 0.65})`;
      g.lineWidth = 1.2;
      const cols = [-1600, -1200, -850, -550, -300, -120, 0, 120, 300, 550, 850, 1200, 1600];
      for (const offset of cols) {
        g.beginPath();
        g.moveTo(VP_X + offset * 0.05, GY);
        g.lineTo(VP_X + offset * 2.8, E.H + 400);
        g.stroke();
      }

      // Soft character shadow pool on floor
      glow(g, CX, GY + 15, 140, '#64748b', 0.25);
    });
  } else {
    // Dark Modern Tech Studio (Cyber Obsidian)
    layer(g, cam, 0.1, (g) => {
      g.fillStyle = linGrad(g, 0, 0, 0, GY, ['#090d16', '#0f172a', '#1e293b']);
      g.fillRect(-E.W, -E.H, E.W * 3, GY + E.H);
      glow(g, CX, GY * 0.3, 500, '#06b6d4', 0.14);
    });

    layer(g, cam, 0.4, (g) => {
      g.fillStyle = linGrad(g, 0, GY, 0, E.H, ['#0b0f19', '#05070b']);
      g.fillRect(-E.W, GY, E.W * 3, E.H * 2);

      // Neon Cyan Floor Grid
      g.strokeStyle = `rgba(6, 182, 212, ${gridAlpha * 0.45})`;
      g.lineWidth = 1.5;
      const hLines = [GY + 15, GY + 45, GY + 90, GY + 155, GY + 245, GY + 365, GY + 520, GY + 720];
      for (const y of hLines) {
        g.beginPath();
        g.moveTo(-E.W, y);
        g.lineTo(E.W * 2, y);
        g.stroke();
      }
      const VP_X = CX;
      for (const offset of [-1200, -700, -350, 0, 350, 700, 1200]) {
        g.beginPath();
        g.moveTo(VP_X + offset * 0.05, GY);
        g.lineTo(VP_X + offset * 2.5, E.H + 400);
        g.stroke();
      }
    });
  }
}

// -------------------------------------------------------------
// 2. HOLOGRAPHIC UI COMPONENT SUITE (Cyan & Electric Blue Glass)
// -------------------------------------------------------------

// Sleek Glass Card with Tech Bracket Corners
export function holoGlassCard(g, x, y, w, h, opts = {}) {
  const t = opts.t || 0;
  const title = opts.title || '';
  const subtitle = opts.subtitle || '';
  const borderColor = opts.color || '#06b6d4'; // Cyan default
  const fillAlpha = opts.fillAlpha ?? 0.88;
  const floatOff = Math.sin((t + (opts.phase || 0)) * 2) * 5;
  const cy = y + floatOff;

  g.save();
  // Ambient back glow
  glow(g, x + w / 2, cy + h / 2, Math.max(w, h) * 0.7, borderColor, 0.18);

  // Frosted dark glass container
  rr(g, x, cy, w, h, 10);
  g.fillStyle = `rgba(15, 23, 42, ${fillAlpha})`;
  g.fill();

  // Glass border with gradient highlight
  g.strokeStyle = borderColor;
  g.lineWidth = 2;
  g.stroke();

  // Tech Corner Accents
  const cSize = 12;
  g.strokeStyle = '#ffffff';
  g.lineWidth = 2.5;
  // Top-left
  g.beginPath(); g.moveTo(x - 2, cy + cSize); g.lineTo(x - 2, cy - 2); g.lineTo(x + cSize, cy - 2); g.stroke();
  // Top-right
  g.beginPath(); g.moveTo(x + w + 2 - cSize, cy - 2); g.lineTo(x + w + 2, cy - 2); g.lineTo(x + w + 2, cy + cSize); g.stroke();
  // Bottom-left
  g.beginPath(); g.moveTo(x - 2, cy + h - cSize); g.lineTo(x - 2, cy + h + 2); g.lineTo(x + cSize, cy + h + 2); g.stroke();
  // Bottom-right
  g.beginPath(); g.moveTo(x + w + 2 - cSize, cy + h + 2); g.lineTo(x + w + 2, cy + h + 2); g.lineTo(x + w + 2, cy + h + 2 - cSize); g.stroke();

  // Header Title
  if (title) {
    // Mini pulsing status dot
    circle(g, x + 20, cy + 24, 4, borderColor);
    glow(g, x + 20, cy + 24, 12, borderColor, 0.8);

    text(g, title.toUpperCase(), x + 34, cy + 28, {
      size: 13,
      color: '#f8fafc',
      font: FONTS.ui,
      weight: 800
    });

    // Divider line
    g.strokeStyle = 'rgba(6, 182, 212, 0.35)';
    g.lineWidth = 1;
    g.beginPath();
    g.moveTo(x + 16, cy + 42);
    g.lineTo(x + w - 16, cy + 42);
    g.stroke();
  }

  if (subtitle) {
    text(g, subtitle, x + 20, cy + 68, {
      size: 14,
      color: '#94a3b8',
      font: FONTS.ui,
      weight: 500
    });
  }

  g.restore();
  return { x, y: cy, w, h };
}

// Dynamic Animated Bar Chart
export function holoBarChart(g, x, y, w, h, bars = [], opts = {}) {
  const card = holoGlassCard(g, x, y, w, h, opts);
  const startY = card.y + 60;
  const chartH = h - 85;
  const chartW = w - 40;
  const barCount = bars.length;
  if (!barCount) return;

  const barW = Math.min(50, (chartW / barCount) * 0.6);
  const gap = chartW / barCount;
  const progress = opts.progress ?? 1.0;

  bars.forEach((b, i) => {
    const bx = card.x + 20 + i * gap + (gap - barW) / 2;
    const maxBarH = chartH - 30;
    const barHeight = maxBarH * (b.value / 100) * progress;
    const by = startY + chartH - barHeight;

    // Glowing Neon Bar
    const barColor = b.color || '#06b6d4';
    rr(g, bx, by, barW, barHeight, 4);
    g.fillStyle = linGrad(g, 0, by, 0, by + barHeight, [barColor, '#1e3a8a']);
    g.fill();
    g.strokeStyle = barColor;
    g.lineWidth = 1.5;
    g.stroke();

    // Top cap glow
    glow(g, bx + barW / 2, by, 16, barColor, 0.7);

    // Percentage Label
    text(g, `${Math.round(b.value * progress)}%`, bx + barW / 2, by - 8, {
      size: 12,
      color: '#ffffff',
      font: FONTS.ui,
      weight: 800,
      align: 'center'
    });

    // Bottom Category Label
    text(g, b.label || '', bx + barW / 2, startY + chartH + 16, {
      size: 11,
      color: '#94a3b8',
      font: FONTS.ui,
      weight: 600,
      align: 'center'
    });
  });
}

// Circular Neon Gauge (0-100% Spin HUD)
export function holoCircularGauge(g, cx, cy, radius, value, opts = {}) {
  const t = opts.t || 0;
  const maxVal = opts.maxVal || 100;
  const label = opts.label || '';
  const unit = opts.unit || '%';
  const color = opts.color || '#06b6d4';
  const floatOff = Math.sin(t * 2) * 4;
  const y = cy + floatOff;

  g.save();
  // Glass back disc
  circle(g, cx, y, radius + 15, 'rgba(15, 23, 42, 0.75)');
  glow(g, cx, y, radius * 1.5, color, 0.25);

  // Background track
  ring(g, cx, y, radius, 8, 'rgba(30, 41, 59, 0.85)');

  // Foreground Arc
  const pct = Math.min(1.0, Math.max(0, value / maxVal));
  const startAngle = -Math.PI / 2;
  const endAngle = startAngle + pct * Math.PI * 2;

  g.strokeStyle = color;
  g.lineWidth = 8;
  g.lineCap = 'round';
  g.beginPath();
  g.arc(cx, y, radius, startAngle, endAngle);
  g.stroke();

  // Glow on the leading needle tip
  const tipX = cx + Math.cos(endAngle) * radius;
  const tipY = y + Math.sin(endAngle) * radius;
  glow(g, tipX, tipY, 20, '#ffffff', 0.9);
  circle(g, tipX, tipY, 5, '#ffffff');

  // Center Value Readout
  text(g, `${Math.round(value)}${unit}`, cx, y + 8, {
    size: radius * 0.45,
    color: '#ffffff',
    font: FONTS.ui,
    weight: 900,
    align: 'center'
  });

  if (label) {
    text(g, label.toUpperCase(), cx, y + radius + 32, {
      size: 12,
      color: '#38bdf8',
      font: FONTS.ui,
      weight: 700,
      align: 'center'
    });
  }

  g.restore();
}

// Split Screen Comparison: 99% Amateur Trap vs 1% Top Discipline Formula
export function holoComparisonSplit(g, x, y, w, h, leftData, rightData, opts = {}) {
  const t = opts.t || 0;
  const floatOff = Math.sin(t * 1.8) * 4;
  const cy = y + floatOff;
  const halfW = (w - 20) / 2;

  // Left Card: The Amateur Trap (Red/Amber)
  holoGlassCard(g, x, cy, halfW, h, {
    title: leftData.title || '99% AMATEUR TRAP',
    color: '#ef4444',
    fillAlpha: 0.82,
    t
  });
  // Red Warning Icon
  circle(g, x + 35, cy + 70, 14, 'rgba(239, 68, 68, 0.2)');
  text(g, '✕', x + 35, cy + 76, { size: 16, color: '#ef4444', font: FONTS.ui, weight: 900, align: 'center' });
  (leftData.points || []).forEach((pt, i) => {
    text(g, `• ${pt}`, x + 60, cy + 74 + i * 28, {
      size: 14,
      color: '#fca5a5',
      font: FONTS.ui,
      weight: 600
    });
  });

  // Right Card: The Master Protocol (Cyan/Emerald)
  holoGlassCard(g, x + halfW + 20, cy, halfW, h, {
    title: rightData.title || '1% DISCIPLINE FORMULA',
    color: '#10b981',
    fillAlpha: 0.82,
    t: t + 0.5
  });
  // Green Check Icon
  circle(g, x + halfW + 55, cy + 70, 14, 'rgba(16, 185, 129, 0.2)');
  text(g, '✓', x + halfW + 55, cy + 76, { size: 16, color: '#10b981', font: FONTS.ui, weight: 900, align: 'center' });
  (rightData.points || []).forEach((pt, i) => {
    text(g, `• ${pt}`, x + halfW + 80, cy + 74 + i * 28, {
      size: 14,
      color: '#6ee7b7',
      font: FONTS.ui,
      weight: 600
    });
  });
}

// Stage Tag Badge (Golden Hook, Disrupt Assumptions, etc.)
export function holoStageBadge(g, x, y, stageNumber, stageTitle, opts = {}) {
  const color = opts.color || '#06b6d4';
  const w = opts.w || 280;
  const h = 38;

  rr(g, x, y, w, h, 6);
  g.fillStyle = 'rgba(15, 23, 42, 0.9)';
  g.fill();
  g.strokeStyle = color;
  g.lineWidth = 1.5;
  g.stroke();

  // Badge pill
  rr(g, x + 6, y + 6, 68, h - 12, 4);
  g.fillStyle = color;
  g.fill();
  text(g, `STAGE ${stageNumber}`, x + 40, y + 23, {
    size: 11,
    color: '#04101d',
    font: FONTS.ui,
    weight: 900,
    align: 'center'
  });

  // Stage name
  text(g, stageTitle.toUpperCase(), x + 84, y + 24, {
    size: 13,
    color: '#ffffff',
    font: FONTS.ui,
    weight: 800
  });

  glow(g, x + 40, y + h / 2, 25, color, 0.5);
}
