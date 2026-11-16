// engine/dayone_rig.js — Dedicated Rig & Entities for Day One Films Style
// Implements:
// 1. Bean / Capsule Humanoid Rig with soft ambient shading and emotional states
// 2. The Metaphorical Shadow Demon (Inner doubt / resistance whisperer)
// 3. Dragging Fatigue Body (Symbolic bodily exhaustion)
// 4. Dynamic Parametric Motivation Meter HUD (100% -> 16% -> 0% -> 47%)
// 5. Minimalist Timeline Banners (DAY 1, DAY 3, DAY 8, DAY 10, DAY 11, DAY 62)
// 6. Master Thesis Infographic Graph (Motivation Spikes vs Discipline Compound)
// 7. In-Scene Environmental Hand-Lettered Typography

import { E, V, clamp, lerp, seg, circle, ring, rr, poly, glow, alpha, shade, mix, text, FONTS, ease } from './core.js';

// Base Colors for Day One Films Rig
export const D1_COLORS = {
  skin: '#f5efe6',         // Warm ivory cream base
  skinShadow: 'rgba(92, 85, 75, 0.28)', // Soft ambient occlusion shading
  ink: '#111217',          // Crisp charcoal black outline
  auraGold: '#ffb800',     // Motivation aura peak
  auraOrange: '#ff8c00',   // Falloff aura
  demonBlack: '#0a0910',   // Shadow Demon core
  demonRed: '#ff2222',     // Demon glowing eyes / whisper accent
  fatigueBrown: '#8c7365', // Exhausted dragging body
  meterBg: 'rgba(15, 17, 23, 0.85)',
  meterBorder: 'rgba(255, 255, 255, 0.15)',
};

// -------------------------------------------------------------
// 1. BEAN / CAPSULE CHARACTER RIG
// -------------------------------------------------------------
export function drawBeanCharacter(g, o = {}) {
  const {
    x = 960,
    y = 800,
    s = 1.0,
    facing = 1,
    pose = 'stand',
    expr = 'motivated', // 'motivated', 'exhausted', 'disciplined', 'shocked', 'neutral'
    aura = false,
    t = 0,
    outfit = 'athletic', // 'athletic', 'hoodie', 'bed', 'shirt'
    darkBags = false,
  } = o;

  g.save();
  g.translate(x, y);
  g.scale(facing * s, s);

  // 1A. MOTIVATION AURA (When Motivation is active > 0)
  if (aura) {
    drawMotivationAura(g, t, aura === true ? 1.0 : aura);
  }

  // 1B. GROUND SHADOW (if not lying in bed)
  if (pose !== 'bed_lying') {
    g.fillStyle = 'rgba(0, 0, 0, 0.35)';
    g.beginPath();
    g.ellipse(0, 4, 46 * s, 10 * s, 0, 0, Math.PI * 2);
    g.fill();
  }

  // 1C. BODY BY POSE
  switch (pose) {
    case 'run_motivated':
    case 'run_disciplined':
      drawRunningBean(g, t, pose, expr, darkBags, outfit);
      break;
    case 'bed_lying':
      drawBedLyingBean(g, t, expr, darkBags);
      break;
    case 'bed_wakeup_fire':
    case 'bed_wakeup_disciplined':
      drawBedWakeupBean(g, t, pose, expr, darkBags);
      break;
    case 'curl_dumbbell':
      drawGymCurlBean(g, t, expr, darkBags);
      break;
    case 'desk_slump':
      drawDeskSlumpBean(g, t, expr, darkBags);
      break;
    case 'drag_body':
      drawDragBodyBean(g, t, expr, darkBags);
      break;
    case 'point':
    case 'pointing':
    case 'explaining':
      drawPointingBean(g, t, expr, darkBags, outfit);
      break;
    case 'think':
    case 'thinking':
      drawThinkingBean(g, t, expr, darkBags, outfit);
      break;
    case 'cheer':
    case 'celebrating':
      drawCheerBean(g, t, expr, darkBags, outfit);
      break;
    case 'stand':
    default:
      drawStandingBean(g, t, expr, darkBags, outfit);
      break;
  }

  g.restore();
}

// -------------------------------------------------------------
// AURA GENERATOR
// -------------------------------------------------------------
function drawMotivationAura(g, t, intensity = 1.0) {
  g.save();
  const pulse = 1.0 + Math.sin(t * 8) * 0.08 * intensity;
  
  // Radial golden bloom
  glow(g, 0, -110, 110 * pulse, D1_COLORS.auraGold, 0.55 * intensity);
  glow(g, 0, -110, 170 * pulse, D1_COLORS.auraOrange, 0.35 * intensity);

  // Floating sparks / energy particles
  const sparkCount = Math.floor(12 * intensity);
  for (let i = 0; i < sparkCount; i++) {
    const seed = i * 47.3;
    const prog = ((t * 2.2 + seed * 0.1) % 1.0);
    const px = Math.sin(seed + t * 3) * 65 * pulse;
    const py = -40 - prog * 170;
    const pr = (1.0 - prog) * 4.5;
    g.fillStyle = i % 2 === 0 ? '#fff3c4' : D1_COLORS.auraGold;
    g.beginPath();
    g.arc(px, py, Math.max(1, pr), 0, Math.PI * 2);
    g.fill();
  }

  // Speed lines radiating outward
  g.strokeStyle = 'rgba(255, 255, 255, 0.45)';
  g.lineWidth = 2.5;
  for (let j = 0; j < 6; j++) {
    const ang = -Math.PI / 2 + (j - 2.5) * 0.35 + Math.sin(t * 12 + j) * 0.1;
    const r1 = 80 + (j % 3) * 15;
    const r2 = r1 + 35 * pulse;
    g.beginPath();
    g.moveTo(Math.cos(ang) * r1, -110 + Math.sin(ang) * r1);
    g.lineTo(Math.cos(ang) * r2, -110 + Math.sin(ang) * r2);
    g.stroke();
  }

  g.restore();
}

