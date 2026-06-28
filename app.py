from flask import Flask, request, render_template_string, jsonify
import random
from collections import defaultdict

app = Flask(__name__)

tournament = {
    "groups": [],
    "matches": []
}

# ================= SHARED CSS =================
SHARED_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700;900&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:       #f0f4f8;
  --surface:  #ffffff;
  --surface2: #f8fafc;
  --border:   #e2e8f0;
  --text:     #0f172a;
  --muted:    #64748b;
  --accent:   #0ea5e9;
  --accent2:  #6366f1;
  --green:    #10b981;
  --amber:    #f59e0b;
  --red:      #ef4444;
  --shadow:   0 1px 3px rgba(0,0,0,.06), 0 4px 16px rgba(0,0,0,.06);
  --shadow-lg:0 8px 32px rgba(0,0,0,.10);
  --radius:   16px;
  --radius-sm:10px;
}

body {
  font-family: 'Vazirmatn', Tahoma, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  direction: rtl;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes pulse-dot {
  0%,100% { transform: scale(1); opacity: 1; }
  50%      { transform: scale(1.4); opacity: .6; }
}
@keyframes slide-in {
  from { transform: translateX(20px); opacity: 0; }
  to   { transform: translateX(0);    opacity: 1; }
}
@keyframes pop {
  0%   { transform: scale(.8); opacity: 0; }
  60%  { transform: scale(1.06); }
  100% { transform: scale(1); opacity: 1; }
}

.anim-fadeup  { animation: fadeUp .45s cubic-bezier(.22,1,.36,1) both; }
.anim-fadein  { animation: fadeIn .3s ease both; }

.stagger > *:nth-child(1)  { animation-delay: .04s; }
.stagger > *:nth-child(2)  { animation-delay: .08s; }
.stagger > *:nth-child(3)  { animation-delay: .12s; }
.stagger > *:nth-child(4)  { animation-delay: .16s; }
.stagger > *:nth-child(5)  { animation-delay: .20s; }
.stagger > *:nth-child(6)  { animation-delay: .24s; }
.stagger > *:nth-child(n+7){ animation-delay: .28s; }

.top-bar {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 18px 32px;
  display: flex;
  align-items: center;
  gap: 12px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 1px 0 var(--border);
}
.top-bar .ball-icon {
  width: 36px; height: 36px;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
}
.top-bar h1 { font-size: 18px; font-weight: 700; letter-spacing: -.3px; }
.top-bar .sub { font-size: 13px; color: var(--muted); margin-right: auto; }

.wrap { max-width: 960px; margin: 0 auto; padding: 36px 20px 60px; }

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow: hidden;
}
.card-head {
  padding: 24px 28px 20px;
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center; gap: 10px;
}
.card-head h2 { font-size: 17px; font-weight: 700; }
.card-head .badge {
  font-size: 11px; font-weight: 600; padding: 3px 10px;
  border-radius: 20px; background: #e0f2fe; color: var(--accent);
}
.card-body { padding: 24px 28px; }

