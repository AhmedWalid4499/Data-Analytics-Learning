<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DPM Learning Hub — Excel · Power BI · Power Automate</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
<style>
  /* learning path timeline */
  .roadmap{margin-top:28px}
  .stage{position:relative;padding:0 0 26px 70px}
  .stage::before{content:"";position:absolute;left:23px;top:10px;bottom:-6px;width:2px;background:var(--line)}
  .stage:last-child::before{display:none}
  .stage .node{position:absolute;left:0;top:0;width:48px;height:48px;border-radius:50%;display:grid;place-items:center;color:#fff;font:800 1.1rem/1 "Bricolage Grotesque",sans-serif;box-shadow:0 2px 10px rgba(0,0,0,.18)}
  .stage .shead{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
  .stage h3{margin:2px 0;font-size:1.2rem}
  .stage .stime{font:600 .7rem/1 "JetBrains Mono",monospace;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 9px;white-space:nowrap}
  .stage p{margin:.35em 0}
  .stage .connects{color:var(--ink-soft);font-size:.95rem}
  .stage .links{margin-top:10px;display:flex;gap:14px;flex-wrap:wrap;align-items:center;font-size:.9rem}
  .stage .links a{font-weight:600}
  .stage .mile{color:var(--muted)}
  .stage .mile b{color:inherit;font-weight:700}
  /* integration pipeline */
  .pipeline{display:flex;flex-wrap:wrap;align-items:stretch;gap:8px;margin-top:8px}
  .pl{flex:1 1 130px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 10px;text-align:center;font-weight:700}
  .pl small{display:block;color:var(--muted);font-weight:500;margin-top:5px;font-size:.78rem}
  .pl-arr{align-self:center;color:var(--accent);font-weight:800;font-size:1.1rem}
  .pl-base{margin-top:10px;background:var(--accent);color:#fff;border-radius:12px;padding:11px 14px;text-align:center;font-weight:700}
  /* study plan */
  .plan td:first-child{white-space:nowrap;font-weight:700}
  .pace{display:flex;gap:10px;flex-wrap:wrap;margin:2px 0 18px}
  .pace .pill{cursor:default}
  /* at-a-glance horizontal timeline */
  .phaseline{display:flex;flex-wrap:wrap;align-items:stretch;gap:8px;margin:18px 0 28px}
  .phase{flex:1 1 120px;border:1px solid var(--line);border-top:3px solid var(--c);border-radius:12px;padding:12px 10px;background:var(--surface);text-align:center;display:flex;flex-direction:column;gap:4px}
  .phase .pn{width:24px;height:24px;border-radius:50%;background:var(--c);color:#fff;font:800 .8rem/24px "Bricolage Grotesque",sans-serif;margin:0 auto}
  .phase b{font-size:.95rem}
  .phase small{color:var(--muted);font:600 .72rem/1 "JetBrains Mono",monospace}
  .phase-arr{align-self:center;color:var(--accent);font-weight:800;font-size:1.05rem}
</style>
</head>
<body data-theme="hub">
<div class="scrollbar"></div>

<nav class="nav"><div class="wrap">
  <a class="brand" href="index.html"><span class="dot"></span> DPM Learning Hub</a>
  <button class="menu-btn" aria-label="Menu">☰</button>
  <div class="nav-links">
    <a href="index.html" aria-current="page">Home</a>
    <a href="data-foundations.html">Foundations</a>
    <a href="excel.html">Excel</a>
    <a href="sql.html">SQL</a>
    <a href="powerbi.html">Power BI</a>
    <a href="powerautomate.html">Power Automate</a>
    <a href="courses.html">Courses</a>
    <a href="downloads.html">Downloads</a>
  </div>
</div></nav>

<header class="hero"><div class="wrap">
  <span class="tool-badge"><span class="glyph">DPM</span> Built for the Delivery PM team</span>
  <h1>Go from spreadsheets<br>to dashboards to<br>automations.</h1>
  <p class="lead">A self-paced hub for new DPMs. Learn the tools we actually use — Excel, Power BI, and Power Automate — with worked examples on real delivery data, hands-on prompts, and answer keys you can check yourself. No prior experience assumed.</p>
  <div class="pills" style="margin-top:22px">
    <span class="pill">Worked examples</span>
    <span class="pill">Practice prompts + answer keys</span>
    <span class="pill">Downloadable sample data</span>
    <span class="pill">Self-check quizzes</span>
  </div>
</div></header>

<section><div class="wrap">
  <span class="eyebrow">Four tracks</span>
  <h2 style="font-size:2rem;margin:.2em 0 .1em">Pick where you want to start</h2>
  <p class="lead" style="margin-bottom:26px">Each track follows its tool's own look and builds from basics to advanced. Work top to bottom, or jump to what you need.</p>

  <div class="grid cols-2">
    <a class="card tool-card" href="data-foundations.html">
      <span class="chip" style="background:#6D28D9">01 · Foundations</span>
      <h3>Understand the data first</h3>
      <p>Tables, keys and relationships, how databases store rows in pages, ER &amp; EER diagrams, star vs snowflake schemas, and OLAP — the groundwork that makes everything else click.</p>
      <span class="arrow">→</span>
    </a>
    <a class="card tool-card" href="excel.html">
      <span class="chip" style="background:#217346">02 · Excel</span>
      <h3>Excel foundations &amp; power moves</h3>
      <p>Functions from <span class="mono">SUM</span> to <span class="mono">LAMBDA</span>, lookups, PivotTables, getting data from the web, and Power Query for repeatable cleaning.</p>
      <span class="arrow">→</span>
    </a>
    <a class="card tool-card" href="sql.html">
      <span class="chip" style="background:#0E7490">03 · SQL</span>
      <h3>Ask your data questions directly</h3>
      <p>SELECT, WHERE, GROUP BY, JOINs and beyond — taught in five levels, with a full SQLite engine in the browser so you can run and be graded on real queries.</p>
      <span class="arrow">→</span>
    </a>
    <a class="card tool-card" href="powerbi.html">
      <span class="chip" style="background:#1a1a1a;color:#F2C811">04 · Power BI</span>
      <h3>From data to dashboards</h3>
      <p>Load &amp; shape data, model relationships, write DAX measures, and choose the right chart — knowing when each one helps and when it misleads.</p>
      <span class="arrow">→</span>
    </a>
    <a class="card tool-card" href="powerautomate.html">
      <span class="chip" style="background:#0066FF">05 · Power Automate</span>
      <h3>Automate the repetitive work</h3>
      <p>Triggers, actions, conditions, loops and expressions explained — then design your own flows and check them against a worked answer key.</p>
      <span class="arrow">→</span>
    </a>
    <a class="card tool-card" href="courses.html">
      <span class="chip" style="background:#FF7900">06 · Courses</span>
      <h3>Keep going further</h3>
      <p>Free Microsoft Learn paths, the certifications worth having, and the best free video channels to deepen each skill.</p>
      <span class="arrow">→</span>
    </a>
  </div>
</div></section>

<!-- LEARNING PATH -->
<section style="background:var(--surface-2)"><div class="wrap">
  <span class="eyebrow">The recommended path</span>
  <h2 style="font-size:2rem;margin:.2em 0 .1em">What to learn, and in what order</h2>
  <p class="lead" style="margin-bottom:8px">You <em>can</em> jump around, but each track is designed to stand on the one before it. Follow the path top to bottom and every new idea lands on something you already know. Plan for roughly <strong>30 hours</strong> of focused study in total.</p>

  <div class="phaseline">
    <div class="phase" style="--c:#6D28D9"><span class="pn">1</span><b>Foundations</b><small>2–3 hrs</small></div>
    <span class="phase-arr">→</span>
    <div class="phase" style="--c:#217346"><span class="pn">2</span><b>Excel</b><small>6–8 hrs</small></div>
    <span class="phase-arr">→</span>
    <div class="phase" style="--c:#0E7490"><span class="pn">3</span><b>SQL</b><small>6–8 hrs</small></div>
    <span class="phase-arr">→</span>
    <div class="phase" style="--c:#1a1a1a"><span class="pn">4</span><b>Power BI</b><small>8–10 hrs</small></div>
    <span class="phase-arr">→</span>
    <div class="phase" style="--c:#0066FF"><span class="pn">5</span><b>Power Automate</b><small>4–6 hrs</small></div>
  </div>

  <div class="roadmap">

    <div class="stage">
      <span class="node" style="background:#6D28D9">1</span>
      <div class="shead"><h3>Foundations</h3><span class="stime">≈ 2–3 hrs</span></div>
      <p><b>Learn:</b> tables, keys &amp; relationships, how data is stored, ER/EER diagrams, star vs snowflake schemas, and OLAP (the cube — slice, dice, drill).</p>
      <p class="connects"><b>Why first:</b> this is the vocabulary for everything else — relational thinking for SQL, the star schema and OLAP for Power BI, and the reason a PivotTable works the way it does.</p>
      <div class="links"><a href="data-foundations.html">Open Foundations →</a> <span class="mile"><b>Checkpoint:</b> the self-check quizzes</span></div>
    </div>

    <div class="stage">
      <span class="node" style="background:#217346">2</span>
      <div class="shead"><h3>Excel</h3><span class="stime">≈ 6–8 hrs</span></div>
      <p><b>Learn:</b> references and the <span class="mono">$</span> lock, conditional aggregation (SUMIFS/COUNTIFS), lookups (XLOOKUP, INDEX/MATCH), PivotTables, and Power Query cleaning.</p>
      <p class="connects"><b>Builds on Foundations:</b> a PivotTable is OLAP on your desktop — rows &amp; columns are dimensions, values are measures. The Power Query you learn here is the <em>same</em> engine you'll use in Power BI.</p>
      <div class="links"><a href="excel.html">Open Excel →</a> <span class="mile"><b>Milestone:</b> pass the Excel exam · keep the cheat sheet</span></div>
    </div>

    <div class="stage">
      <span class="node" style="background:#0E7490">3</span>
      <div class="shead"><h3>SQL</h3><span class="stime">≈ 6–8 hrs</span></div>
      <p><b>Learn:</b> SELECT / WHERE / ORDER BY, GROUP BY &amp; HAVING, JOINs, subqueries, CTEs and window functions — run live against a real database in your browser.</p>
      <p class="connects"><b>Connects:</b> <span class="mono">GROUP BY</span> is the PivotTable idea written in code, and the relational model from Foundations made real. Clean query results become the source you load into Power BI.</p>
      <div class="links"><a href="sql.html">Open SQL →</a> <span class="mile"><b>Milestone:</b> pass the SQL exam · keep the cheat sheet</span></div>
    </div>

    <div class="stage">
      <span class="node" style="background:#1a1a1a;color:#F2C811">4</span>
      <div class="shead"><h3>Power BI</h3><span class="stime">≈ 8–10 hrs</span></div>
      <p><b>Learn:</b> get &amp; shape data (Power Query), model it as a star schema, write DAX measures, and choose the right visual for the question.</p>
      <p class="connects"><b>Pulls it all together:</b> it stacks Power Query (Excel), the star schema &amp; OLAP (Foundations) and data you can pull with SQL into interactive dashboards. This is where the earlier tracks pay off.</p>
      <div class="links"><a href="powerbi.html">Open Power BI →</a> <span class="mile"><b>Milestone:</b> pass the Power BI exam · keep the DAX cheat sheet</span></div>
    </div>

    <div class="stage">
      <span class="node" style="background:#0066FF">5</span>
      <div class="shead"><h3>Power Automate</h3><span class="stime">≈ 4–6 hrs</span></div>
      <p><b>Learn:</b> triggers, actions, conditions, loops and expressions — then design flows of your own.</p>
      <p class="connects"><b>Automates the rest:</b> once you can analyse, you automate the delivery — refresh and email a report, alert when a status changes, chase an approval. It removes the repetitive work around everything above.</p>
      <div class="links"><a href="powerautomate.html">Open Power Automate →</a> <span class="mile"><b>Milestone:</b> pass the Power Automate exam · build one real flow</span></div>
    </div>

  </div>

  <div class="note" style="margin-top:6px"><span class="ic">i</span><div>Two tracks support you the whole way: <a href="courses.html">Courses</a> for going deeper on any tool, and <a href="downloads.html">Downloads</a> for the printable cheat sheets to keep beside you while you practise.</div></div>
</div></section>

<!-- HOW THEY FIT TOGETHER -->
<section><div class="wrap">
  <span class="eyebrow">How it all connects</span>
  <h2 style="font-size:2rem;margin:.2em 0 .3em">Five tracks, one pipeline</h2>
  <p class="lead">The tools aren't five separate skills — they're stages of the same workflow: get data, shape it, model it, show it, and automate it. Foundations sits underneath, explaining <em>why</em> each stage works.</p>

  <div class="pipeline">
    <div class="pl">Get the data<small>Excel · SQL</small></div>
    <span class="pl-arr">→</span>
    <div class="pl">Shape &amp; clean<small>Power Query</small></div>
    <span class="pl-arr">→</span>
    <div class="pl">Model &amp; measure<small>Power BI · DAX</small></div>
    <span class="pl-arr">→</span>
    <div class="pl">Visualise<small>Power BI</small></div>
    <span class="pl-arr">→</span>
    <div class="pl">Automate &amp; share<small>Power Automate</small></div>
  </div>
  <div class="pl-base">Foundations — the relational &amp; OLAP concepts beneath every stage</div>

  <div class="note" style="margin-top:20px"><span class="ic">★</span><div><b>The thread that ties it together:</b> the same question — "<em>a measure</em> by <em>a dimension</em> by <em>a dimension</em>" (revenue by region by quarter) — is a <strong>PivotTable</strong> in Excel, a <strong>GROUP BY</strong> in SQL, and a <strong>visual on a star schema</strong> in Power BI. Learn it once in Foundations and you recognise it everywhere.</div></div>
</div></section>

<!-- STUDY PLAN -->
<section><div class="wrap">
  <span class="eyebrow">A study plan</span>
  <h2 style="font-size:2rem;margin:.2em 0 .3em">If you want a schedule to follow</h2>
  <p class="lead" style="margin-bottom:6px">No plan is required — the hub is self-paced. But if you like structure, here's a steady six-week plan at a few hours a week, with the exams as your checkpoints.</p>
  <div class="pace">
    <span class="pill">Steady: ~5 hrs/week · 6 weeks</span>
    <span class="pill">Intensive: full-time · ~2 weeks</span>
  </div>

  <h3 style="margin:18px 0 8px">Steady — about 5 hours a week for 6 weeks</h3>
  <table class="tbl plan">
    <thead><tr><th>Week</th><th>Focus</th><th>Milestone by the end</th></tr></thead>
    <tbody>
      <tr><td>Week 1</td><td>Foundations in full, then start Excel (references, conditional aggregation).</td><td>Comfortable with tables, keys &amp; OLAP; Excel basics clicking.</td></tr>
      <tr><td>Week 2</td><td>Finish Excel: lookups, PivotTables, Power Query.</td><td>Pass the <a href="excel.html">Excel</a> exam.</td></tr>
      <tr><td>Week 3</td><td>SQL basics → intermediate: SELECT, WHERE, GROUP BY, JOINs (run every query).</td><td>Confident reading &amp; summarising data in SQL.</td></tr>
      <tr><td>Week 4</td><td>SQL advanced: subqueries, CTEs, window functions.</td><td>Pass the <a href="sql.html">SQL</a> exam.</td></tr>
      <tr><td>Week 5</td><td>Power BI: shape, model a star schema, DAX measures, choose visuals.</td><td>Pass the <a href="powerbi.html">Power BI</a> exam; build one small dashboard.</td></tr>
      <tr><td>Week 6</td><td>Power Automate + consolidate everything on the sample data.</td><td>Pass the <a href="powerautomate.html">Power Automate</a> exam; build one real flow.</td></tr>
    </tbody>
  </table>
  <h3 style="margin:26px 0 8px">Intensive — about two weeks full-time</h3>
  <table class="tbl plan">
    <thead><tr><th>Day</th><th>Focus</th><th>Milestone by the end</th></tr></thead>
    <tbody>
      <tr><td>Days 1–2</td><td>Foundations in full, then begin Excel (references, conditional aggregation).</td><td>Relational &amp; OLAP ideas solid; Excel underway.</td></tr>
      <tr><td>Day 3</td><td>Finish Excel: lookups, PivotTables, Power Query.</td><td>Pass the <a href="excel.html">Excel</a> exam.</td></tr>
      <tr><td>Days 4–5</td><td>SQL: SELECT → WHERE → GROUP BY → JOINs, running every query.</td><td>Confident querying the sample data.</td></tr>
      <tr><td>Day 6</td><td>SQL advanced: subqueries, CTEs, window functions.</td><td>Pass the <a href="sql.html">SQL</a> exam.</td></tr>
      <tr><td>Days 7–8</td><td>Power BI: shape, model a star schema, write DAX, choose visuals.</td><td>Pass the <a href="powerbi.html">Power BI</a> exam; build a small dashboard.</td></tr>
      <tr><td>Day 9</td><td>Power Automate: triggers, actions, conditions and expressions.</td><td>Pass the <a href="powerautomate.html">Power Automate</a> exam.</td></tr>
      <tr><td>Day 10</td><td>End-to-end mini-project on the sample data: query → model → dashboard → an automated alert.</td><td>One project that uses all five tracks together.</td></tr>
    </tbody>
  </table>
  <p class="hint" style="color:var(--muted);font-size:.9rem;margin-top:10px">Pick whichever pace fits — the content is identical, only the calendar changes. The exams are your checkpoints either way.</p>

  <h3 style="margin:26px 0 10px">Five habits that make it stick</h3>
  <div class="grid cols-2">
    <div class="card"><h3>Treat the exam as a checkpoint</h3><p>Don't move on until you can pass a track's exam comfortably. It reshuffles each attempt, so retake it until the score is reliable, not lucky.</p></div>
    <div class="card"><h3>Always attempt the <em>Try it</em> first</h3><p>Have a real go before you reveal the answer. The few minutes of being stuck are where the learning actually happens.</p></div>
    <div class="card"><h3>Keep the cheat sheet open</h3><p>Download the track's cheat sheet and have it beside you while you practise — recall comes from use, not memorising.</p></div>
    <div class="card"><h3>Use the one dataset throughout</h3><p>Answering the same questions in Excel, SQL and Power BI is what reveals how the tools connect — and makes each new one faster to learn.</p></div>
  </div>
  <div class="note" style="margin-top:16px"><span class="ic">i</span><div>Stuck on a tool concept that feels abstract? Jump back to <a href="data-foundations.html">Foundations</a> — most confusion in the tools traces back to a modelling idea explained there.</div></div>
</div></section>

<section style="background:var(--surface-2)"><div class="wrap">
  <div class="grid cols-2" style="align-items:center;gap:40px">
    <div>
      <span class="eyebrow">One dataset, everywhere</span>
      <h2 style="font-size:2rem;margin:.2em 0 .3em">Practice on delivery data that looks like ours</h2>
      <p>Every track uses the same fictional dataset: 72 delivery orders across customers like SKF and Harman, with sites, regions, service types, statuses, dates, FTE days and revenue. Download it once and use it for every exercise.</p>
      <p>There's also a deliberately <strong>messy</strong> copy — inconsistent text, missing values, European decimals and text dates — for the Power Query cleaning practice.</p>
      <div class="pills" style="margin:18px 0">
        <a class="dl" href="assets/data/dpm_projects.xlsx" download>⬇ Sample workbook (.xlsx)</a>
        <a class="dl ghost" href="assets/data/dpm_projects.csv" download>⬇ CSV</a>
        <a class="dl ghost" href="assets/data/dpm_messy_data.csv" download>⬇ Messy CSV</a>
      </div>
    </div>
    <div class="card">
      <table class="tbl" style="margin:0">
        <thead><tr><th>Order ID</th><th>Customer</th><th>Service</th><th>Status</th></tr></thead>
        <tbody>
          <tr><td class="mono">10-1735&hellip;</td><td>SKF Industrial</td><td>LAN Refresh</td><td>Delivered</td></tr>
          <tr><td class="mono">10-1736&hellip;</td><td>Harman Intl</td><td>Wireless Migration</td><td>In Progress</td></tr>
          <tr><td class="mono">10-1737&hellip;</td><td>Network Intl</td><td>SD-WAN Migration</td><td>Staging</td></tr>
          <tr><td class="mono">10-1738&hellip;</td><td>Volvo Group</td><td>MPLS Service Order</td><td>On Hold</td></tr>
        </tbody>
      </table>
      <p class="hint" style="color:var(--muted);font-size:.85rem;margin:.6em 0 0">17 columns · 72 rows · fictional, for training only</p>
    </div>
  </div>
</div></section>

<section><div class="wrap">
  <span class="eyebrow">How to use this hub</span>
  <h2 style="font-size:2rem;margin:.2em 0 .3em">Learn by doing, then check yourself</h2>
  <div class="grid cols-3">
    <div class="card"><h3>1 · Read the worked example</h3><p>Each lesson explains the concept and shows it applied to the sample data, with the exact formula or step.</p></div>
    <div class="card"><h3>2 · Try the prompt first</h3><p>Open the workbook and attempt the <em>Try it</em> task on your own before peeking. That struggle is where the learning sticks.</p></div>
    <div class="card"><h3>3 · Reveal the answer key</h3><p>Click <em>Show answer</em> to compare your approach. If it differs but works — great, there's often more than one right way.</p></div>
  </div>
</div></section>

<footer class="foot"><div class="wrap">
  <p><strong>DPM Learning Hub</strong> · A training resource for the Delivery Project Management team.<br>
  Sample data is fictional. Built to be hosted on GitHub Pages — drop the folder into your repo and it just works.</p>
</div></footer>

<script src="assets/js/main.js"></script>
</body>
</html>
