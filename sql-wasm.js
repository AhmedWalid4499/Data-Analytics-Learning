/* ============================================================
   DPM Learning Hub — final-exam engine
   <div class="exam" data-bank="excelBank" data-count="9" data-typed="3"></div>
   <script type="application/json" id="excelBank">[ ...items ]</script>

   Item types:
     Multiple choice : {"q","opts":[...],"correct":0,"why"}            (default)
     Excel formula   : {"type":"formula","q","expect","answer","why", ...}
     SQL query       : {"type":"sql","q","expect","answer","why", ...}

   "formula" answers are evaluated with window.ExcelEngine; "sql" answers
   run against the shared SQLite DB (window.DPM_SQL_READY) — the same
   tables as the SQL runner. Both compare the produced value to "expect"
   (number within tol, or case-insensitive string). Randomised each attempt.
   Count attribute aliases: data-typed = data-formulas = data-sql.
   ============================================================ */
(function () {
  'use strict';

  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function esc(s) { return String(s); }
  function escAttr(s) { return String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;'); }
  function isTyped(it) { return it && (it.type === 'formula' || it.type === 'sql'); }

  function fmt(v) {
    if (typeof v === 'number') return (Math.round(v * 100) / 100).toLocaleString('en-US');
    return v;
  }
  function compare(got, exp, tol) {
    if (got === null || got === undefined) return false;
    if (typeof exp === 'number') { var t = (tol != null) ? tol : 0.01; var n = Number(got); return isFinite(n) && Math.abs(n - exp) <= t; }
    return String(got).trim().toLowerCase() === String(exp).trim().toLowerCase();
  }

  // ----- Excel formula evaluation -----
  function evalFormula(str) {
    if (!window.ExcelEngine || !window.DPM_DATA) return { ok: false, error: 'engine unavailable' };
    return window.ExcelEngine.evaluate(str, { headers: window.DPM_DATA.excelHeaders, rows: window.DPM_DATA.rows });
  }
  // ----- SQL evaluation against the shared DB -----
  function runSql(db, str) {
    try {
      var res = db.exec(str);
      if (!res.length || !res[res.length - 1].values.length) return { ok: true, value: null, rows: 0 };
      var last = res[res.length - 1];
      return { ok: true, value: last.values[0][0], rows: last.values.length };
    } catch (e) { return { ok: false, error: e.message }; }
  }

  function buildExam(host) {
    var bank;
    try { bank = JSON.parse(document.getElementById(host.dataset.bank).textContent); }
    catch (e) { host.innerHTML = '<p>Exam bank not found.</p>'; return; }

    var excelReady = !!(window.ExcelEngine && window.DPM_DATA);
    var bankHasSql = bank.some(function (i) { return i.type === 'sql'; });
    var sqlReady = bankHasSql ? (window.DPM_SQL_READY ||
      (window.initSqlJs && window.DPM_buildSqlDb
        ? window.initSqlJs({ locateFile: function (f) { return 'assets/vendor/' + f; } }).then(function (SQL) { return window.DPM_buildSqlDb(SQL); })
        : null)) : null;

    var typedItems = bank.filter(function (i) {
      if (i.type === 'formula') return excelReady;
      if (i.type === 'sql') return !!sqlReady;
      return false;
    });
    var mcItems = bank.filter(function (i) { return !isTyped(i); });

    var total = Math.min(parseInt(host.dataset.count || '8', 10), bank.length);
    var wantTyped = [host.dataset.typed, host.dataset.formulas, host.dataset.sql].filter(function (x) { return x != null; })[0];
    wantTyped = wantTyped != null ? parseInt(wantTyped, 10) : Math.min(3, typedItems.length);
    var nT = Math.min(wantTyped, typedItems.length, total);
    var nMC = Math.min(total - nT, mcItems.length);

    function render() {
      var picked = shuffle(typedItems).slice(0, nT).concat(shuffle(mcItems).slice(0, nMC));
      picked = shuffle(picked).map(function (q) {
        if (isTyped(q)) return { kind: q.type, q: q.q, why: q.why, expect: q.expect, tol: q.tol, answer: q.answer, hint: q.hint };
        var opts = q.opts.map(function (text, i) { return { text: text, correct: i === q.correct }; });
        return { kind: 'mc', q: q.q, why: q.why, opts: shuffle(opts) };
      });

      var typedLabel = nT ? (nT + ' you write &amp; we grade · ') : '';
      var html = '<div class="exam-head"><h3 style="margin:0">Final exam</h3>' +
        '<span class="meta">' + picked.length + ' questions · ' + typedLabel + 'randomised each attempt</span></div>' +
        '<p style="color:var(--ink-soft);margin:.2em 0 8px;font-size:.95rem">Answer each question — pick an option, or for the <b>write-it-yourself</b> ones type a real ' +
        (bankHasSql ? 'SQL query' : 'Excel formula') + ' against the sample data. Press <b>Test</b> to preview, then <b>Check answers</b> to grade. Hit <b>New set</b> for a fresh mix.</p>';

      picked.forEach(function (item, qi) {
        if (item.kind === 'mc') {
          html += '<div class="eq" data-qi="' + qi + '">';
          html += '<p class="qtext"><span class="num">Q' + (qi + 1) + '.</span> ' + esc(item.q) + '</p>';
          item.opts.forEach(function (o, oi) {
            html += '<button class="opt" data-qi="' + qi + '" data-oi="' + oi + '" data-correct="' + (o.correct ? 1 : 0) + '">' + esc(o.text) + '</button>';
          });
          html += '<p class="why">' + esc(item.why) + '</p></div>';
        } else {
          var sql = item.kind === 'sql';
          var ph = sql ? 'SELECT ...' : '=...';
          var tag = sql ? 'write SQL' : 'type a formula';
          html += '<div class="eq fq" data-qi="' + qi + '">';
          html += '<p class="qtext"><span class="num">Q' + (qi + 1) + '.</span> <span class="ftag">' + tag + '</span> ' + esc(item.q) + '</p>';
          html += '<div class="fx-row">';
          if (sql) html += '<textarea class="fx fx-sql" data-qi="' + qi + '" spellcheck="false" rows="2" placeholder="' + ph + '"></textarea>';
          else html += '<input class="fx" data-qi="' + qi + '" spellcheck="false" autocomplete="off" placeholder="' + ph + '" ' + (item.hint ? 'title="' + escAttr(item.hint) + '"' : '') + '>';
          html += '<button class="btn ghost fx-test" data-qi="' + qi + '" type="button">Test</button></div>';
          html += '<div class="fx-live" data-qi="' + qi + '"></div>';
          html += '<p class="why"></p></div>';
        }
      });

      html += '<div class="exam-actions">' +
        '<button class="btn" data-act="check" type="button">Check answers</button>' +
        '<button class="btn ghost" data-act="new" type="button">New set</button>' +
        '<span class="score" style="display:none"></span></div>';

      host.innerHTML = html;
      wire(picked);
    }

    function val(qi) { var el = host.querySelector('.fx[data-qi="' + qi + '"]'); return el ? el.value : ''; }

    function wire(picked) {
      var checked = false;
      var selected = {};
      var sqlDb = null;
      if (sqlReady) sqlReady.then(function (db) { sqlDb = db; }).catch(function () { sqlDb = null; });

      host.querySelectorAll('.opt').forEach(function (btn) {
        btn.addEventListener('click', function () {
          if (checked) return;
          var qi = btn.dataset.qi;
          host.querySelectorAll('.opt[data-qi="' + qi + '"]').forEach(function (b) { b.classList.remove('sel'); });
          btn.classList.add('sel'); selected[qi] = btn.dataset.oi;
        });
      });

      host.querySelectorAll('.fx-test').forEach(function (b) {
        b.addEventListener('click', function () {
          if (checked) return;
          var qi = b.dataset.qi;
          var item = picked[qi];
          var live = host.querySelector('.fx-live[data-qi="' + qi + '"]');
          var v = val(qi).trim();
          if (!v) { live.className = 'fx-live'; live.textContent = 'Write something, then Test.'; return; }
          if (item.kind === 'sql') {
            if (!sqlDb) { live.className = 'fx-live'; live.textContent = 'Preparing the database…'; return; }
            var r = runSql(sqlDb, v);
            if (!r.ok) { live.className = 'fx-live err'; live.innerHTML = 'SQL error: <b>' + esc(r.error) + '</b>'; }
            else if (r.value === null) { live.className = 'fx-live'; live.textContent = 'Query ran but returned no value.'; }
            else { live.className = 'fx-live ok'; live.innerHTML = 'First result: <b>' + fmt(r.value) + '</b>' + (r.rows > 1 ? ' (' + r.rows + ' rows)' : ''); }
          } else {
            var e = evalFormula(v);
            if (e.ok) { live.className = 'fx-live ok'; live.innerHTML = 'Result: <b>' + fmt(e.value) + '</b>'; }
            else { live.className = 'fx-live err'; live.innerHTML = 'Error: <b>' + esc(e.error) + '</b>'; }
          }
        });
      });
      host.querySelectorAll('.fx').forEach(function (el) {
        el.addEventListener('keydown', function (e) {
          if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') { e.preventDefault(); host.querySelector('.fx-test[data-qi="' + el.dataset.qi + '"]').click(); }
        });
      });

      host.querySelector('[data-act="new"]').addEventListener('click', render);

      host.querySelector('[data-act="check"]').addEventListener('click', function () {
        if (checked) return; checked = true;
        var self = this;
        var needsDb = picked.some(function (p) { return p.kind === 'sql'; });
        (needsDb && sqlReady ? sqlReady : Promise.resolve(null)).then(function (db) {
          gradeAll(db || sqlDb);
        }, function () { gradeAll(null); });

        function gradeAll(db) {
          var correct = 0;
          picked.forEach(function (item, qi) {
            var why = host.querySelector('.eq[data-qi="' + qi + '"] .why');
            if (item.kind === 'mc') {
              var btns = host.querySelectorAll('.opt[data-qi="' + qi + '"]');
              var sel = selected[qi];
              btns.forEach(function (b) {
                b.style.cursor = 'default';
                var isC = b.dataset.correct === '1';
                if (isC) { b.classList.add('correct'); b.innerHTML += '<span class="mk">&#10003;</span>'; }
                if (sel !== undefined && b.dataset.oi === sel && !isC) { b.classList.add('wrong'); b.innerHTML += '<span class="mk">&#10007;</span>'; }
              });
              if (sel !== undefined && btns[sel] && btns[sel].dataset.correct === '1') correct++;
              why.classList.add('show');
            } else {
              var el = host.querySelector('.fx[data-qi="' + qi + '"]');
              el.setAttribute('readonly', 'readonly');
              var live = host.querySelector('.fx-live[data-qi="' + qi + '"]');
              var v = el.value, r, got = null, errTxt = null, answered = !!v.trim();
              if (!answered) { errTxt = 'No answer given.'; }
              else if (item.kind === 'sql') {
                if (!db) errTxt = 'database unavailable';
                else { r = runSql(db, v); if (!r.ok) errTxt = 'SQL error (' + r.error + ')'; else got = r.value; }
              } else {
                r = evalFormula(v); if (!r.ok) errTxt = r.error; else got = r.value;
              }
              var ok = errTxt === null && compare(got, item.expect, item.tol);
              if (ok) {
                correct++; el.classList.add('correct');
                live.className = 'fx-live ok'; live.innerHTML = '&#10003; Correct — returns <b>' + fmt(got) + '</b>';
              } else {
                el.classList.add('wrong');
                var detail = errTxt ? esc(errTxt) : ('returns <b>' + fmt(got) + '</b>, expected <b>' + fmt(item.expect) + '</b>');
                live.className = 'fx-live err'; live.innerHTML = '&#10007; Your answer ' + detail + '.';
              }
              why.innerHTML = '<b>Model answer:</b> <code>' + escAttr(item.answer) + '</code><br>' + esc(item.why);
              why.classList.add('show');
            }
          });
          self.disabled = true;
          var pct = Math.round(correct / picked.length * 100);
          var msg = pct === 100 ? 'Perfect - you have got this.' : pct >= 75 ? 'Strong. Review the misses and retake.' : pct >= 50 ? 'Getting there - try a new set.' : 'Worth another pass through the lessons.';
          var sc = host.querySelector('.score');
          sc.style.display = 'inline';
          sc.innerHTML = 'Score: <span class="pct">' + correct + '/' + picked.length + ' (' + pct + '%)</span> - ' + msg;
          sc.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      });
    }

    render();
  }

  document.querySelectorAll('.exam').forEach(buildExam);
})();
