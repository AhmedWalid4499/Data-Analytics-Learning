/* ============================================================
   DPM Learning Hub — code playgrounds
   Wires up whichever runners are present on the page:
     #xl-play  → Excel formula engine (ExcelEngine)
     #dax-play → DAX validator (DaxValidator)
     #sql-play → SQLite via vendored sql.js
   All run fully client-side. Data = window.DPM_DATA.
   ============================================================ */
(function () {
  'use strict';
  var D = window.DPM_DATA || { excelHeaders: [], sqlColumns: [], sqlTypes: [], rows: [] };
  function $(id) { return document.getElementById(id); }
  function escHtml(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

  function colLetter(n) { var s = ''; n++; while (n > 0) { var m = (n - 1) % 26; s = String.fromCharCode(65 + m) + s; n = (n - m - 1) / 26; } return s; }

  // ---------------- EXCEL ----------------
  (function () {
    var host = $('xl-play'); if (!host || !window.ExcelEngine) return;
    var input = $('xl-in'), out = $('xl-out');
    function run() {
      var r = window.ExcelEngine.evaluate(input.value, { headers: D.excelHeaders, rows: D.rows });
      if (r.ok) { out.className = 'out ok'; out.innerHTML = '<span class="res-val">' + escHtml(r.value) + '</span>'; }
      else { out.className = 'out err'; out.innerHTML = '<b>' + escHtml(r.error) + '</b> — check the formula and try again.'; }
    }
    $('xl-run').addEventListener('click', run);
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) { e.preventDefault(); run(); } });
    host.querySelectorAll('.chip-btn').forEach(function (c) { c.addEventListener('click', function () { input.value = c.dataset.f; run(); input.focus(); }); });
    run();
  })();

  // ---------------- DAX ----------------
  (function () {
    var host = $('dax-play'); if (!host || !window.DaxValidator) return;
    var input = $('dax-in'), out = $('dax-out');
    function run() {
      var r = window.DaxValidator.validate(input.value);
      var html = '';
      if (r.ok) html += '<b style="color:var(--good)">✓ Syntax looks valid.</b>';
      else { html += '<b style="color:var(--bad)">Issues found:</b>'; r.issues.forEach(function (i) { html += '<div class="tip-line">' + i + '</div>'; }); }
      if (r.notes && r.notes.length) r.notes.forEach(function (n) { html += '<div class="tip-line">' + n + '</div>'; });
      if (r.tips && r.tips.length) { html += '<div style="margin-top:8px;font-weight:700;font-size:.9rem">Tips</div>'; r.tips.forEach(function (t) { html += '<div class="tip-line">' + t + '</div>'; }); }
      html += '<p class="legend" style="margin-top:10px">This is a syntax &amp; style check — DAX needs a Power BI model to actually run.</p>';
      out.className = r.ok ? 'out ok' : 'out err';
      out.innerHTML = html;
    }
    $('dax-run').addEventListener('click', run);
    host.querySelectorAll('.chip-btn').forEach(function (c) { c.addEventListener('click', function () { input.value = c.dataset.f; run(); input.focus(); }); });
    run();
  })();

  // ---------------- SQL ----------------
  (function () {
    var host = $('sql-play'); if (!host || typeof window.initSqlJs !== 'function') {
      if (host && typeof window.initSqlJs !== 'function') { var o = $('sql-out'); if (o) { o.className = 'out err'; o.textContent = 'SQL engine failed to load.'; } }
      return;
    }
    var input = $('sql-in'), out = $('sql-out'), status = $('sql-status'), runBtn = $('sql-run');
    var db = null;
    runBtn.disabled = true; if (status) status.textContent = 'Loading SQL engine…';

    window.initSqlJs({ locateFile: function (f) { return 'assets/vendor/' + f; } }).then(function (SQL) {
      db = new SQL.Database();
      var cols = D.sqlColumns, types = D.sqlTypes;
      var ddl = 'CREATE TABLE orders (' + cols.map(function (c, i) { return c + ' ' + (types[i] || 'TEXT'); }).join(', ') + ');';
      db.run(ddl);
      var ph = cols.map(function () { return '?'; }).join(',');
      var stmt = db.prepare('INSERT INTO orders VALUES (' + ph + ')');
      D.rows.forEach(function (row) { stmt.run(row.map(function (v) { return v === null ? null : v; })); });
      stmt.free();
      // small dimension table so learners can practise JOINs
      db.run('CREATE TABLE targets (region TEXT, revenue_target INTEGER);');
      db.run("INSERT INTO targets VALUES ('EMEA',1200000),('APAC',150000),('Americas',120000);");
      runBtn.disabled = false;
      if (status) status.textContent = 'Ready · "orders" (' + D.rows.length + ' rows) and "targets" (3 rows) loaded.';
    }).catch(function (e) {
      if (status) status.textContent = '';
      out.className = 'out err'; out.textContent = 'Could not start the SQL engine: ' + e.message;
    });

    function run() {
      if (!db) return;
      try {
        var res = db.exec(input.value);
        if (!res.length) { out.className = 'out ok'; out.innerHTML = '<b style="color:var(--good)">Query OK.</b> No rows returned.'; return; }
        var last = res[res.length - 1];
        var rows = last.values, cols = last.columns, cap = 200;
        var html = '<div style="max-height:340px;overflow:auto"><table class="rtbl"><tr>' +
          cols.map(function (c) { return '<th>' + escHtml(c) + '</th>'; }).join('') + '</tr>';
        rows.slice(0, cap).forEach(function (r) { html += '<tr>' + r.map(function (v) { return '<td>' + escHtml(v) + '</td>'; }).join('') + '</tr>'; });
        html += '</table></div>';
        var note = rows.length + ' row' + (rows.length === 1 ? '' : 's') + (rows.length > cap ? ' (showing first ' + cap + ')' : '');
        out.className = 'out ok';
        out.innerHTML = '<div style="font-size:.84rem;color:var(--muted);margin-bottom:6px">' + note + '</div>' + html;
      } catch (e) {
        out.className = 'out err';
        out.innerHTML = '<b>SQL error:</b> ' + escHtml(e.message);
      }
    }
    runBtn.addEventListener('click', run);
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) { e.preventDefault(); run(); } });
    host.querySelectorAll('.chip-btn').forEach(function (c) { c.addEventListener('click', function () { input.value = c.dataset.f; run(); input.focus(); }); });
  })();
})();
