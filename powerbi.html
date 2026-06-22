#!/usr/bin/env python3
"""Shared Posit-style cheat-sheet builder. build_cheatsheet(...) renders a
2-page, 3-column landscape reference card. Colours are themeable per track."""
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Table, TableStyle, Spacer, KeepTogether, Flowable,
                                NextPageTemplate)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT


def build_cheatsheet(out, title, subtitle, sections, *, accent, code_border=None,
                     code_bg="#EEF5F0", code_ink="#0F3D29", line="#D9E5DD",
                     band_title_color="#FFFFFF", footer_label="DPM Learning Hub",
                     url="ahmedwalid4499.github.io", intro=""):
    ACCENT = colors.HexColor(accent)
    CBORD = colors.HexColor(code_border or accent)
    INK = colors.HexColor("#26323F"); MUTED = colors.HexColor("#6B7280")
    CODEBG = colors.HexColor(code_bg); CODEINK = colors.HexColor(code_ink)
    LINE = colors.HexColor(line); BANDTXT = colors.HexColor(band_title_color)

    PW, PH = landscape(letter)
    M = 0.38 * inch; GUT = 13; HEADER_H = 62; NCOL = 3
    COLW = (PW - 2*M - (NCOL-1)*GUT) / NCOL

    desc = ParagraphStyle("desc", fontName="Helvetica", fontSize=7.2, leading=8.6, textColor=INK, alignment=TA_LEFT)
    codes = ParagraphStyle("code", fontName="Courier-Bold", fontSize=7.0, leading=8.4, textColor=CODEINK)
    introst = ParagraphStyle("intro", fontName="Helvetica", fontSize=7.4, leading=9.2, textColor=INK)

    class SectionHeader(Flowable):
        def __init__(self, text, w): super().__init__(); self.text=text; self.w=w; self.h=13
        def wrap(self, *a): return (self.w, self.h)
        def draw(self):
            c=self.canv; c.setFillColor(ACCENT); c.roundRect(0,0,self.w,self.h,2.5,fill=1,stroke=0)
            t=self.text.replace("&amp;","&").replace("&gt;",">").replace("&lt;","<")
            c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8); c.drawString(5,3.3,t.upper())

    def kv_table(rows, w):
        cw0=w*0.46; cw1=w-cw0
        data=[[Paragraph(code,codes),Paragraph(d,desc)] for code,d in rows]
        t=Table(data,colWidths=[cw0,cw1])
        t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),
            ("LEFTPADDING",(0,0),(-1,-1),3),("RIGHTPADDING",(0,0),(-1,-1),3),
            ("TOPPADDING",(0,0),(-1,-1),1.6),("BOTTOMPADDING",(0,0),(-1,-1),1.6),
            ("BACKGROUND",(0,0),(0,-1),CODEBG),("LINEBELOW",(0,0),(-1,-2),0.3,LINE),
            ("BOX",(0,0),(-1,-1),0.3,LINE)]))
        return t

    def section(titletext, rows, w=COLW):
        return KeepTogether([SectionHeader(titletext,w),Spacer(1,2.5),kv_table(rows,w),Spacer(1,7)])

    story=[NextPageTemplate("later")]
    if intro:
        story.append(Paragraph(intro, introst)); story.append(Spacer(1,7))
    for st, rows in sections:
        story.append(section(st, rows))

    def draw_header(canvas, doc, first):
        canvas.saveState()
        if first:
            canvas.setFillColor(ACCENT); canvas.rect(0,PH-HEADER_H,PW,HEADER_H,fill=1,stroke=0)
            canvas.setFillColor(BANDTXT); canvas.setFont("Helvetica-Bold",19); canvas.drawString(M,PH-30,title)
            canvas.setFont("Helvetica",9.5); canvas.drawString(M,PH-46,subtitle)
            canvas.setFont("Helvetica-Bold",9); canvas.drawRightString(PW-M,PH-38,url)
        canvas.setFillColor(MUTED); canvas.setFont("Helvetica",7)
        canvas.drawString(M,M*0.55,footer_label)
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

    doc=BaseDocTemplate(out,pagesize=landscape(letter),leftMargin=M,rightMargin=M,topMargin=M,bottomMargin=M,
                        title=title,author="DPM Learning Hub")
    doc.addPageTemplates([
        PageTemplate(id="first",frames=make_frames(PH-HEADER_H-6),onPage=on_first),
        PageTemplate(id="later",frames=make_frames(PH-M),onPage=on_later),
    ])
    doc.build(story)
    print("built:", out)
