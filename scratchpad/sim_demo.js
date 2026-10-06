// Pulls the pure functions of the canvas demo out of index.html (resolve,
// pairsOf, cascadeAt, fire, land) and runs thousands of shots with no browser.
// It is the only way to measure the rate of matches and combos: in the browser
// rAF drops to 1 fps with the window in the background and the measurement lies.
//
//     node scratchpad/sim_demo.js
const fs = require('fs');
const path = require('path');

// Resolved from this file, so the script works from any clone and any folder.
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');

function num(re, name) {
  const m = html.match(re);
  if (!m) throw new Error('cannot find ' + name);
  return parseFloat(m[1]);
}
const NCOL = (html.match(/var NAMES = \[([^\]]+)\]/)[1].match(/'/g).length) / 2;
const BIAS = num(/Math\.random\(\) < ([\d.]+)\) \? tail\.c/, 'pair bias');
const PREF = num(/multi\.length && Math\.random\(\) < ([\d.]+)\)/, 'cascade preference');
const GUN  = num(/Math\.random\(\) < ([\d.]+)\)\{\s*[\r\n]+\s*var opts/, 'gun bias');
const MAXC = num(/chain\.length < (\d+) &&/, 'chain cap');

const R = () => Math.floor(Math.random() * NCOL);

let chain = [];
for (let i = 0; i < MAXC; i++) {
  const prv = chain[i - 1];
  chain.push((prv !== undefined && Math.random() < BIAS) ? prv : R());
}

let popped = 0, matches = 0;
const comboHist = {};

function resolve(i, depth) {
  const c = chain[i];
  if (c === undefined) return;
  let a = i, b = i;
  while (a - 1 >= 0 && chain[a - 1] === c) a--;
  while (b + 1 < chain.length && chain[b + 1] === c) b++;
  const n = b - a + 1;
  if (n < 3) return;
  chain.splice(a, n);
  popped += n; matches++;
  if (depth >= 2) comboHist['x' + depth] = (comboHist['x' + depth] || 0) + 1;
  if (a > 0 && a < chain.length && chain[a - 1] === chain[a]) resolve(a, depth + 1);
}

function pairsOf(c) {
  const out = [];
  for (let i = 0; i + 1 < chain.length; i++) if (chain[i] === c && chain[i + 1] === c) out.push(i);
  return out;
}

function cascadeAt(i, col) {
  const arr = chain.slice();
  arr.splice(i, 0, col);
  let depth = 0, at = i;
  while (true) {
    const c = arr[at];
    if (c === undefined) break;
    let a = at, b = at;
    while (a - 1 >= 0 && arr[a - 1] === c) a--;
    while (b + 1 < arr.length && arr[b + 1] === c) b++;
    if (b - a + 1 < 3) break;
    arr.splice(a, b - a + 1); depth++;
    if (a > 0 && a < arr.length && arr[a - 1] === arr[a]) at = a; else break;
  }
  return depth;
}

let next = R();
function loadGun() {
  if (Math.random() < GUN) {
    const opts = [];
    for (let c = 0; c < NCOL; c++) if (pairsOf(c).length) opts.push(c);
    if (opts.length) { next = opts[Math.floor(Math.random() * opts.length)]; return; }
  }
  next = R();
}
loadGun();

const SHOTS = 4000;
let noMatch = 0;
for (let s = 0; s < SHOTS; s++) {
  // refill from the tail, with the same pair bias the game uses
  while (chain.length < MAXC) {
    const tail = chain[chain.length - 1];
    chain.push((tail !== undefined && Math.random() < BIAS) ? tail : R());
  }
  const col = next;
  let cand = pairsOf(col), idx = -1;
  if (cand.length) {
    const multi = cand.filter(i => cascadeAt(i, col) >= 2);
    const pool = (multi.length && Math.random() < PREF) ? multi : cand;
    idx = pool[Math.floor(Math.random() * pool.length)];
  }
  if (idx < 0) {
    const same = []; for (let i = 0; i < chain.length; i++) if (chain[i] === col) same.push(i);
    idx = same.length ? same[Math.floor(Math.random() * same.length)]
                      : Math.floor(Math.random() * chain.length);
  }
  const before = matches;
  chain.splice(idx, 0, col);
  resolve(idx, 1);
  if (matches === before) noMatch++;
  loadGun();
}

const combos = Object.values(comboHist).reduce((a, b) => a + b, 0);
console.log('  colours in play       ', NCOL);
console.log('  pair bias             ', BIAS, ' cascade preference', PREF, ' gun', GUN);
console.log('  shots simulated       ', SHOTS);
console.log('  shots that match      ', ((SHOTS - noMatch) * 100 / SHOTS).toFixed(1) + '%');
console.log('  orbs burst per shot   ', (popped / SHOTS).toFixed(2));
console.log('  COMBOS (cascades)     ', (combos * 100 / SHOTS).toFixed(1) + '% of the shots', comboHist);
console.log('  -> at one shot every ~1.6 s, a combo every',
            (1.6 * SHOTS / Math.max(combos, 1)).toFixed(0), 'seconds');
