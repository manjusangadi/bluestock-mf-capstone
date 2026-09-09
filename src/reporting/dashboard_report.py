import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

PDF_PATH_ROOT = "Dashboard.pdf"
PDF_PATH_REPORTS = "reports/Dashboard.pdf"

# Image mockup paths
images = {
    "page1": "reports/charts/page1_mockup.png",
    "page2": "reports/charts/page2_mockup.png",
    "page3": "reports/charts/page3_mockup.png",
    "page4": "reports/charts/page4_mockup.png"
}

# Custom Canvas for Page Numbering (Page X of Y)
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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Draw header on all pages except the cover (page 1)
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#1A365D"))
            self.drawString(54, 750, "BLUESTOCK MUTUAL FUND ANALYTICS")
            self.setFont("Helvetica", 8)
            self.drawRightString(558, 750, "Day 5: Power BI Dashboard & Visualizations")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            self.restoreState()

        # Draw footer on all pages
        self.saveState()
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 55, 558, 55)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 42, "CONFIDENTIAL - FOR TRAINING & LEARNING PURPOSES")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 42, page_str)
        self.restoreState()


def build_pdf(target_path):
    print(f"Generating Power BI Dashboard PDF Report at: {target_path}...")
    doc = SimpleDocTemplate(
        target_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#475569"),
        spaceAfter=30
    )
    
    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2C5282"),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceAfter=8
    )

    code_style = ParagraphStyle(
        'CodeCustom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F8FAFC"),
        borderColor=colors.HexColor("#E2E8F0"),
        borderWidth=0.5,
        borderPadding=6,
        spaceAfter=8
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white,
        alignment=1 # Center
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#334155")
    )
    
    table_cell_bold_style = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1A365D")
    )

    story = []

    # -------------------------------------------------------------
    # PAGE 1: COVER PAGE
    # -------------------------------------------------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph("Day 5 Capstone Deliverable", ParagraphStyle('CoverPre', fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=colors.HexColor("#3182CE"), spaceAfter=10)))
    story.append(Paragraph("Mutual Fund Analytics Dashboard Setup Guide", title_style))
    story.append(Paragraph("A Multi-Page Power BI Dashboard Design Document, Data Model Schema, and Custom DAX Calculations Guide", subtitle_style))
    
    # Metadata table for cover page
    metadata_data = [
        [Paragraph("<b>Date:</b>", body_style), Paragraph("August 16, 2026", body_style)],
        [Paragraph("<b>Authors:</b>", body_style), Paragraph("Manju Angadi (angadimanju052)<br/>Kavya Chigullapally<br/>Hrushikesh<br/>Rajendra Srinivas", body_style)],
        [Paragraph("<b>Status:</b>", body_style), Paragraph("Day 5 Dashboard Visualizations Completed", body_style)],
        [Paragraph("<b>Project:</b>", body_style), Paragraph("Bluestock Mutual Fund Analytics Capstone Project", body_style)]
    ]
    meta_table = Table(metadata_data, colWidths=[80, 250])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    
    story.append(Spacer(1, 100))
    
    # Quick disclaimer box on cover page
    disclaimer_text = (
        "<b>Dashboard Deliverables Notice:</b> This report contains the complete specifications of the 4 dashboard "
        "pages, including high-fidelity design mockups, relationship keys, and DAX calculations. It serves as "
        "the final deliverable report alongside the .pbix dashboard file."
    )
    disc_table = Table([[Paragraph(disclaimer_text, ParagraphStyle('DiscStyle', parent=body_style, fontSize=9, leading=12, textColor=colors.HexColor("#475569")))]], colWidths=[460])
    disc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(disc_table)
    
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 2: STAR SCHEMA & DATA MODEL RELATIONSHIPS
    # -------------------------------------------------------------
    story.append(Paragraph("1. Data Modeling & Star Schema Relationships", h1_style))
    story.append(Paragraph(
        "A robust relational data model is critical for ensuring clean visual interactions and correct DAX cross-filtering. "
        "The Power BI dashboard is built as a Star Schema, with <b>dim_fund</b> and <b>dim_date</b> as central dimension tables, "
        "mapping to multiple transaction and history fact tables:",
        body_style
    ))

    # Relationships Table
    rel_rows = [
        [
            Paragraph("<b>Source Table & Column (1)</b>", table_header_style),
            Paragraph("<b>Relationship</b>", table_header_style),
            Paragraph("<b>Target Table & Column (Many)</b>", table_header_style),
            Paragraph("<b>Cross-Filter</b>", table_header_style)
        ],
        [Paragraph("dim_fund [amfi_code]", table_cell_bold_style), Paragraph("1 ─── *", table_cell_style), Paragraph("fact_nav [amfi_code]", table_cell_style), Paragraph("Single", table_cell_style)],
        [Paragraph("dim_fund [amfi_code]", table_cell_bold_style), Paragraph("1 ─── *", table_cell_style), Paragraph("fact_performance [amfi_code]", table_cell_style), Paragraph("Single", table_cell_style)],
        [Paragraph("dim_fund [amfi_code]", table_cell_bold_style), Paragraph("1 ─── *", table_cell_style), Paragraph("fact_transactions [amfi_code]", table_cell_style), Paragraph("Single", table_cell_style)],
        [Paragraph("dim_fund [amfi_code]", table_cell_bold_style), Paragraph("1 ─── *", table_cell_style), Paragraph("portfolio_holdings [amfi_code]", table_cell_style), Paragraph("Single", table_cell_style)],
        [Paragraph("dim_date [date]", table_cell_bold_style), Paragraph("1 ─── *", table_cell_style), Paragraph("fact_nav [date]", table_cell_style), Paragraph("Single", table_cell_style)],
        [Paragraph("dim_date [date]", table_cell_bold_style), Paragraph("1 ─── *", table_cell_style), Paragraph("fact_transactions [date]", table_cell_style), Paragraph("Single", table_cell_style)],
        [Paragraph("dim_date [date]", table_cell_bold_style), Paragraph("1 ─── *", table_cell_style), Paragraph("benchmark_indices [date]", table_cell_style), Paragraph("Single", table_cell_style)],
        [Paragraph("dim_date [date]", table_cell_bold_style), Paragraph("1 ─── *", table_cell_style), Paragraph("portfolio_holdings [portfolio_date]", table_cell_style), Paragraph("Single", table_cell_style)]
    ]
    rel_table = Table(rel_rows, colWidths=[150, 80, 150, 70])
    rel_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(rel_table)

    story.append(Spacer(1, 15))
    story.append(Paragraph("Relationships Considerations & Best Practices:", h2_style))
    story.append(Paragraph(
        "• <b>Active Relationships</b>: All key relationships are set to Active. Single-direction filtering is used "
        "to prevent ambiguity in relationships.<br/>"
        "• <b>Date Integrity</b>: The calendar dimension `dim_date` covers a continuous date range (from Jan 1996 to Dec 2026), "
        "satisfying all date joints and ensuring time-intelligence DAX functions behave correctly.",
        body_style
    ))
    
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 3: PAGE 1 — INDUSTRY OVERVIEW
    # -------------------------------------------------------------
    story.append(Paragraph("2. Page 1 — Industry Overview Dashboard", h1_style))
    story.append(Paragraph(
        "Provides a high-level view of assets under management (AUM) and systematic investment plan (SIP) inflow trends "
        "across the entire mutual fund industry. It incorporates 4 high-level KPI cards and trend visuals:",
        body_style
    ))

    # Embed Page 1
    if os.path.exists(images["page1"]):
        story.append(KeepTogether([
            Image(images["page1"], width=440, height=248),
            Spacer(1, 4),
            Paragraph("<b>Figure 1:</b> Page 1 — Industry Overview UI Mockup.", ParagraphStyle('Cap1', parent=body_style, fontSize=8, alignment=1, textColor=colors.HexColor("#475569")))
        ]))
    
    story.append(Paragraph("Core DAX Measures Implemented:", h2_style))
    story.append(Paragraph(
        "<b>Total Industry AUM (₹ Lakh Cr)</b>:<br/>"
        "Total AUM = CALCULATE(SUM(fact_aum[aum_lakh_crore]), FILTER(fact_aum, fact_aum[date] = MAX(fact_aum[date])))<br/>"
        "<b>Monthly SIP Inflow (₹ Cr)</b>:<br/>"
        "SIP Inflow = CALCULATE(SUM(monthly_sip_inflows[sip_inflow_crore]), FILTER(monthly_sip_inflows, monthly_sip_inflows[month] = MAX(monthly_sip_inflows[month])))",
        code_style
    ))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 4: PAGE 2 — FUND PERFORMANCE
    # -------------------------------------------------------------
    story.append(Paragraph("3. Page 2 — Fund Performance & Scorecard", h1_style))
    story.append(Paragraph(
        "Focuses on individual fund performance and risk-adjusted analytics. It features a risk vs return scatter bubble chart "
        "and a fully sortable scorecard table for selecting funds based on performance metrics:",
        body_style
    ))

    # Embed Page 2
    if os.path.exists(images["page2"]):
        story.append(KeepTogether([
            Image(images["page2"], width=440, height=248),
            Spacer(1, 4),
            Paragraph("<b>Figure 2:</b> Page 2 — Fund Performance Dashboard UI Mockup.", ParagraphStyle('Cap2', parent=body_style, fontSize=8, alignment=1, textColor=colors.HexColor("#475569")))
        ]))
    
    story.append(Paragraph("Core DAX Measures Implemented:", h2_style))
    story.append(Paragraph(
        "<b>Annualized Return Volatility (Risk)</b>:<br/>"
        "Fund Volatility = STDEV.S(fact_nav[daily_return]) * SQRT(252)<br/>"
        "<b>Sharpe Ratio Measure</b>:<br/>"
        "Sharpe Ratio = DIVIDE(AVERAGE(fact_nav[daily_return]) - (0.065 / 252), STDEV.S(fact_nav[daily_return])) * SQRT(252)",
        code_style
    ))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 5: PAGE 3 — INVESTOR ANALYTICS
    # -------------------------------------------------------------
    story.append(Paragraph("4. Page 3 — Investor Analytics Dashboard", h1_style))
    story.append(Paragraph(
        "Highlights investor demographics, transaction details, and regional distribution to evaluate "
        "market penetration across Indian states and city tiers:",
        body_style
    ))

    # Embed Page 3
    if os.path.exists(images["page3"]):
        story.append(KeepTogether([
            Image(images["page3"], width=440, height=248),
            Spacer(1, 4),
            Paragraph("<b>Figure 3:</b> Page 3 — Investor Analytics UI Mockup.", ParagraphStyle('Cap3', parent=body_style, fontSize=8, alignment=1, textColor=colors.HexColor("#475569")))
        ]))
    
    story.append(Paragraph("Core DAX Measures Implemented:", h2_style))
    story.append(Paragraph(
        "<b>Average Ticket Size (₹)</b>:<br/>"
        "Avg Ticket Size = AVERAGE(fact_transactions[amount_inr])<br/>"
        "<b>Total Transaction Volume (Cr)</b>:<br/>"
        "Total Amount Crore = SUM(fact_transactions[amount_inr]) / 10000000.0",
        code_style
    ))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 6: PAGE 4 — SIP & MARKET TRENDS
    # -------------------------------------------------------------
    story.append(Paragraph("5. Page 4 — SIP & Market Trends Dashboard", h1_style))
    story.append(Paragraph(
        "Evaluates the correlations between retail systematic investment plan (SIP) inflows and broader "
        "index benchmarks (like Nifty 50) over time, and displays asset class net category inflows:",
        body_style
    ))

    # Embed Page 4
    if os.path.exists(images["page4"]):
        story.append(KeepTogether([
            Image(images["page4"], width=440, height=248),
            Spacer(1, 4),
            Paragraph("<b>Figure 4:</b> Page 4 — SIP & Market Trends UI Mockup.", ParagraphStyle('Cap4', parent=body_style, fontSize=8, alignment=1, textColor=colors.HexColor("#475569")))
        ]))
    
    story.append(Paragraph("Core DAX Measures Implemented:", h2_style))
    story.append(Paragraph(
        "<b>Benchmark Cumulative Performance (Nifty 50 Base 100)</b>:<br/>"
        "N50 Base 100 = DIVIDE(SUM(benchmark_indices[close_value]), CALCULATE(SUM(benchmark_indices[close_value]), FILTER(ALL(dim_date), dim_date[date] = MIN(dim_date[date])))) * 100",
        code_style
    ))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 7: INTERACTIVITY & POWER BI SETUP GUIDE
    # -------------------------------------------------------------
    story.append(Paragraph("6. Interactivity & Visual Setup Instructions", h1_style))
    story.append(Paragraph(
        "To compile the Power BI dashboard correctly using the processed CSV files, please follow these steps:",
        body_style
    ))
    
    setup_text = (
        "<b>1. Import Data</b>: Open Power BI Desktop, select 'Get Data -> Text/CSV', and import all 10 cleaned CSV files from "
        "<code>data/processed/</code>.<br/>"
        "<b>2. Define Relationships</b>: Go to the 'Model view' and map relationships on <code>amfi_code</code> and <code>date</code> "
        "exactly as specified in Section 1.<br/>"
        "<b>3. Set Slicers & Interactivity</b>: Configure the slicers for Category, Plan, and Fund House on Page 2 and Page 3. "
        "Enable Drill-through by dragging the <code>amfi_code</code> field onto the Drill-through section of Page 2, allowing users "
        "to right-click on any fund name and drill down to its historical NAV trend details."
    )
    setup_table = Table([[Paragraph(setup_text, body_style)]], colWidths=[460])
    setup_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(setup_table)
    
    story.append(Spacer(1, 20))
    story.append(Paragraph("Bluestock Color Palette Hex Codes:", h2_style))
    story.append(Paragraph(
        "• Primary (Dark Indigo): <code>#1A365D</code><br/>"
        "• Secondary (Slate Blue): <code>#3182CE</code><br/>"
        "• Light Grey Backgrounds: <code>#F8FAFC</code><br/>"
        "• Accent Green (Positive return): <code>#48BB78</code>",
        body_style
    ))
    
    story.append(Spacer(1, 40))
    # Sign-off box
    sign_off_data = [
        [Paragraph("<b>Dashboard Specification:</b>", body_style), Paragraph("Bluestock Mutual Fund Analytics Capstone", body_style)],
        [Paragraph("<b>Verified By:</b>", body_style), Paragraph("Google Antigravity AI Coding Assistant", body_style)],
        [Paragraph("<b>Deliverable Status:</b>", body_style), Paragraph("Day 5 Dashboard Spec & Mockups Ready", body_style)]
    ]
    sign_off_table = Table(sign_off_data, colWidths=[155, 200])
    sign_off_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(KeepTogether([
        Paragraph("Document Verification & Audit Trail", h2_style),
        sign_off_table
    ]))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF Report compiled successfully at: {target_path}")


if __name__ == "__main__":
    build_pdf(PDF_PATH_ROOT)
    build_pdf(PDF_PATH_REPORTS)