// -------------------------------------------------------------
// HEAD & FACE DRAWING
// -------------------------------------------------------------
function drawBeanHead(g, hx, hy, r, expr = 'motivated', darkBags = false) {
  g.save();
  g.lineCap = 'round';
  g.lineJoin = 'round';

  // Head Base Fill & Outline (Smooth cranium / egg)
  g.fillStyle = D1_COLORS.skin;
  g.beginPath();
  g.ellipse(hx, hy, r, r * 1.15, 0, 0, Math.PI * 2);
  g.fill();

  // Ambient shading under jawline / bottom of head
  const grad = g.createRadialGradient(hx, hy - r * 0.2, r * 0.3, hx, hy + r * 0.4, r * 1.1);
  grad.addColorStop(0, 'rgba(0,0,0,0)');
  grad.addColorStop(0.7, 'rgba(0,0,0,0)');
  grad.addColorStop(1, D1_COLORS.skinShadow);
  g.fillStyle = grad;
  g.beginPath();
  g.ellipse(hx, hy, r, r * 1.15, 0, 0, Math.PI * 2);
  g.fill();

  // Head Outline
  g.strokeStyle = D1_COLORS.ink;
  g.lineWidth = 4.5;
  g.beginPath();
  g.ellipse(hx, hy, r, r * 1.15, 0, 0, Math.PI * 2);
  g.stroke();

  // Eyes & Eyebrows
  const eyeY = hy - r * 0.05;
  const leftEyeX = hx - r * 0.32;
  const rightEyeX = hx + r * 0.32;
  const eyeR = r * 0.18;

  // Dark bags under eyes (burnout / sleep deprivation)
  if (darkBags || expr === 'exhausted') {
    g.strokeStyle = '#524b5c';
    g.lineWidth = 3.0;
    // Under eye crescent 1
    g.beginPath();
    g.arc(leftEyeX, eyeY + eyeR * 0.9, eyeR * 1.1, 0.2, Math.PI - 0.2);
    g.stroke();
    // Under eye crescent 2
    g.beginPath();
    g.arc(rightEyeX, eyeY + eyeR * 0.9, eyeR * 1.1, 0.2, Math.PI - 0.2);
    g.stroke();
  }

  // Draw Eyes by Expression
  if (expr === 'exhausted') {
    // Heavy sagging eyelids, tired slits
    g.fillStyle = D1_COLORS.ink;
    for (const ex of [leftEyeX, rightEyeX]) {
      g.beginPath();
      g.arc(ex, eyeY, eyeR * 0.8, 0.15, Math.PI - 0.15);
      g.stroke();
      circle(g, ex, eyeY + eyeR * 0.2, eyeR * 0.35, D1_COLORS.ink);
    }
    // Flat tired mouth
    seg(g, [[hx - r * 0.22, hy + r * 0.45], [hx + r * 0.22, hy + r * 0.48]], 3.5, D1_COLORS.ink);
    // Drooping tired brows
    seg(g, [[leftEyeX - eyeR, eyeY - eyeR * 1.2], [leftEyeX + eyeR, eyeY - eyeR * 0.8]], 3.5, D1_COLORS.ink);
    seg(g, [[rightEyeX - eyeR, eyeY - eyeR * 0.8], [rightEyeX + eyeR, eyeY - eyeR * 1.2]], 3.5, D1_COLORS.ink);

  } else if (expr === 'disciplined') {
    // Cold resolute hunter eyes (focused horizontal straight brows)
    for (const ex of [leftEyeX, rightEyeX]) {
      circle(g, ex, eyeY, eyeR * 0.75, D1_COLORS.ink);
      // Small catchlight
      circle(g, ex + 2, eyeY - 2, 2.0, '#ffffff');
    }
    // Determined horizontal brows
    seg(g, [[leftEyeX - eyeR * 1.3, eyeY - eyeR * 1.3], [leftEyeX + eyeR * 1.1, eyeY - eyeR * 0.9]], 4.2, D1_COLORS.ink);
    seg(g, [[rightEyeX - eyeR * 1.1, eyeY - eyeR * 0.9], [rightEyeX + eyeR * 1.3, eyeY - eyeR * 1.3]], 4.2, D1_COLORS.ink);
    // Firm straight mouth
    seg(g, [[hx - r * 0.2, hy + r * 0.42], [hx + r * 0.2, hy + r * 0.42]], 3.8, D1_COLORS.ink);

  } else if (expr === 'shocked') {
    // Wide open shocked eyes & open mouth
    for (const ex of [leftEyeX, rightEyeX]) {
      circle(g, ex, eyeY, eyeR * 1.1, D1_COLORS.ink);
      circle(g, ex, eyeY, eyeR * 0.45, '#ffffff');
    }
    // Raised high arched brows
    g.strokeStyle = D1_COLORS.ink;
    g.lineWidth = 3.5;
    g.beginPath(); g.arc(leftEyeX, eyeY - eyeR * 1.4, eyeR * 1.1, Math.PI * 1.2, Math.PI * 1.8); g.stroke();
    g.beginPath(); g.arc(rightEyeX, eyeY - eyeR * 1.4, eyeR * 1.1, Math.PI * 1.2, Math.PI * 1.8); g.stroke();
    // Open 'O' mouth
    ring(g, hx, hy + r * 0.44, eyeR * 0.85, 3.5, D1_COLORS.ink);

  } else {
    // Motivated (Default): Sharp aggressive downward angled brows
    for (const ex of [leftEyeX, rightEyeX]) {
      circle(g, ex, eyeY, eyeR * 0.85, D1_COLORS.ink);
      circle(g, ex + 2.5, eyeY - 2.5, 2.5, '#ffffff');
    }
    // Sharp diagonal brows angled inward (35 deg)
    seg(g, [[leftEyeX - eyeR * 1.3, eyeY - eyeR * 1.5], [leftEyeX + eyeR * 1.1, eyeY - eyeR * 0.6]], 4.5, D1_COLORS.ink);
    seg(g, [[rightEyeX - eyeR * 1.1, eyeY - eyeR * 0.6], [rightEyeX + eyeR * 1.3, eyeY - eyeR * 1.5]], 4.5, D1_COLORS.ink);
    // Determined grim smirk
    seg(g, [[hx - r * 0.18, hy + r * 0.42], [hx + r * 0.22, hy + r * 0.38]], 3.8, D1_COLORS.ink);
  }

  g.restore();
}

