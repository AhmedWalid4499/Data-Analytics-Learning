#!/usr/bin/env python3
# SQL Cheat Sheet — Posit/RStudio-style reference card (2-page, 3-column), teal theme.
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Table, TableStyle, Spacer, KeepTogether, Flowable,
                                NextPageTemplate)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

OUT = "/mnt/user-data/outputs/SQL-Cheat-Sheet.pdf"

TEAL = colors.HexColor("#0E7490"); DARK = colors.HexColor("#14233A")
INK = colors.HexColor("#26323F"); MUTED = colors.HexColor("#6B7280")
CODEBG = colors.HexColor("#ECF6F9"); CODEINK = colors.HexColor("#0B3B45")
LINE = colors.HexColor("#D5E6EC")

PW, PH = landscape(letter)
M = 0.38 * inch; GUT = 13; HEADER_H = 62; NCOL = 3
COLW = (PW - 2*M - (NCOL-1)*GUT) / NCOL

desc = ParagraphStyle("desc", fontName="Helvetica", fontSize=7.2, leading=8.6, textColor=INK, alignment=TA_LEFT)
codes = ParagraphStyle("code", fontName="Courier-Bold", fontSize=7.0, leading=8.4, textColor=CODEINK)
sub = ParagraphStyle("sub", fontName="Helvetica-Bold", fontSize=7.4, leading=9, textColor=TEAL)
intro = ParagraphStyle("intro", fontName="Helvetica", fontSize=7.4, leading=9.2, textColor=INK)

class SectionHeader(Flowable):
    def __init__(self, text, w): super().__init__(); self.text=text; self.w=w; self.h=13
    def wrap(self,*a): return (self.w,self.h)
    def draw(self):
        c=self.canv; c.setFillColor(TEAL); c.roundRect(0,0,self.w,self.h,2.5,fill=1,stroke=0)
        txt=self.text.replace("&amp;","&").replace("&gt;",">").replace("&lt;","<")
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8); c.drawString(5,3.3,txt.upper())

def kv_table(rows,w):
    cw0=w*0.46; cw1=w-cw0
    data=[[Paragraph(code,codes),Paragraph(d,desc)] for code,d in rows]
    t=Table(data,colWidths=[cw0,cw1])
    t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),3),("RIGHTPADDING",(0,0),(-1,-1),3),
        ("TOPPADDING",(0,0),(-1,-1),1.6),("BOTTOMPADDING",(0,0),(-1,-1),1.6),
        ("BACKGROUND",(0,0),(0,-1),CODEBG),("LINEBELOW",(0,0),(-1,-2),0.3,LINE),
        ("BOX",(0,0),(-1,-1),0.3,LINE)]))
    return t

def section(title,rows,w=COLW):
    return KeepTogether([SectionHeader(title,w),Spacer(1,2.5),kv_table(rows,w),Spacer(1,7)])

story=[NextPageTemplate("later")]
story.append(Paragraph("A printable quick reference for everyday SQL — reading, summarising and joining data. "
    "Examples use standard / SQLite-style syntax; a few dialect differences are flagged at the end.", intro))
story.append(Spacer(1,7))

