"""
Bluestock Mutual Fund Analytics - 12-Slide Presentation Generator
================================================================
Builds a professional 16:9 widescreen PowerPoint presentation (.pptx)
for the Bluestock Capstone Final Deliverable using python-pptx.

Slide Structure (Exactly 12 Slides):
1. Title Slide
2. Problem Statement & Project Objectives
3. Data Sources & Ingestion Pipeline
4. System Architecture & Database Design
5. EDA Highlights (1): Industry AUM & SIP Growth
6. EDA Highlights (2): Investor Demographics & Behavior
7. Performance Metrics (1): Risk-Adjusted Returns & Scorecard
8. Advanced Analytics (2): Tail Risk, Rolling Sharpe & HHI
9. Dashboard Showcase (1): Industry Overview & Fund Performance
10. Dashboard Showcase (2): Investor Analytics & Market Trends
11. Strategic Recommendations & Business Impact
12. Conclusion & Thank You / Q&A
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHARTS_DIR = os.path.join(BASE_DIR, "reports", "charts")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
OUTPUT_PPTX_ROOT = os.path.join(BASE_DIR, "Bluestock_MF_Presentation.pptx")
OUTPUT_PPTX_REP = os.path.join(REPORTS_DIR, "Bluestock_MF_Presentation.pptx")

# Bluestock Corporate Color Palette
COLOR_NAVY = RGBColor(26, 54, 93)       # #1A365D Primary Brand Navy
COLOR_BLUE = RGBColor(49, 130, 206)     # #3182CE Slate Accent Blue
COLOR_DARK = RGBColor(45, 55, 72)       # #2D3748 Body Text
COLOR_MUTED = RGBColor(113, 128, 150)   # #718096 Subtle Gray
COLOR_LIGHT_BG = RGBColor(248, 250, 252)# #F8FAFC Card Background
COLOR_WHITE = RGBColor(255, 255, 255)   # #FFFFFF Clean White
COLOR_BORDER = RGBColor(226, 232, 240)  # #E2E8F0 Border
COLOR_GREEN = RGBColor(56, 161, 105)    # #38A169 Emerald
COLOR_ORANGE = RGBColor(221, 107, 32)   # #DD6B20 Accent


def create_header(slide, title_text, category_text="BLUESTOCK FINTECH  |  CAPSTONE PROJECT"):
    """Adds a standardized corporate header banner to a slide."""
    # Category / Tagline
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.35))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.name = "Calibri"
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_BLUE

    # Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.7))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = "Calibri"
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_NAVY


def add_card(slide, left, top, width, height, bg_color=COLOR_LIGHT_BG, border_color=COLOR_BORDER):
    """Adds a soft rounded card container for content grouping."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1)
    return shape