// -------------------------------------------------------------
// STANDING BEAN
// -------------------------------------------------------------
function drawStandingBean(g, t, expr, darkBags, outfit) {
  const HR = 30;
  const hy = -190 + Math.sin(t * 2) * 2;
  const sy = -140 + Math.sin(t * 2) * 1.5;

  // Legs
  g.lineWidth = 14;
  g.lineCap = 'round';
  g.strokeStyle = D1_COLORS.ink;
  seg(g, [[-16, -70], [-16, 0]], 14, D1_COLORS.ink);
  seg(g, [[16, -70], [16, 0]], 14, D1_COLORS.ink);
  // Feet
  rr(g, -26, -6, 22, 10, 5); g.fillStyle = D1_COLORS.ink; g.fill();
  rr(g, 6, -6, 22, 10, 5); g.fill();

  // Torso (Smooth capsule bean shape)
  rr(g, -28, sy, 56, 85, 24);
  g.fillStyle = outfit === 'hoodie' ? '#1c1b24' : '#222838';
  g.fill();
  g.strokeStyle = D1_COLORS.ink;
  g.lineWidth = 4;
  g.stroke();

  // Arms (relaxed at sides or on hips)
  seg(g, [[-26, sy + 15], [-38, sy + 50], [-30, sy + 75]], 12, D1_COLORS.ink);
  seg(g, [[26, sy + 15], [38, sy + 50], [30, sy + 75]], 12, D1_COLORS.ink);

  // Head
  drawBeanHead(g, 0, hy, HR, expr, darkBags);
}

// -------------------------------------------------------------
// POINTING / EXPLAINING BEAN (For Studio Tech & Data Presentation)
// -------------------------------------------------------------
function drawPointingBean(g, t, expr, darkBags, outfit) {
  const HR = 30;
  const hy = -190 + Math.sin(t * 2) * 2;
  const sy = -140 + Math.sin(t * 2) * 1.5;

  // Legs & Feet
  seg(g, [[-16, -70], [-16, 0]], 14, D1_COLORS.ink);
  seg(g, [[16, -70], [16, 0]], 14, D1_COLORS.ink);
  rr(g, -26, -6, 22, 10, 5); g.fillStyle = D1_COLORS.ink; g.fill();
  rr(g, 6, -6, 22, 10, 5); g.fill();

  // Torso
  rr(g, -28, sy, 56, 85, 24);
  g.fillStyle = outfit === 'hoodie' ? '#1c1b24' : '#222838';
  g.fill();
  g.strokeStyle = D1_COLORS.ink;
  g.lineWidth = 4;
  g.stroke();

  // Left Arm (on hip)
  seg(g, [[-26, sy + 15], [-44, sy + 42], [-28, sy + 62]], 12, D1_COLORS.ink);

  // Right Arm (pointing forward-up at holographic screen)
  const pointPulse = Math.sin(t * 4) * 4;
  seg(g, [[26, sy + 15], [52, sy + 5], [92 + pointPulse, sy - 25]], 12, D1_COLORS.ink);
  circle(g, 92 + pointPulse, sy - 25, 6, D1_COLORS.ink);
  // Laser fingertip accent
  glow(g, 94 + pointPulse, sy - 25, 14, '#06b6d4', 0.85);

  // Head
  drawBeanHead(g, 0, hy, HR, expr, darkBags);
}