story.append(section("The basics",[
    ("SELECT a, b","Choose the columns to return."),
    ("SELECT *","Return every column."),
    ("FROM t","The table to read from."),
    ("AS name","Rename a column or table (alias)."),
    (";","Ends a statement."),
    ("-- text","Single-line comment ( /* … */ block)."),
]))
story.append(section("Clause order",[
    ("Written:","SELECT &gt; FROM &gt; WHERE &gt; GROUP BY &gt; HAVING &gt; ORDER BY &gt; LIMIT"),
    ("Runs as:","FROM &gt; WHERE &gt; GROUP BY &gt; HAVING &gt; SELECT &gt; ORDER BY &gt; LIMIT"),
    ("Why it matters","SELECT runs late — so a column alias can't be used in WHERE."),
]))
story.append(section("Filter rows — WHERE",[
    ("WHERE region = 'EMEA'","Keep matching rows. Text in single quotes."),
    ("= &lt;&gt; &gt; &lt; &gt;= &lt;=","Comparison operators (&lt;&gt; = not equal)."),
    ("AND / OR / NOT","Combine or negate conditions."),
    ("( … )","Group conditions to control precedence."),
]))
story.append(section("Match &amp; ranges",[
    ("LIKE 'SD-WAN%'","Pattern: % = any text, _ = one char."),
    ("IN ('A','B','C')","Equals any value in a list."),
    ("BETWEEN 10 AND 20","Inclusive range (numbers or dates)."),
    ("IS NULL / IS NOT NULL","Test for missing values."),
    ("NOT IN / NOT LIKE","Negate a match."),
]))
story.append(section("Sort, limit, dedupe",[
    ("ORDER BY revenue DESC","Sort high-to-low (ASC = default)."),
    ("ORDER BY 2","Sort by the 2nd selected column."),
    ("LIMIT 10","Return only the first 10 rows."),
    ("LIMIT 10 OFFSET 20","Skip 20, then take 10 (paging)."),
    ("SELECT DISTINCT col","Return each value once."),
]))
story.append(section("Aggregate functions",[
    ("COUNT(*)","Number of rows."),
    ("COUNT(col)","Non-NULL values in a column."),
    ("COUNT(DISTINCT col)","Number of distinct values."),
    ("SUM / AVG(col)","Total / mean."),
    ("MIN / MAX(col)","Smallest / largest."),
    ("ROUND(x, 1)","Round to n decimals."),
]))
story.append(section("GROUP BY &amp; HAVING",[
    ("GROUP BY region","One result row per group."),
    ("SUM(rev) AS total","Aggregate within each group; alias it."),
    ("HAVING COUNT(*) &gt;= 10","Filter groups after aggregating."),
    ("WHERE vs HAVING","WHERE filters rows first; HAVING filters groups."),
]))
story.append(section("Joins",[
    ("FROM a JOIN b ON a.id=b.id","INNER join — only matching rows."),
    ("LEFT JOIN b ON …","All left rows + matches (NULLs if none)."),
    ("RIGHT / FULL JOIN","All right / all rows from both sides."),
    ("CROSS JOIN","Every combination (no ON)."),
    ("FROM orders o JOIN …","Alias tables to keep refs short (o.col)."),
    ("USING (region)","Shorthand when the key name matches."),
]))
story.append(section("Set operators",[
    ("UNION","Stack two results, remove duplicates."),
    ("UNION ALL","Stack, keep duplicates (faster)."),
    ("INTERSECT","Rows present in both."),
    ("EXCEPT","Rows in the first but not the second."),
]))
story.append(section("Subqueries",[
    ("WHERE x &gt; (SELECT AVG(x) …)","Scalar — a single value."),
    ("WHERE id IN (SELECT id …)","List — match against many values."),
    ("WHERE EXISTS (SELECT 1 …)","True if the subquery returns any row."),
    ("FROM (SELECT …) AS s","Derived table — query a query."),
]))
story.append(section("CTE — WITH",[
    ("WITH t AS (","Name a temporary result set,"),
    ("  SELECT … )","build it once,"),
    ("SELECT * FROM t","then use it like a table — clearer than nesting."),
    ("WITH a AS(…), b AS(…)","Chain several CTEs with commas."),
]))
story.append(section("Window functions",[
    ("ROW_NUMBER() OVER (ORDER BY x)","Sequential number per row."),
    ("RANK() / DENSE_RANK()","Ranking (with / without gaps)."),
    ("SUM(x) OVER (PARTITION BY g)","Group total shown on every row."),
    ("SUM(x) OVER (ORDER BY d)","Running total."),
    ("LAG / LEAD(x) OVER (ORDER BY d)","Previous / next row's value."),
]))
story.append(section("CASE — if/then",[
    ("CASE WHEN x&gt;=30000","Start a conditional expression."),
    ("  THEN 'big'","Result when the test is true."),
    ("  ELSE 'small' END","Fallback; END closes it."),
    ("Use it in SELECT","…or inside SUM() to pivot, or in ORDER BY."),
]))
story.append(section("Text functions",[
    ("UPPER(s) / LOWER(s)","Change case."),
    ("LENGTH(s)","Number of characters."),
    ("SUBSTR(s, start, len)","Slice out part of a string."),
    ("TRIM(s)","Strip leading/trailing spaces."),
    ("REPLACE(s, old, new)","Swap text by content."),
    ("a || b","Concatenate (CONCAT() in some dialects)."),
]))
story.append(section("Numbers &amp; math",[
    ("ROUND(x, n) / ABS(x)","Round / absolute value."),
    ("CEIL(x) / FLOOR(x)","Round up / down to integer."),
    ("a % b","Remainder (MOD(a,b) in some dialects)."),
    ("100.0 * a / b","Force decimals — integer / integer truncates."),
]))
story.append(section("Dates (vary by dialect)",[
    ("CURRENT_DATE / NOW()","Today / current timestamp."),
    ("SQLite","DATE('now'), strftime('%Y', d)"),
    ("PostgreSQL","DATE_PART('year', d), d - INTERVAL '7 day'"),
    ("SQL Server","GETDATE(), DATEPART(year, d)"),
    ("Tip","Store dates as DATE/ISO text, not free text."),
]))
story.append(section("NULL handling",[
    ("IS NULL / IS NOT NULL","The only safe NULL test."),
    ("x = NULL","Never matches — NULL is 'unknown'."),
    ("COALESCE(a, b, 0)","First value that isn't NULL."),
    ("NULLIF(a, b)","NULL when a equals b (avoid /0)."),
]))
story.append(section("Create &amp; constrain (DDL)",[
    ("CREATE TABLE t (","Define a new table:"),
    ("  id INTEGER PRIMARY KEY,","types: INTEGER, REAL, TEXT, DATE, BOOLEAN"),
    ("  region TEXT NOT NULL,","NOT NULL · UNIQUE · DEFAULT v"),
    ("  cust_id INT REFERENCES c(id))","FOREIGN KEY links tables."),
    ("DROP / ALTER TABLE","Remove a table / add a column."),
]))
story.append(section("Modify data (DML)",[
    ("INSERT INTO t (a,b) VALUES (1,'x')","Add a row."),
    ("INSERT INTO t SELECT …","Insert query results."),
    ("UPDATE t SET a=1 WHERE id=5","Change rows — always add WHERE!"),
    ("DELETE FROM t WHERE id=5","Remove rows — WHERE or you clear all."),
]))
story.append(section("Common patterns",[
    ("Top-N per group","ROW_NUMBER() OVER(PARTITION BY g ORDER BY x DESC), keep rn&lt;=3"),
    ("% of total","100.0 * x / SUM(x) OVER ()"),
    ("Running total","SUM(x) OVER (ORDER BY d)"),
    ("Pivot a column","SUM(CASE WHEN region='EMEA' THEN rev END)"),
    ("De-duplicate","GROUP BY key  —or—  SELECT DISTINCT"),
]))
story.append(section("Gotchas",[
    ("'text' vs \"ident\"","Single quotes = text; double quotes = column/table names."),
    ("= NULL","Use IS NULL — equality never matches NULL."),
    ("Integer division","3/2 = 1; multiply by 1.0 for decimals."),
    ("COUNT(col)","Skips NULLs; COUNT(*) counts all rows."),
    ("Aggregates in WHERE","Not allowed — use HAVING."),
]))
story.append(section("Dialect quick notes",[
    ("Limit rows","LIMIT n (SQLite/PG/MySQL) · TOP n (SQL Server) · FETCH FIRST n ROWS"),
    ("Concatenate","a || b (standard/SQLite/PG) · CONCAT(a,b) (MySQL/SQL Server)"),
    ("Quote a name","\"col\" standard · [col] SQL Server · `col` MySQL"),
    ("Case sensitivity","LIKE is case-insensitive in some engines, not others."),
]))

