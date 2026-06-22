#!/usr/bin/env python3
# DPM Learning Hub — 12-Week Study Plan (printable PDF planner).
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Table, TableStyle, Spacer, KeepTogether, Flowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

OUT = "/mnt/user-data/outputs/DPM-12-Week-Study-Plan.pdf"

NAVY = colors.HexColor("#14233A"); ACCENT = colors.HexColor("#FF7900")
INK = colors.HexColor("#26323F"); MUTED = colors.HexColor("#6B7280")
LINE = colors.HexColor("#E2E6EB"); SOFT = colors.HexColor("#F4F6F8")

PW, PH = letter
M = 0.7 * inch; BAND_H = 96
CW = PW - 2*M

h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=NAVY, spaceBefore=2, spaceAfter=1)
body = ParagraphStyle("body", fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=INK)
small = ParagraphStyle("small", fontName="Helvetica", fontSize=8.6, leading=12, textColor=MUTED)
task = ParagraphStyle("task", fontName="Helvetica", fontSize=9.3, leading=12.6, textColor=INK)
chkp = ParagraphStyle("chkp", fontName="Helvetica-BoldOblique", fontSize=8.8, leading=12, textColor=colors.HexColor("#B45309"))
wkhead = ParagraphStyle("wkhead", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=NAVY)
wktime = ParagraphStyle("wktime", fontName="Helvetica", fontSize=8.3, leading=11, textColor=MUTED, alignment=2)
lead = ParagraphStyle("lead", fontName="Helvetica", fontSize=10, leading=14.5, textColor=INK)


class Box(Flowable):
    def __init__(self, s=9): super().__init__(); self.s=s
    def wrap(self,*a): return (self.s+3, self.s)
    def draw(self):
        c=self.canv; c.setStrokeColor(ACCENT); c.setLineWidth(1); c.roundRect(0,0,self.s,self.s,1.5,stroke=1,fill=0)


class MonthBar(Flowable):
    def __init__(self, num, title, w): super().__init__(); self.num=num; self.title=title; self.w=w; self.h=22
    def wrap(self,*a): return (self.w, self.h)
    def draw(self):
        c=self.canv; c.setFillColor(NAVY); c.roundRect(0,0,self.w,self.h,3,fill=1,stroke=0)
        c.setFillColor(ACCENT); c.rect(0,0,5,self.h,fill=1,stroke=0)
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",11.5)
        c.drawString(14,6.5,("MONTH %d  ·  " % self.num)+self.title.upper())


def tasks_table(items):
    data=[[Box(), Paragraph(t, task)] for t in items]
    t=Table(data, colWidths=[16, CW-16])
    t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),2.5),("BOTTOMPADDING",(0,0),(-1,-1),2.5),
        ("LEFTPADDING",(1,0),(1,-1),6)]))
    return t


def week(num, focus, time, items, foot, milestone=False):
    head=Table([[Paragraph("Week %d &nbsp;·&nbsp; %s" % (num, focus), wkhead),
                 Paragraph(time, wktime)]], colWidths=[CW*0.72, CW*0.28])
    head.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),3),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    foot_p=Paragraph(("&#9873; Milestone: " if milestone else "&#10003; Checkpoint: ")+foot, chkp)
    inner=[head, tasks_table(items), Spacer(1,3), foot_p]
    block=Table([[inner]], colWidths=[CW])
    block.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),SOFT),("BOX",(0,0),(-1,-1),0.5,LINE),
        ("LEFTPADDING",(0,0),(-1,-1),11),("RIGHTPADDING",(0,0),(-1,-1),11),
        ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),9),("ROUNDEDCORNERS",[4,4,4,4])]))
    return KeepTogether([block, Spacer(1,9)])


story=[]
story.append(Paragraph("This plan turns the hub into a guided, twelve-week course — about <b>4–6 hours a week</b>. "
    "Each week lists what to study, what to practise in the in-browser runners, and a checkpoint to tick off. "
    "The order matters: each tool builds on the one before, so resist jumping ahead.", lead))
story.append(Spacer(1,7))
legend=Table([[Box(), Paragraph("a task to complete", small), Paragraph("&#10003; checkpoint = prove you can do it", small),
               Paragraph("&#9873; milestone = a graded exam &#8805; 80%", small)]],
             colWidths=[16, CW*0.30, CW*0.36, CW*0.40-16])
legend.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),0),
    ("RIGHTPADDING",(0,0),(-1,-1),4),("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
    ("LEFTPADDING",(1,0),(1,0),6)]))
story.append(legend)
story.append(Spacer(1,11))

# Path at a glance
story.append(Paragraph("The path at a glance", h2))
path=[("1","Foundations","Wk 1","how data is structured — the groundwork"),
      ("2","Excel","Wk 2–4","everyday analysis, lookups & PivotTables"),
      ("3","SQL","Wk 5–8","ask the same data bigger questions"),
      ("4","Power BI","Wk 9–10","model the data and visualise it"),
      ("5","Power Automate","Wk 11","automate the work around it"),
      ("\u2605","Capstone","Wk 12","put all four together, end to end")]