// -------------------------------------------------------------
// THINKING BEAN (Reflecting on Science / Dilemma)
// -------------------------------------------------------------
function drawThinkingBean(g, t, expr, darkBags, outfit) {
  const HR = 30;
  const hy = -190 + Math.sin(t * 2) * 2;
  const sy = -140 + Math.sin(t * 2) * 1.5;

  // Legs & Feet
  seg(g, [[-16, -70], [-16, 0]], 14, D1_COLORS.ink);
  seg(g, [[16, -70], [16, 0]], 14, D1_COLORS.ink);
  rr(g, -26, -6, 22, 10, 5); g.fillStyle = D1_COLORS.ink; g.fill();
  rr(g, 6, -6, 22, 10, 5); g.fill();

  // Torso
  rr(g, -28, sy, 56, 85, 24);
  g.fillStyle = outfit === 'hoodie' ? '#1c1b24' : '#222838';
  g.fill();
  g.strokeStyle = D1_COLORS.ink;
  g.lineWidth = 4;
  g.stroke();

  // Left Arm (folded across chest)
  seg(g, [[-26, sy + 15], [-12, sy + 52], [22, sy + 46]], 12, D1_COLORS.ink);

  // Right Arm (elbow resting on left arm, hand on chin)
  seg(g, [[26, sy + 15], [24, sy + 44], [10, hy + 22]], 12, D1_COLORS.ink);

  // Head slightly tilted
  drawBeanHead(g, 4, hy, HR, 'thinking', darkBags);
}

// -------------------------------------------------------------
// CHEERING BEAN (Victory / Breakthrough Celebration)
// -------------------------------------------------------------
function drawCheerBean(g, t, expr, darkBags, outfit) {
  const HR = 30;
  const hop = Math.abs(Math.sin(t * 5)) * 12;
  const hy = -190 - hop;
  const sy = -140 - hop;

  // Legs & Feet
  seg(g, [[-18, -70 - hop], [-24, 0]], 14, D1_COLORS.ink);
  seg(g, [[18, -70 - hop], [24, 0]], 14, D1_COLORS.ink);
  rr(g, -34, -6, 22, 10, 5); g.fillStyle = D1_COLORS.ink; g.fill();
  rr(g, 14, -6, 22, 10, 5); g.fill();

  // Torso
  rr(g, -28, sy, 56, 85, 24);
  g.fillStyle = outfit === 'hoodie' ? '#1c1b24' : '#222838';
  g.fill();
  g.strokeStyle = D1_COLORS.ink;
  g.lineWidth = 4;
  g.stroke();

  // Both Arms Raised in V Victory
  seg(g, [[-26, sy + 15], [-55, sy - 25], [-75, sy - 65]], 12, D1_COLORS.ink);
  seg(g, [[26, sy + 15], [55, sy - 25], [75, sy - 65]], 12, D1_COLORS.ink);
  circle(g, -75, sy - 65, 7, D1_COLORS.ink);
  circle(g, 75, sy - 65, 7, D1_COLORS.ink);

  // Head
  drawBeanHead(g, 0, hy, HR, 'motivated', darkBags);
}


// -------------------------------------------------------------
// RUNNING BEAN (Dynamic lean, high knees, speed lines)
// -------------------------------------------------------------
function drawRunningBean(g, t, pose, expr, darkBags, outfit) {
  const HR = 28;
  const phase = t * 9; // Run cadence
  const bob = Math.abs(Math.sin(phase)) * 14;
  const lean = 24; // Forward lean
  const hy = -180 + bob;
  const sy = -135 + bob;

  // Running Legs IK-like motion
  const leg1X = Math.sin(phase) * 45;
  const leg1Y = -Math.abs(Math.cos(phase)) * 32;
  const leg2X = -Math.sin(phase) * 45;
  const leg2Y = -Math.abs(Math.cos(phase + Math.PI)) * 32;

  // Far Leg
  seg(g, [[-10, sy + 65], [leg2X - 5, sy + 95], [leg2X, 0 + leg2Y]], 13, '#1c1d24');
  rr(g, leg2X - 4, -8 + leg2Y, 22, 11, 5); g.fillStyle = D1_COLORS.ink; g.fill();

  // Torso with forward lean
  g.save();
  g.translate(lean * 0.5, sy + 35);
  g.rotate(0.24); // 14 degree lean
  rr(g, -24, -38, 48, 76, 20);
  g.fillStyle = '#1c1b24';
  g.fill();
  g.strokeStyle = D1_COLORS.ink;
  g.lineWidth = 4;
  g.stroke();
  g.restore();

  // Near Leg
  seg(g, [[10, sy + 65], [leg1X + 5, sy + 95], [leg1X + 10, 0 + leg1Y]], 14, D1_COLORS.ink);
  rr(g, leg1X + 6, -8 + leg1Y, 24, 11, 5); g.fillStyle = D1_COLORS.ink; g.fill();

  // Pumping Arms
  const arm1X = -Math.sin(phase) * 35;
  const arm2X = Math.sin(phase) * 35;
  seg(g, [[lean - 15, sy + 15], [lean + arm1X, sy + 45]], 12, D1_COLORS.ink);
  seg(g, [[lean + 15, sy + 15], [lean + arm2X + 20, sy + 45]], 12, D1_COLORS.ink);

  // Head
  drawBeanHead(g, lean, hy, HR, expr, darkBags);

  // Foot dust puffs on asphalt
  if (bob < 4) {
    for (let d = 0; d < 3; d++) {
      circle(g, -35 - d * 18, 0 - d * 4, 6 - d * 1.5, 'rgba(255,255,255,0.25)');
    }
  }
}

