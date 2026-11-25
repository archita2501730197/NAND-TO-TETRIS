#!/usr/bin/env python3
"""
Generates the Complete, Professional Capstone Project Report PDF
for Archita (Roll No: 2501730197, K = 97)
School of Engineering & Technology, K.R. Mangalam University
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Omit header on first page
        if self._pageNumber > 1:
            self.drawString(54, 750, "Nand to Tetris – I (ETCNTC301) | Capstone Project: Make the Computer Draw a Box")
            self.drawRightString(612 - 54, 750, "Archita (2501730197) | K = 97")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 612 - 54, 744)
            
        # Footer on all pages
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 612 - 54, 45)
        self.drawString(54, 32, "School of Engineering & Technology, K.R. Mangalam University")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 32, page_text)
            
        self.restoreState()


def build_pdf(output_path="Archita_2501730197_Capstone_Report.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=26,
        alignment=1,
        textColor=colors.HexColor("#0F172A")
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        alignment=1,
        textColor=colors.HexColor("#1E40AF")
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        spaceBefore=12,
        spaceAfter=5,
        textColor=colors.HexColor("#0F172A"),
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        spaceBefore=8,
        spaceAfter=3,
        textColor=colors.HexColor("#1E3A8A"),
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=5
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor("#0F172A")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#1E293B")
    )

    story = []

    # Title & Metadata Banner
    story.append(Paragraph("CAPSTONE PROJECT REPORT", title_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>Make the Computer Draw a Box</b>", ParagraphStyle('Sub', parent=title_style, fontSize=16, leading=20, textColor=colors.HexColor("#1D4ED8"))))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Course: Nand to Tetris – I (ETCNTC301 / ETCCNT301) | Individual Capstone Assignment<br/>School of Engineering & Technology, K.R. Mangalam University", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1D4ED8"), spaceAfter=10))

    # Section 1: Student Information & K Calculation
    story.append(Paragraph("1. Student Information & Personal Number (K = 97)", h1_style))
    
    k_table_data = [
        [Paragraph("Parameter / Field", table_header_style), Paragraph("Calculation / Specification", table_header_style)],
        [Paragraph("<b>Student Name</b>", table_cell_style), Paragraph("Archita", table_cell_style)],
        [Paragraph("<b>University Roll Number</b>", table_cell_style), Paragraph("2501730197", table_cell_style)],
        [Paragraph("<b>Course & Branch</b>", table_cell_style), Paragraph("B.Tech Computer Science & Engineering (AI & ML), Semester III", table_cell_style)],
        [Paragraph("<b>Personal Number (K)</b>", table_cell_style), Paragraph("<b>K = 97</b> (last two digits of 2501730197)", table_cell_style)],
        [Paragraph("<b>Assembler Extra Feature</b>", table_cell_style), Paragraph("<b>97 mod 3 = 1</b>: Line-numbered error reporting (e.g. <code>Line 7: invalid instruction</code>) instead of crashing on malformed input", table_cell_style)],
        [Paragraph("<b>Box Starting Row</b>", table_cell_style), Paragraph("<b>Row 97</b>", table_cell_style)],
        [Paragraph("<b>Box Height</b>", table_cell_style), Paragraph("<b>20 screen rows</b> (Rows 97 through 116 inclusive)", table_cell_style)],
        [Paragraph("<b>Box Width Calculation</b>", table_cell_style), Paragraph("<b>97 mod 4 = 1</b> &rarr; 16 &times; ((1) + 1) = <b>32 pixels</b> (2 consecutive 16-bit words per row)", table_cell_style)],
        [Paragraph("<b>Screen Base Address</b>", table_cell_style), Paragraph("SCREEN + 32 &times; K = 16384 + (32 &times; 97) = <b>19488</b> (0x4C20)", table_cell_style)],
        [Paragraph("<b>Interactive Behavior</b>", table_cell_style), Paragraph("Continuously senses keyboard (KBD = 24576). When any key is pressed, draws 32&times;20 black box (-1). When key is released, immediately erases box back to white (0).", table_cell_style)]
    ]
    k_table = Table(k_table_data, colWidths=[150, 354])
    k_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1D4ED8")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#F8FAFC"), colors.HexColor("#FFFFFF")])
    ]))
    story.append(k_table)
    story.append(Spacer(1, 10))

    # Section 2: Part A - Build Hack Computer
    story.append(Paragraph("2. Part A – Hack Computer HDL Implementation", h1_style))
    story.append(Paragraph(
        "The Hack computer hardware platform was built using HDL modules developed during the Nand to Tetris course:", body_style
    ))
    story.append(Paragraph(
        "<b>• Memory.hdl:</b> Implements the complete 15-bit address space. Addresses 0..16383 map to <code>RAM16K</code> (address[14]=0), addresses 16384..24575 map to the <code>Screen</code> memory buffer (address[14..13]=10), and address 24576 maps to the memory-mapped <code>Keyboard</code> register (address[14..13]=11). A <code>DMux4Way</code> routes the write load signal and a <code>Mux4Way16</code> routes the output.", body_style
    ))
    story.append(Paragraph(
        "<b>• CPU.hdl:</b> Executes 16-bit Hack machine instructions. For A-instructions (bit 15 = 0), the constant is loaded into the A register. For C-instructions (bit 15 = 1), ALU control bits c1..c6 perform arithmetic/logic on D and A/M, destination bits d1..d3 drive register loading and <code>writeM</code>, and jump bits j1..j3 combined with ALU flags <code>zr</code> and <code>ng</code> control PC branching.", body_style
    ))
    story.append(Paragraph(
        "<b>• Computer.hdl:</b> Interconnects <code>ROM32K</code>, <code>CPU</code>, and <code>Memory</code> into a self-contained Harvard architecture computer.", body_style
    ))

    # HDL Test Verification Table
    hdl_test_data = [
        [Paragraph("Test Script", table_header_style), Paragraph("Comparison File", table_header_style), Paragraph("Verification Result", table_header_style), Paragraph("Status", table_header_style)],
        [Paragraph("<code>CPU.tst</code>", table_cell_style), Paragraph("<code>CPU.cmp</code>", table_cell_style), Paragraph("Comparison ended successfully (All cycles matched)", table_cell_style), Paragraph("<b>PASSED</b>", table_cell_style)],
        [Paragraph("<code>Memory.tst</code>", table_cell_style), Paragraph("<code>Memory.cmp</code>", table_cell_style), Paragraph("Comparison ended successfully (RAM, Screen, KBD verified)", table_cell_style), Paragraph("<b>PASSED</b>", table_cell_style)],
        [Paragraph("<code>ComputerAdd.tst</code>", table_cell_style), Paragraph("<code>ComputerAdd.cmp</code>", table_cell_style), Paragraph("Comparison ended successfully (R0 = 2 + 3 = 5)", table_cell_style), Paragraph("<b>PASSED</b>", table_cell_style)]
    ]
    hdl_table = Table(hdl_test_data, colWidths=[90, 90, 244, 80])
    hdl_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0F766E")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('TEXTCOLOR', (3, 1), (3, -1), colors.HexColor("#047857")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#F0FDFA"), colors.HexColor("#FFFFFF")])
    ]))
    story.append(hdl_table)
    story.append(Spacer(1, 10))

    # Section 3: Part B - Python Assembler
    story.append(Paragraph("3. Part B – Two-Pass Python Assembler (assembler.py)", h1_style))
    story.append(Paragraph(
        "The Python assembler converts Hack symbolic instructions (<code>.asm</code>) into 16-bit binary machine code (<code>.hack</code>) using a two-pass architecture:", body_style
    ))
    story.append(Paragraph(
        "<b>1. First Pass (Label Discovery & Line Mapping):</b> Iterates through the assembly source, strips comments (<code>//</code>) and whitespace, tracks original line numbers, and maps pseudo-instructions like <code>(LOOP)</code> to the ROM instruction address of the subsequent instruction without advancing the ROM program counter.", body_style
    ))
    story.append(Paragraph(
        "<b>2. Second Pass (Translation & Symbol Allocation):</b> Translates A-instructions (<code>@value</code>) and C-instructions (<code>dest=comp;jump</code>). Predefined symbols (<code>R0-R15</code>, <code>SP</code>, <code>SCREEN</code>, <code>KBD</code>) and labels are resolved; new variables are dynamically assigned sequential RAM addresses starting at 16.", body_style
    ))
    story.append(Paragraph(
        "<b>3. Assigned Feature (K mod 3 = 1):</b> The assembler validates every token against official Hack specification tables. If an instruction contains an unknown comp mnemonic, invalid destination, invalid jump, or malformed label, it reports <code>Line &lt;N&gt;: invalid instruction (&lt;reason&gt;)</code> to <code>stderr</code> and terminates cleanly with exit code 1 without a Python exception traceback.", body_style
    ))

    # Assembler Benchmark Table
    asm_test_data = [
        [Paragraph("Benchmark", table_header_style), Paragraph("Instruction Types Tested", table_header_style), Paragraph("Official Comparison", table_header_style), Paragraph("Result", table_header_style)],
        [Paragraph("<code>Add.asm</code>", table_cell_style), Paragraph("A-instructions, constant loading, D/A arithmetic", table_cell_style), Paragraph("6 lines generated, exact 1:1 match", table_cell_style), Paragraph("<b>PASSED</b>", table_cell_style)],
        [Paragraph("<code>Max.asm</code>", table_cell_style), Paragraph("Labels, conditional jumps (JGT, JLE), variables", table_cell_style), Paragraph("16 lines generated, exact 1:1 match", table_cell_style), Paragraph("<b>PASSED</b>", table_cell_style)],
        [Paragraph("<code>Rect.asm</code>", table_cell_style), Paragraph("Screen base pointers, loops, memory writes", table_cell_style), Paragraph("25 lines generated, exact 1:1 match", table_cell_style), Paragraph("<b>PASSED</b>", table_cell_style)],
        [Paragraph("<code>Pong.asm</code>", table_cell_style), Paragraph("Complex Jack OS program with 27,000+ instructions", table_cell_style), Paragraph("27,483 lines, exact 1:1 match", table_cell_style), Paragraph("<b>PASSED</b>", table_cell_style)],
        [Paragraph("<code>test_bad.asm</code>", table_cell_style), Paragraph("Error diagnostics for K mod 3 = 1 on line 7", table_cell_style), Paragraph("Output: <code>Line 7: invalid instruction</code>", table_cell_style), Paragraph("<b>PASSED</b>", table_cell_style)]
    ]
    asm_table = Table(asm_test_data, colWidths=[80, 160, 184, 80])
    asm_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4338CA")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('TEXTCOLOR', (3, 1), (3, -1), colors.HexColor("#047857")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#EEF2FF"), colors.HexColor("#FFFFFF")])
    ]))
    story.append(asm_table)
    story.append(Spacer(1, 10))

    # Section 4: Part C - Box Program
    story.append(Paragraph("4. Part C – Box Drawing Program (Box.asm)", h1_style))
    story.append(Paragraph(
        "<b>Screen Memory Architecture:</b> The Hack screen consists of 256 rows &times; 512 columns. Each row is represented by 32 consecutive 16-bit words (32 &times; 16 = 512 pixels). Memory starts at <code>SCREEN</code> (16384).<br/>"
        "For <b>K = 97</b>, the box starts at <b>Row 97</b> &rarr; <code>SCREEN + 32 &times; 97 = 19488</code>.<br/>"
        "Width = <code>16 &times; ((97 mod 4) + 1) = 32 pixels</code> &rarr; <b>2 consecutive words per row</b> (Word 0 and Word 1 from left edge).<br/>"
        "Height = <b>20 screen rows</b> (spanning row 97 to row 116 inclusive).", body_style
    ))

    # ASCII Visual Map of Hack Screen
    ascii_box = """Hack Screen Buffer Simulation (Rows 95-118, Columns 0..35):