story.append(section("Transactions",[
    ("BEGIN; … COMMIT;","Group changes and save them together."),
    ("ROLLBACK;","Undo everything since BEGIN."),
    ("Use for multi-step writes","All-or-nothing — no half-finished updates."),
]))
story.append(section("Views &amp; indexes",[
    ("CREATE VIEW v AS SELECT …","Save a query as a reusable virtual table."),
    ("SELECT * FROM v","Query the view like any table."),
    ("CREATE INDEX ix ON t(col)","Speed up filters and joins on a column."),
    ("Trade-off","Faster reads, slightly slower writes."),
]))
story.append(section("Performance tips",[
    ("Filter early","WHERE before joins/aggregates cuts the work."),
    ("Avoid SELECT *","Pull only the columns you need."),
    ("Index join &amp; filter keys","Big speed-up on large tables."),
    ("EXPLAIN your query","See how the engine plans to run it."),
    ("Keep functions off filters","WHERE YEAR(d)=2025 can skip an index."),
]))

story.append(section("Window frames",[
    ("… OVER (ORDER BY d","Add a frame to a window function:"),
    ("  ROWS BETWEEN 2 PRECEDING","a 3-row moving window"),
    ("  AND CURRENT ROW)","e.g. a 3-period moving average."),
    ("UNBOUNDED PRECEDING","From the first row (running total)."),
]))
story.append(section("String aggregation",[
    ("GROUP_CONCAT(col, ', ')","SQLite / MySQL: join a group into one string."),
    ("STRING_AGG(col, ', ')","PostgreSQL / SQL Server equivalent."),
    ("With GROUP BY","One combined value per group."),
]))
story.append(section("Conditional aggregation",[
    ("SUM(CASE WHEN c THEN 1 END)","Count rows meeting a condition."),
    ("AVG(CASE WHEN c THEN x END)","Aggregate just a subset, inline."),
    ("One CASE per column","Turns rows into a pivot table."),
]))
story.append(section("Reading a query",[
    ("Read inside-out","Start at FROM and the innermost subquery."),
    ("Build up gradually","Add one clause, run, check, repeat."),
    ("SELECT * first","See raw rows before you aggregate."),
    ("Comment to isolate","-- out lines to find a problem."),
]))
story.append(section("Tables &amp; relationships",[
    ("Primary key","Uniquely identifies each row."),
    ("One-to-many","Foreign key lives on the 'many' side."),
    ("Many-to-many","Add a junction table holding both keys."),
    ("See Foundations","for ERDs &amp; schema design."),
]))

