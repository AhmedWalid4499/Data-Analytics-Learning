const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, LevelFormat, HeadingLevel, BorderStyle, WidthType, ShadingType,
  Header, Footer, PageNumber, TableOfContents, ExternalHyperlink, PageBreak
} = require('docx');

const ACCENT = "0E7490";   // teal to match the SQL track
const INK = "14233A";
const CODEBG = "F1F5F9";
const TIPBG = "ECFEFF";

// ---------- helpers ----------
function h1(text) { return new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(text)] }); }
function h2(text) { return new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(text)] }); }
function h3(text) { return new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun(text)] }); }

function p(runs, opts) {
  if (typeof runs === 'string') runs = [new TextRun(runs)];
  return new Paragraph(Object.assign({ spacing: { after: 140, line: 276 }, children: runs }, opts || {}));
}
function b(t) { return new TextRun({ text: t, bold: true }); }
function t(t2) { return new TextRun(t2); }
function mono(t3) { return new TextRun({ text: t3, font: "Consolas", size: 21 }); }

function step(ref, runs) {
  if (typeof runs === 'string') runs = [new TextRun(runs)];
  return new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 90, line: 270 }, children: runs });
}
function bullet(runs) {
  if (typeof runs === 'string') runs = [new TextRun(runs)];
  return new Paragraph({ numbering: { reference: "bul", level: 0 }, spacing: { after: 80, line: 270 }, children: runs });
}
// code block: one shaded monospace paragraph per line
function code(lines) {
  return lines.map((ln, i) => new Paragraph({
    shading: { type: ShadingType.CLEAR, fill: CODEBG },
    spacing: { before: i === 0 ? 60 : 0, after: i === lines.length - 1 ? 140 : 0, line: 264 },
    border: {
      left: { style: BorderStyle.SINGLE, size: 18, color: ACCENT, space: 8 },
      top: i === 0 ? { style: BorderStyle.SINGLE, size: 2, color: CODEBG, space: 4 } : undefined,
    },
    indent: { left: 120 },
    children: [new TextRun({ text: ln || " ", font: "Consolas", size: 21, color: "0B3B45" })]
  }));
}
function tip(label, runs) {
  if (typeof runs === 'string') runs = [new TextRun(runs)];
  return new Paragraph({
    shading: { type: ShadingType.CLEAR, fill: TIPBG },
    spacing: { before: 60, after: 160, line: 270 },
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: ACCENT, space: 8 } },
    indent: { left: 120, right: 120 },
    children: [new TextRun({ text: label + " ", bold: true, color: ACCENT })].concat(runs)
  });
}
function link(text, url) {
  return new ExternalHyperlink({ link: url, children: [new TextRun({ text: text, style: "Hyperlink" })] });
}

// table
const cellBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCD6DD" };
const borders = { top: cellBorder, bottom: cellBorder, left: cellBorder, right: cellBorder };
function tcell(text, width, opts) {
  opts = opts || {};
  const runs = Array.isArray(text) ? text : [new TextRun({ text: String(text), bold: !!opts.bold, color: opts.color })];
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    shading: opts.fill ? { type: ShadingType.CLEAR, fill: opts.fill } : undefined,
    margins: { top: 70, bottom: 70, left: 120, right: 120 },
    children: [new Paragraph({ children: runs })]
  });
}
function tableOf(headers, rows, widths) {
  const total = widths.reduce((a, c) => a + c, 0);
  const headRow = new TableRow({ tableHeader: true, children: headers.map((hh, i) => tcell(hh, widths[i], { bold: true, fill: ACCENT, color: "FFFFFF" })) });
  const bodyRows = rows.map(r => new TableRow({ children: r.map((c, i) => tcell(c, widths[i])) }));
  return new Table({ width: { size: total, type: WidthType.DXA }, columnWidths: widths, rows: [headRow].concat(bodyRows) });
}