def build_presentation():
    prs = Presentation()
    # 16:9 Widescreen standard dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    # Hero Navy Background
    hero = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    hero.fill.solid()
    hero.fill.fore_color.rgb = COLOR_NAVY
    hero.line.fill.background()

    # Pre-title
    pre_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(0.5))
    tf_pre = pre_box.text_frame
    p_pre = tf_pre.paragraphs[0]
    p_pre.text = "BLUESTOCK FINTECH  •  DATA ANALYST INTERNSHIP CAPSTONE"
    p_pre.font.name = "Calibri"
    p_pre.font.size = Pt(13)
    p_pre.font.bold = True
    p_pre.font.color.rgb = RGBColor(144, 205, 244)  # Light blue

    # Main Title
    title_box = s1.shapes.add_textbox(Inches(1.2), Inches(2.3), Inches(11.0), Inches(1.6))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_t = tf_title.paragraphs[0]
    p_t.text = "Mutual Fund Analytics Platform"
    p_t.font.name = "Calibri"
    p_t.font.size = Pt(40)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_WHITE

    # Subtitle
    sub_box = s1.shapes.add_textbox(Inches(1.2), Inches(3.9), Inches(10.5), Inches(0.9))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "End-to-End Data Engineering, Quantitative Risk Modeling, and Interactive BI Dashboard Architecture"
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = RGBColor(226, 232, 240)

    # Metadata Card
    add_card(s1, Inches(1.2), Inches(5.2), Inches(10.9), Inches(1.3), bg_color=RGBColor(30, 64, 110), border_color=RGBColor(49, 130, 206))
    meta_box = s1.shapes.add_textbox(Inches(1.4), Inches(5.3), Inches(10.5), Inches(1.1))
    tf_m = meta_box.text_frame
    p_m1 = tf_m.paragraphs[0]
    p_m1.text = "Project Scope: 40 Real Schemes  |  10 Datasets (87K+ Rows)  |  SQLite Star Schema  |  Power BI / Python"
    p_m1.font.bold = True
    p_m1.font.size = Pt(13)
    p_m1.font.color.rgb = COLOR_WHITE
    p_m2 = tf_m.add_paragraph()
    p_m2.text = "Author: Manju Angadi  •  Date: June 2026  •  Capstone Submission (Final v1.0)"
    p_m2.font.size = Pt(12)
    p_m2.font.color.rgb = RGBColor(190, 227, 248)

    # ==========================================
    # SLIDE 2: Problem Statement & Objectives
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    create_header(s2, "Problem Statement & Strategic Objectives")

    # Column 1: Problem Statements
    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3))
    pb_box = s2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.9))
    tf_pb = pb_box.text_frame
    tf_pb.word_wrap = True
    p_pb_h = tf_pb.paragraphs[0]
    p_pb_h.text = "The Retail Investment Dilemma"
    p_pb_h.font.size = Pt(16)
    p_pb_h.font.bold = True
    p_pb_h.font.color.rgb = COLOR_NAVY

    points_pb = [
        ("Data Fragmentation: ", "NAV, AUM, folio counts, and transaction flows are scattered across AMFI, SEBI, and disparate exchange portals in TXT, HTML, and CSV formats."),
        ("Lack of Unified Analytics: ", "Retail investors struggle to assess true risk-adjusted performance, often misjudging high trailing returns without evaluating downside volatility."),
        ("SIP Friction & Drop-Offs: ", "High initial investor excitement is plagued by mandate skips, bank balance defaults, and lack of automated cadenced retention tracking.")
    ]
    for bold_prefix, text in points_pb:
        p = tf_pb.add_paragraph()
        p.space_before = Pt(12)
        run_b = p.add_run()
        run_b.text = "• " + bold_prefix
        run_b.font.bold = True
        run_b.font.color.rgb = COLOR_BLUE
        run_t = p.add_run()
        run_t.text = text
        run_t.font.color.rgb = COLOR_DARK

    # Column 2: Capstone Deliverables & Objectives
    add_card(s2, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.3))
    obj_box = s2.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.2), Inches(4.9))
    tf_obj = obj_box.text_frame
    tf_obj.word_wrap = True
    p_obj_h = tf_obj.paragraphs[0]
    p_obj_h.text = "Capstone Solution Pillars"
    p_obj_h.font.size = Pt(16)
    p_obj_h.font.bold = True
    p_obj_h.font.color.rgb = COLOR_NAVY

    points_obj = [
        ("Automated ETL Pipeline: ", "Ingest, clean, and validate 10 relational datasets with automated live NAV integration via mfapi.in."),
        ("Relational Star Schema: ", "Architect a high-performance SQLite data warehouse linking dimension and fact tables for fast BI querying."),
        ("Quantitative Risk Modeling: ", "Compute CAGR, Sharpe, Sortino, Alpha, Beta, Max Drawdown, 95% Historical VaR/CVaR, and Sector HHI."),
        ("Interactive BI Dashboard: ", "Design 4 visual pages in Power BI with drill-through navigation, category slicers, and executive KPI cards.")
    ]
    for bold_prefix, text in points_obj:
        p = tf_obj.add_paragraph()
        p.space_before = Pt(10)
        run_b = p.add_run()
        run_b.text = "✔ " + bold_prefix
        run_b.font.bold = True
        run_b.font.color.rgb = COLOR_GREEN
        run_t = p.add_run()
        run_t.text = text
        run_t.font.color.rgb = COLOR_DARK

    # ==========================================
    # SLIDE 3: Data Sources & Ingestion Pipeline
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    create_header(s3, "Data Sources & Ingestion Ecosystem")

    # 3 Summary Cards
    cards_data = [
        ("Public Data Sources", "AMFI India, mfapi.in, NSE/BSE", "Aggregates real scheme NAVs, benchmark indices (Nifty 50, Nifty 100), and monthly industry flows without private credentials.", Inches(0.8)),
        ("Dataset Scale", "10 Tables  |  87,000+ Rows", "Covers 40 real schemes, 32,000+ investor transactions, 320 portfolio holdings, and multi-year daily NAV timelines.", Inches(4.85)),
        ("Validation & Quality", "100% Schema Validation", "Forward-fills weekend gaps, enforces strict positive NAV constraints, removes duplicates, and flags synthetic anomalies.", Inches(8.9))
    ]
    for title, subtitle, desc, left in cards_data:
        add_card(s3, left, Inches(1.6), Inches(3.6), Inches(2.2))
        tb = s3.shapes.add_textbox(left + Inches(0.2), Inches(1.8), Inches(3.2), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.bold = True
        p1.font.size = Pt(14)
        p1.font.color.rgb = COLOR_NAVY
        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.bold = True
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_BLUE
        p2.space_before = Pt(4)
        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(10)
        p3.font.color.rgb = COLOR_DARK
        p3.space_before = Pt(6)

    # Table of Core Datasets
    add_card(s3, Inches(0.8), Inches(4.1), Inches(11.7), Inches(2.8))
    tb_t = s3.shapes.add_textbox(Inches(1.0), Inches(4.2), Inches(11.3), Inches(2.5))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    p_th = tf_t.paragraphs[0]
    p_th.text = "Dataset Catalog & Mapping"
    p_th.font.bold = True
    p_th.font.size = Pt(13)
    p_th.font.color.rgb = COLOR_NAVY

    datasets_summary = [
        ("01_fund_master.csv", "40 Schemes", "amfi_code, fund_house, scheme_name, category, benchmark, expense_ratio, risk_grade"),
        ("02_nav_history.csv", "43,000+ Rows", "amfi_code, date, nav (Historical daily NAV series 2022–2026)"),
        ("07_scheme_performance.csv", "40 Schemes", "1Y/3Y/5Y CAGR, Alpha, Beta, Sharpe, Sortino, Max Drawdown, Volatility"),
        ("08_investor_transactions.csv", "32,778 Rows", "investor_id, date, amfi_code, type (SIP/Lumpsum/Redemption), amount, state, age, tier"),
        ("09_portfolio_holdings.csv", "320 Holdings", "amfi_code, stock_symbol, sector, weight_pct, market_value_cr"),
        ("10_benchmark_indices.csv", "8,000+ Rows", "date, nifty_50, nifty_100, nifty_midcap_150, bse_smallcap, crisil_liquid")
    ]
    for name, scale, desc in datasets_summary:
        p = tf_t.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        r1.text = f"• {name} ({scale}): "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_BLUE
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_DARK

    # ==========================================
    # SLIDE 4: Architecture & Database Design
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    create_header(s4, "System Architecture & Relational Star Schema")

    steps = [
        ("1. Data Ingestion", "Fetch & Load", "Extract raw CSVs and query live NAV data from mfapi.in REST API.", Inches(0.8)),
        ("2. Data Cleaning", "Transform & Clean", "Forward-fill holidays, validate constraints, and structure processed CSVs.", Inches(3.85)),
        ("3. SQLite Warehouse", "Star Schema DB", "Load relational tables with primary/foreign keys on amfi_code and date.", Inches(6.9)),
        ("4. Analytics & BI", "Insights & Visuals", "Execute risk models, scorecard ranking, and interactive Power BI pages.", Inches(9.95))
    ]
    for step_num, step_sub, step_desc, left in steps:
        add_card(s4, left, Inches(1.6), Inches(2.6), Inches(2.0))
        tb = s4.shapes.add_textbox(left + Inches(0.15), Inches(1.75), Inches(2.3), Inches(1.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = step_num
        p1.font.bold = True
        p1.font.size = Pt(12)
        p1.font.color.rgb = COLOR_NAVY
        p2 = tf.add_paragraph()
        p2.text = step_sub
        p2.font.bold = True
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_BLUE
        p2.space_before = Pt(3)
        p3 = tf.add_paragraph()
        p3.text = step_desc
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = COLOR_DARK
        p3.space_before = Pt(4)

    # Star Schema Relational Layout Details
    add_card(s4, Inches(0.8), Inches(3.9), Inches(11.75), Inches(3.0))
    tb_schema = s4.shapes.add_textbox(Inches(1.0), Inches(4.0), Inches(11.35), Inches(2.7))
    tf_s = tb_schema.text_frame
    tf_s.word_wrap = True
    ps_h = tf_s.paragraphs[0]
    ps_h.text = "Star Schema Relational Design (bluestock_mf.db)"
    ps_h.font.bold = True
    ps_h.font.size = Pt(14)
    ps_h.font.color.rgb = COLOR_NAVY

    schema_points = [
        ("Central Dimension 1 — dim_fund [amfi_code] (1-to-Many):", "Filters fact_nav, fact_performance, fact_transactions, and portfolio_holdings."),
        ("Central Dimension 2 — dim_date [date] (1-to-Many):", "Filters daily NAV records, benchmark indices, monthly SIP inflows, and investor transactions."),
        ("Fact Tables:", "fact_nav (daily valuation series), fact_performance (risk & return statistics), fact_transactions (32K investor records)."),
        ("Performance Optimizations:", "B-Tree indexed on amfi_code and date; ensures sub-10ms query latency across analytical SQL aggregations.")
    ]
    for b_title, b_desc in schema_points:
        p = tf_s.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = "• " + b_title + " "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = COLOR_BLUE
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_DARK

    # ==========================================
    # SLIDE 5: EDA Highlights (1)
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    create_header(s5, "EDA Highlights (1): Industry AUM & SIP Inflow Momentum")

    # Image 1: AUM Growth
    img1_path = os.path.join(CHARTS_DIR, "02_aum_growth.png")
    if os.path.exists(img1_path):
        s5.shapes.add_picture(img1_path, Inches(0.8), Inches(1.6), width=Inches(5.6))

    # Image 2: SIP Inflows
    img2_path = os.path.join(CHARTS_DIR, "03_sip_inflows.png")
    if os.path.exists(img2_path):
        s5.shapes.add_picture(img2_path, Inches(6.9), Inches(1.6), width=Inches(5.6))

    # Bottom Takeaway Card
    add_card(s5, Inches(0.8), Inches(5.4), Inches(11.7), Inches(1.6))
    tb_eda1 = s5.shapes.add_textbox(Inches(1.0), Inches(5.5), Inches(11.3), Inches(1.4))
    tf_e1 = tb_eda1.text_frame
    tf_e1.word_wrap = True
    pe1 = tf_e1.paragraphs[0]
    pe1.text = "Key Macro Takeaways:"
    pe1.font.bold = True
    pe1.font.size = Pt(12)
    pe1.font.color.rgb = COLOR_NAVY
    
    bullets_e1 = [
        "Industry AUM Expansion: Exploded from ₹38 Lakh Crore in early 2022 to over ₹81 Lakh Crore by Dec 2025 (~26% CAGR).",
        "SIP Democratization: Monthly SIP contributions grew from ₹11,500 Cr to over ₹31,000 Cr, reflecting persistent retail dollar-cost averaging."
    ]
    for b in bullets_e1:
        p = tf_e1.add_paragraph()
        p.space_before = Pt(3)
        p.text = "✔ " + b
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_DARK

    # ==========================================
    # SLIDE 6: EDA Highlights (2)
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    create_header(s6, "EDA Highlights (2): Demographics & Investor Behavior")

    # Image 1: SIP by State
    img3_path = os.path.join(CHARTS_DIR, "08_sip_by_state.png")
    if os.path.exists(img3_path):
        s6.shapes.add_picture(img3_path, Inches(0.8), Inches(1.6), width=Inches(5.6))

    # Image 2: SIP Box by Age
    img4_path = os.path.join(CHARTS_DIR, "06_sip_box_by_age.png")
    if os.path.exists(img4_path):
        s6.shapes.add_picture(img4_path, Inches(6.9), Inches(1.6), width=Inches(5.6))

    # Bottom Takeaway Card
    add_card(s6, Inches(0.8), Inches(5.4), Inches(11.7), Inches(1.6))
    tb_eda2 = s6.shapes.add_textbox(Inches(1.0), Inches(5.5), Inches(11.3), Inches(1.4))
    tf_e2 = tb_eda2.text_frame
    tf_e2.word_wrap = True
    pe2 = tf_e2.paragraphs[0]
    pe2.text = "Key Demographic Takeaways:"
    pe2.font.bold = True
    pe2.font.size = Pt(12)
    pe2.font.color.rgb = COLOR_NAVY

    bullets_e2 = [
        "Geographic Concentration: Maharashtra, Gujarat, and Karnataka account for over 54% of total transaction capital.",
        "Age Group Ticket Sizes: While 26–35 age group drives transaction count (fintech apps), 46–55 cohorts commit the highest median SIP amounts."
    ]
    for b in bullets_e2:
        p = tf_e2.add_paragraph()
        p.space_before = Pt(3)
        p.text = "✔ " + b
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_DARK

    # ==========================================
    # SLIDE 7: Performance Analytics (1)
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    create_header(s7, "Performance Analytics (1): Benchmark Comparisons & Scorecard")

    # Left: Benchmark chart
    img_bench = os.path.join(CHARTS_DIR, "benchmark_comparison.png")
    if os.path.exists(img_bench):
        s7.shapes.add_picture(img_bench, Inches(0.8), Inches(1.6), width=Inches(6.2))

    # Right: Scorecard Highlights
    add_card(s7, Inches(7.3), Inches(1.6), Inches(5.2), Inches(5.3))
    tb_sc = s7.shapes.add_textbox(Inches(7.5), Inches(1.8), Inches(4.8), Inches(4.9))
    tf_sc = tb_sc.text_frame
    tf_sc.word_wrap = True
    psc = tf_sc.paragraphs[0]
    psc.text = "Composite Fund Scorecard (0–100)"
    psc.font.bold = True
    psc.font.size = Pt(15)
    psc.font.color.rgb = COLOR_NAVY

    sc_bullets = [
        ("Multi-Factor Formula: ", "30% 3Y Return + 25% Sharpe + 20% Alpha + 15% Low Expense + 10% Low Max DD."),
        ("Rank 1 — Mirae Asset Large Cap: ", "Score 87.25 | Sharpe 1.06 | 3Y CAGR 14.81% | Steady large-cap compounder."),
        ("Rank 2 — HDFC Mid-Cap Opportunities: ", "Score 84.10 | Alpha +27.11% | Strong manager outperformance vs Nifty 100."),
        ("Rank 3 — Kotak Flexicap Fund: ", "Score 81.50 | Sharpe 1.02 | Dynamic multi-cap market allocation."),
        ("Expense Sensitivity: ", "Direct plans generate 0.8% to 1.2% higher annualized return due to zero distributor commission drag.")
    ]
    for b_title, b_desc in sc_bullets:
        p = tf_sc.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = "• " + b_title
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_BLUE
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_DARK

    # ==========================================
    # SLIDE 8: Advanced Analytics (2)
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    create_header(s8, "Performance Analytics (2): Tail Risk, Rolling Sharpe & Concentration")

    # Left: Rolling Sharpe chart
    img_rs = os.path.join(CHARTS_DIR, "rolling_sharpe_chart.png")
    if os.path.exists(img_rs):
        s8.shapes.add_picture(img_rs, Inches(0.8), Inches(1.6), width=Inches(6.2))

    # Right: Advanced Risk Insights Card
    add_card(s8, Inches(7.3), Inches(1.6), Inches(5.2), Inches(5.3))
    tb_ar = s8.shapes.add_textbox(Inches(7.5), Inches(1.8), Inches(4.8), Inches(4.9))
    tf_ar = tb_ar.text_frame
    tf_ar.word_wrap = True
    par = tf_ar.paragraphs[0]
    par.text = "Advanced Quantitative Takeaways"
    par.font.bold = True
    par.font.size = Pt(15)
    par.font.color.rgb = COLOR_NAVY

    ar_points = [
        ("Historical VaR & CVaR (95%): ", "Small cap schemes exhibit 1-day VaR of -2.69% and CVaR of -3.24% (worst 5% days), contrasting with Liquid funds at -0.03%."),
        ("Rolling Sharpe Instability: ", "HDFC Mid-Cap Sharpe oscillated between -0.80 and +3.20, showing that point-in-time metrics can misrepresent cyclical volatility."),
        ("SIP Continuity & Churn: ", "97.8% of investors with 6+ SIPs have average gaps > 35 days (cohort mean 64.9 days), revealing widespread mandate pauses."),
        ("Sector HHI Concentration: ", "Axis Bluechip has HHI of 2,967 (48.7% IT). Funds with HHI > 2,500 carry acute single-sector vulnerability.")
    ]
    for b_title, b_desc in ar_points:
        p = tf_ar.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = "• " + b_title
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_BLUE
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_DARK

    # ==========================================
    # SLIDE 9: Power BI Dashboard (1)
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    create_header(s9, "Power BI Dashboard Showcase (Pages 1 & 2)")

    # Left: Page 1
    img_p1 = os.path.join(CHARTS_DIR, "page1_mockup.png")
    if os.path.exists(img_p1):
        s9.shapes.add_picture(img_p1, Inches(0.8), Inches(1.6), width=Inches(5.6))
    add_card(s9, Inches(0.8), Inches(5.4), Inches(5.6), Inches(1.6))
    tb_p1 = s9.shapes.add_textbox(Inches(0.9), Inches(5.5), Inches(5.4), Inches(1.4))
    tf_p1 = tb_p1.text_frame
    tf_p1.word_wrap = True
    pp1 = tf_p1.paragraphs[0]
    pp1.text = "Page 1: Industry Overview"
    pp1.font.bold = True
    pp1.font.size = Pt(12)
    pp1.font.color.rgb = COLOR_NAVY
    p_p1_d = tf_p1.add_paragraph()
    p_p1_d.text = "Displays executive KPI cards (₹81L Cr AUM, ₹31K Cr SIP, 26.12 Cr Folios), multi-year AUM growth timeline, and AMC market share distribution."
    p_p1_d.font.size = Pt(9.5)
    p_p1_d.font.color.rgb = COLOR_DARK

    # Right: Page 2
    img_p2 = os.path.join(CHARTS_DIR, "page2_mockup.png")
    if os.path.exists(img_p2):
        s9.shapes.add_picture(img_p2, Inches(6.9), Inches(1.6), width=Inches(5.6))
    add_card(s9, Inches(6.9), Inches(5.4), Inches(5.6), Inches(1.6))
    tb_p2 = s9.shapes.add_textbox(Inches(7.0), Inches(5.5), Inches(5.4), Inches(1.4))
    tf_p2 = tb_p2.text_frame
    tf_p2.word_wrap = True
    pp2 = tf_p2.paragraphs[0]
    pp2.text = "Page 2: Fund Performance"
    pp2.font.bold = True
    pp2.font.size = Pt(12)
    pp2.font.color.rgb = COLOR_NAVY
    p_p2_d = tf_p2.add_paragraph()
    p_p2_d.text = "Features a Risk vs. Return scatter plot (CAGR vs Volatility), interactive scorecard table, benchmark NAV line chart, and AMC/category slicers."
    p_p2_d.font.size = Pt(9.5)
    p_p2_d.font.color.rgb = COLOR_DARK

    # ==========================================
    # SLIDE 10: Power BI Dashboard (2)
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    create_header(s10, "Power BI Dashboard Showcase (Pages 3 & 4)")

    # Left: Page 3
    img_p3 = os.path.join(CHARTS_DIR, "page3_mockup.png")
    if os.path.exists(img_p3):
        s10.shapes.add_picture(img_p3, Inches(0.8), Inches(1.6), width=Inches(5.6))
    add_card(s10, Inches(0.8), Inches(5.4), Inches(5.6), Inches(1.6))
    tb_p3 = s10.shapes.add_textbox(Inches(0.9), Inches(5.5), Inches(5.4), Inches(1.4))
    tf_p3 = tb_p3.text_frame
    tf_p3.word_wrap = True
    pp3 = tf_p3.paragraphs[0]
    pp3.text = "Page 3: Investor Analytics"
    pp3.font.bold = True
    pp3.font.size = Pt(12)
    pp3.font.color.rgb = COLOR_NAVY
    p_p3_d = tf_p3.add_paragraph()
    p_p3_d.text = "State-wise capital allocation, SIP vs. Lumpsum vs. Redemption donut breakdown, age-group ticket size distribution, and monthly transaction volumes."
    p_p3_d.font.size = Pt(9.5)
    p_p3_d.font.color.rgb = COLOR_DARK

    # Right: Page 4
    img_p4 = os.path.join(CHARTS_DIR, "page4_mockup.png")
    if os.path.exists(img_p4):
        s10.shapes.add_picture(img_p4, Inches(6.9), Inches(1.6), width=Inches(5.6))
    add_card(s10, Inches(6.9), Inches(5.4), Inches(5.6), Inches(1.6))
    tb_p4 = s10.shapes.add_textbox(Inches(7.0), Inches(5.5), Inches(5.4), Inches(1.4))
    tf_p4 = tb_p4.text_frame
    tf_p4.word_wrap = True
    pp4 = tf_p4.paragraphs[0]
    pp4.text = "Page 4: SIP & Market Trends"
    pp4.font.bold = True
    pp4.font.size = Pt(12)
    pp4.font.color.rgb = COLOR_NAVY
    p_p4_d = tf_p4.add_paragraph()
    p_p4_d.text = "Dual-axis chart correlating monthly SIP inflows with Nifty 50 closing level, category net flow heatmap, and top 5 inflow leader rankings."
    p_p4_d.font.size = Pt(9.5)
    p_p4_d.font.color.rgb = COLOR_DARK

    # ==========================================
    # SLIDE 11: Strategic Recommendations
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    create_header(s11, "Strategic Recommendations for Bluestock Fintech")

    recs = [
        ("1. Automated SIP Pre-Debit Retention Nudges", 
         "With 97.8% of regular SIP investors exhibiting cadence gaps > 35 days (mean 64.9 days), implement WhatsApp/SMS balance reminders 48h prior to debit dates to prevent mandate churn and bank drop-offs."),
        ("2. Multi-Metric Fund Scorecard Integration", 
         "Replace simple 1-year trailing return leaderboards in the retail app with our composite Scorecard (Return + Sharpe + Alpha + Expense + Drawdown) to prevent retail capital chasing past peak cyclical returns."),
        ("3. Tail-Risk (VaR) Warnings for Small Cap Funds", 
         "Small-cap schemes carry daily VaR of -2.69% and CVaR exceeding -3.24%. Embed automated risk disclosure popups to set realistic expectations for first-time retail investors."),
        ("4. Sector Concentration Guardrails (HHI > 2500)", 
         "Flag mutual funds exhibiting high sector concentration (e.g. Axis Bluechip at 48.7% IT). Offer automated portfolio rebalancing suggestions to safeguard retail portfolios from idiosyncratic industry shocks.")
    ]
    
    for i, (title, desc) in enumerate(recs):
        top_pos = Inches(1.6 + i * 1.35)
        add_card(s11, Inches(0.8), top_pos, Inches(11.7), Inches(1.2))
        tb = s11.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.1), Inches(11.3), Inches(1.0))
        tf = tb.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.bold = True
        pt.font.size = Pt(13)
        pt.font.color.rgb = COLOR_NAVY
        pd_ = tf.add_paragraph()
        pd_.text = desc
        pd_.font.size = Pt(10.5)
        pd_.font.color.rgb = COLOR_DARK
        pd_.space_before = Pt(3)

    # ==========================================
    # SLIDE 12: Conclusion & Thank You
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    # Hero Navy Background
    hero12 = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    hero12.fill.solid()
    hero12.fill.fore_color.rgb = COLOR_NAVY
    hero12.line.fill.background()

    tb_end = s12.shapes.add_textbox(Inches(1.5), Inches(2.0), Inches(10.3), Inches(2.2))
    tf_end = tb_end.text_frame
    tf_end.word_wrap = True
    pe_h = tf_end.paragraphs[0]
    pe_h.text = "Thank You!"
    pe_h.font.bold = True
    pe_h.font.size = Pt(44)
    pe_h.font.color.rgb = COLOR_WHITE

    pe_sub = tf_end.add_paragraph()
    pe_sub.text = "Bluestock Mutual Fund Analytics Capstone Project Complete"
    pe_sub.font.size = Pt(20)
    pe_sub.font.color.rgb = RGBColor(144, 205, 244)
    pe_sub.space_before = Pt(8)

    add_card(s12, Inches(1.5), Inches(4.5), Inches(10.3), Inches(1.8), bg_color=RGBColor(30, 64, 110), border_color=RGBColor(49, 130, 206))
    tb_c = s12.shapes.add_textbox(Inches(1.8), Inches(4.7), Inches(9.7), Inches(1.4))
    tf_c = tb_c.text_frame
    pc1 = tf_c.paragraphs[0]
    pc1.text = "All Deliverables Successfully Implemented & Verified:"
    pc1.font.bold = True
    pc1.font.size = Pt(13)
    pc1.font.color.rgb = COLOR_WHITE

    deliverables_text = "• 10 Cleaned Datasets  • SQLite Database (Star Schema)  • EDA & Performance Notebooks\n• 4-Page Power BI Dashboard  • 15–20 Page Final Report PDF  • Quantitative Risk Engine"
    pc2 = tf_c.add_paragraph()
    pc2.text = deliverables_text
    pc2.font.size = Pt(11)
    pc2.font.color.rgb = RGBColor(226, 232, 240)
    pc2.space_before = Pt(4)

    # Save presentations
    prs.save(OUTPUT_PPTX_ROOT)
    prs.save(OUTPUT_PPTX_REP)
    print(f"Successfully created 12-slide presentation at:\n  - {OUTPUT_PPTX_ROOT}\n  - {OUTPUT_PPTX_REP}")


if __name__ == "__main__":
    build_presentation()
