/* ============================================================
   DPM Learning Hub — Excel formula engine (no dependencies)
   Supports a curated, well-tested subset of Excel functions
   evaluated against a sample grid (headers in row 1, data 2+).
   Exposes window.ExcelEngine.evaluate(formula, grid)
   ============================================================ */
(function (root) {
  'use strict';

  // ---------- helpers ----------
  function colToNum(letters) { // "A"->1, "AA"->27
    let n = 0;
    for (let i = 0; i < letters.length; i++) n = n * 26 + (letters.charCodeAt(i) - 64);
    return n;
  }
  function isBlank(v) { return v === null || v === undefined || v === ''; }
  function toNum(v) {
    if (typeof v === 'number') return v;
    if (typeof v === 'boolean') return v ? 1 : 0;
    if (isBlank(v)) return 0;
    const n = Number(String(v).replace(/,/g, ''));
    if (isNaN(n)) throw new CellError('#VALUE!');
    return n;
  }
  function CellError(code) { this.isError = true; this.code = code; }
  CellError.prototype.toString = function () { return this.code; };

  // ---------- tokenizer ----------
  function tokenize(src) {
    const toks = [];
    let i = 0;
    const ops = ['<=', '>=', '<>', '+', '-', '*', '/', '^', '&', '=', '<', '>', '(', ')', ',', '%', ':'];
    while (i < src.length) {
      const c = src[i];
      if (c === ' ' || c === '\t' || c === '\n' || c === '\r') { i++; continue; }
      if (c === '"') { // string
        let j = i + 1, s = '';
        while (j < src.length) {
          if (src[j] === '"' && src[j + 1] === '"') { s += '"'; j += 2; continue; }
          if (src[j] === '"') break;
          s += src[j++];
        }
        if (src[j] !== '"') throw new CellError('#PARSE!');
        toks.push({ t: 'str', v: s }); i = j + 1; continue;
      }
      if (/[0-9.]/.test(c)) { // number
        let j = i, s = '';
        while (j < src.length && /[0-9.]/.test(src[j])) s += src[j++];
        toks.push({ t: 'num', v: parseFloat(s) }); i = j; continue;
      }
      // two-char ops first
      const two = src.substr(i, 2);
      if (['<=', '>=', '<>'].includes(two)) { toks.push({ t: 'op', v: two }); i += 2; continue; }
      if (ops.includes(c)) { toks.push({ t: 'op', v: c }); i++; continue; }
      if (/[A-Za-z_$]/.test(c)) { // identifier / cell / function / bool
        let j = i, s = '';
        while (j < src.length && /[A-Za-z0-9_$.]/.test(src[j])) s += src[j++];
        // function call if followed by (
        let k = j; while (k < src.length && /\s/.test(src[k])) k++;
        if (src[k] === '(') { toks.push({ t: 'func', v: s.toUpperCase() }); i = j; continue; }
        const up = s.toUpperCase();
        if (up === 'TRUE') { toks.push({ t: 'num', v: 1, bool: true }); i = j; continue; }
        if (up === 'FALSE') { toks.push({ t: 'num', v: 0, bool: true }); i = j; continue; }
        // cell or range token (e.g. A1, $A$1, A:A) — ref part captured, ranges handled by ':' op
        toks.push({ t: 'ref', v: s.toUpperCase() }); i = j; continue;
      }
      throw new CellError('#PARSE!');
    }
    return toks;
  }

  // ---------- parser (recursive descent) ----------
  // precedence: compare < & < +- < */ < ^ < unary < postfix% < primary
  function parse(toks) {
    let p = 0;
    const peek = () => toks[p];
    const next = () => toks[p++];
    function expect(v) { if (!peek() || peek().v !== v) throw new CellError('#PARSE!'); return next(); }

    function parseCompare() {
      let left = parseConcat();
      while (peek() && peek().t === 'op' && ['=', '<>', '<', '>', '<=', '>='].includes(peek().v)) {
        const op = next().v; const right = parseConcat();
        left = { type: 'binop', op, left, right };
      }
      return left;
    }
    function parseConcat() {
      let left = parseAdd();
      while (peek() && peek().t === 'op' && peek().v === '&') { next(); left = { type: 'binop', op: '&', left, right: parseAdd() }; }
      return left;
    }
    function parseAdd() {
      let left = parseMul();
      while (peek() && peek().t === 'op' && (peek().v === '+' || peek().v === '-')) { const op = next().v; left = { type: 'binop', op, left, right: parseMul() }; }
      return left;
    }
    function parseMul() {
      let left = parsePow();
      while (peek() && peek().t === 'op' && (peek().v === '*' || peek().v === '/')) { const op = next().v; left = { type: 'binop', op, left, right: parsePow() }; }
      return left;
    }
    function parsePow() {
      let left = parseUnary();
      while (peek() && peek().t === 'op' && peek().v === '^') { next(); left = { type: 'binop', op: '^', left, right: parseUnary() }; }
      return left;
    }
    function parseUnary() {
      if (peek() && peek().t === 'op' && (peek().v === '-' || peek().v === '+')) { const op = next().v; return { type: 'unary', op, arg: parseUnary() }; }
      return parsePostfix();
    }
    function parsePostfix() {
      let node = parsePrimary();
      while (peek() && peek().t === 'op' && peek().v === '%') { next(); node = { type: 'percent', arg: node }; }
      return node;
    }
    function parsePrimary() {
      const tk = peek();
      if (!tk) throw new CellError('#PARSE!');
      if (tk.t === 'num') { next(); return { type: 'num', v: tk.v }; }
      if (tk.t === 'str') { next(); return { type: 'str', v: tk.v }; }
      if (tk.t === 'op' && tk.v === '(') { next(); const e = parseCompare(); expect(')'); return e; }
      if (tk.t === 'func') {
        const name = next().v; expect('(');
        const args = [];
        if (peek() && !(peek().t === 'op' && peek().v === ')')) {
          args.push(parseCompare());
          while (peek() && peek().t === 'op' && peek().v === ',') { next(); args.push(parseCompare()); }
        }
        expect(')');
        return { type: 'func', name, args };
      }
      if (tk.t === 'ref') {
        next();
        // range?  ref ':' ref
        if (peek() && peek().t === 'op' && peek().v === ':') {
          next(); const r2 = peek();
          if (!r2 || r2.t !== 'ref') throw new CellError('#PARSE!');
          next();
          return { type: 'range', a: tk.v, b: r2.v };
        }
        return { type: 'ref', v: tk.v };
      }
      throw new CellError('#PARSE!');
    }
    const tree = parseCompare();
    if (p !== toks.length) throw new CellError('#PARSE!');
    return tree;
  }

  // ---------- grid access ----------
  function makeGrid(headers, rows) {
    // row 1 = headers; data rows 2..(rows.length+1)
    const nCols = headers.length;
    const nRows = rows.length + 1;
    function cell(colLetters, rowNum) {
      const c = colToNum(colLetters);
      if (c < 1 || c > nCols || rowNum < 1 || rowNum > nRows) return null;
      if (rowNum === 1) return headers[c - 1];
      return rows[rowNum - 2][c - 1];
    }
    return { nCols, nRows, cell };
  }
  function parseRef(ref) { // "$A$2" -> {col:'A', row:2}
    const m = /^\$?([A-Z]+)\$?([0-9]+)$/.exec(ref);
    if (!m) return null;
    return { col: m[1], row: parseInt(m[2], 10) };
  }
  function parseColOnly(ref) { const m = /^\$?([A-Z]+)$/.exec(ref); return m ? m[1] : null; }

  function resolveRange(node, grid) {
    // returns flat array of values
    const aCol = parseColOnly(node.a), bCol = parseColOnly(node.b);
    if (aCol && bCol) { // whole-column range A:A
      const c1 = colToNum(aCol), c2 = colToNum(bCol);
      const out = [];
      for (let c = Math.min(c1, c2); c <= Math.max(c1, c2); c++)
        for (let r = 1; r <= grid.nRows; r++) out.push(grid.cell(numToCol(c), r));
      return { values: out, rectCols: Math.abs(c2 - c1) + 1, rectRows: grid.nRows };
    }
    const a = parseRef(node.a), b = parseRef(node.b);
    if (!a || !b) throw new CellError('#REF!');
    const c1 = colToNum(a.col), c2 = colToNum(b.col);
    const r1 = a.row, r2 = b.row;
    const out = [];
    for (let r = Math.min(r1, r2); r <= Math.max(r1, r2); r++)
      for (let c = Math.min(c1, c2); c <= Math.max(c1, c2); c++)
        out.push(grid.cell(numToCol(c), r));
    return { values: out, rectCols: Math.abs(c2 - c1) + 1, rectRows: Math.abs(r2 - r1) + 1 };
  }
  function numToCol(n) { let s = ''; while (n > 0) { const m = (n - 1) % 26; s = String.fromCharCode(65 + m) + s; n = (n - m - 1) / 26; } return s; }

  // ---------- criteria (for *IF / *IFS) ----------
  function makeCriteria(crit) {
    let op = '=', val = crit;
    if (typeof crit === 'string') {
      const m = /^(<=|>=|<>|=|<|>)(.*)$/.exec(crit);
      if (m) { op = m[1]; val = m[2]; }
    }
    const numVal = (typeof val === 'number') ? val : (val !== '' && !isNaN(Number(val)) ? Number(val) : null);
    // wildcard handling for = / <>
    let regex = null;
    if ((op === '=' || op === '<>') && typeof val === 'string' && /[*?]/.test(val)) {
      regex = new RegExp('^' + val.replace(/[.+^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '.*').replace(/\?/g, '.') + '$', 'i');
    }
    return function (x) {
      if (regex) { const t = regex.test(String(x == null ? '' : x)); return op === '=' ? t : !t; }
      if (numVal !== null && typeof x === 'number') {
        switch (op) { case '=': return x === numVal; case '<>': return x !== numVal; case '<': return x < numVal; case '>': return x > numVal; case '<=': return x <= numVal; case '>=': return x >= numVal; }
      }
      const xs = String(x == null ? '' : x).toLowerCase();
      const vs = String(val).toLowerCase();
      switch (op) { case '=': return xs === vs; case '<>': return xs !== vs; case '<': return xs < vs; case '>': return xs > vs; case '<=': return xs <= vs; case '>=': return xs >= vs; }
      return false;
    };
  }

  // ---------- evaluator ----------
  function evalNode(node, grid) {
    switch (node.type) {
      case 'num': return node.v;
      case 'str': return node.v;
      case 'ref': {
        const r = parseRef(node.v);
        if (!r) throw new CellError('#REF!');
        return grid.cell(r.col, r.row);
      }
      case 'range': return resolveRange(node, grid); // returns {values,...}
      case 'unary': { const a = toNum(evalNode(node.arg, grid)); return node.op === '-' ? -a : a; }
      case 'percent': return toNum(evalNode(node.arg, grid)) / 100;
      case 'binop': return evalBin(node, grid);
      case 'func': return callFunc(node.name, node.args, grid);
    }
    throw new CellError('#PARSE!');
  }
  function scalar(v) { if (v && v.values) return v.values.length ? v.values[0] : null; return v; }
  function evalBin(node, grid) {
    const op = node.op;
    if (op === '&') return strOf(scalar(evalNode(node.left, grid))) + strOf(scalar(evalNode(node.right, grid)));
    const L = scalar(evalNode(node.left, grid)), R = scalar(evalNode(node.right, grid));
    if (['=', '<>', '<', '>', '<=', '>='].includes(op)) {
      let a = L, b = R;
      if (typeof a === 'number' && typeof b === 'number') { }
      else { a = String(a == null ? '' : a).toLowerCase(); b = String(b == null ? '' : b).toLowerCase(); }
      switch (op) { case '=': return a === b; case '<>': return a !== b; case '<': return a < b; case '>': return a > b; case '<=': return a <= b; case '>=': return a >= b; }
    }
    const a = toNum(L), b = toNum(R);
    switch (op) { case '+': return a + b; case '-': return a - b; case '*': return a * b; case '/': if (b === 0) throw new CellError('#DIV/0!'); return a / b; case '^': return Math.pow(a, b); }
    throw new CellError('#VALUE!');
  }
  function strOf(v) { if (v === true) return 'TRUE'; if (v === false) return 'FALSE'; if (isBlank(v)) return ''; return String(v); }
  function flat(args, grid) { // expand args into flat numeric-capable array of values
    const out = [];
    for (const a of args) { const v = evalNode(a, grid); if (v && v.values) out.push(...v.values); else out.push(v); }
    return out;
  }
  function nums(vals) { return vals.filter(v => typeof v === 'number' || (typeof v === 'string' && v !== '' && !isNaN(Number(v)))).map(v => typeof v === 'number' ? v : Number(v)); }

  const FN = {
    SUM: (a, g) => nums(flat(a, g)).reduce((s, x) => s + x, 0),
    SUMPRODUCT: (a, g) => {
      const arrs = a.map(n => { const v = evalNode(n, g); return v && v.values ? v.values.map(x => typeof x === 'number' ? x : (x === '' || x == null ? 0 : Number(x) || 0)) : [toNum(v)]; });
      const len = Math.max(...arrs.map(x => x.length));
      let s = 0; for (let i = 0; i < len; i++) { let p = 1; for (const arr of arrs) p *= (arr[i] || 0); s += p; } return s;
    },
    AVERAGE: (a, g) => { const n = nums(flat(a, g)); if (!n.length) throw new CellError('#DIV/0!'); return n.reduce((s, x) => s + x, 0) / n.length; },
    MEDIAN: (a, g) => { const n = nums(flat(a, g)).sort((x, y) => x - y); if (!n.length) throw new CellError('#NUM!'); const m = Math.floor(n.length / 2); return n.length % 2 ? n[m] : (n[m - 1] + n[m]) / 2; },
    COUNT: (a, g) => nums(flat(a, g)).length,
    COUNTA: (a, g) => flat(a, g).filter(v => !isBlank(v)).length,
    MIN: (a, g) => { const n = nums(flat(a, g)); return n.length ? Math.min(...n) : 0; },
    MAX: (a, g) => { const n = nums(flat(a, g)); return n.length ? Math.max(...n) : 0; },
    ROUND: (a, g) => { const x = toNum(scalar(evalNode(a[0], g))), d = a[1] ? toNum(scalar(evalNode(a[1], g))) : 0; const f = Math.pow(10, d); return Math.round(x * f) / f; },
    ROUNDUP: (a, g) => { const x = toNum(scalar(evalNode(a[0], g))), d = a[1] ? toNum(scalar(evalNode(a[1], g))) : 0; const f = Math.pow(10, d); return (x < 0 ? -1 : 1) * Math.ceil(Math.abs(x) * f) / f; },
    ROUNDDOWN: (a, g) => { const x = toNum(scalar(evalNode(a[0], g))), d = a[1] ? toNum(scalar(evalNode(a[1], g))) : 0; const f = Math.pow(10, d); return (x < 0 ? -1 : 1) * Math.floor(Math.abs(x) * f) / f; },
    INT: (a, g) => Math.floor(toNum(scalar(evalNode(a[0], g)))),
    ABS: (a, g) => Math.abs(toNum(scalar(evalNode(a[0], g)))),
    MOD: (a, g) => { const n = toNum(scalar(evalNode(a[0], g))), d = toNum(scalar(evalNode(a[1], g))); if (d === 0) throw new CellError('#DIV/0!'); return n - d * Math.floor(n / d); },
    IF: (a, g) => { const c = evalNode(a[0], g); const truthy = (c === true) || (typeof c === 'number' && c !== 0); return truthy ? scalar(evalNode(a[1], g)) : (a[2] !== undefined ? scalar(evalNode(a[2], g)) : false); },
    IFERROR: (a, g) => { try { return scalar(evalNode(a[0], g)); } catch (e) { if (e instanceof CellError) return scalar(evalNode(a[1], g)); throw e; } },
    AND: (a, g) => flat(a, g).every(v => (v === true) || (typeof v === 'number' && v !== 0)),
    OR: (a, g) => flat(a, g).some(v => (v === true) || (typeof v === 'number' && v !== 0)),
    NOT: (a, g) => { const c = scalar(evalNode(a[0], g)); return !((c === true) || (typeof c === 'number' && c !== 0)); },
    SUMIF: (a, g) => criteriaAgg(a, g, 'sum', 1),
    AVERAGEIF: (a, g) => criteriaAgg(a, g, 'avg', 1),
    COUNTIF: (a, g) => {
      const rng = evalNode(a[0], g).values; const pred = makeCriteria(scalar(evalNode(a[1], g)));
      return rng.filter(pred).length;
    },
    SUMIFS: (a, g) => criteriaAggS(a, g, 'sum'),
    AVERAGEIFS: (a, g) => criteriaAggS(a, g, 'avg'),
    COUNTIFS: (a, g) => {
      const pairs = []; for (let i = 0; i < a.length; i += 2) pairs.push([evalNode(a[i], g).values, makeCriteria(scalar(evalNode(a[i + 1], g)))]);
      const len = pairs[0][0].length; let c = 0;
      for (let i = 0; i < len; i++) if (pairs.every(([rng, pred]) => pred(rng[i]))) c++;
      return c;
    },
    VLOOKUP: (a, g) => {
      const key = scalar(evalNode(a[0], g)); const tbl = evalNode(a[1], g);
      const colIdx = toNum(scalar(evalNode(a[2], g)));
      const cols = tbl.rectCols, rows = tbl.rectRows, vals = tbl.values;
      for (let r = 0; r < rows; r++) {
        const first = vals[r * cols];
        if (String(first).toLowerCase() === String(key).toLowerCase()) return vals[r * cols + (colIdx - 1)];
      }
      throw new CellError('#N/A');
    },
    XLOOKUP: (a, g) => {
      const key = scalar(evalNode(a[0], g)); const lookup = evalNode(a[1], g).values; const ret = evalNode(a[2], g).values;
      for (let i = 0; i < lookup.length; i++) if (String(lookup[i]).toLowerCase() === String(key).toLowerCase()) return ret[i];
      if (a[3] !== undefined) return scalar(evalNode(a[3], g));
      throw new CellError('#N/A');
    },
    LEN: (a, g) => strOf(scalar(evalNode(a[0], g))).length,
    LEFT: (a, g) => strOf(scalar(evalNode(a[0], g))).slice(0, a[1] ? toNum(scalar(evalNode(a[1], g))) : 1),
    RIGHT: (a, g) => { const s = strOf(scalar(evalNode(a[0], g))); const n = a[1] ? toNum(scalar(evalNode(a[1], g))) : 1; return s.slice(s.length - n); },
    MID: (a, g) => strOf(scalar(evalNode(a[0], g))).substr(toNum(scalar(evalNode(a[1], g))) - 1, toNum(scalar(evalNode(a[2], g)))),
    UPPER: (a, g) => strOf(scalar(evalNode(a[0], g))).toUpperCase(),
    LOWER: (a, g) => strOf(scalar(evalNode(a[0], g))).toLowerCase(),
    PROPER: (a, g) => strOf(scalar(evalNode(a[0], g))).replace(/\w\S*/g, t => t.charAt(0).toUpperCase() + t.substr(1).toLowerCase()),
    TRIM: (a, g) => strOf(scalar(evalNode(a[0], g))).replace(/\s+/g, ' ').trim(),
    CONCAT: (a, g) => flat(a, g).map(strOf).join(''),
    CONCATENATE: (a, g) => flat(a, g).map(strOf).join(''),
    TEXTJOIN: (a, g) => {
      const delim = strOf(scalar(evalNode(a[0], g))); const ignore = (() => { const c = scalar(evalNode(a[1], g)); return (c === true) || (typeof c === 'number' && c !== 0); })();
      const rest = []; for (let i = 2; i < a.length; i++) { const v = evalNode(a[i], g); if (v && v.values) rest.push(...v.values); else rest.push(v); }
      return rest.map(strOf).filter(s => ignore ? s !== '' : true).join(delim);
    },
    YEAR: (a, g) => dateParts(scalar(evalNode(a[0], g))).y,
    MONTH: (a, g) => dateParts(scalar(evalNode(a[0], g))).m,
    DAY: (a, g) => dateParts(scalar(evalNode(a[0], g))).d,
    TODAY: () => { const d = new Date(); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  };
  function dateParts(v) { const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(String(v)); if (!m) throw new CellError('#VALUE!'); return { y: +m[1], m: +m[2], d: +m[3] }; }

  function criteriaAgg(a, g, mode, critIdx) {
    const rng = evalNode(a[0], g).values;
    const pred = makeCriteria(scalar(evalNode(a[critIdx], g)));
    const sumRange = a[2] ? evalNode(a[2], g).values : rng;
    let total = 0, cnt = 0;
    for (let i = 0; i < rng.length; i++) if (pred(rng[i])) { const x = sumRange[i]; if (typeof x === 'number') { total += x; cnt++; } else if (x !== '' && x != null && !isNaN(Number(x))) { total += Number(x); cnt++; } }
    if (mode === 'avg') { if (!cnt) throw new CellError('#DIV/0!'); return total / cnt; }
    return total;
  }
  function criteriaAggS(a, g, mode) {
    const sumRange = evalNode(a[0], g).values;
    const pairs = []; for (let i = 1; i < a.length; i += 2) pairs.push([evalNode(a[i], g).values, makeCriteria(scalar(evalNode(a[i + 1], g)))]);
    let total = 0, cnt = 0;
    for (let i = 0; i < sumRange.length; i++) {
      if (pairs.every(([rng, pred]) => pred(rng[i]))) { const x = sumRange[i]; if (typeof x === 'number') { total += x; cnt++; } else if (x !== '' && x != null && !isNaN(Number(x))) { total += Number(x); cnt++; } }
    }
    if (mode === 'avg') { if (!cnt) throw new CellError('#DIV/0!'); return total / cnt; }
    return total;
  }

  function callFunc(name, args, grid) {
    const fn = FN[name];
    if (!fn) throw new CellError('#NAME?');
    return fn(args, grid);
  }

  // ---------- public ----------
  function evaluate(formula, gridData) {
    let f = String(formula).trim();
    if (f[0] === '=') f = f.slice(1);
    if (!f) return { ok: false, error: 'Empty formula' };
    const grid = makeGrid(gridData.headers, gridData.rows);
    try {
      const toks = tokenize(f);
      const tree = parse(toks);
      let val = evalNode(tree, grid);
      val = scalar(val);
      if (val === true) val = 'TRUE'; else if (val === false) val = 'FALSE';
      if (typeof val === 'number' && !isFinite(val)) throw new CellError('#NUM!');
      if (typeof val === 'number') val = Math.round(val * 1e10) / 1e10;
      return { ok: true, value: isBlank(val) ? '(empty)' : val };
    } catch (e) {
      if (e instanceof CellError) return { ok: false, error: e.code };
      return { ok: false, error: 'Could not parse formula' };
    }
  }

  root.ExcelEngine = { evaluate };
  if (typeof module !== 'undefined' && module.exports) module.exports = root.ExcelEngine;
})(typeof window !== 'undefined' ? window : globalThis);