// -------------------------------------------------------------
// BED LYING BEAN (Lying down horizontally or under covers)
// -------------------------------------------------------------
function drawBedLyingBean(g, t, expr, darkBags) {
  const HR = 28;
  const hx = -60;
  const hy = -55;

  // Bed Pillow
  rr(g, hx - 42, hy - 25, 84, 52, 16);
  g.fillStyle = '#e2dfeb';
  g.fill();
  g.strokeStyle = 'rgba(0,0,0,0.2)';
  g.lineWidth = 3;
  g.stroke();

  // Head resting on pillow
  drawBeanHead(g, hx, hy, HR, expr, darkBags);

  // Body under blanket / duvet
  rr(g, -40, -45, 180, 55, 14);
  g.fillStyle = '#242c42'; // Dark navy duvet
  g.fill();
  g.strokeStyle = D1_COLORS.ink;
  g.lineWidth = 4;
  g.stroke();

  // Fold of the sheet
  seg(g, [[-40, -45], [-40, 10]], 6, '#475569');
}

// -------------------------------------------------------------
// BED WAKEUP BEAN (Explosive or Disciplined 5:01 AM Sit-up)
// -------------------------------------------------------------
function drawBedWakeupBean(g, t, pose, expr, darkBags) {
  const HR = 28;
  const isDisciplined = (pose === 'bed_wakeup_disciplined');
  const hx = 0;
  const hy = -160;

  // Edge of mattress
  rr(g, -120, -50, 240, 60, 8);
  g.fillStyle = '#1c202d';
  g.fill();

  // Torso sitting upright at edge of bed
  rr(g, -26, -120, 52, 80, 20);
  g.fillStyle = '#222838';
  g.fill();
  g.strokeStyle = D1_COLORS.ink;
  g.lineWidth = 4;
  g.stroke();

  // Bare feet touching floor (discipline moment)
  seg(g, [[-16, -50], [-16, 0]], 13, D1_COLORS.skin);
  seg(g, [[16, -50], [16, 0]], 13, D1_COLORS.skin);
  rr(g, -24, -4, 20, 8, 4); g.fillStyle = D1_COLORS.skin; g.fill();
  rr(g, 8, -4, 20, 8, 4); g.fill();

  // Hands resting on knees
  seg(g, [[-24, -100], [-36, -65], [-16, -45]], 11, D1_COLORS.ink);
  seg(g, [[24, -100], [36, -65], [16, -45]], 11, D1_COLORS.ink);

  // Head
  drawBeanHead(g, hx, hy, HR, isDisciplined ? 'disciplined' : 'motivated', darkBags);
}

// -------------------------------------------------------------
// GYM CURL BEAN (Dumbbell workout)
// -------------------------------------------------------------
function drawGymCurlBean(g, t, expr, darkBags) {
  const HR = 28;
  const hy = -185;
  const sy = -135;
  const curlPhase = Math.sin(t * 3.5); // Curling motion

  // Standing legs
  seg(g, [[-18, -65], [-18, 0]], 14, D1_COLORS.ink);
  seg(g, [[18, -65], [18, 0]], 14, D1_COLORS.ink);
  rr(g, -28, -6, 24, 10, 5); g.fillStyle = D1_COLORS.ink; g.fill();
  rr(g, 8, -6, 24, 10, 5); g.fill();

  // Torso (Sleeveless athletic tank top)
  rr(g, -26, sy, 52, 80, 20);
  g.fillStyle = '#1e293b';
  g.fill();
  g.strokeStyle = D1_COLORS.ink;
  g.lineWidth = 4;
  g.stroke();

  // Left arm on hip
  seg(g, [[-24, sy + 15], [-42, sy + 45], [-20, sy + 65]], 12, D1_COLORS.ink);

  // Right arm curling heavy dumbbell
  const handY = sy + 60 - (curlPhase + 1) * 22;
  const elbowX = 40;
  seg(g, [[24, sy + 15], [elbowX, sy + 45], [32, handY]], 14, D1_COLORS.ink);

  // Heavy cast iron dumbbell in hand
  g.save();
  g.translate(34, handY);
  // Dumbbell bar
  g.fillStyle = '#94a3b8';
  g.fillRect(-18, -4, 36, 8);
  // Heavy plates
  rr(g, -26, -22, 10, 44, 4); g.fillStyle = '#0f172a'; g.fill();
  rr(g, 16, -22, 10, 44, 4); g.fill();
  g.restore();

  // Head
  drawBeanHead(g, 0, hy, HR, 'motivated', darkBags);
}

// -------------------------------------------------------------
// DESK SLUMP BEAN (Burnout, Day 8 exhaustion)
// -------------------------------------------------------------
function drawDeskSlumpBean(g, t, expr, darkBags) {
  const HR = 28;
  const deskY = -70;

  // Chair
  seg(g, [[-35, -110], [-35, 0]], 8, '#1e2030');

  // Slumped back & hunched torso over desk
  g.save();
  g.translate(-10, deskY - 30);
  g.rotate(0.55); // Heavy hunch forward
  rr(g, -22, -35, 44, 75, 18);
  g.fillStyle = '#1c1f2e';
  g.fill();
  g.strokeStyle = D1_COLORS.ink;
  g.lineWidth = 4;
  g.stroke();
  g.restore();

  // Stack of books on desk
  for (let b = 0; b < 3; b++) {
    rr(g, 10, deskY - 14 - b * 16, 75, 15, 3);
    g.fillStyle = b === 0 ? '#3b82f6' : b === 1 ? '#ef4444' : '#10b981';
    g.fill();
    g.strokeStyle = D1_COLORS.ink;
    g.lineWidth = 2.5;
    g.stroke();
  }

  // Head resting directly on top of books
  drawBeanHead(g, 45, deskY - 75, HR, 'exhausted', true);

  // Desk surface
  rr(g, -90, deskY, 220, 16, 4);
  g.fillStyle = '#332924';
  g.fill();
  seg(g, [[-80, deskY], [-80, 0]], 7, '#1f1916');
  seg(g, [[120, deskY], [120, 0]], 7, '#1f1916');
}