prow=[]
for n,t,wk,_ in path:
    prow.append(Paragraph("<b>%s</b> %s<br/><font size=7 color='#6B7280'>%s</font>"%(n,t,wk),
                ParagraphStyle("p",fontName="Helvetica",fontSize=8.6,leading=10.5,textColor=INK,alignment=1)))
pt=Table([prow], colWidths=[CW/6]*6)
pt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),NAVY),("TEXTCOLOR",(0,0),(-1,-1),colors.white),
    ("BOX",(0,0),(-1,-1),0,NAVY),("INNERGRID",(0,0),(-1,-1),0.5,colors.HexColor("#2C3E55")),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
# recolor text white via paragraph color override
prow2=[]
for n,t,wk,_ in path:
    prow2.append(Paragraph("<b>%s &nbsp;%s</b><br/><font size=7>%s</font>"%(n,t,wk),
                 ParagraphStyle("pw",fontName="Helvetica",fontSize=8.6,leading=11,textColor=colors.white,alignment=1)))
pt=Table([prow2], colWidths=[CW/6]*6)
pt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),NAVY),("INNERGRID",(0,0),(-1,-1),0.6,colors.HexColor("#2C3E55")),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
story.append(pt)
story.append(Spacer(1,5))
story.append(Paragraph("<b>How they fit together:</b> the same idea recurs in every tool — summarise a measure by a dimension. "
    "Excel's <font face='Courier'>SUMIFS</font> &#8776; SQL's <font face='Courier'>GROUP BY</font> &#8776; Power BI's "
    "<font face='Courier'>CALCULATE</font>. A PivotTable is OLAP on your desktop, and the star schema you learn in Foundations "
    "powers both your SQL joins and your Power BI model.", small))
story.append(Spacer(1,12))

# ---- MONTH 1 ----
story.append(MonthBar(1, "Foundations & Excel", CW)); story.append(Spacer(1,8))
story.append(week(1,"Data foundations","~4 hrs",
    ["Read the <b>Foundations</b> page end to end: tables &amp; keys, how rows are stored, ER &amp; EER diagrams, star vs snowflake, and OLAP.",
     "Do all the self-check quizzes. Be able to explain a star schema and the five OLAP operations (slice, dice, drill down, roll up, pivot).",
     "Skim the Excel cheat sheet so you know what's coming."],
    "you can explain primary vs foreign keys and what OLAP slice / dice / drill mean."))
story.append(week(2,"Excel — Basics","~5 hrs",
    ["Excel track, <b>Basic</b> tier: SUM / AVERAGE / COUNT, cell references and the <font face='Courier'>$</font> lock, IF and IFERROR.",
     "Download the sample workbook and follow along; use the <b>formula runner</b> for every <i>Try it</i>.",
     "Keep the Excel cheat sheet open as you work."],
    "rebuild three Basic worked examples from scratch in your own sheet."))
story.append(week(3,"Excel — Intermediate","~5 hrs",
    ["<b>Intermediate</b> tier: SUMIFS &amp; COUNTIFS, XLOOKUP and INDEX/MATCH, the key text and date functions.",
     "Practise writing criteria (\"&gt;100\", wildcards, cell references) until they're automatic."],
    "answer five \"by region / by status\" questions using SUMIFS and COUNTIFS."))
story.append(week(4,"Excel — Advanced + PivotTables","~6 hrs",
    ["<b>Advanced</b> tier: dynamic arrays (FILTER / UNIQUE / SORT) and LET; plus Power Query basics for repeatable cleaning.",
     "Work the <b>PivotTables</b> section and map each layout back to OLAP — rows/columns are dimensions, Values is the measure.",
     "Sit the <b>Excel exam</b>. Retake it until you're comfortable."],
    "Excel exam &#8805; 80%.", milestone=True))

# ---- MONTH 2 ----
story.append(MonthBar(2, "SQL", CW)); story.append(Spacer(1,8))
story.append(week(5,"SQL — Basics","~5 hrs",
    ["SQL track, <b>Basic</b> tier: SELECT / FROM, WHERE, ORDER BY / LIMIT, DISTINCT.",
     "Run every example in the <b>SQL runner</b> (a real database in your browser) and tweak it to see what changes."],
    "write five queries that filter and sort the orders table."))
story.append(week(6,"SQL — Intermediate","~5 hrs",
    ["Aggregates + GROUP BY, HAVING, and JOINs across the orders and targets tables.",
     "Notice the bridge from last month: Excel's SUMIFS is SQL's GROUP BY."],
    "reproduce a PivotTable result (revenue by region) as a GROUP BY query."))
story.append(week(7,"SQL — Advanced","~6 hrs",
    ["CASE for if-then logic, subqueries, CTEs (WITH), and window functions (RANK, running totals).",
     "Rewrite a nested subquery as a CTE to feel why CTEs read better."],
    "return the top-N orders per region using a window function."))
