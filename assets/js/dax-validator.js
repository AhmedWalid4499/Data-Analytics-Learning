/* ============================================================
   DPM Learning Hub — DAX validator (static analysis)
   DAX cannot execute in a browser (it needs a tabular engine),
   so this checks SYNTAX and common mistakes, and offers tips.
   Exposes window.DaxValidator.validate(expr)
   ============================================================ */
(function (root) {
  'use strict';

  // Curated list of common DAX functions (not exhaustive, but covers the basics + intermediate).
  var KNOWN = ('SUM SUMX AVERAGE AVERAGEX MIN MINX MAX MAXX COUNT COUNTA COUNTAX COUNTROWS COUNTBLANK ' +
    'DISTINCTCOUNT DISTINCT VALUES CALCULATE CALCULATETABLE FILTER ALL ALLEXCEPT ALLSELECTED REMOVEFILTERS ' +
    'KEEPFILTERS DIVIDE IF IFERROR SWITCH AND OR NOT TRUE FALSE BLANK ISBLANK ISERROR HASONEVALUE SELECTEDVALUE ' +
    'RELATED RELATEDTABLE EARLIER RANKX TOPN SUMMARIZE SUMMARIZECOLUMNS ADDCOLUMNS SELECTCOLUMNS GROUPBY ' +
    'TOTALYTD TOTALQTD TOTALMTD DATESYTD DATESMTD DATESQTD SAMEPERIODLASTYEAR PREVIOUSMONTH PREVIOUSYEAR ' +
    'PREVIOUSQUARTER PREVIOUSDAY NEXTMONTH DATEADD DATESBETWEEN DATESINPERIOD PARALLELPERIOD ENDOFMONTH ' +
    'STARTOFMONTH FIRSTDATE LASTDATE CALENDAR CALENDARAUTO DATE YEAR MONTH DAY HOUR MINUTE SECOND WEEKDAY ' +
    'WEEKNUM EOMONTH EDATE TODAY NOW FORMAT CONCATENATE CONCATENATEX LEFT RIGHT MID LEN UPPER LOWER TRIM ' +
    'SUBSTITUTE REPLACE SEARCH FIND VALUE ROUND ROUNDUP ROUNDDOWN INT ABS MOD CEILING FLOOR TRUNC POWER SQRT ' +
    'DIVIDE COALESCE LOOKUPVALUE USERELATIONSHIP CROSSFILTER TREATAS UNION INTERSECT EXCEPT NATURALINNERJOIN ' +
    'ROW GENERATESERIES VAR RETURN MAXA MINA MEDIAN PERCENTILE PERCENTILEX STDEV STDEVX RANK PRODUCT PRODUCTX ' +
    'CONTAINS CONTAINSSTRING ISFILTERED ISCROSSFILTERED ISINSCOPE PATH PATHITEM').split(/\s+/);
  var KNOWN_SET = {}; KNOWN.forEach(function (k) { KNOWN_SET[k] = true; });

  function balance(expr) {
    var issues = [];
    var stack = [];
    var inStr = false, strCh = '';
    for (var i = 0; i < expr.length; i++) {
      var c = expr[i];
      if (inStr) {
        if (c === strCh) {
          // doubled quote = escape
          if (expr[i + 1] === strCh) { i++; continue; }
          inStr = false;
        }
        continue;
      }
      if (c === '"' || c === "'") { inStr = true; strCh = c; continue; }
      if (c === '(' || c === '[') stack.push({ c: c, i: i });
      else if (c === ')') { if (!stack.length || stack[stack.length - 1].c !== '(') issues.push('Unmatched ")" — check your parentheses.'); else stack.pop(); }
      else if (c === ']') { if (!stack.length || stack[stack.length - 1].c !== '[') issues.push('Unmatched "]" — column/measure brackets look off.'); else stack.pop(); }
    }
    if (inStr) issues.push('A text string is missing its closing quote (' + strCh + ').');
    stack.forEach(function (s) { issues.push('Unclosed "' + s.c + '" — you have more openings than closings.'); });
    return issues;
  }

  function stripStrings(expr) {
    return expr.replace(/"(?:[^"]|"")*"/g, '""').replace(/'[^']*'/g, "''");
  }

  function validate(expr) {
    var raw = String(expr || '').trim();
    var issues = [], tips = [], notes = [];
    if (!raw) return { ok: false, issues: ['Nothing to check — type a DAX expression first.'], tips: [], notes: [] };

    // allow "Measure Name := expression"
    var body = raw;
    var nameMatch = /^\s*([A-Za-z0-9 _]+?)\s*:?=\s*([\s\S]+)$/.exec(raw);
    if (nameMatch && /:=/.test(raw)) { body = nameMatch[2]; notes.push('Reads as a named measure: <b>' + nameMatch[1].trim() + '</b>.'); }

    issues = issues.concat(balance(body));

    var noStr = stripStrings(body);

    // unknown function detection: WORD( where WORD not known
    var fnRe = /([A-Za-z_][A-Za-z0-9_]*)\s*\(/g, m;
    var unknown = {};
    while ((m = fnRe.exec(noStr))) {
      var fn = m[1].toUpperCase();
      if (!KNOWN_SET[fn]) unknown[fn] = true;
    }
    Object.keys(unknown).forEach(function (fn) {
      issues.push('"' + fn + '(...)" isn\'t a DAX function I recognise — check the spelling, or it may be an advanced function not in this checker\'s list.');
    });

    // references
    var hasColRef = /\[[^\]]+\]/.test(noStr);
    if (!hasColRef && /\b(SUM|AVERAGE|MIN|MAX|COUNT|DISTINCTCOUNT)\s*\(/i.test(noStr))
      tips.push('Aggregations like SUM() expect a column reference such as <code>Fact_Orders[revenue]</code> or <code>[revenue]</code>.');

    // lint tips
    if (/[^A-Za-z_]\/[^*]/.test(noStr) && !/DIVIDE\s*\(/i.test(noStr))
      tips.push('You\'re dividing with "/". In DAX, prefer <code>DIVIDE(numerator, denominator, 0)</code> — it handles divide-by-zero safely.');
    if (/\bCALCULATE\s*\(/i.test(noStr)) {
      var inside = /CALCULATE\s*\(([\s\S]*)\)/i.exec(body);
      if (inside && !/,/.test(inside[1])) tips.push('CALCULATE with no filter argument just returns the expression. Add a filter, e.g. <code>CALCULATE([Total Revenue], Fact_Orders[status]="Delivered")</code>.');
    }
    if (/\bSUMX?\s*\(\s*FILTER\s*\(/i.test(noStr)) notes.push('Nice — iterating with SUMX over a FILTER is a solid pattern for row-by-row logic.');
    if (/=\s*=/.test(noStr)) tips.push('DAX uses a single "=" for comparison inside filters, not "==".');
    if (/\bIF\s*\(/i.test(noStr) && /\bIF\s*\([\s\S]*\bIF\s*\(/i.test(noStr)) tips.push('Nested IFs can often be replaced by <code>SWITCH(TRUE(), cond1, val1, cond2, val2, …)</code> for readability.');
    if (/\bDISTINCTCOUNT\s*\(/i.test(noStr)) notes.push('DISTINCTCOUNT counts unique values — great for "how many customers / sites".');

    var ok = issues.length === 0;
    return { ok: ok, issues: issues, tips: tips, notes: notes };
  }

  root.DaxValidator = { validate: validate, functions: KNOWN.slice().sort() };
  if (typeof module !== 'undefined' && module.exports) module.exports = root.DaxValidator;
})(typeof window !== 'undefined' ? window : globalThis);