// -------------------------------------------------------------
// DRAGGING BODY BEAN (Day 11, dragging the fatigued brown body)
// -------------------------------------------------------------
function drawDragBodyBean(g, t, expr, darkBags) {
  // Main character running forward
  drawRunningBean(g, t, 'run_disciplined', 'disciplined', true, 'hoodie');

  // Arm reaching back holding tether/arm
  seg(g, [[-20, -115], [-70, -75]], 12, D1_COLORS.ink);

  // Dragging tired brown body behind on the ground
  drawFatigueFigure(g, { x: -140, y: 0, s: 0.9, t });
}


// -------------------------------------------------------------
// 2. THE METAPHORICAL SHADOW DEMON (Inner Doubt Whisperer)
// -------------------------------------------------------------
export function drawShadowDemon(g, o = {}) {
  const {
    x = 1150,
    y = 750,
    s = 1.35,
    facing = -1,
    whisperText = 'wait till you feel it again...',
    t = 0
  } = o;

  g.save();
  g.translate(x, y);
  g.scale(facing * s, s);

  const pulse = Math.sin(t * 4) * 0.05;
  const tendrilWave = Math.sin(t * 6) * 12;

  // Red ambient aura radiating from the shadow demon
  glow(g, 0, -160, 140, D1_COLORS.demonRed, 0.45);
  glow(g, 0, -160, 210, '#b91c1c', 0.25);

  // Wispy organic smoky silhouette body
  g.fillStyle = D1_COLORS.demonBlack;
  g.beginPath();
  g.moveTo(-50, 0);
  g.bezierCurveTo(-75 + tendrilWave, -100, -70 - tendrilWave, -200, -35, -250);
  g.bezierCurveTo(-25, -290, 25, -290, 35, -250);
  g.bezierCurveTo(70 + tendrilWave, -200, 75 - tendrilWave, -100, 50, 0);
  g.closePath();
  g.fill();

  // Shoulder smoke tendrils
  for (let i = 0; i < 5; i++) {
    const tx = -40 + i * 20;
    const ty = -240 + Math.sin(t * 5 + i * 1.5) * 25;
    circle(g, tx, ty, 18 - Math.abs(i - 2) * 3, D1_COLORS.demonBlack);
  }

  // Piercing glowing red slit eyes
  const eyeY = -230;
  glow(g, -16, eyeY, 24, D1_COLORS.demonRed, 0.85);
  glow(g, 16, eyeY, 24, D1_COLORS.demonRed, 0.85);

  g.fillStyle = D1_COLORS.demonRed;
  // Left eye slit
  g.beginPath();
  g.ellipse(-16, eyeY, 11, 4.5, -0.3, 0, Math.PI * 2);
  g.fill();
  // Right eye slit
  g.beginPath();
  g.ellipse(16, eyeY, 11, 4.5, 0.3, 0, Math.PI * 2);
  g.fill();

  // Sinister needle-sharp Cheshire grin
  g.strokeStyle = D1_COLORS.demonRed;
  g.lineWidth = 3.2;
  g.beginPath();
  g.arc(0, eyeY + 16, 28, 0.25, Math.PI - 0.25);
  g.stroke();

  // Sharp jagged teeth
  g.fillStyle = '#fee2e2';
  for (let tooth = -3; tooth <= 3; tooth++) {
    const tx = tooth * 7;
    const ty = eyeY + 38 - Math.abs(tooth) * 2;
    poly(g, [[tx - 2.5, ty], [tx + 2.5, ty], [tx, ty - 6]], '#fee2e2');
  }

  // Floating Whisper Comic Speech
  if (whisperText) {
    g.save();
    g.scale(facing, 1); // un-flip text
    const bubbleX = 40;
    const bubbleY = -285 + Math.sin(t * 3) * 6;

    // Red whisper bubble frame
    rr(g, bubbleX - 10, bubbleY - 26, 320, 48, 12);
    g.fillStyle = 'rgba(15, 10, 18, 0.92)';
    g.fill();
    g.strokeStyle = 'rgba(239, 68, 68, 0.6)';
    g.lineWidth = 2.5;
    g.stroke();

    // Red whisper glow dot
    circle(g, bubbleX + 12, bubbleY - 2, 4, D1_COLORS.demonRed);
    glow(g, bubbleX + 12, bubbleY - 2, 14, D1_COLORS.demonRed, 0.8);

    // Whisper Text
    text(g, whisperText, bubbleX + 28, bubbleY + 5, {
      size: 17,
      color: '#fca5a5',
      font: FONTS.ui,
      weight: 700,
      align: 'left'
    });
    g.restore();
  }

  g.restore();
}