story.append(week(8,"Consolidate SQL","~4 hrs",
    ["Redo the trickiest <i>Try it</i> tasks without looking. Optionally install SQL Server with the setup guide and load the CSV.",
     "Sit the <b>SQL exam</b>."],
    "SQL exam &#8805; 80%.", milestone=True))

# ---- MONTH 3 ----
story.append(MonthBar(3, "Power BI, Power Automate & integration", CW)); story.append(Spacer(1,8))
story.append(week(9,"Power BI — model","~5 hrs",
    ["Power BI track, <b>Basic</b> &amp; <b>Intermediate</b>: Power Query (get &amp; shape), then relationships and the star schema.",
     "This is where Foundations pays off — build the model the way week 1 described."],
    "load the sample data and build a clean star-schema model."))
story.append(week(10,"Power BI — DAX & visuals","~6 hrs",
    ["<b>Advanced</b> tier: measures vs columns, CALCULATE and filter context, time intelligence; then the chart chooser.",
     "Use the <b>DAX checker</b> to validate each measure as you write it.",
     "Sit the <b>Power BI exam</b>."],
    "Power BI exam &#8805; 80%.", milestone=True))
story.append(week(11,"Power Automate","~5 hrs",
    ["Power Automate track: triggers and actions, conditions and loops, and expressions; plus the four flow types.",
     "Sketch a flow that emails an alert when an order is overdue.",
     "Sit the <b>Power Automate exam</b>."],
    "Power Automate exam &#8805; 80%.", milestone=True))
story.append(week(12,"Capstone — put it together","~6 hrs",
    ["End to end: clean the <b>messy dataset</b> in Power Query &#8594; model it in Power BI &#8594; write three key measures &#8594; build a one-page report &#8594; design a Power Automate alert around it.",
     "Revisit any track whose exam was below 80% and close the gap."],
    "a one-page dashboard plus an automation design, built start to finish.", milestone=True))

# Tips
story.append(MonthBar(0, "Make it stick", CW)) if False else None
tipbar=MonthBar(1,"",0)  # not used
story.append(Spacer(1,2))
story.append(Paragraph("Five tips to finish", h2))
for t in ["<b>Consistency beats intensity.</b> Three or four short sessions a week beat one long cram.",
          "<b>Always try before you reveal.</b> The struggle on each <i>Try it</i> is where the learning sticks.",
          "<b>Keep the cheat sheet for the current tool open</b> while you practise.",
          "<b>Type, don't read.</b> Re-run every example in the runner and change something.",
          "<b>Retake the exams.</b> They're randomised — a score above 80% twice means it's real."]:
    story.append(tasks_table([t])); 
story.append(Spacer(1,6))
story.append(Paragraph("Everything you need is in the hub at <b>ahmedwalid4499.github.io</b> — pages, runners, exams and the cheat sheets on the Downloads page.", small))


def band(canvas, doc, first):
    canvas.saveState()
    if first:
        canvas.setFillColor(NAVY); canvas.rect(0, PH-BAND_H, PW, BAND_H, fill=1, stroke=0)
        canvas.setFillColor(ACCENT); canvas.rect(0, PH-BAND_H, PW, 5, fill=1, stroke=0)
        canvas.setFillColor(ACCENT); canvas.setFont("Helvetica-Bold",10); canvas.drawString(M, PH-32, "DPM LEARNING HUB")
        canvas.setFillColor(colors.white); canvas.setFont("Helvetica-Bold",26); canvas.drawString(M, PH-60, "12-Week Study Plan")
        canvas.setFillColor(colors.HexColor("#C7D0DC")); canvas.setFont("Helvetica",11)
        canvas.drawString(M, PH-80, "From spreadsheets to dashboards to automations  ·  about 4\u20136 hours a week")
    canvas.setFillColor(MUTED); canvas.setFont("Helvetica",7.5)
    canvas.drawString(M, M*0.5, "DPM Learning Hub — 12-Week Study Plan")
    canvas.drawRightString(PW-M, M*0.5, "Page %d" % doc.page)
    canvas.setStrokeColor(LINE); canvas.setLineWidth(0.5); canvas.line(M, M*0.5+11, PW-M, M*0.5+11)
    canvas.restoreState()

def on_first(c,d): band(c,d,True)
def on_later(c,d): band(c,d,False)

doc=BaseDocTemplate(OUT, pagesize=letter, leftMargin=M, rightMargin=M, topMargin=M, bottomMargin=M,
                    title="DPM Learning Hub — 12-Week Study Plan", author="DPM Learning Hub")
fb=M*0.5+16
first=Frame(M, fb, CW, PH-BAND_H-12-fb, leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
later=Frame(M, fb, CW, PH-M-fb, leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
doc.addPageTemplates([PageTemplate(id="first",frames=[first],onPage=on_first),
                      PageTemplate(id="later",frames=[later],onPage=on_later)])
from reportlab.platypus import NextPageTemplate
story.insert(0, NextPageTemplate("later"))
doc.build(story)
print("built:", OUT)