.field-label {
  font-size: 13px; font-weight: 600; color: var(--muted);
  margin-bottom: 8px; display: block; letter-spacing: .3px;
}
textarea {
  width: 100%; height: 280px;
  border: 1.5px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 16px 18px;
  font-size: 15px;
  font-family: 'Vazirmatn', Tahoma, monospace;
  color: var(--text);
  background: var(--surface2);
  resize: vertical;
  outline: none;
  transition: border-color .2s, box-shadow .2s;
  line-height: 1.9;
}
textarea:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(14,165,233,.12);
  background: #fff;
}
textarea::placeholder { color: #94a3b8; }

.hint-box {
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: var(--radius-sm);
  padding: 14px 18px;
  margin-bottom: 18px;
  font-size: 13px;
  color: #0369a1;
  line-height: 1.8;
}
.hint-box b { color: var(--accent); }

.btn-primary {
  display: flex; align-items: center; justify-content: center; gap: 8px;
  width: 100%; padding: 16px;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  color: #fff; font-size: 16px; font-weight: 700;
  border: none; border-radius: var(--radius-sm);
  cursor: pointer; margin-top: 16px;
  transition: opacity .2s, transform .15s, box-shadow .2s;
  box-shadow: 0 4px 14px rgba(14,165,233,.35);
  font-family: 'Vazirmatn', Tahoma, sans-serif;
}
.btn-primary:hover  { opacity: .92; transform: translateY(-1px); }
.btn-primary:active { transform: translateY(0); }

.btn-win {
  flex: 1; padding: 8px 10px;
  border: 1.5px solid var(--border);
  border-radius: 8px; cursor: pointer; font-size: 12px; font-weight: 600;
  background: #fff; color: var(--text);
  font-family: 'Vazirmatn', Tahoma, sans-serif;
  transition: all .15s;
}
.btn-win:hover { background: var(--green); color: #fff; border-color: var(--green); transform: translateY(-1px); }
.btn-win:disabled { opacity: .5; cursor: not-allowed; transform: none; }

.btn-final {
  display: flex; align-items: center; justify-content: center; gap: 10px;
  width: 100%; padding: 18px;
  background: linear-gradient(135deg, var(--amber), #f97316);
  color: #fff; font-size: 17px; font-weight: 700;
  border: none; border-radius: var(--radius-sm);
  cursor: pointer; margin-top: 36px;
  transition: opacity .2s, transform .15s, box-shadow .2s;
  box-shadow: 0 4px 14px rgba(245,158,11,.35);
  font-family: 'Vazirmatn', Tahoma, sans-serif;
}
.btn-final:hover { opacity:.92; transform:translateY(-1px); }

.error-box {
  display: flex; align-items: center; gap: 10px;
  background: #fef2f2; border: 1px solid #fecaca;
  border-radius: var(--radius-sm); padding: 14px 18px;
  margin-top: 16px; color: var(--red); font-size: 14px;
  animation: slide-in .3s ease;
}

.groups-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.group-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow: hidden;
  animation: fadeUp .4s cubic-bezier(.22,1,.36,1) both;
}
.group-head {
  padding: 14px 20px;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  color: #fff;
  display: flex; align-items: center; justify-content: space-between;
}
.group-head .g-title { font-size: 15px; font-weight: 700; }
.group-head .g-num {
  width: 28px; height: 28px; border-radius: 50%;
  background: rgba(255,255,255,.25);
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 800;
}
.group-body { padding: 16px; }

.player-row {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 14px;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 10px;
  margin-bottom: 8px;
  font-size: 14px;
}
.player-avatar {
  width: 32px; height: 32px; border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  color: #fff; font-size: 13px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.player-name { font-weight: 600; flex: 1; }
.level-badge { font-size: 11px; font-weight: 700; padding: 2px 9px; border-radius: 20px; }
.level-1 { background: #fee2e2; color: #dc2626; }
.level-2 { background: #fef3c7; color: #d97706; }
.level-3 { background: #dcfce7; color: #16a34a; }
.club-pill {
  font-size: 11px; padding: 2px 9px; border-radius: 20px;
  background: #ede9fe; color: var(--accent2); font-weight: 600;
}
.warn-pill {
  display: flex; align-items: center; gap: 6px;
  font-size: 12px; color: #92400e;
  background: #fef3c7; border: 1px solid #fde68a;
  border-radius: 8px; padding: 6px 12px; margin-bottom: 10px;
}
.divider { height: 1px; background: var(--border); margin: 12px 0; }
.section-label {
  font-size: 11px; font-weight: 700; color: var(--muted);
  letter-spacing: .8px; text-transform: uppercase; margin-bottom: 10px;
}

.match-card {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 12px 14px;
  margin-bottom: 10px;
  transition: box-shadow .15s;
}
.match-vs {
  font-size: 13px; font-weight: 700; margin-bottom: 10px;
  display: flex; align-items: center; gap: 6px;
}
.match-vs .vs-tag {
  background: var(--border); border-radius: 6px;
  padding: 1px 7px; font-size: 11px; color: var(--muted);
}
.score-row {
  display: flex; align-items: center; gap: 8px; margin-bottom: 8px;
}
.score-input {
  flex: 1; padding: 8px; border: 1.5px solid var(--border);
  border-radius: 8px; text-align: center; font-size: 14px;
  font-family: 'Vazirmatn', Tahoma, sans-serif;
  background: #fff; color: var(--text);
  outline: none; transition: border-color .2s;
}
.score-input:focus { border-color: var(--accent); }
.score-sep { color: var(--muted); font-weight: 700; font-size: 16px; }
.win-row { display: flex; gap: 8px; }

.done-tag {
  display: inline-flex; align-items: center; gap: 5px;
  background: #dcfce7; color: #15803d;
  border-radius: 8px; padding: 6px 12px;
  font-size: 12px; font-weight: 700; margin-top: 8px;
  animation: pop .35s cubic-bezier(.22,1,.36,1) both;
}
.done-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--green); animation: pulse-dot 1.4s infinite; }

/* ── Final page ── */
.final-wrap { max-width: 960px; margin: 0 auto; padding: 40px 20px 60px; }
.final-head  { text-align: center; margin-bottom: 36px; animation: fadeUp .4s ease; }
.final-head h1 { font-size: 28px; font-weight: 900; }
.final-head p  { color: var(--muted); font-size: 14px; margin-top: 6px; }

.result-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow: hidden;
  margin-bottom: 16px;
  animation: fadeUp .4s cubic-bezier(.22,1,.36,1) both;
}
.result-head {
  padding: 12px 20px;
  background: var(--surface2);
  border-bottom: 1px solid var(--border);
  font-size: 14px; font-weight: 700; color: var(--muted);
}
.result-body { padding: 16px 20px; }
.podium-row {
  display: flex; align-items: center; gap: 14px;
  padding: 10px 0; border-bottom: 1px solid var(--border);
}
.podium-row:last-of-type { border-bottom: none; }
.podium-medal { font-size: 22px; width: 32px; text-align: center; flex-shrink: 0; }
.podium-name  { font-size: 15px; font-weight: 700; flex: 1; }
.podium-club  { font-size: 12px; color: var(--muted); }

.advance-tag {
  display: inline-flex; align-items: center; gap: 6px;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  color: #fff; border-radius: 20px; padding: 6px 14px;
  font-size: 12px; font-weight: 700; margin-top: 12px;
}

/* ── Bracket page ── */
.bracket-layout {
  display: flex;
  gap: 0;
  overflow-x: auto;
  padding-bottom: 20px;
  align-items: flex-start;
  direction: ltr;
}
.bracket-round {
  display: flex;
  flex-direction: column;
  min-width: 180px;
  flex-shrink: 0;
}
.round-label {
  font-size: 11px; font-weight: 700; color: var(--muted);
  letter-spacing: .8px; text-transform: uppercase;
  text-align: center; padding: 0 10px 16px;
}
.bracket-slots {
  display: flex;
  flex-direction: column;
  flex: 1;
  position: relative;
}
.bracket-match-wrap {
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
}
.bracket-match {
  margin: 0 10px;
  border: 1.5px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
  background: var(--surface);
  box-shadow: var(--shadow);
  position: relative;
  z-index: 1;
}
.bracket-slot {
  padding: 9px 12px;
  font-size: 13px; font-weight: 600;
  display: flex; align-items: center; gap: 8px;
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  transition: background .15s;
  min-height: 38px;
}
.bracket-slot:last-child { border-bottom: none; }
.bracket-slot:hover:not(.empty):not(.winner-slot) { background: #f0f9ff; }
.bracket-slot.winner-slot { background: #dcfce7; color: #15803d; }
.bracket-slot.empty { color: var(--muted); font-style: italic; font-weight: 400; font-size: 12px; }
.bracket-slot .slot-num {
  width: 20px; height: 20px; border-radius: 50%;
  background: var(--border); color: var(--muted);
  font-size: 10px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.bracket-slot.winner-slot .slot-num { background: #bbf7d0; color: #15803d; }

/* connector lines */
.bracket-connector {
  position: absolute;
  right: 0;
  top: 50%;
  width: 10px;
  border-top: 2px solid var(--border);
}
.bracket-connector-v {
  position: absolute;
  right: 0;
  border-right: 2px solid var(--border);
}

.champion-card {
  text-align: center;
  padding: 30px 20px;
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  border: 1.5px solid #fbbf24;
  border-radius: var(--radius);
  margin: 0 10px;
}
.champion-card .trophy { font-size: 40px; }
.champion-card .champ-label { font-size: 12px; font-weight: 700; color: #92400e; margin-top: 8px; }
.champion-card .champ-name { font-size: 20px; font-weight: 900; color: #78350f; margin-top: 4px; }

/* manual bracket input */
.bracket-input-area {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 28px;
  margin-bottom: 24px;
}
.bracket-input-area h3 { font-size: 16px; font-weight: 700; margin-bottom: 6px; }
.bracket-input-area p  { font-size: 13px; color: var(--muted); margin-bottom: 16px; line-height: 1.7; }
.names-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 10px;
  margin-bottom: 16px;
}
.name-input {
  padding: 10px 14px;
  border: 1.5px solid var(--border);
  border-radius: 9px;
  font-size: 14px;
  font-family: 'Vazirmatn', Tahoma, sans-serif;
  background: var(--surface2);
  color: var(--text);
  outline: none;
  transition: border-color .2s;
  width: 100%;
}
.name-input:focus { border-color: var(--accent); background: #fff; }
.btn-build {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 12px 28px;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  color: #fff; font-size: 15px; font-weight: 700;
  border: none; border-radius: var(--radius-sm);
  cursor: pointer;
  font-family: 'Vazirmatn', Tahoma, sans-serif;
  transition: opacity .2s, transform .15s;
  box-shadow: 0 4px 14px rgba(14,165,233,.3);
}
.btn-build:hover { opacity: .92; transform: translateY(-1px); }

.bracket-tabs {
  display: flex; gap: 10px; margin-bottom: 24px; flex-wrap: wrap;
}
.tab-btn {
  padding: 9px 20px;
  border: 1.5px solid var(--border);
  border-radius: 9px;
  background: var(--surface);
  font-size: 14px; font-weight: 600;
  cursor: pointer;
  font-family: 'Vazirmatn', Tahoma, sans-serif;
  transition: all .15s;
  color: var(--muted);
}
.tab-btn.active {
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  color: #fff; border-color: transparent;
}
.tab-btn:hover:not(.active) { border-color: var(--accent); color: var(--accent); }

@media(max-width:600px){
  .wrap,.final-wrap{ padding:20px 12px 50px; }
  .card-body{ padding:16px; }
  .top-bar{ padding:14px 16px; }
  .bracket-round { min-width: 150px; }
}
"""

# ================= HOME =================
HOME_HTML = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>مسابقات پینگ‌پنگ</title>
<style>{{ css }}</style>
<style>

/* ════════════════════════════════════
   HOME PAGE — EXTRA STYLES
════════════════════════════════════ */

/* ── animated bg orbs ── */
body { overflow-x: hidden; }
.bg-orbs {
  position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden;
}
.orb {
  position: absolute; border-radius: 50%; filter: blur(80px); opacity: .18;
  animation: drift linear infinite;
}
.orb1 { width:380px;height:380px; background:#6366f1; top:-80px; right:-80px; animation-duration:18s; }
.orb2 { width:300px;height:300px; background:#0ea5e9; bottom:-60px; left:-60px; animation-duration:24s; animation-direction:reverse; }
.orb3 { width:220px;height:220px; background:#f59e0b; top:45%; left:30%; animation-duration:30s; opacity:.1; }
@keyframes drift {
  0%   { transform: translate(0,0) scale(1); }
  33%  { transform: translate(30px,-20px) scale(1.05); }
  66%  { transform: translate(-20px,30px) scale(.95); }
  100% { transform: translate(0,0) scale(1); }
}

/* ── page wrap ── */
.wrap { position: relative; z-index: 1; }

/* ── hero header ── */
.hero {
  text-align: center;
  padding: 48px 20px 36px;
  animation: fadeUp .6s cubic-bezier(.22,1,.36,1) both;
}
.hero-ball {
  width: 72px; height: 72px;
  background: linear-gradient(135deg, #0ea5e9, #6366f1);
  border-radius: 50%;
  margin: 0 auto 18px;
  display: flex; align-items: center; justify-content: center;
  font-size: 34px;
  box-shadow: 0 12px 40px rgba(99,102,241,.35), 0 0 0 12px rgba(99,102,241,.08);
  animation: float 3s ease-in-out infinite;
}
@keyframes float {
  0%,100% { transform: translateY(0); box-shadow: 0 12px 40px rgba(99,102,241,.35), 0 0 0 12px rgba(99,102,241,.08); }
  50%      { transform: translateY(-8px); box-shadow: 0 22px 50px rgba(99,102,241,.4), 0 0 0 16px rgba(99,102,241,.06); }
}
.hero h1 {
  font-size: 26px; font-weight: 900; letter-spacing: -.5px;
  background: linear-gradient(135deg, #0f172a 0%, #6366f1 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero p { color: var(--muted); font-size: 14px; margin-top: 6px; }

/* ── glass card ── */
.glass-card {
  background: rgba(255,255,255,.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,.6);
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(0,0,0,.08), 0 1px 0 rgba(255,255,255,.8) inset;
  overflow: hidden;
  animation: fadeUp .5s .1s cubic-bezier(.22,1,.36,1) both;
}
.gc-head {
  padding: 20px 28px 18px;
  border-bottom: 1px solid rgba(226,232,240,.8);
  display: flex; align-items: center; gap: 10px;
}
.gc-head h2 { font-size: 17px; font-weight: 800; }
.gc-head .cnt-pill {
  margin-right: auto;
  font-size: 12px; font-weight: 700;
  padding: 4px 12px; border-radius: 20px;
  background: linear-gradient(135deg, #e0f2fe, #ede9fe);
  color: #6366f1;
  transition: all .3s;
}
.gc-body { padding: 24px 28px; }

/* ── Input area ── */
.inp-zone {
  background: var(--surface2);
  border: 1.5px solid var(--border);
  border-radius: 16px;
  padding: 18px;
  margin-bottom: 20px;
  transition: border-color .2s, box-shadow .2s;
}
.inp-zone:focus-within {
  border-color: rgba(99,102,241,.4);
  box-shadow: 0 0 0 4px rgba(99,102,241,.07);
}

.inp-zone-row1 {
  display: flex; gap: 10px; align-items: center; margin-bottom: 14px; flex-wrap: wrap;
}
.name-wrap {
  flex: 1; min-width: 140px;
  position: relative;
}
.name-wrap .name-icon {
  position: absolute; right: 14px; top: 50%; transform: translateY(-50%);
  font-size: 16px; pointer-events: none;
}
.name-field {
  width: 100%;
  padding: 12px 42px 12px 14px;
  border: 1.5px solid transparent;
  border-radius: 12px;
  font-size: 15px; font-weight: 500;
  font-family: 'Vazirmatn', Tahoma, sans-serif;
  color: var(--text);
  background: #fff;
  outline: none;
  box-shadow: 0 1px 4px rgba(0,0,0,.06);
  transition: border-color .2s, box-shadow .2s;
}
.name-field:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99,102,241,.12), 0 1px 4px rgba(0,0,0,.06);
}
.name-field::placeholder { color: #94a3b8; font-weight: 400; }

.club-wrap { position: relative; flex-shrink: 0; width: 150px; }
.club-wrap .club-icon {
  position: absolute; right: 14px; top: 50%; transform: translateY(-50%);
  font-size: 15px; pointer-events: none;
}
.club-field {
  width: 100%;
  padding: 12px 40px 12px 14px;
  border: 1.5px solid transparent;
  border-radius: 12px;
  font-size: 14px;
  font-family: 'Vazirmatn', Tahoma, sans-serif;
  color: var(--text);
  background: #fff;
  outline: none;
  box-shadow: 0 1px 4px rgba(0,0,0,.06);
  transition: border-color .2s, box-shadow .2s;
}
.club-field:focus {
  border-color: #0ea5e9;
  box-shadow: 0 0 0 3px rgba(14,165,233,.12);
}
.club-field::placeholder { color: #94a3b8; font-weight: 400; }

/* ── Seed cards (level selector) ── */
.seed-row {
  display: flex; gap: 10px; margin-bottom: 0;
}
.seed-input { display: none; }
.seed-card {
  flex: 1;
  display: flex; flex-direction: column; align-items: center; gap: 4px;
  padding: 12px 8px 10px;
  border-radius: 14px;
  border: 2px solid transparent;
  cursor: pointer;
  transition: transform .2s cubic-bezier(.22,1,.36,1), box-shadow .2s, border-color .2s, background .2s;
  user-select: none;
  position: relative;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0,0,0,.07);
}
.seed-card::before {
  content: '';
  position: absolute; inset: 0;
  opacity: 0;
  transition: opacity .2s;
  border-radius: 12px;
}
.seed-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,.1); }
.seed-card:active { transform: scale(.96); }

/* seed 1 — قوی */
.seed-card.s1::before { background: linear-gradient(135deg, #fef2f2, #fee2e2); }
.seed-input.s1:checked ~ .seed-card.s1,
.seed-card.s1.active {
  border-color: #ef4444;
  box-shadow: 0 0 0 4px rgba(239,68,68,.15), 0 6px 20px rgba(239,68,68,.2);
  transform: translateY(-3px) scale(1.02);
}
.seed-input.s1:checked ~ .seed-card.s1::before,
.seed-card.s1.active::before { opacity: 1; }

/* seed 2 — متوسط */
.seed-card.s2::before { background: linear-gradient(135deg, #fffbeb, #fef3c7); }
.seed-input.s2:checked ~ .seed-card.s2,
.seed-card.s2.active {
  border-color: #f59e0b;
  box-shadow: 0 0 0 4px rgba(245,158,11,.15), 0 6px 20px rgba(245,158,11,.2);
  transform: translateY(-3px) scale(1.02);
}
.seed-input.s2:checked ~ .seed-card.s2::before,
.seed-card.s2.active::before { opacity: 1; }

/* seed 3 — ضعیف */
.seed-card.s3::before { background: linear-gradient(135deg, #f0fdf4, #dcfce7); }
.seed-input.s3:checked ~ .seed-card.s3,
.seed-card.s3.active {
  border-color: #10b981;
  box-shadow: 0 0 0 4px rgba(16,185,129,.15), 0 6px 20px rgba(16,185,129,.2);
  transform: translateY(-3px) scale(1.02);
}
.seed-input.s3:checked ~ .seed-card.s3::before,
.seed-card.s3.active::before { opacity: 1; }

.seed-emoji { font-size: 26px; position: relative; z-index: 1; }
.seed-num {
  font-size: 10px; font-weight: 800; letter-spacing: .5px;
  text-transform: uppercase; position: relative; z-index: 1;
  opacity: .6;
}
.seed-label { font-size: 12px; font-weight: 700; position: relative; z-index: 1; }
.s1 .seed-label { color: #dc2626; }
.s2 .seed-label { color: #d97706; }
.s3 .seed-label { color: #059669; }

/* seed selected indicator dot */
.seed-check {
  position: absolute; top: 7px; left: 7px;
  width: 16px; height: 16px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 9px; color: #fff; font-weight: 900;
  opacity: 0;
  transform: scale(0);
  transition: opacity .2s, transform .2s cubic-bezier(.22,1,.36,1);
}
.s1 .seed-check { background: #ef4444; }
.s2 .seed-check { background: #f59e0b; }
.s3 .seed-check { background: #10b981; }
.seed-card.active .seed-check { opacity: 1; transform: scale(1); }

/* ── Add button ── */
.btn-add {
  display: flex; align-items: center; justify-content: center; gap: 8px;
  width: 100%; margin-top: 16px;
  padding: 14px;
  background: linear-gradient(135deg, #6366f1, #0ea5e9);
  color: #fff; font-size: 15px; font-weight: 800;
  border: none; border-radius: 14px; cursor: pointer;
  font-family: 'Vazirmatn', Tahoma, sans-serif;
  letter-spacing: -.2px;
  position: relative; overflow: hidden;
  transition: transform .2s, box-shadow .2s;
  box-shadow: 0 4px 18px rgba(99,102,241,.4);
}
.btn-add::after {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,.15), transparent);
  opacity: 0;
  transition: opacity .2s;
}
.btn-add:hover { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(99,102,241,.45); }
.btn-add:hover::after { opacity: 1; }
.btn-add:active { transform: scale(.97); }
.btn-add .plus-icon {
  width: 24px; height: 24px; border-radius: 50%;
  background: rgba(255,255,255,.25);
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; font-weight: 900; line-height: 1;
}

/* ── counter strip ── */
.counter-strip {
  display: flex; gap: 8px; margin-bottom: 16px; align-items: center; flex-wrap: wrap;
}
.cs-pill {
  display: flex; align-items: center; gap: 5px;
  padding: 5px 12px 5px 8px;
  border-radius: 20px; font-size: 12px; font-weight: 700;
  border: 1.5px solid transparent;
  transition: all .3s;
}
.cs-pill .dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.cs-p1 { background: #fef2f2; border-color: #fecaca; color: #dc2626; }
.cs-p1 .dot { background: #ef4444; }
.cs-p2 { background: #fffbeb; border-color: #fde68a; color: #d97706; }
.cs-p2 .dot { background: #f59e0b; }
.cs-p3 { background: #f0fdf4; border-color: #bbf7d0; color: #059669; }
.cs-p3 .dot { background: #10b981; }
.cs-status {
  margin-right: auto;
  font-size: 12px; font-weight: 700; padding: 5px 12px;
  border-radius: 20px;
  transition: all .4s;
}
.cs-ok  { background: #dcfce7; color: #15803d; border: 1.5px solid #bbf7d0; }
.cs-warn{ background: #fff7ed; color: #c2410c; border: 1.5px solid #fed7aa; }
.cs-idle{ background: var(--surface2); color: var(--muted); border: 1.5px solid var(--border); }

/* ── player list ── */
.pl-list { min-height: 60px; }

@keyframes slideInRight {
  from { opacity: 0; transform: translateX(24px) scale(.96); }
  to   { opacity: 1; transform: translateX(0) scale(1); }
}
@keyframes slideOutLeft {
  from { opacity: 1; transform: translateX(0) scale(1); max-height: 80px; margin-bottom: 8px; }
  to   { opacity: 0; transform: translateX(-24px) scale(.95); max-height: 0; margin-bottom: 0; padding: 0; }
}

.pl-item {
  display: flex; align-items: center; gap: 10px;
  padding: 11px 14px;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 12px;
  margin-bottom: 8px;
  font-size: 14px;
  animation: slideInRight .35s cubic-bezier(.22,1,.36,1) both;
  transition: box-shadow .15s;
}
.pl-item:hover { box-shadow: 0 4px 14px rgba(0,0,0,.07); }
.pl-item.removing { animation: slideOutLeft .3s ease forwards; }

.pl-num {
  width: 22px; height: 22px; border-radius: 50%;
  background: var(--surface2); border: 1px solid var(--border);
  color: var(--muted); font-size: 11px; font-weight: 800;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.pl-avatar {
  width: 36px; height: 36px; border-radius: 50%;
  font-size: 15px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  position: relative;
}
.pl-av1 { background: linear-gradient(135deg, #fecaca, #fee2e2); color: #dc2626; }
.pl-av2 { background: linear-gradient(135deg, #fde68a, #fef3c7); color: #d97706; }
.pl-av3 { background: linear-gradient(135deg, #bbf7d0, #dcfce7); color: #059669; }

.pl-name { font-weight: 700; flex: 1; }
.pl-seed {
  font-size: 10px; font-weight: 800; padding: 3px 9px;
  border-radius: 20px; flex-shrink: 0; letter-spacing: .3px;
}
.pl-s1 { background: #fee2e2; color: #dc2626; }
.pl-s2 { background: #fef3c7; color: #d97706; }
.pl-s3 { background: #dcfce7; color: #059669; }
.pl-club {
  font-size: 11px; padding: 3px 9px; border-radius: 20px;
  background: #ede9fe; color: #6366f1; font-weight: 700;
}
.btn-del {
  width: 30px; height: 30px;
  background: none; border: none; cursor: pointer;
  color: #cbd5e1; font-size: 16px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  transition: color .15s, background .15s, transform .15s;
  flex-shrink: 0;
}
.btn-del:hover { color: #ef4444; background: #fef2f2; transform: scale(1.15); }

/* empty state */
.empty-state {
  text-align: center; padding: 36px 20px;
  animation: fadeIn .4s ease;
}
.empty-ball {
  font-size: 48px; margin-bottom: 12px;
  animation: float 3s ease-in-out infinite;
}
.empty-state p { color: #94a3b8; font-size: 14px; line-height: 1.7; }
.empty-state strong { color: #6366f1; }

/* ── submit button ── */
.btn-launch {
  display: flex; align-items: center; justify-content: center; gap: 10px;
  width: 100%; padding: 17px;
  background: linear-gradient(135deg, #f59e0b 0%, #ef4444 50%, #6366f1 100%);
  background-size: 200% 200%;
  color: #fff; font-size: 16px; font-weight: 900;
  border: none; border-radius: 16px; cursor: pointer;
  font-family: 'Vazirmatn', Tahoma, sans-serif;
  margin-top: 20px;
  transition: transform .2s, box-shadow .2s, background-position .4s;
  box-shadow: 0 6px 24px rgba(239,68,68,.35);
  letter-spacing: -.2px;
  animation: fadeUp .5s .3s cubic-bezier(.22,1,.36,1) both;
}
.btn-launch:hover {
  transform: translateY(-2px);
  background-position: right center;
  box-shadow: 0 10px 32px rgba(99,102,241,.4);
}
.btn-launch:active { transform: scale(.98); }
.btn-launch .launch-icon { font-size: 20px; }

@keyframes shake {
  0%,100% { transform: translateX(0); }
  20%      { transform: translateX(-8px) rotate(-1deg); }
  40%      { transform: translateX(8px) rotate(1deg); }
  60%      { transform: translateX(-6px); }
  80%      { transform: translateX(6px); }
}
.shake { animation: shake .4s ease; }

@media(max-width:600px){
  .gc-body { padding: 16px; }
  .seed-emoji { font-size: 22px; }
  .club-wrap { width: 100%; }
  .inp-zone-row1 { gap: 8px; }
}
</style>
</head>
<body>

<!-- animated background orbs -->
<div class="bg-orbs">
  <div class="orb orb1"></div>
  <div class="orb orb2"></div>
  <div class="orb orb3"></div>
</div>

<div class="top-bar" style="background:rgba(255,255,255,.8);backdrop-filter:blur(16px);">
  <div class="ball-icon">🏓</div>
  <h1>مسابقات پینگ‌پنگ</h1>
  <span class="sub">سیستم گروه‌بندی هوشمند</span>
</div>

<div class="wrap" style="max-width:680px;">

  <!-- hero -->
  <div class="hero">
    <div class="hero-ball">🏓</div>
    <h1>بازیکنا رو ثبت کن</h1>
    <p>سطح رو مشخص کن، باشگاهش رو بزن، شروع کن</p>
  </div>

  <!-- glass card -->
  <div class="glass-card">
    <div class="gc-head">
      <span style="font-size:20px;">👥</span>
      <h2>افزودن بازیکن</h2>
      <span class="cnt-pill" id="total-badge">۰ نفر ثبت شده</span>
    </div>
    <div class="gc-body">

      <!-- input zone -->
      <div class="inp-zone">

        <!-- row 1: name + club -->
        <div class="inp-zone-row1">
          <div class="name-wrap">
            <span class="name-icon">👤</span>
            <input class="name-field" type="text" id="inp-name"
                   placeholder="اسم بازیکن را بنویس…" maxlength="40"
                   onkeydown="if(event.key==='Enter') addPlayer()">
          </div>
          <div class="club-wrap">
            <span class="club-icon">🏢</span>
            <input class="club-field" type="text" id="inp-club"
                   placeholder="باشگاه…" maxlength="30"
                   onkeydown="if(event.key==='Enter') addPlayer()">
          </div>
        </div>

        <!-- row 2: seed cards -->
        <div class="seed-row" id="seed-row">

          <!-- Seed 1 -->
          <div class="seed-card s1 active" onclick="selectSeed(1)" id="sc1">
            <div class="seed-check">✓</div>
            <div class="seed-emoji">🔥</div>
            <div class="seed-num">سید ۱</div>
            <div class="seed-label">قوی</div>
          </div>

          <!-- Seed 2 -->
          <div class="seed-card s2" onclick="selectSeed(2)" id="sc2">
            <div class="seed-check">✓</div>
            <div class="seed-emoji">⚡</div>
            <div class="seed-num">سید ۲</div>
            <div class="seed-label">متوسط</div>
          </div>

          <!-- Seed 3 -->
          <div class="seed-card s3" onclick="selectSeed(3)" id="sc3">
            <div class="seed-check">✓</div>
            <div class="seed-emoji">🌱</div>
            <div class="seed-num">سید ۳</div>
            <div class="seed-label">ضعیف</div>
          </div>

        </div>

        <!-- add button -->
        <button class="btn-add" onclick="addPlayer()">
          <span class="plus-icon">+</span>
          افزودن به لیست
        </button>

      </div>
      <!-- /inp-zone -->

      <!-- counter strip -->
      <div class="counter-strip">
        <span class="cs-pill cs-p1"><span class="dot"></span>🔥 قوی: <b id="c1">۰</b></span>
        <span class="cs-pill cs-p2"><span class="dot"></span>⚡ متوسط: <b id="c2">۰</b></span>
        <span class="cs-pill cs-p3"><span class="dot"></span>🌱 ضعیف: <b id="c3">۰</b></span>
        <span class="cs-status cs-idle" id="c-status">منتظر ثبت…</span>
      </div>

      <!-- player list -->
      <div class="pl-list" id="player-list">
        <div class="empty-state">
          <div class="empty-ball">🏓</div>
          <p>هنوز کسی ثبت نشده!<br>اسم اولین بازیکن رو بنویس و <strong>افزودن</strong> رو بزن</p>
        </div>
      </div>

      {% if error %}
      <div class="error-box" style="margin-top:12px;">⚠️ <span>{{ error }}</span></div>
      {% endif %}

      <!-- submit -->
      <form method="POST" action="/create" id="main-form">
        <input type="hidden" name="players" id="players-data">
        <button class="btn-launch" type="button" onclick="submitForm()">
          <span class="launch-icon">⚡</span>
          ساخت گروه‌ها و شروع مسابقات
        </button>
      </form>

    </div>
  </div>

</div>

<script>
const players = [];
let uid = 0;
let selectedSeed = 1;

const seedLabel = { 1: 'سید ۱ — قوی', 2: 'سید ۲ — متوسط', 3: 'سید ۳ — ضعیف' };
const seedEmoji = { 1: '🔥', 2: '⚡', 3: '🌱' };
const seedClass = { 1: 'pl-s1', 2: 'pl-s2', 3: 'pl-s3' };
const avClass   = { 1: 'pl-av1', 2: 'pl-av2', 3: 'pl-av3' };
const toFa = n => String(n).replace(/\\d/g, d => '۰۱۲۳۴۵۶۷۸۹'[d]);

function selectSeed(n) {
  selectedSeed = n;
  [1,2,3].forEach(i => {
    document.getElementById('sc'+i).classList.toggle('active', i === n);
  });
  // micro-bounce
  const el = document.getElementById('sc'+n);
  el.style.transition = 'transform .15s';
  el.style.transform = 'scale(1.08) translateY(-4px)';
  setTimeout(() => { el.style.transform = ''; }, 180);
}

function addPlayer() {
  const nameEl = document.getElementById('inp-name');
  const clubEl = document.getElementById('inp-club');
  const name = nameEl.value.trim();
  const club = clubEl.value.trim();

  if (!name) {
    nameEl.classList.add('shake');
    nameEl.focus();
    setTimeout(() => nameEl.classList.remove('shake'), 450);
    return;
  }

  players.push({ id: uid++, name, level: selectedSeed, club });
  nameEl.value = '';
  clubEl.value = '';
  nameEl.focus();
  render();
}

function removePlayer(id) {
  const el = document.getElementById('pi-' + id);
  if (el) {
    el.classList.add('removing');
    setTimeout(() => {
      const idx = players.findIndex(p => p.id === id);
      if (idx !== -1) players.splice(idx, 1);
      render();
    }, 280);
  }
}

function render() {
  const list = document.getElementById('player-list');
  const c = { 1: 0, 2: 0, 3: 0 };
  players.forEach(p => c[p.level]++);

  document.getElementById('c1').textContent = toFa(c[1]);
  document.getElementById('c2').textContent = toFa(c[2]);
  document.getElementById('c3').textContent = toFa(c[3]);
  document.getElementById('total-badge').textContent = toFa(players.length) + ' نفر ثبت شده';

  const n = players.length;
  const balanced = n > 0 && c[1] === c[2] && c[2] === c[3];
  const statusEl = document.getElementById('c-status');
  if (n === 0) {
    statusEl.textContent = 'منتظر ثبت…';
    statusEl.className = 'cs-status cs-idle';
  } else if (balanced) {
    statusEl.textContent = '✓ آماده گروه‌بندی!';
    statusEl.className = 'cs-status cs-ok';
  } else {
    const diff = Math.max(c[1],c[2],c[3]) - Math.min(c[1],c[2],c[3]);
    statusEl.textContent = 'هر سطح باید مساوی باشد';
    statusEl.className = 'cs-status cs-warn';
  }

  if (players.length === 0) {
    list.innerHTML = `<div class="empty-state">
      <div class="empty-ball">🏓</div>
      <p>هنوز کسی ثبت نشده!<br>اسم اولین بازیکن رو بنویس و <strong>افزودن</strong> رو بزن</p>
    </div>`;
    return;
  }

  list.innerHTML = players.map((p, i) => `
    <div class="pl-item" id="pi-${p.id}">
      <span class="pl-num">${toFa(i+1)}</span>
      <div class="pl-avatar ${avClass[p.level]}">${seedEmoji[p.level]}</div>
      <span class="pl-name">${p.name}</span>
      <span class="pl-seed ${seedClass[p.level]}">${seedLabel[p.level]}</span>
      ${p.club ? `<span class="pl-club">🏢 ${p.club}</span>` : ''}
      <button class="btn-del" onclick="removePlayer(${p.id})" title="حذف">🗑️</button>
    </div>
  `).join('');
}

function submitForm() {
  if (players.length === 0) {
    document.getElementById('inp-name').classList.add('shake');
    setTimeout(() => document.getElementById('inp-name').classList.remove('shake'), 450);
    return;
  }
  const lines = players.map(p =>
    p.club ? `${p.name} , ${p.level} , ${p.club}` : `${p.name} , ${p.level}`
  );
  document.getElementById('players-data').value = lines.join('\\n');
  document.getElementById('main-form').submit();
}
</script>
</body>
</html>
"""

# ================= GROUP =================
GROUP_HTML = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>گروه‌بندی</title>
<style>{{ css }}</style>
</head>
<body>
<div class="top-bar">
  <div class="ball-icon">🏓</div>
  <h1>گروه‌بندی مسابقات</h1>
  <span class="sub">{{ groups|length }} گروه</span>
</div>

<div class="wrap">
  <div class="groups-grid stagger">
  {% for g in groups %}
  {% set gid = loop.index0 %}
    <div class="group-card">
      <div class="group-head">
        <span class="g-title">گروه {{ loop.index }}</span>
        <span class="g-num">{{ loop.index }}</span>
      </div>
      <div class="group-body">
        {% set clubs = g | map(attribute='club') | list %}
        {% set same = [] %}
        {% for i in range(clubs|length) %}
          {% for j in range(i+1, clubs|length) %}
            {% if clubs[i] and clubs[j] and clubs[i] == clubs[j] %}{% if same.append(1) %}{% endif %}{% endif %}
          {% endfor %}
        {% endfor %}
        {% if same %}
        <div class="warn-pill">⚠️ هم‌باشگاهی (اجتناب‌ناپذیر)</div>
        {% endif %}

        {% for p in g %}
        <div class="player-row">
          <div class="player-avatar">{{ p["name"][0] }}</div>
          <span class="player-name">{{ p["name"] }}</span>
          <span class="level-badge level-{{ p['level'] }}">سطح {{ p["level"] }}</span>
          {% if p["club"] %}<span class="club-pill">{{ p["club"] }}</span>{% endif %}
        </div>
        {% endfor %}

        <div class="divider"></div>
        <div class="section-label">مسابقات</div>

        {% for m in matches[gid] %}
        {% set mid = loop.index0 %}
        <div class="match-card" id="match-{{ gid }}-{{ mid }}">
          <div class="match-vs">
            {{ m["p1"]["name"] }}
            <span class="vs-tag">vs</span>
            {{ m["p2"]["name"] }}
          </div>
          {% if m.get("done") %}
          <div class="done-tag">
            <span class="done-dot"></span>
            انجام شد — برنده: {{ m["winner"]["name"] }}
          </div>
          {% else %}
          <div class="score-row">
            <input class="score-input" type="number" id="s1-{{ gid }}-{{ mid }}" placeholder="{{ m['p1']['name'] }}" min="0">
            <span class="score-sep">—</span>
            <input class="score-input" type="number" id="s2-{{ gid }}-{{ mid }}" placeholder="{{ m['p2']['name'] }}" min="0">
          </div>
          <div class="win-row">
            <button class="btn-win" onclick="saveMatch({{ gid }}, {{ mid }}, 0, this)">🏆 {{ m["p1"]["name"] }}</button>
            <button class="btn-win" onclick="saveMatch({{ gid }}, {{ mid }}, 1, this)">🏆 {{ m["p2"]["name"] }}</button>
          </div>
          {% endif %}
        </div>
        {% endfor %}
      </div>
    </div>
  {% endfor %}
  </div>

  <button class="btn-final" onclick="window.location.href='/final'">
    🏆 &nbsp; نمایش رتبه‌بندی نهایی
  </button>
</div>

<script>
function saveMatch(gid, mid, winner, btn) {
  const s1 = document.getElementById('s1-' + gid + '-' + mid)?.value || '';
  const s2 = document.getElementById('s2-' + gid + '-' + mid)?.value || '';

  // disable buttons to prevent double-click
  const card = document.getElementById('match-' + gid + '-' + mid);
  card.querySelectorAll('.btn-win').forEach(b => b.disabled = true);

  fetch('/save_ajax', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({g: gid, m: mid, w: winner, s1: s1, s2: s2})
  })
  .then(r => r.json())
  .then(data => {
    if (data.ok) {
      // replace content of match card in place
      const winnerName = data.winner_name;
      card.innerHTML = `
        <div class="match-vs">
          ${data.p1_name}
          <span class="vs-tag">vs</span>
          ${data.p2_name}
        </div>
        <div class="done-tag">
          <span class="done-dot"></span>
          انجام شد — برنده: ${winnerName}
        </div>
      `;
    } else {
      card.querySelectorAll('.btn-win').forEach(b => b.disabled = false);
      alert('خطا: ' + data.error);
    }
  })
  .catch(() => {
    card.querySelectorAll('.btn-win').forEach(b => b.disabled = false);
    alert('خطا در ارتباط با سرور');
  });
}
</script>
</body>
</html>
"""

# ================= FINAL =================
FINAL_HTML = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>نتایج نهایی</title>
<style>{{ css }}</style>
</head>
<body>
<div class="top-bar">
  <div class="ball-icon">🏆</div>
  <h1>نتایج نهایی</h1>
  <span class="sub">{{ results|length }} گروه</span>
</div>

<div class="final-wrap">
  <div class="final-head">
    <h1>🏆 رتبه‌بندی نهایی</h1>
    <p>صعودکنندگان نفر اول و دوم هر گروه هستند</p>
  </div>

  <div class="stagger">
  {% for g in results %}
  <div class="result-card">
    <div class="result-head">گروه {{ loop.index }}</div>
    <div class="result-body">
      <div class="podium-row">
        <span class="podium-medal">🥇</span>
        <span class="podium-name">{{ g[0]["name"] }}</span>
        {% if g[0]["club"] %}<span class="podium-club">{{ g[0]["club"] }}</span>{% endif %}
      </div>
      <div class="podium-row">
        <span class="podium-medal">🥈</span>
        <span class="podium-name">{{ g[1]["name"] }}</span>
        {% if g[1]["club"] %}<span class="podium-club">{{ g[1]["club"] }}</span>{% endif %}
      </div>
      {% if g|length > 2 %}
      <div class="podium-row">
        <span class="podium-medal">🥉</span>
        <span class="podium-name">{{ g[2]["name"] }}</span>
        {% if g[2]["club"] %}<span class="podium-club">{{ g[2]["club"] }}</span>{% endif %}
      </div>
      {% endif %}
      <div class="advance-tag">🚀 صعود: {{ g[0]["name"] }} و {{ g[1]["name"] }}</div>
    </div>
  </div>
  {% endfor %}
  </div>

  <button class="btn-final" onclick="window.location.href='/bracket'">
    🎯 &nbsp; جدول حذفی
  </button>
</div>
</body>
</html>
"""

# ================= BRACKET PAGE =================
BRACKET_HTML = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>جدول حذفی</title>
<style>{{ css }}</style>
<style>
/* extra bracket styles */
.bracket-outer { overflow-x: auto; padding-bottom: 24px; }
.bracket-tree {
  display: flex;
  flex-direction: row;
  align-items: stretch;
  gap: 0;
  direction: ltr;
  min-width: max-content;
}
.round-col {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.round-title {
  font-size: 11px; font-weight: 700; color: var(--muted);
  letter-spacing: .8px; padding: 0 20px 12px;
  text-align: center;
  white-space: nowrap;
}
.round-matches {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  flex: 1;
  gap: 0;
  position: relative;
}
.match-block {
  display: flex;
  align-items: center;
  position: relative;
}
.match-node {
  width: 160px;
  border: 1.5px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
  background: var(--surface);
  box-shadow: var(--shadow);
  flex-shrink: 0;
}
.match-player {
  padding: 9px 12px;
  font-size: 13px; font-weight: 600;
  display: flex; align-items: center; gap: 7px;
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  transition: background .15s;
  min-height: 38px;
  user-select: none;
}
.match-player:last-child { border-bottom: none; }
.match-player:hover:not(.bye):not(.won) { background: #f0f9ff; }
.match-player.won { background: #dcfce7; color: #15803d; font-weight: 700; }
.match-player.bye { color: var(--muted); font-style: italic; font-size: 12px; cursor: default; }
.match-player .pnum {
  width: 18px; height: 18px; border-radius: 50%;
  background: var(--border); color: var(--muted);
  font-size: 10px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.match-player.won .pnum { background: #bbf7d0; color: #15803d; }

/* connector lines */
.conn-right {
  width: 20px; height: 2px;
  background: var(--border);
  flex-shrink: 0;
}
.conn-wrap {
  display: flex; flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  width: 20px;
  position: relative;
}

.champ-col {
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  padding: 0 20px;
}
.champ-box {
  text-align: center;
  padding: 24px 20px;
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  border: 1.5px solid #fbbf24;
  border-radius: var(--radius);
  min-width: 160px;
}
.champ-box .trophy { font-size: 36px; }
.champ-box .cl { font-size: 11px; font-weight: 700; color: #92400e; margin-top: 8px; }
.champ-box .cn { font-size: 16px; font-weight: 900; color: #78350f; margin-top: 4px; min-height: 24px; }
</style>
</head>
<body>
<div class="top-bar">
  <div class="ball-icon">🎯</div>
  <h1>جدول حذفی</h1>
  <span class="sub">مرحله نهایی</span>
</div>

<div class="wrap">

  <!-- Tabs -->
  <div class="bracket-tabs">
    <button class="tab-btn {% if mode=='auto' %}active{% endif %}" onclick="setMode('auto')">🤖 خودکار (از گروه‌ها)</button>
    <button class="tab-btn {% if mode=='manual' %}active{% endif %}" onclick="setMode('manual')">✏️ دستی</button>
  </div>

  <!-- Auto mode info -->
  <div id="auto-panel" style="{% if mode!='auto' %}display:none{% endif %}">
    {% if auto_names %}
    <div class="hint-box" style="margin-bottom:20px;">
      <b>صعودکنندگان خودکار:</b><br>
      {% for n in auto_names %}{{ n }}{% if not loop.last %} ، {% endif %}{% endfor %}
    </div>
    {% else %}
    <div class="hint-box" style="margin-bottom:20px; background:#fff7ed; border-color:#fed7aa; color:#9a3412;">
      هنوز نتیجه‌ای ثبت نشده. ابتدا مرحله گروهی را تکمیل کنید یا از حالت دستی استفاده کنید.
    </div>
    {% endif %}
  </div>

  <!-- Manual mode input -->
  <div id="manual-panel" style="{% if mode!='manual' %}display:none{% endif %}">
    <div class="bracket-input-area">
      <h3>ورود دستی بازیکنان</h3>
      <p>اسامی بازیکنان را وارد کنید. سیستم به صورت خودکار جدول حذفی می‌سازد. اسامی تکراری در نظر گرفته می‌شوند.</p>
      <div class="names-grid" id="names-grid">
        <input class="name-input" placeholder="بازیکن ۱" id="p0">
        <input class="name-input" placeholder="بازیکن ۲" id="p1">
        <input class="name-input" placeholder="بازیکن ۳" id="p2">
        <input class="name-input" placeholder="بازیکن ۴" id="p3">
      </div>
      <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center;">
        <button class="btn-build" onclick="addMore()">+ افزودن بازیکن</button>
        <button class="btn-build" onclick="buildManual()" style="background:linear-gradient(135deg,var(--green),#059669);">🎯 ساخت جدول</button>
      </div>
    </div>
  </div>

  <!-- Bracket display -->
  <div id="bracket-display">
    {% if bracket %}
    {{ bracket_html | safe }}
    {% endif %}
  </div>

</div>

<script>
let currentMode = '{{ mode }}';
let playerCount = 4;

function setMode(m) {
  currentMode = m;
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  document.getElementById('auto-panel').style.display = (m === 'auto') ? '' : 'none';
  document.getElementById('manual-panel').style.display = (m === 'manual') ? '' : 'none';
  if (m === 'auto') {
    fetchBracket({{ auto_names | tojson }});
  }
}

function addMore() {
  const grid = document.getElementById('names-grid');
  const inp = document.createElement('input');
  inp.className = 'name-input';
  inp.placeholder = 'بازیکن ' + (playerCount + 1);
  inp.id = 'p' + playerCount;
  grid.appendChild(inp);
  playerCount++;
  inp.focus();
}

function buildManual() {
  const names = [];
  for (let i = 0; i < playerCount; i++) {
    const el = document.getElementById('p' + i);
    if (el && el.value.trim()) names.push(el.value.trim());
  }
  if (names.length < 2) { alert('حداقل ۲ بازیکن وارد کنید'); return; }
  fetchBracket(names);
}

function fetchBracket(names) {
  fetch('/bracket_build', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({names: names})
  })
  .then(r => r.json())
  .then(data => {
    document.getElementById('bracket-display').innerHTML = data.html;
  });
}

function pickWinner(matchId, slot) {
  fetch('/bracket_pick', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({match_id: matchId, slot: slot})
  })
  .then(r => r.json())
  .then(data => {
    document.getElementById('bracket-display').innerHTML = data.html;
  });
}

// Auto-load bracket if in auto mode and names exist
{% if mode == 'auto' and auto_names %}
window.addEventListener('DOMContentLoaded', () => fetchBracket({{ auto_names | tojson }}));
{% endif %}
</script>
</body>
</html>
"""


# ================= LOGIC =================

def make(name, level, club=""):
    return {"name": name, "level": level, "club": club, "win": 0, "sf": 0, "sa": 0}

def rank(group):
    return sorted(group, key=lambda x: (x["win"], x["sf"] - x["sa"]), reverse=True)

def group_conflicts(group):
    count = 0
    for i in range(len(group)):
        for j in range(i + 1, len(group)):
            if group[i]["club"] and group[j]["club"] and group[i]["club"] == group[j]["club"]:
                count += 1
    return count

def assign_groups_optimized(strong, medium, weak):
    n = len(strong)

    def spread_by_club(lst):
        buckets = defaultdict(list)
        for p in lst:
            key = p.get("club") or "__none__"
            buckets[key].append(p)
        result = []
        while any(buckets.values()):
            for k in list(buckets.keys()):
                if buckets[k]:
                    result.append(buckets[k].pop(0))
        return result

    strong_s = spread_by_club(strong)
    medium_s = spread_by_club(medium)
    weak_s   = spread_by_club(weak)

    groups_raw = [[strong_s[i], medium_s[i], weak_s[i]] for i in range(n)]

    improved = True
    max_iter = n * 5
    iteration = 0

    while improved and iteration < max_iter:
        improved = False
        iteration += 1
        for i in range(n):
            for j in range(i + 1, n):
                for level_idx in range(3):
                    before = group_conflicts(groups_raw[i]) + group_conflicts(groups_raw[j])
                    groups_raw[i][level_idx], groups_raw[j][level_idx] = groups_raw[j][level_idx], groups_raw[i][level_idx]
                    after = group_conflicts(groups_raw[i]) + group_conflicts(groups_raw[j])
                    if after < before:
                        improved = True
                    else:
                        groups_raw[i][level_idx], groups_raw[j][level_idx] = groups_raw[j][level_idx], groups_raw[i][level_idx]

    return groups_raw


# ========== BRACKET LOGIC ==========

# In-memory bracket state
bracket_state = {
    "rounds": [],   # list of rounds; each round is list of matches
    # match = {"p1": name, "p2": name, "winner": name or None}
}

def build_bracket(names):
    """Build a single-elimination bracket from a list of names. Pads with BYE if not power of 2."""
    import math
    n = len(names)
    if n < 2:
        return []
    # next power of 2
    size = 1
    while size < n:
        size *= 2
    # pad with BYE
    padded = names[:] + ["BYE"] * (size - n)
    # shuffle so BYEs spread out
    random.shuffle(padded)
    # build rounds
    rounds = []
    current = padded
    while len(current) > 1:
        matches = []
        for i in range(0, len(current), 2):
            p1 = current[i]
            p2 = current[i+1]
            # auto-advance if BYE
            winner = None
            if p1 == "BYE":
                winner = p2
            elif p2 == "BYE":
                winner = p1
            matches.append({"p1": p1, "p2": p2, "winner": winner})
        rounds.append(matches)
        # next round placeholders
        current = [m["winner"] if m["winner"] else "TBD" for m in matches]
        if len(current) == 1:
            break
    return rounds


def render_bracket_html(rounds):
    """Render bracket as HTML string."""
    if not rounds:
        return "<p style='color:var(--muted);padding:20px;'>جدول خالی است.</p>"

    round_labels = {1: "فینال", 2: "نیمه‌نهایی", 4: "یک‌چهارم", 8: "یک‌هشتم", 16: "یک‌شانزدهم"}

    html = '<div class="bracket-outer"><div class="bracket-tree">'

    for ri, round_matches in enumerate(rounds):
        size = len(round_matches)
        label = round_labels.get(size, f"دور {ri+1}")
        html += f'<div class="round-col">'
        html += f'<div class="round-title">{label}</div>'
        html += f'<div class="round-matches">'

        for mi, m in enumerate(round_matches):
            match_id = f"{ri}-{mi}"
            p1_class = "match-player"
            p2_class = "match-player"
            if m["p1"] == "BYE": p1_class += " bye"
            if m["p2"] == "BYE": p2_class += " bye"
            if m["winner"] == m["p1"] and m["p1"] != "BYE": p1_class += " won"
            if m["winner"] == m["p2"] and m["p2"] != "BYE": p2_class += " won"

            p1_click = "" if "bye" in p1_class or m.get("winner") else f"onclick=\"pickWinner('{match_id}',0)\""
            p2_click = "" if "bye" in p2_class or m.get("winner") else f"onclick=\"pickWinner('{match_id}',1)\""

            p1_lbl = m["p1"] if m["p1"] not in ("BYE","TBD") else ("BYE" if m["p1"]=="BYE" else "—")
            p2_lbl = m["p2"] if m["p2"] not in ("BYE","TBD") else ("BYE" if m["p2"]=="BYE" else "—")

            html += f'''
            <div class="match-block" style="margin: 12px 0;">
              <div class="match-node">
                <div class="{p1_class}" {p1_click}>
                  <span class="pnum">1</span>{p1_lbl}
                </div>
                <div class="{p2_class}" {p2_click}>
                  <span class="pnum">2</span>{p2_lbl}
                </div>
              </div>
              <div class="conn-right"></div>
            </div>
            '''

        html += '</div></div>'

        # connector column between rounds
        if ri < len(rounds) - 1:
            html += '<div style="display:flex;flex-direction:column;justify-content:space-around;padding:0 0 0 0;">'
            # vertical lines
            html += '</div>'

    # champion
    last_round = rounds[-1]
    champ = last_round[0]["winner"] if last_round and last_round[0]["winner"] else "؟"
    html += f'''
    <div class="champ-col">
      <div class="round-title">🏆 قهرمان</div>
      <div class="champ-box">
        <div class="trophy">🏆</div>
        <div class="cl">قهرمان</div>
        <div class="cn">{champ if champ not in ("BYE","TBD","؟") else "؟"}</div>
      </div>
    </div>
    '''

    html += '</div></div>'
    return html


# ================= ROUTES =================

@app.route("/")
def home():
    return render_template_string(HOME_HTML, css=SHARED_CSS, error=None)

@app.route("/create", methods=["POST"])
def create():
    raw = request.form.get("players", "").strip().splitlines()
    players = []
    for line in raw:
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 2:
            return render_template_string(HOME_HTML, css=SHARED_CSS,
                error=f"خط «{line}» فرمت درست ندارد. باید اسم , سطح باشه.")
        name  = parts[0]
        try:
            level = int(parts[1])
            if level not in (1, 2, 3):
                raise ValueError
        except ValueError:
            return render_template_string(HOME_HTML, css=SHARED_CSS,
                error=f"سطح «{parts[1]}» معتبر نیست. باید 1، 2 یا 3 باشه.")
        club = parts[2] if len(parts) > 2 else ""
        players.append(make(name, level, club))

    if len(players) < 3:
        return render_template_string(HOME_HTML, css=SHARED_CSS,
            error="حداقل ۳ بازیکن نیاز داریم.")
    if len(players) % 3 != 0:
        return render_template_string(HOME_HTML, css=SHARED_CSS,
            error=f"تعداد بازیکنان ({len(players)}) باید مضرب ۳ باشه.")

    strong = [p for p in players if p["level"] == 1]
    medium = [p for p in players if p["level"] == 2]
    weak   = [p for p in players if p["level"] == 3]
    n = len(players) // 3
    if len(strong) != n or len(medium) != n or len(weak) != n:
        return render_template_string(HOME_HTML, css=SHARED_CSS,
            error=f"باید تعداد مساوی از هر سطح باشه. الان: قوی={len(strong)}, متوسط={len(medium)}, ضعیف={len(weak)}")

    random.shuffle(strong); random.shuffle(medium); random.shuffle(weak)
    groups = assign_groups_optimized(strong, medium, weak)

    tournament["groups"] = groups
    tournament["matches"] = []
    for g in groups:
        gm = []
        for i in range(len(g)):
            for j in range(i + 1, len(g)):
                gm.append({"p1": g[i], "p2": g[j], "done": False, "winner": None})
        tournament["matches"].append(gm)

    return render_template_string(GROUP_HTML, css=SHARED_CSS,
        groups=tournament["groups"], matches=tournament["matches"])

@app.route("/save_ajax", methods=["POST"])
def save_ajax():
    data = request.get_json()
    try:
        gid = int(data["g"])
        mid = int(data["m"])
        w   = int(data["w"])
        s1  = data.get("s1", "")
        s2  = data.get("s2", "")
    except (KeyError, ValueError, TypeError) as e:
        return jsonify({"ok": False, "error": str(e)})

    try:
        match = tournament["matches"][gid][mid]
    except IndexError:
        return jsonify({"ok": False, "error": "match not found"})

    winner = match["p1"] if w == 0 else match["p2"]
    loser  = match["p2"] if w == 0 else match["p1"]

    winner["win"] += 1
    try:
        score1 = int(s1) if s1 != "" else 0
        score2 = int(s2) if s2 != "" else 0
    except ValueError:
        score1 = score2 = 0

    if w == 0:
        winner["sf"] += score1; winner["sa"] += score2
        loser["sf"]  += score2; loser["sa"]  += score1
    else:
        winner["sf"] += score2; winner["sa"] += score1
        loser["sf"]  += score1; loser["sa"]  += score2

    match["done"]   = True
    match["winner"] = winner

    return jsonify({
        "ok": True,
        "winner_name": winner["name"],
        "p1_name": match["p1"]["name"],
        "p2_name": match["p2"]["name"],
    })

@app.route("/final", methods=["GET", "POST"])
def final():
    results = []
    for g in tournament["groups"]:
        results.append(rank(g))
    return render_template_string(FINAL_HTML, css=SHARED_CSS, results=results)

@app.route("/bracket")
def bracket_page():
    # Collect auto names: top 2 from each group
    auto_names = []
    for g in tournament["groups"]:
        ranked = rank(g)
        if len(ranked) >= 2:
            auto_names.append(ranked[0]["name"])
            auto_names.append(ranked[1]["name"])

    return render_template_string(BRACKET_HTML, css=SHARED_CSS,
        mode="auto",
        auto_names=auto_names,
        bracket=None,
        bracket_html="")

@app.route("/bracket_build", methods=["POST"])
def bracket_build():
    data = request.get_json()
    names = data.get("names", [])
    names = [n for n in names if n and n != "BYE"]
    if len(names) < 2:
        return jsonify({"html": "<p style='color:var(--red);padding:20px;'>حداقل ۲ بازیکن لازم است.</p>"})

    rounds = build_bracket(names)
    bracket_state["rounds"] = rounds
    html = render_bracket_html(rounds)
    return jsonify({"html": html})

@app.route("/bracket_pick", methods=["POST"])
def bracket_pick():
    data = request.get_json()
    match_id = data.get("match_id", "")
    slot = int(data.get("slot", 0))

    try:
        ri, mi = [int(x) for x in match_id.split("-")]
        rounds = bracket_state["rounds"]
        match = rounds[ri][mi]
        winner = match["p1"] if slot == 0 else match["p2"]
        if winner in ("BYE", "TBD"):
            return jsonify({"html": render_bracket_html(rounds)})
        match["winner"] = winner

        # propagate to next round
        if ri + 1 < len(rounds):
            next_match_idx = mi // 2
            if mi % 2 == 0:
                rounds[ri + 1][next_match_idx]["p1"] = winner
            else:
                rounds[ri + 1][next_match_idx]["p2"] = winner
            # clear winner of next match since it changed
            next_m = rounds[ri + 1][next_match_idx]
            if next_m["winner"] not in (next_m["p1"], next_m["p2"]):
                next_m["winner"] = None
            # auto-advance if BYE
            if next_m["p1"] == "BYE":
                next_m["winner"] = next_m["p2"]
            elif next_m["p2"] == "BYE":
                next_m["winner"] = next_m["p1"]

    except Exception as e:
        pass

    html = render_bracket_html(bracket_state["rounds"])
    return jsonify({"html": html})

if __name__ == "__main__":
    app.run(debug=True)