Row  95: ....................................
Row  96: ....................................
Row  97: ################################.... <== Box Starts at Row 97 (32 pixels wide)
Row  98: ################################....
Row  99: ################################....
Row 100: ################################....
Row 101: ################################....
Row 102: ################################....
Row 103: ################################....
Row 104: ################################....
Row 105: ################################....
Row 106: ################################....
Row 107: ################################....
Row 108: ################################....
Row 109: ################################....
Row 110: ################################....
Row 111: ################################....
Row 112: ################################....
Row 113: ################################....
Row 114: ################################....
Row 115: ################################....
Row 116: ################################.... <== Box Ends at Row 116 (20 rows high)
Row 117: ....................................
Row 118: ...................................."""
    story.append(Preformatted(ascii_box, code_style))
    story.append(Spacer(1, 8))

    # Section 5: Mistake Encountered & Fixed
    story.append(Paragraph("5. Programming Mistake Encountered & How It Was Fixed", h1_style))
    story.append(Paragraph(
        "<b>Mistake Encountered:</b> During the development of <code>Box.asm</code>, the assembler halted with an error:<br/>"
        "<code>Line 76: invalid instruction (Unknown computation mnemonic 'M+D' in 'M=M+D')</code><br/>"
        "<b>Technical Analysis:</b> Although mathematical addition is commutative, the Hack CPU hardware routes the D register to the ALU x-bus and the Memory/A-register to the y-bus. The Hack specification defines <code>D+M</code> as the only valid addition mnemonic between D and M; <code>M+D</code> is an illegal token in Hack assembly.<br/>"
        "<b>Resolution:</b> Thanks to our assigned feature (K mod 3 = 1), the exact line and invalid token were identified instantly without an unhandled program crash. The line was corrected to <code>M=D+M</code>. Additionally, the pointer reset logic for <code>rowAddr</code> (19488) and <code>rowCount</code> (20) was placed strictly inside the <code>(RENDER)</code> block, guaranteeing that every keypress cycle starts at row 97 without vertical memory drift.", body_style
    ))
    story.append(Spacer(1, 6))

    # Section 6: Viva Voce Preparation
    story.append(Paragraph("6. Individual Viva Voce Preparation (Quick Reference)", h1_style))
    viva_data = [
        [Paragraph("Viva Question", table_header_style), Paragraph("Precise Technical Explanation", table_header_style)],
        [Paragraph("<b>Q1. How does Memory.hdl route address buses?</b>", table_cell_style), Paragraph("Bits 14 and 13 decode address space: <code>00</code>/<code>01</code> access 16K RAM, <code>10</code> accesses 8K Screen map (16384-24575), and <code>11</code> accesses the Keyboard register at 24576.", table_cell_style)],
        [Paragraph("<b>Q2. How are labels vs variables handled in assembler.py?</b>", table_cell_style), Paragraph("Pass 1 records labels <code>(LABEL)</code> with their ROM instruction index. Pass 2 resolves labels and assigns new variables sequentially to RAM registers starting at 16.", table_cell_style)],
        [Paragraph("<b>Q3. How does the K mod 3 = 1 feature work?</b>", table_cell_style), Paragraph("Validates syntax against specification dictionaries. If an invalid token occurs, an <code>AssemblyError</code> outputs <code>Line &lt;N&gt;: invalid instruction</code> and exits cleanly.", table_cell_style)],
        [Paragraph("<b>Q4. How would you move the box down during viva?</b>", table_cell_style), Paragraph("Modify the base address <code>@19488</code> in <code>Box.asm</code>. Since each row contains 32 words, shifting down by 10 rows means changing <code>@19488</code> to <code>@19808</code> (19488 + 320).", table_cell_style)],
        [Paragraph("<b>Q5. How would you change the box width?</b>", table_cell_style), Paragraph("Inside <code>ROW_LOOP</code>, write to additional consecutive words per row (e.g. <code>rowAddr + 2</code> for 48 pixels, <code>rowAddr + 3</code> for 64 pixels).", table_cell_style)]
    ]
    viva_table = Table(viva_data, colWidths=[150, 354])
    viva_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0284C7")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#F0F9FF"), colors.HexColor("#FFFFFF")])
    ]))
    story.append(viva_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    out_pdf = "Archita_2501730197_Capstone_Report.pdf"
    if len(sys.argv) > 1:
        out_pdf = sys.argv[1]
    build_pdf(out_pdf)
