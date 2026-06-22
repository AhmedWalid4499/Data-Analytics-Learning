#!/usr/bin/env python3
# Excel Formula & Function Cheat Sheet — Posit/RStudio-style reference card (2-page, 3-column).
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Table, TableStyle, Spacer, KeepTogether, Flowable,
                                NextPageTemplate)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

OUT = "/mnt/user-data/outputs/Excel-Formula-Cheat-Sheet.pdf"

GREEN = colors.HexColor("#217346"); DARK = colors.HexColor("#14233A")
INK = colors.HexColor("#26323F"); MUTED = colors.HexColor("#6B7280")
CODEBG = colors.HexColor("#EEF5F0"); CODEINK = colors.HexColor("#0F3D29")
LINE = colors.HexColor("#D9E5DD")

PW, PH = landscape(letter)
M = 0.38 * inch; GUT = 13; HEADER_H = 62; NCOL = 3
COLW = (PW - 2*M - (NCOL-1)*GUT) / NCOL

desc = ParagraphStyle("desc", fontName="Helvetica", fontSize=7.2, leading=8.6, textColor=INK, alignment=TA_LEFT)
codes = ParagraphStyle("code", fontName="Courier-Bold", fontSize=7.0, leading=8.4, textColor=CODEINK)
sub = ParagraphStyle("sub", fontName="Helvetica-Bold", fontSize=7.4, leading=9, textColor=GREEN)
intro = ParagraphStyle("intro", fontName="Helvetica", fontSize=7.4, leading=9.2, textColor=INK)

class SectionHeader(Flowable):
    def __init__(self, text, w): super().__init__(); self.text=text; self.w=w; self.h=13
    def wrap(self,*a): return (self.w,self.h)
    def draw(self):
        c=self.canv; c.setFillColor(GREEN); c.roundRect(0,0,self.w,self.h,2.5,fill=1,stroke=0)
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
def subsection(title,rows,w=COLW):
    return KeepTogether([Spacer(1,1),Paragraph(title,sub),Spacer(1,1.5),kv_table(rows,w),Spacer(1,6)])

story=[NextPageTemplate("later")]
story.append(Paragraph("A printable reference for the formulas, functions and moves that cover most day-to-day Excel work. "
    "Examples assume a table with headers in row 1 and data in rows 2&#8211;100.", intro))
story.append(Spacer(1,7))

