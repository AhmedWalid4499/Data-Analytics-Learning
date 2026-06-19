/* ============================================================
   DPM Learning Hub — final-exam engine
   <div class="exam" data-bank="excelBank" data-count="8" data-formulas="3"></div>
   <script type="application/json" id="excelBank">[ ...items ]</script>

   Item types:
     Multiple choice : {"q","opts":[...],"correct":0,"why"}        (default)
     Formula (graded): {"type":"formula","q","expect","answer","why",
                        "tol"(optional),"hint"(optional)}
   Formula answers are evaluated live with window.ExcelEngine against
   window.DPM_DATA, so the learner types a real formula and is graded
   on the value it produces. Randomised every attempt.
   ============================================================ */
(function () {
  'use strict';

  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function esc(s) { return String(s); }                 // bank text is authored/trusted
  function escAttr(s) { return String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;'); }
  function isFormula(it) { return it && it.type === 'formula'; }

  function evalFormula(str) {
    if (!window.ExcelEngine || !window.DPM_DATA) return { ok: false, error: 'engine unavailable' };
    return window.ExcelEngine.evaluate(str, { headers: window.DPM_DATA.excelHeaders, rows: window.DPM_DATA.rows });
  }
  function fmt(v) {
    if (typeof v === 'number') return (Math.round(v * 100) / 100).toLocaleString('en-US');
    return v;
  }
  function gradeFormula(item, userStr) {
    if (!userStr || !userStr.trim()) return { answered: false, correct: false };
    var res = evalFormula(userStr);
    if (!res.ok) return { answered: true, correct: false, err: res.error, got: null };
    var got = res.value, exp = item.expect, correct;
    if (typeof exp === 'number') {
      var tol = (item.tol != null) ? item.tol : 0.01;
      correct = (typeof got === 'number') && Math.abs(got - exp) <= tol;
    } else {
      correct = String(got).trim().toLowerCase() === String(exp).trim().toLowerCase();
    }
    return { answered: true, correct: correct, got: got };
  }

  function buildExam(host) {
    var bank;
    try { bank = JSON.parse(document.getElementById(host.dataset.bank).textContent); }
    catch (e) { host.innerHTML = '<p>Exam bank not found.</p>'; return; }

    var engineReady = !!(window.ExcelEngine && window.DPM_DATA);
    var mcItems = bank.filter(function (i) { return !isFormula(i); });
    var fItems = engineReady ? bank.filter(isFormula) : [];

    var total = Math.min(parseInt(host.dataset.count || '8', 10), bank.length);
    var wantF = host.dataset.formulas != null ? parseInt(host.dataset.formulas, 10)
      : Math.min(3, fItems.length);
    var nF = Math.min(wantF, fItems.length, total);
    var nMC = Math.min(total - nF, mcItems.length);

    function render() {
      var picked = shuffle(fItems).slice(0, nF).concat(shuffle(mcItems).slice(0, nMC));
      picked = shuffle(picked).map(function (q) {
        if (isFormula(q)) return { kind: 'formula', q: q.q, why: q.why, expect: q.expect, tol: q.tol, answer: q.answer, hint: q.hint };
        var opts = q.opts.map(function (text, i) { return { text: text, correct: i === q.correct }; });
        return { kind: 'mc', q: q.q, why: q.why, opts: shuffle(opts) };
      });

      var html = '<div class="exam-head"><h3 style="margin:0">Final exam</h3>' +
        '<span class="meta">' + picked.length + ' questions · ' +
        (nF ? nF + ' you type &amp; we grade · ' : '') + 'randomised each attempt</span></div>' +
        '<p style="color:var(--ink-soft);margin:.2em 0 8px;font-size:.95rem">Answer each question — pick an option, or for the <b>type-a-formula</b> ones write a real Excel formula against the sample data (rows 2-73). Press <b>Test</b> to preview a result, then <b>Check answers</b> to grade. Hit <b>New set</b> for a fresh mix.</p>';

      picked.forEach(function (item, qi) {
        if (item.kind === 'formula') {
          html += '<div class="eq fq" data-qi="' + qi + '">';
          html += '<p class="qtext"><span class="num">Q' + (qi + 1) + '.</span> <span class="ftag">type a formula</span> ' + esc(item.q) + '</p>';
          html += '<div class="fx-row">' +
            '<input class="fx" data-qi="' + qi + '" spellcheck="false" autocomplete="off" placeholder="=..." ' + (item.hint ? 'title="' + escAttr(item.hint) + '"' : '') + '>' +
            '<button class="btn ghost fx-test" data-qi="' + qi + '" type="button">Test</button>' +
            '</div>';
          html += '<div class="fx-live" data-qi="' + qi + '"></div>';
          html += '<p class="why"></p>';
          html += '</div>';
        } else {
          html += '<div class="eq" data-qi="' + qi + '">';
          html += '<p class="qtext"><span class="num">Q' + (qi + 1) + '.</span> ' + esc(item.q) + '</p>';
          item.opts.forEach(function (o, oi) {
            html += '<button class="opt" data-qi="' + qi + '" data-oi="' + oi + '" data-correct="' + (o.correct ? 1 : 0) + '">' + esc(o.text) + '</button>';
          });
          html += '<p class="why">' + esc(item.why) + '</p>';
          html += '</div>';
        }
      });

      html += '<div class="exam-actions">' +
        '<button class="btn" data-act="check" type="button">Check answers</button>' +
        '<button class="btn ghost" data-act="new" type="button">New set</button>' +
        '<span class="score" style="display:none"></span></div>';

      host.innerHTML = html;
      wire(picked);
    }

    function wire(picked) {
      var checked = false;
      var selected = {};   // qi -> oi  (mc)

      host.querySelectorAll('.opt').forEach(function (btn) {
        btn.addEventListener('click', function () {
          if (checked) return;
          var qi = btn.dataset.qi;
          host.querySelectorAll('.opt[data-qi="' + qi + '"]').forEach(function (b) { b.classList.remove('sel'); });
          btn.classList.add('sel');
          selected[qi] = btn.dataset.oi;
        });
      });

      host.querySelectorAll('.fx-test').forEach(function (b) {
        b.addEventListener('click', function () {
          if (checked) return;
          var qi = b.dataset.qi;
          var inp = host.querySelector('.fx[data-qi="' + qi + '"]');
          var live = host.querySelector('.fx-live[data-qi="' + qi + '"]');
          var v = inp.value.trim();
          if (!v) { live.className = 'fx-live'; live.textContent = 'Type a formula, then Test.'; return; }
          var r = evalFormula(v);
          if (r.ok) { live.className = 'fx-live ok'; live.innerHTML = 'Result: <b>' + fmt(r.value) + '</b>'; }
          else { live.className = 'fx-live err'; live.innerHTML = 'Error: <b>' + esc(r.error) + '</b>'; }
        });
      });
      host.querySelectorAll('.fx').forEach(function (inp) {
        inp.addEventListener('keydown', function (e) {
          if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') { e.preventDefault(); host.querySelector('.fx-test[data-qi="' + inp.dataset.qi + '"]').click(); }
        });
      });

      host.querySelector('[data-act="new"]').addEventListener('click', render);

      host.querySelector('[data-act="check"]').addEventListener('click', function () {
        if (checked) return; checked = true;
        var correct = 0;

        picked.forEach(function (item, qi) {
          var why = host.querySelector('.eq[data-qi="' + qi + '"] .why');
          if (item.kind === 'formula') {
            var inp = host.querySelector('.fx[data-qi="' + qi + '"]');
            inp.setAttribute('readonly', 'readonly');
            var g = gradeFormula(item, inp.value);
            var live = host.querySelector('.fx-live[data-qi="' + qi + '"]');
            if (g.correct) {
              correct++;
              inp.classList.add('correct');
              live.className = 'fx-live ok'; live.innerHTML = '&#10003; Correct - your formula returns <b>' + fmt(g.got) + '</b>';
            } else {
              inp.classList.add('wrong');
              var detail = !g.answered ? 'No answer given.'
                : (g.err ? 'Your formula errored (<b>' + esc(g.err) + '</b>).'
                  : 'Your formula returns <b>' + fmt(g.got) + '</b>, expected <b>' + fmt(item.expect) + '</b>.');
              live.className = 'fx-live err'; live.innerHTML = '&#10007; ' + detail;
            }
            why.innerHTML = '<b>Model answer:</b> <code>' + escAttr(item.answer) + '</code><br>' + esc(item.why);
            why.classList.add('show');
          } else {
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
          }
        });

        this.disabled = true;
        var pct = Math.round(correct / picked.length * 100);
        var msg = pct === 100 ? 'Perfect - you have got this.' : pct >= 75 ? 'Strong. Review the misses and retake.' : pct >= 50 ? 'Getting there - try a new set.' : 'Worth another pass through the lessons.';
        var sc = host.querySelector('.score');
        sc.style.display = 'inline';
        sc.innerHTML = 'Score: <span class="pct">' + correct + '/' + picked.length + ' (' + pct + '%)</span> - ' + msg;
        sc.scrollIntoView({ behavior: 'smooth', block: 'center' });
      });
    }

    render();
  }

  document.querySelectorAll('.exam').forEach(buildExam);
})();