// -------------------------------------------------------------
// 3. THE DRAGGING FATIGUE FIGURE (Exhaustion metaphor)
// -------------------------------------------------------------
export function drawFatigueFigure(g, o = {}) {
  const { x = 700, y = 800, s = 1.0, facing = 1, t = 0 } = o;

  g.save();
  g.translate(x, y);
  g.scale(facing * s, s);

  // Slouched collapsed silhouette dragged along asphalt
  g.fillStyle = D1_COLORS.fatigueBrown;
  
  // Head dragging on ground
  circle(g, -35, -20, 22, D1_COLORS.fatigueBrown);
  
  // Slumped horizontal torso
  rr(g, -20, -32, 70, 32, 14);
  g.fill();

  // Limp trailing legs
  seg(g, [[45, -20], [85, -8], [115, 0]], 11, D1_COLORS.fatigueBrown);
  seg(g, [[45, -15], [80, -4], [105, 0]], 10, D1_COLORS.fatigueBrown);

  // Stretched arm being pulled forward
  seg(g, [[0, -25], [-20, -45], [-60, -65]], 9, D1_COLORS.fatigueBrown);

  g.restore();
}


// -------------------------------------------------------------
// 4. DYNAMIC MOTIVATION METER HUD (100% -> 16% -> 0% -> 47%)
// -------------------------------------------------------------
export function drawMotivationMeter(g, o = {}) {
  const {
    pct = 100,
    x = 180,
    y = 80,
    w = 340,
    h = 36,
    label = 'MOTIVATION',
    t = 0
  } = o;

  g.save();
  const clampedPct = clamp(pct, 0, 100);
  const frac = clampedPct / 100;

  // Determine meter color (Gold when high, Dark slate when 0, Amber on recovery)
  let fillColor = D1_COLORS.auraGold;
  if (clampedPct <= 0) {
    fillColor = '#475569';
  } else if (clampedPct < 30) {
    fillColor = '#ef4444'; // Red alarm warning
  } else if (clampedPct < 60) {
    fillColor = '#f59e0b'; // Amber recovery
  }

  // Outer pill background
  rr(g, x, y, w, h, h / 2);
  g.fillStyle = D1_COLORS.meterBg;
  g.fill();
  g.strokeStyle = D1_COLORS.meterBorder;
  g.lineWidth = 2.5;
  g.stroke();

  // Filled energy progress
  if (frac > 0.02) {
    const fillW = Math.max(h, (w - 8) * frac);
    rr(g, x + 4, y + 4, fillW, h - 8, (h - 8) / 2);
    g.fillStyle = fillColor;
    g.fill();

    // Pulse glow if high
    if (clampedPct > 60) {
      glow(g, x + fillW, y + h / 2, 28, fillColor, 0.45);
    }
  }

  // Segment dividers (10-pip meter look)
  g.strokeStyle = 'rgba(0, 0, 0, 0.35)';
  g.lineWidth = 2;
  const segments = 10;
  for (let i = 1; i < segments; i++) {
    const segX = x + (w / segments) * i;
    g.beginPath();
    g.moveTo(segX, y + 6);
    g.lineTo(segX, y + h - 6);
    g.stroke();
  }

  // Label & Percentage Text
  const labelStr = `${label} ${Math.round(clampedPct)}%`;
  text(g, labelStr, x + w / 2, y + h / 2 + 5, {
    size: 15,
    color: '#ffffff',
    font: FONTS.ui,
    weight: 900,
    align: 'center'
  });

  g.restore();
}


// -------------------------------------------------------------
// 5. MINIMALIST TIMELINE BANNER (DAY 1, DAY 3, DAY 8, DAY 10, DAY 62)
// -------------------------------------------------------------
export function drawDayBanner(g, o = {}) {
  const {
    text: bannerText = 'DAY 1',
    subtext = '',
    x = E.W / 2,
    y = 85,
    accentColor = '#ffb800'
  } = o;

  g.save();
  const bw = 240;
  const bh = 54;

  // Dark sleek pill badge
  rr(g, x - bw / 2, y - bh / 2, bw, bh, 14);
  g.fillStyle = 'rgba(13, 15, 22, 0.92)';
  g.fill();
  g.strokeStyle = 'rgba(255, 255, 255, 0.15)';
  g.lineWidth = 2.5;
  g.stroke();

  // Amber accent line at top
  seg(g, [[x - bw / 2 + 20, y - bh / 2 + 3], [x + bw / 2 - 20, y - bh / 2 + 3]], 3, accentColor);
  glow(g, x, y - bh / 2 + 3, 20, accentColor, 0.5);

  // Main Day text
  text(g, bannerText.toUpperCase(), x, y + (subtext ? -2 : 6), {
    size: 24,
    color: '#ffffff',
    font: FONTS.ui,
    weight: 900,
    align: 'center'
  });

  // Optional subtext (e.g., '05:00 AM')
  if (subtext) {
    text(g, subtext, x, y + 17, {
      size: 12,
      color: '#94a3b8',
      font: FONTS.ui,
      weight: 700,
      align: 'center'
    });
  }

  g.restore();
}