story.append(section("The basics",[
    ("=","Every formula starts with an equals sign."),
    ("=A1+A2*3","Operators: + - * / ^  and  &amp; (join text)."),
    ("( )","Parentheses force the order of evaluation."),
    ("F4","Toggle $ absolute refs while editing."),
    ("Ctrl+Enter","Fill the whole selection with one formula."),
    ("Alt+=","AutoSum the column/row above or left."),
]))
story.append(section("Operators &amp; order",[
    ("^","Power — evaluated first."),
    ("* /","Then multiply / divide."),
    ("+ -","Then add / subtract."),
    ("&amp;","Join text together."),
    ("= &lt;&gt; &gt; &lt; &gt;= &lt;=","Comparisons (evaluated last)."),
    ("( )","Override the order with parentheses."),
]))
story.append(section("Cell references",[
    ("A1","Relative — shifts when copied."),
    ("$A$1","Absolute — locked row and column."),
    ("A$1 / $A1","Mixed — lock row only / column only."),
    ("A1:B10","A rectangular range."),
    ("A:A / 2:2","A whole column / whole row."),
    ("Sheet2!A1","A cell on another sheet."),
    ("Table[Col]","A structured reference (Excel Table)."),
]))
story.append(section("Math &amp; statistics",[
    ("SUM(rng)","Add all numbers in a range."),
    ("AVERAGE(rng)","Arithmetic mean."),
    ("MEDIAN(rng)","Middle value."),
    ("COUNT(rng)","Count cells containing numbers."),
    ("COUNTA(rng)","Count non-empty cells."),
    ("COUNTBLANK(rng)","Count empty cells."),
    ("MIN / MAX(rng)","Smallest / largest value."),
    ("ROUND(x, n)","Round x to n decimals."),
    ("ROUNDUP / ROUNDDOWN","Round away from / toward zero."),
    ("INT(x) / MOD(a,b)","Integer part / remainder."),
    ("ABS(x)","Absolute (non-negative) value."),
    ("SUMPRODUCT(a, b)","Multiply arrays then sum — weighted totals."),
]))
story.append(section("Conditional aggregation",[
    ("SUMIF(rng, crit, [sum])","Sum where one condition is met."),
    ("SUMIFS(sum, r1,c1, r2,c2)","Sum where ALL conditions met. Sum range first."),
    ("COUNTIF(rng, crit)","Count matching one condition."),
    ("COUNTIFS(r1,c1, r2,c2)","Count matching all conditions."),
    ("AVERAGEIF(S)(...)","Mean of matching rows."),
    ("MAXIFS / MINIFS(...)","Max / min of matching rows."),
]))
story.append(subsection("Criteria you can pass",[
    ('"&gt;100"',"Greater than 100 (quote operators)."),
    ('"&lt;&gt;EMEA"',"Not equal to EMEA."),
    ('"*WAN*"',"Wildcards: * = any text, ? = one char."),
    ('"&gt;"&amp;G1',"Build criteria from a cell with &amp;."),
]))
story.append(section("Logic",[
    ("IF(test, yes, no)","Branch on a true/false test."),
    ("IFS(t1,v1, t2,v2, …)","Many tests in order — no nesting."),
    ("AND(a, b) / OR(a, b)","All true / any true."),
    ("NOT(a)","Reverse a true/false value."),
    ("IFERROR(x, fallback)","Replace any error with a fallback."),
    ("IFNA(x, fallback)","Catch only #N/A."),
    ("SWITCH(v, k1,r1, …, def)","Match a value to a result."),
]))
story.append(section("Lookups",[
    ("XLOOKUP(find, in, return,","Best modern lookup — looks left or right,"),
    ("  [if_na], [mode])","exact by default, with a not-found value."),
    ("VLOOKUP(find, tbl, col, 0)","Legacy. 0/FALSE = exact. Looks right only."),
    ("INDEX(rng, row, [col])","Value at a position in a range."),
    ("MATCH(find, rng, 0)","Position of a value (0 = exact)."),
    ("INDEX(ret, MATCH(...))","2-way lookup; survives column moves."),
]))
story.append(section("Common patterns",[
    ("=O2/SUM($O$2:$O$100)","% of total (lock the total)."),
    ("=SUM($O$2:O2)","Running total down a column."),
    ("=RANK.EQ(O2,$O$2:$O$100)","Rank a value within a list."),
    ("=(cur-prev)/prev","Year-on-year / growth %."),
    ("=COUNTIF($B$2:B2,B2)&gt;1","Flag duplicate rows TRUE/FALSE."),
    ('=IF(x=0,"",x)',"Show blank instead of zero."),
]))
story.append(section("Text",[
    ("LEN(t)","Number of characters."),
    ("LEFT / RIGHT(t, n)","First / last n characters."),
    ("MID(t, start, n)","n characters from a position."),
    ("FIND / SEARCH(sub, t)","Position of text (SEARCH ignores case)."),
    ("SUBSTITUTE(t, old, new)","Replace text by content."),
    ("UPPER / LOWER / PROPER","Change case."),
    ("TRIM(t)","Strip extra spaces."),
    ("CONCAT(a, b) / a&amp;b","Join text."),
    ('TEXTJOIN(", ",TRUE,rng)',"Join a range, skip blanks."),
    ('TEXT(v, "0.0%")',"Format a number as text by a pattern."),
]))
story.append(section("Dates &amp; time",[
    ("TODAY() / NOW()","Current date / date-time (live)."),
    ("DATE(y, m, d)","Build a date from parts."),
    ("YEAR / MONTH / DAY(d)","Pull a part out of a date."),
    ("EDATE(d, n)","n months after a date."),
    ("EOMONTH(d, n)","End of month, n months out."),
    ("WEEKDAY(d, 2)","Day number (2 = Mon..Sun)."),
    ("NETWORKDAYS(a, b)","Working days between two dates."),
    ('DATEDIF(a, b, "d")',"Difference in d / m / y units."),
]))
story.append(section("Number format codes",[
    ("0","Whole number."),
    ("#,##0","Thousands separator."),
    ("0.0%","Percent, one decimal."),
    ('"€"#,##0',"Currency prefix."),
    ("yyyy-mm-dd","ISO date."),
    ("0;[Red]-0","Negatives in red."),
]))
story.append(section("Dynamic arrays (365)",[
    ("FILTER(rng, condition)","Return only rows meeting a condition."),
    ("SORT(rng, [col], [order])","Sort a range; spills automatically."),
    ("SORTBY(rng, byrng, …)","Sort by another range."),
    ("UNIQUE(rng)","Distinct values, live."),
    ("SEQUENCE(rows, [cols])","Generate a list of numbers."),
    ("A2#","The # spill operator = the whole spilled range."),
]))
story.append(section("LET &amp; LAMBDA (365)",[
    ("LET(name, val, …, calc)","Name sub-results once, reuse them; clearer &amp; faster."),
    ("LAMBDA(x, x*2)","Define a reusable custom function."),
    ("Name Manager","Save a LAMBDA as your own named function."),
]))
story.append(section("Financial",[
    ("PMT(rate, nper, pv)","Loan/lease payment per period."),
    ("FV(rate, nper, pmt)","Future value of savings."),
    ("PV(rate, nper, pmt)","Present value."),
    ("NPV(rate, cashflows)","Net present value of cash flows."),
    ("RATE(nper, pmt, pv)","Interest rate per period."),
]))
story.append(section("Error values",[
    ("#DIV/0!","Divided by zero or an empty cell."),
    ("#N/A","A lookup found no match."),
    ("#VALUE!","Wrong type — text where a number is needed."),
    ("#NAME?","Unknown function or misspelt name."),
    ("#REF!","A referenced cell was deleted."),
    ("#NUM!","Invalid number for the calculation."),
    ("#SPILL!","A dynamic array can't spill — clear the cells."),
]))
story.append(section("PivotTable in 5 steps",[
    ("1","Click any cell in your data."),
    ("2","Insert &gt; PivotTable &gt; OK."),
    ("3","Drag a category to Rows."),
    ("4","Drag a number to Values."),
    ("5","Set Values to Sum (not Count) &amp; format."),
]))
story.append(section("Power Query in 5 steps",[
    ("1","Data &gt; Get Data (or From Table/Range)."),
    ("2","Clean: split, replace, change types, remove cols."),
    ("3","Each action is recorded as an Applied Step."),
    ("4","Close &amp; Load to a sheet."),
    ("5","New file next week? Just Refresh All."),
]))
story.append(section("Conditional formatting",[
    ("1","Select the range."),
    ("2","Home &gt; Conditional Formatting."),
    ("3","Pick a rule (Highlight, Data Bars, Scales)."),
    ("4","Use a formula rule for full control."),
]))
story.append(section("Data validation (dropdowns)",[
    ("1","Select the cells."),
    ("2","Data &gt; Data Validation."),
    ("3","Allow: List &gt; Source = range or items."),
    ("4","Add optional input / error messages."),
]))
story.append(section("Named ranges",[
    ("Name box","Type a name for a selection, press Enter."),
    ("=Revenue","Use the name in any formula."),
    ("Formulas &gt; Name Mgr","Edit or delete names."),
]))
story.append(section("Handy shortcuts (Windows)",[
    ("Ctrl+; / Ctrl+Shift+;","Insert today's date / time."),
    ("Ctrl+Shift+L","Toggle filters."),
    ("Ctrl+T","Make a range an Excel Table."),
    ("Ctrl+Arrow","Jump to edge of data."),
    ("Ctrl+Shift+Arrow","Select to edge of data."),
    ("F2 / Esc","Edit a cell / cancel editing."),
    ("Ctrl+`","Show formulas instead of results."),
]))
story.append(section("Tips that save hours",[
    ("Lock with $","Press F4 before copying a formula down."),
    ("Tables, not ranges","Ctrl+T — formulas auto-extend &amp; read clearly."),
    ("IFERROR wrap","Hide expected errors, not real bugs."),
    ("XLOOKUP &gt; VLOOKUP","No column counting; looks both directions."),
    ("Don't repeat work","Cleaning weekly? Use Power Query."),
]))

def draw_header(canvas,doc,first):
    canvas.saveState()
    if first:
        canvas.setFillColor(GREEN); canvas.rect(0,PH-HEADER_H,PW,HEADER_H,fill=1,stroke=0)
        canvas.setFillColor(colors.white); canvas.setFont("Helvetica-Bold",19)
        canvas.drawString(M,PH-30,"Excel Formula & Function Cheat Sheet")
        canvas.setFont("Helvetica",9.5)
        canvas.drawString(M,PH-46,"A double-sided quick reference  ·  DPM Learning Hub")
        canvas.setFont("Helvetica-Bold",9); canvas.drawRightString(PW-M,PH-38,"ahmedwalid4499.github.io")
    canvas.setFillColor(MUTED); canvas.setFont("Helvetica",7)
    canvas.drawString(M,M*0.55,"DPM Learning Hub — Excel track")
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
                    title="Excel Formula & Function Cheat Sheet",author="DPM Learning Hub")
doc.addPageTemplates([
    PageTemplate(id="first",frames=make_frames(PH-HEADER_H-6),onPage=on_first),
    PageTemplate(id="later",frames=make_frames(PH-M),onPage=on_later),
])
doc.build(story)
print("built:",OUT)