const numRefs = ["nDownload", "nSsms", "nConnect", "nQuery", "nImport", "nTrouble", "nUninstall"];
const numberingConfig = numRefs.map(ref => ({
  reference: ref,
  levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 600, hanging: 320 } } } }]
})).concat([{
  reference: "bul",
  levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 280 } } } }]
}]);

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22, color: INK } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 30, bold: true, font: "Arial", color: ACCENT },
        paragraph: { spacing: { before: 320, after: 160 }, outlineLevel: 0, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "D6E6EB", space: 6 } } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 25, bold: true, font: "Arial", color: INK },
        paragraph: { spacing: { before: 220, after: 120 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 22, bold: true, font: "Arial", color: ACCENT },
        paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 2 } },
      { id: "Hyperlink", name: "Hyperlink", basedOn: "Normal", run: { color: ACCENT, underline: {} } }
    ]
  },
  numbering: { config: numberingConfig },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1300, right: 1440, bottom: 1300, left: 1440 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 0 }, children: [new TextRun({ text: "Setting up SQL Server on Windows", color: "94A3B8", size: 16 })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "DPM Learning Hub  ·  page ", color: "94A3B8", size: 16 }), new TextRun({ children: [PageNumber.CURRENT], color: "94A3B8", size: 16 })] })] }) },
    children: [
      // ---- Title block ----
      new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: "DPM LEARNING HUB", bold: true, color: ACCENT, size: 18 })] }),
      new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "Setting up SQL Server on your Windows laptop", bold: true, size: 44, color: INK })] }),
      new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: "A plain-English, start-to-finish guide: install the database engine, install the tools, connect, and run your first query — then load the sample data and fix the things that commonly go wrong.", size: 22, color: "475569" })] }),
      new Paragraph({ spacing: { after: 220 }, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: ACCENT, space: 6 } }, children: [new TextRun({ text: "Companion to the SQL track. Everything here is free. Last reviewed June 2026.", italics: true, size: 18, color: "94A3B8" })] }),

      // ---- Contents ----
      new Paragraph({ children: [new TextRun({ text: "Contents", bold: true, size: 24, color: INK })], spacing: { after: 120 } }),
      ...[
        "What you're actually installing",
        "Before you start",
        "Install the SQL Server database engine",
        "Install SQL Server Management Studio (SSMS)",
        "Connect to your database",
        "Create a database and run your first query",
        "Load the hub's sample data (optional)",
        "Connecting from other tools",
        "Troubleshooting the common problems",
        "Starting, stopping and removing it later",
      ].map((title, i) => new Paragraph({
        spacing: { after: 50, line: 264 }, indent: { left: 200 },
        children: [new TextRun({ text: (i + 1) + ".  ", bold: true, color: ACCENT }), new TextRun({ text: title })]
      })),
      new Paragraph({ spacing: { after: 50, line: 264 }, indent: { left: 200 }, children: [new TextRun({ text: "+  ", bold: true, color: ACCENT }), new TextRun({ text: "Quick reference" })] }),
      new Paragraph({ children: [new PageBreak()] }),

      // ---- 1. What you're installing ----
      h1("1. What you're actually installing"),
      p([t("Two separate things are easy to confuse, and most first-time problems come from mixing them up:")]),
      p([b("The SQL Server database engine"), t(" — the actual database that stores your data and runs queries. This runs quietly in the background as a Windows service.")]),
      p([b("SQL Server Management Studio (SSMS)"), t(" — the app you actually open and click around in to write queries and manage the database. SSMS is just a client; it does "), b("not"), t(" contain a database itself.")]),
      tip("In short —", [t("you install the "), b("engine"), t(" once, then install "), b("SSMS"), t(" to talk to it. You need both.")]),

      h2("Which edition should you pick?"),
      p("All the editions below are free for learning. For a laptop you're studying on, Developer Edition is the best choice — it's the full product with no feature limits, just not licensed for production use."),
      tableOf(
        ["Edition", "Cost", "Good for", "Notes"],
        [
          ["Developer", "Free", "Learning & testing (recommended)", "Full features; non-production use only"],
          ["Express", "Free", "Small apps, light learning", "Free for production; database size capped (50 GB)"],
          ["Standard / Enterprise", "Paid", "Real production systems", "Not needed for learning"],
        ],
        [1700, 1100, 3060, 3500]
      ),
      p([t("This guide uses "), b("SQL Server 2025"), t(" (the current release) with "), b("SSMS 22"), t(". The steps are nearly identical for SQL Server 2019/2022 if you already have those.")], { spacing: { before: 140, after: 140 } }),

      // ---- 2. Before you start ----
      h1("2. Before you start"),
      bullet([t("A laptop running "), b("Windows 10 or Windows 11"), t(" (64-bit).")]),
      bullet([t("About "), b("6–10 GB of free disk space"), t(" for the engine and tools.")]),
      bullet([t("An account with "), b("administrator rights"), t(" (you'll be installing software and a Windows service).")]),
      bullet([t("A stable internet connection — both installers download components as they run.")]),
      tip("Heads up —", "the install takes 20–40 minutes end to end, mostly waiting on downloads. Set aside time and don't cancel midway."),

      // ---- 3. Install the engine ----
      h1("3. Install the SQL Server database engine"),
      h3("Download"),
      step("nDownload", [t("Go to the official downloads page: "), link("microsoft.com/en-us/sql-server/sql-server-downloads", "https://www.microsoft.com/en-us/sql-server/sql-server-downloads"), t(".")]),
      step("nDownload", [t("Under "), b("Developer"), t(" (or "), b("Express"), t(" if you prefer), click "), b("Download now"), t(". You'll get a small installer such as "), mono("SQL2025-SSEI-Dev.exe"), t(".")]),
      step("nDownload", [t("Right-click the downloaded file and choose "), b("Run as administrator"), t(".")]),
      tip("Faster option —", [t("if you like the command line, open "), b("PowerShell as administrator"), t(" and run a single winget command instead of the website download:")]),
      ...code(["winget install Microsoft.SQLServer.2025.Developer"]),

      h3("Run the installer"),
      step("nDownload", [t("When the installer opens, choose the "), b("Basic"), t(" installation type. This installs the engine with sensible defaults — perfect for learning.")]),
      step("nDownload", [t("Accept the licence terms and confirm the install location (the default is fine). Click "), b("Install"), t(" and wait for it to finish.")]),
      step("nDownload", [t("When it completes, the final screen shows your "), b("Connection String"), t(" and, importantly, the "), b("Instance name"), t(". Note it down — for Basic installs it's usually "), mono("MSSQLSERVER"), t(" (the default instance), so you'll connect to the server name "), mono("localhost"), t(".")]),
      tip("Express note —", [t("the Express installer creates a "), b("named"), t(" instance instead. You'll connect to "), mono(".\\SQLEXPRESS"), t(" (a dot, a backslash, then "), mono("SQLEXPRESS"), t(") rather than "), mono("localhost"), t(".")]),

      // ---- 4. Install SSMS ----
      h1("4. Install SQL Server Management Studio (SSMS)"),
      p("SSMS is the tool you'll spend your time in. It's a separate, free download from the engine."),
      step("nSsms", [t("Open the official install page: "), link("learn.microsoft.com/ssms/install/install", "https://learn.microsoft.com/en-us/ssms/install/install"), t(", and click "), b("Download SSMS 22 installer"), t(".")]),
      step("nSsms", [t("Run the downloaded installer as administrator. Modern SSMS installs through the "), b("Visual Studio Installer"), t(" — when it opens, select the "), b("SQL Server Management Studio"), t(" workload and click "), b("Install"), t(".")]),
      step("nSsms", [t("Reboot if you're prompted to. Then open "), b("SQL Server Management Studio"), t(" from the Start menu.")]),
      tip("Command line —", [t("SSMS is also available via winget: "), mono("winget install Microsoft.SQLServerManagementStudio"), t(".")]),

      // ---- 5. Connect ----
      h1("5. Connect to your database"),
      p([t("When SSMS opens, a "), b("Connect to Server"), t(" dialog appears. Fill it in like this:")]),
      tableOf(
        ["Field", "What to enter"],
        [
          ["Server type", "Database Engine"],
          ["Server name", "localhost   (or  .\\SQLEXPRESS  for Express)"],
          ["Authentication", "Windows Authentication"],
          ["Encryption / Trust certificate", "Tick \u201cTrust server certificate\u201d"],
        ],
        [2600, 6760]
      ),
      p([t("Click "), b("Connect"), t(". On the left, the "), b("Object Explorer"), t(" panel now shows your server. You're in.")], { spacing: { before: 140 } }),
      tip("Can't connect? ", [t("Jump to "), b("section 9 (Troubleshooting)"), t(" — the two usual culprits are the service not running and a mistyped instance name.")]),

      // ---- 6. First query ----
      h1("6. Create a database and run your first query"),
      p([t("Open a new query window ("), b("New Query"), t(" on the toolbar) and run each block with the "), b("Execute"), t(" button (or press "), mono("F5"), t("). Try these in order — they build a tiny version of the delivery dataset used across the hub.")]),
      h3("Create a database"),
      ...code(["CREATE DATABASE DPM_Training;", "GO", "USE DPM_Training;", "GO"]),
      h3("Create a table"),
      ...code([
        "CREATE TABLE orders (",
        "    order_id     VARCHAR(20) PRIMARY KEY,",
        "    customer     VARCHAR(100),",
        "    region       VARCHAR(20),",
        "    status       VARCHAR(30),",
        "    revenue      INT",
        ");"
      ]),
      h3("Add a few rows"),
      ...code([
        "INSERT INTO orders VALUES",
        "  ('10-001','Volvo Group','EMEA','Delivered',40684),",
        "  ('10-002','Harman International','Americas','In Progress',31411),",
        "  ('10-003','Network International','EMEA','Delivered',31385);"
      ]),
      h3("Ask a question"),
      ...code([
        "SELECT region, COUNT(*) AS orders, SUM(revenue) AS total_rev",
        "FROM orders",
        "GROUP BY region",
        "ORDER BY total_rev DESC;"
      ]),
      p([t("The results grid at the bottom shows revenue grouped by region. That's the same kind of query you practise in the "), b("SQL track's in-browser runner"), t(" — now running on a real SQL Server on your own machine.")], { spacing: { before: 120 } }),

      // ---- 7. Import sample data ----
      h1("7. Load the hub's sample data (optional)"),
      p([t("Want the full 72-row dataset rather than three rows? You can import the "), mono("dpm_projects.csv"), t(" file from the learning hub straight into SQL Server.")]),
      step("nImport", [t("In Object Explorer, expand "), b("Databases"), t(", right-click "), b("DPM_Training"), t(" ▸ "), b("Tasks"), t(" ▸ "), b("Import Flat File\u2026")]),
      step("nImport", [t("Browse to "), mono("dpm_projects.csv"), t(", give the new table a name (e.g. "), mono("projects"), t("), and click "), b("Next"), t(".")]),
      step("nImport", [t("The wizard previews the data and guesses each column's type. Adjust any that look wrong (for example make "), mono("revenue"), t(" an integer), then click "), b("Finish"), t(".")]),
      step("nImport", [t("Run "), mono("SELECT * FROM projects;"), t(" to confirm all 72 rows loaded.")]),
      tip("Tip —", "if the import wizard misreads a numeric column as text, set its type explicitly on the preview screen rather than fixing it afterwards — it's much less work."),

      // ---- 8. Other tools ----
      h1("8. Connecting from other tools"),
      p([t("SSMS is the main tool on Windows, but you have options:")]),
      bullet([b("Visual Studio Code"), t(" with the "), b("MSSQL extension"), t(" — a lightweight, cross-platform way to run queries. This is now Microsoft's recommended companion to SSMS.")]),
      bullet([b("Azure Data Studio"), t(" — "), b("retired in February 2026"), t(" and no longer updated. If you have it installed, migrate to VS Code with the MSSQL extension.")]),
      bullet([t("Excel and Power BI can both "), b("connect directly"), t(" to your SQL Server (Get Data ▸ SQL Server database) using the same server name, "), mono("localhost"), t(".")]),

      // ---- 9. Troubleshooting ----
      h1("9. Troubleshooting the common problems"),
      tableOf(
        ["Symptom", "Likely cause & fix"],
        [
          ["\u201cA network-related or instance-specific error\u201d when connecting", "The engine service isn't running, or the server name is wrong. See the two checks below."],
          ["Wrong server name", "Default install = localhost. Express = .\\SQLEXPRESS. Don't guess — confirm the instance name (see below)."],
          ["\u201cLogin failed for user\u201d", "Use Windows Authentication for a fresh install. SQL logins only work if you enabled Mixed Mode."],
          ["Certificate / encryption error", "Tick \u201cTrust server certificate\u201d in the connect dialog."],
          ["A remote machine can't reach it", "Enable TCP/IP and open firewall port 1433 (not needed for localhost)."],
        ],
        [3400, 5960]
      ),
      h3("Check 1 — is the service running?"),
      step("nTrouble", [t("Press "), mono("Win + R"), t(", type "), mono("services.msc"), t(", press Enter.")]),
      step("nTrouble", [t("Find "), b("SQL Server (MSSQLSERVER)"), t(" — or "), b("SQL Server (SQLEXPRESS)"), t(". Its status should be "), b("Running"), t(". If not, right-click ▸ "), b("Start"), t(", and set "), b("Startup type"), t(" to "), b("Automatic"), t(" so it starts with Windows.")]),
      h3("Check 2 — what's my exact instance name?"),
      step("nTrouble", [t("Open "), b("SQL Server Configuration Manager"), t(" from the Start menu.")]),
      step("nTrouble", [t("Under "), b("SQL Server Services"), t(", the running service name in brackets is your instance. Connect to "), mono("localhost\\<thatname>"), t(" (or just "), mono("localhost"), t(" if it says MSSQLSERVER).")]),
      h3("Enabling SQL logins (only if you need them)"),
      p([t("By default the server uses Windows Authentication only. To allow username/password (\u201cSQL\u201d) logins: in SSMS, right-click the server ▸ "), b("Properties"), t(" ▸ "), b("Security"), t(" ▸ select "), b("SQL Server and Windows Authentication mode"), t(", click OK, then restart the service from "), mono("services.msc"), t(".")]),

      // ---- 10. Managing & removing ----
      h1("10. Starting, stopping and removing it later"),
      bullet([b("Start / stop"), t(" the engine any time from "), mono("services.msc"), t(" or SQL Server Configuration Manager. Stopping it frees memory when you're not using it.")]),
      bullet([b("Uninstall"), t(" via "), b("Settings ▸ Apps ▸ Installed apps"), t(": remove "), b("Microsoft SQL Server 2025"), t(" (run its setup to remove specific features) and "), b("SQL Server Management Studio"), t(" separately.")]),
      step("nUninstall", [t("To remove a database without uninstalling everything, right-click it in Object Explorer ▸ "), b("Delete"), t(" ▸ tick "), b("Close existing connections"), t(" ▸ OK.")]),

      // ---- Appendix ----
      h1("Quick reference"),
      tableOf(
        ["Setting", "Default install", "Express install"],
        [
          ["Server name", "localhost", ".\\SQLEXPRESS"],
          ["Authentication", "Windows Authentication", "Windows Authentication"],
          ["Service name", "SQL Server (MSSQLSERVER)", "SQL Server (SQLEXPRESS)"],
          ["Default port", "1433", "dynamic"],
          ["Run a query", "New Query, then F5", "New Query, then F5"],
        ],
        [2600, 3380, 3380]
      ),
      p([b("Useful links")], { spacing: { before: 180, after: 60 } }),
      bullet([link("SQL Server downloads", "https://www.microsoft.com/en-us/sql-server/sql-server-downloads")]),
      bullet([link("Install SSMS", "https://learn.microsoft.com/en-us/ssms/install/install")]),
      bullet([link("MSSQL extension for VS Code", "https://learn.microsoft.com/en-us/sql/tools/visual-studio-code/mssql-extensions")]),
      p([t("Then come back to the hub's "), b("SQL track"), t(" and run the examples against your own server.")], { spacing: { before: 160 } }),
    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("/mnt/user-data/outputs/Setting-up-SQL-Server-on-Windows.docx", buf);
  console.log("written:", buf.length, "bytes");
});