// -------------------------------------------------------------
// 6. MASTER THESIS INFOGRAPHIC GRAPH (Motivation Spikes vs Discipline Compound)
// -------------------------------------------------------------
export function drawDisciplineGraph(g, o = {}) {
  const {
    x = E.W / 2 - 380,
    y = 260,
    w = 760,
    h = 420,
    t = 3,
    dur = 6
  } = o;

  g.save();
  const p = clamp(t / Math.max(1, dur));

  // Dark slate graph frame
  rr(g, x, y, w, h, 16);
  g.fillStyle = 'rgba(10, 12, 18, 0.94)';
  g.fill();
  g.strokeStyle = 'rgba(255, 255, 255, 0.12)';
  g.lineWidth = 2.5;
  g.stroke();

  // Grid lines
  g.strokeStyle = 'rgba(255, 255, 255, 0.06)';
  g.lineWidth = 1.5;
  for (let grid = 1; grid < 5; grid++) {
    const gy = y + (h / 5) * grid;
    seg(g, [[x + 60, gy], [x + w - 40, gy]], 1.5, 'rgba(255,255,255,0.06)');
  }

  // Axes
  seg(g, [[x + 60, y + 40], [x + 60, y + h - 50]], 3, '#64748b'); // Y-Axis
  seg(g, [[x + 60, y + h - 50], [x + w - 40, y + h - 50]], 3, '#64748b'); // X-Axis

  // Axis Labels
  text(g, 'PROGRESS', x + 50, y + 25, { size: 14, color: '#94a3b8', font: FONTS.ui, weight: 800, align: 'center' });
  text(g, 'DAYS / TIME →', x + w - 100, y + h - 25, { size: 14, color: '#94a3b8', font: FONTS.ui, weight: 800, align: 'center' });

  // Dashed GOAL Line
  const goalY = y + 130;
  g.save();
  g.setLineDash([10, 8]);
  seg(g, [[x + 60, goalY], [x + w - 40, goalY]], 2.5, '#f59e0b');
  g.restore();
  text(g, '★ GOAL THRESHOLD', x + w - 150, goalY - 12, { size: 13, color: '#f59e0b', font: FONTS.ui, weight: 900 });

  // 1. MOTIVATION CURVE (Erratic spikes plunging to 0)
  g.save();
  g.strokeStyle = '#f97316'; // Orange
  g.lineWidth = 3.5;
  g.beginPath();
  const startX = x + 60;
  const baseY = y + h - 50;
  g.moveTo(startX, baseY);

  const spikePoints = [
    [0.05, 0.75], // High spike at start
    [0.15, 0.40],
    [0.25, 0.85], // Second spike
    [0.35, 0.10], // Crash
    [0.50, 0.02], // Complete flatline
    [0.70, 0.00],
    [1.00, 0.00]
  ];

  for (const pt of spikePoints) {
    if (pt[0] <= p + 0.05) {
      const px = startX + (w - 120) * pt[0];
      const py = baseY - (baseY - (y + 60)) * pt[1];
      g.lineTo(px, py);
    }
  }
  g.stroke();
  g.restore();

  // 2. DISCIPLINE CURVE (Steady compounding staircase crossing GOAL)
  g.save();
  g.strokeStyle = '#10b981'; // Teal / Green
  g.lineWidth = 4.5;
  g.beginPath();
  g.moveTo(startX, baseY);

  const disciplineSteps = 20;
  for (let s = 1; s <= disciplineSteps; s++) {
    const frac = s / disciplineSteps;
    if (frac <= p) {
      const px = startX + (w - 120) * frac;
      // Exponential / steady compounding curve: y = x^1.4
      const curveVal = Math.pow(frac, 1.25) * 1.15;
      const py = baseY - (baseY - (y + 60)) * curveVal;
      g.lineTo(px, py);
    }
  }
  g.stroke();
  // Glowing head on discipline curve
  if (p > 0.05) {
    const curX = startX + (w - 120) * p;
    const curVal = Math.pow(p, 1.25) * 1.15;
    const curY = baseY - (baseY - (y + 60)) * curVal;
    circle(g, curX, curY, 6, '#10b981');
    glow(g, curX, curY, 22, '#10b981', 0.8);
  }
  g.restore();

  // Legend at bottom
  // Motivation Legend
  seg(g, [[x + 90, y + h - 22], [x + 130, y + h - 22]], 3.5, '#f97316');
  text(g, 'MOTIVATION (UNRELIABLE)', x + 145, y + h - 17, { size: 13, color: '#f97316', font: FONTS.ui, weight: 800, align: 'left' });

  // Discipline Legend
  seg(g, [[x + 380, y + h - 22], [x + 420, y + h - 22]], 4.5, '#10b981');
  text(g, 'DISCIPLINE (COMPOUNDING)', x + 435, y + h - 17, { size: 13, color: '#10b981', font: FONTS.ui, weight: 900, align: 'left' });

  g.restore();
}


// -------------------------------------------------------------
// 7. IN-SCENE HAND-LETTERED TYPOGRAPHY
// -------------------------------------------------------------
export function drawInSceneText(g, o = {}) {
  const {
    text: quoteText = 'tomorrow. 5:00.',
    x = 960,
    y = 400,
    size = 28,
    color = '#f8fafc',
    rot = -0.04
  } = o;

  g.save();
  g.translate(x, y);
  g.rotate(rot);

  // Handwritten comic style quote
  text(g, quoteText, 0, 0, {
    size,
    color,
    font: FONTS.hand || FONTS.ui,
    weight: 900,
    align: 'center'
  });

  g.restore();
}