def draw_header(canvas,doc,first):
    canvas.saveState()
    if first:
        canvas.setFillColor(TEAL); canvas.rect(0,PH-HEADER_H,PW,HEADER_H,fill=1,stroke=0)
        canvas.setFillColor(colors.white); canvas.setFont("Helvetica-Bold",19)
        canvas.drawString(M,PH-30,"SQL Cheat Sheet")
        canvas.setFont("Helvetica",9.5)
        canvas.drawString(M,PH-46,"A double-sided quick reference  ·  DPM Learning Hub")
        canvas.setFont("Helvetica-Bold",9); canvas.drawRightString(PW-M,PH-38,"ahmedwalid4499.github.io")
    canvas.setFillColor(MUTED); canvas.setFont("Helvetica",7)
    canvas.drawString(M,M*0.55,"DPM Learning Hub — SQL track")
    canvas.drawRightString(PW-M,M*0.55,"Page %d of 2"%doc.page)
    canvas.setStrokeColor(LINE); canvas.setLineWidth(0.5); canvas.line(M,M*0.55+11,PW-M,M*0.55+11)
    canvas.restoreState()

def on_first(c,d): draw_header(c,d,True)
def on_later(c,d): draw_header(c,d,False)

def make_frames(top_y):
    frames=[]; bottom=M*0.55+14; height=top_y-bottom
    for i in range(NCOL):
        x=M+i*(COLW+GUT)
        frames.append(Frame(x,bottom,COLW,height,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id="c%d"%i))
    return frames

doc=BaseDocTemplate(OUT,pagesize=landscape(letter),leftMargin=M,rightMargin=M,topMargin=M,bottomMargin=M,
                    title="SQL Cheat Sheet",author="DPM Learning Hub")
doc.addPageTemplates([
    PageTemplate(id="first",frames=make_frames(PH-HEADER_H-6),onPage=on_first),
    PageTemplate(id="later",frames=make_frames(PH-M),onPage=on_later),
])
doc.build(story)
print("built:",OUT)
