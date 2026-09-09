"""
Reporting Module: 12-Slide Presentation Generator
=================================================
Builds a professional 16:9 widescreen PowerPoint presentation (.pptx).
"""

import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CHARTS_DIR = PROJECT_ROOT / "reports" / "charts"
REPORTS_DIR = PROJECT_ROOT / "reports"
OUTPUT_PPTX = REPORTS_DIR / "Bluestock_MF_Presentation.pptx"

COLOR_NAVY = RGBColor(26, 54, 93)
COLOR_BLUE = RGBColor(49, 130, 206)
COLOR_DARK = RGBColor(45, 55, 72)
COLOR_LIGHT_BG = RGBColor(248, 250, 252)
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_BORDER = RGBColor(226, 232, 240)
COLOR_GREEN = RGBColor(56, 161, 105)

def create_header(slide, title_text, category_text="BLUESTOCK FINTECH  |  CAPSTONE PROJECT"):
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.35))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.name = "Calibri"
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_BLUE

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
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1)
    return shape

def generate_presentation_deck(out_file: Path = OUTPUT_PPTX) -> str:
    """Builds the 12-slide executive presentation."""
    print("\n" + "=" * 80)
    print(f"STAGE 7: Compiling 12-Slide Presentation to {out_file}")
    print("=" * 80)
    
    os.makedirs(out_file.parent, exist_ok=True)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Slide 1: Title
    s1 = prs.slides.add_slide(blank_layout)
    hero = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    hero.fill.solid()
    hero.fill.fore_color.rgb = COLOR_NAVY
    hero.line.fill.background()

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(2.0), Inches(11.0), Inches(3.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = "BLUESTOCK FINTECH  •  DATA ANALYST INTERNSHIP CAPSTONE"
    p0.font.bold = True
    p0.font.size = Pt(13)
    p0.font.color.rgb = RGBColor(144, 205, 244)
    p1 = tf.add_paragraph()
    p1.text = "Mutual Fund Analytics Platform"
    p1.font.bold = True
    p1.font.size = Pt(40)
    p1.font.color.rgb = COLOR_WHITE
    p2 = tf.add_paragraph()
    p2.text = "End-to-End Data Engineering, Quantitative Risk Modeling, and Interactive BI Dashboard Architecture"
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(226, 232, 240)
    p2.space_before = Pt(8)

    # Slide 2: Objectives
    s2 = prs.slides.add_slide(blank_layout)
    create_header(s2, "Problem Statement & Strategic Objectives")
    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3))
    add_card(s2, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.3))
    
    tb2_1 = s2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.9))
    tb2_1.text_frame.word_wrap = True
    p = tb2_1.text_frame.paragraphs[0]
    p.text = "The Retail Investment Dilemma"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = COLOR_NAVY
    for title, desc in [
        ("Data Fragmentation: ", "Scattered datasets across AMFI, exchanges, and SEBI portals."),
        ("Recency Bias: ", "Chasing trailing returns without factoring downside tail volatility."),
        ("SIP Friction: ", "Mandate drop-offs and irregular cadence hampering compounding.")
    ]:
        p = tb2_1.text_frame.add_paragraph()
        p.space_before = Pt(12)
        r = p.add_run()
        r.text = "• " + title
        r.font.bold = True
        r.font.color.rgb = COLOR_BLUE
        r2 = p.add_run()
        r2.text = desc
        r2.font.color.rgb = COLOR_DARK

    tb2_2 = s2.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.2), Inches(4.9))
    tb2_2.text_frame.word_wrap = True
    p = tb2_2.text_frame.paragraphs[0]
    p.text = "Capstone Solution Pillars"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = COLOR_NAVY
    for title, desc in [
        ("Automated ETL Pipeline: ", "Ingest, clean, and validate 10 relational tables."),
        ("Relational Star Schema: ", "SQLite warehouse optimized for fast BI queries."),
        ("Quantitative Risk Modeling: ", "VaR 95%, CVaR, Rolling Sharpe, and Sector HHI."),
        ("Interactive BI Dashboard: ", "4-page layout with slicers and KPI tracking.")
    ]:
        p = tb2_2.text_frame.add_paragraph()
        p.space_before = Pt(10)
        r = p.add_run()
        r.text = "[OK] " + title
        r.font.bold = True
        r.font.color.rgb = COLOR_GREEN
        r2 = p.add_run()
        r2.text = desc
        r2.font.color.rgb = COLOR_DARK

    # Slides 3 to 12
    # Slide 3: Datasets
    s3 = prs.slides.add_slide(blank_layout)
    create_header(s3, "Data Sources & Ingestion Ecosystem")
    add_card(s3, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.3))
    tb3 = s3.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.9))
    tb3.text_frame.word_wrap = True
    p = tb3.text_frame.paragraphs[0]
    p.text = "10 Public Datasets Analyzed (87,000+ Records)"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = COLOR_NAVY
    for dset in [
        "01_fund_master.csv (40 Schemes, Expense ratios, Benchmarks, SEBI risk tiers)",
        "02_nav_history.csv (43,000+ daily NAV records spanning 2022–2026)",
        "07_scheme_performance.csv (1Y/3Y/5Y CAGR, Sharpe, Sortino, Alpha, Beta, Max DD)",
        "08_investor_transactions.csv (32,778 SIP and Lumpsum transaction records)",
        "09_portfolio_holdings.csv (320 equity holdings across sectors)",
        "10_benchmark_indices.csv (8,000+ daily benchmark closing levels: NIFTY 50, NIFTY 100)"
    ]:
        p = tb3.text_frame.add_paragraph()
        p.space_before = Pt(8)
        p.text = "• " + dset
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_DARK

    # Slide 4: Architecture
    s4 = prs.slides.add_slide(blank_layout)
    create_header(s4, "System Architecture & Relational Star Schema")
    add_card(s4, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.3))
    tb4 = s4.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.9))
    tb4.text_frame.word_wrap = True
    p = tb4.text_frame.paragraphs[0]
    p.text = "Star Schema Architecture (bluestock_mf.db)"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = COLOR_NAVY
    for item in [
        "dim_fund [amfi_code] (1-to-many) filters fact_nav, fact_performance, fact_transactions",
        "dim_date [date] (1-to-many) filters fact_nav, fact_transactions, benchmark_indices",
        "Compound B-Tree indexing on (amfi_code, date) yields sub-15ms join latency",
        "Zero duplicate primary keys, forward-filled weekend gaps, strict referential integrity"
    ]:
        p = tb4.text_frame.add_paragraph()
        p.space_before = Pt(8)
        p.text = "• " + item
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_DARK

    # Slide 5: EDA 1
    s5 = prs.slides.add_slide(blank_layout)
    create_header(s5, "EDA Highlights (1): Industry AUM & SIP Inflow Momentum")
    img_aum = CHARTS_DIR / "02_aum_growth.png"
    img_sip = CHARTS_DIR / "03_sip_inflows.png"
    if img_aum.exists():
        s5.shapes.add_picture(str(img_aum), Inches(0.8), Inches(1.6), width=Inches(5.6))
    if img_sip.exists():
        s5.shapes.add_picture(str(img_sip), Inches(6.9), Inches(1.6), width=Inches(5.6))
    add_card(s5, Inches(0.8), Inches(5.4), Inches(11.7), Inches(1.6))
    tb5 = s5.shapes.add_textbox(Inches(1.0), Inches(5.5), Inches(11.3), Inches(1.4))
    tb5.text_frame.word_wrap = True
    p = tb5.text_frame.paragraphs[0]
    p.text = "Key Takeaways: Industry AUM expanded from ₹38.2L Cr to ₹81.4L Cr (+26.3% CAGR). Monthly SIP inflows surged past ₹31,000 Cr."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_DARK

    # Slide 6: EDA 2
    s6 = prs.slides.add_slide(blank_layout)
    create_header(s6, "EDA Highlights (2): Demographics & Investor Behavior")
    img_state = CHARTS_DIR / "08_sip_by_state.png"
    img_box = CHARTS_DIR / "06_sip_box_by_age.png"
    if img_state.exists():
        s6.shapes.add_picture(str(img_state), Inches(0.8), Inches(1.6), width=Inches(5.6))
    if img_box.exists():
        s6.shapes.add_picture(str(img_box), Inches(6.9), Inches(1.6), width=Inches(5.6))
    add_card(s6, Inches(0.8), Inches(5.4), Inches(11.7), Inches(1.6))
    tb6 = s6.shapes.add_textbox(Inches(1.0), Inches(5.5), Inches(11.3), Inches(1.4))
    tb6.text_frame.word_wrap = True
    p = tb6.text_frame.paragraphs[0]
    p.text = "Key Takeaways: Maharashtra, Gujarat, and Karnataka drive 54% of capital. 26-35 age group leads count; 46-55 leads ticket size (₹14,200)."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_DARK

    # Slide 7: Performance 1
    s7 = prs.slides.add_slide(blank_layout)
    create_header(s7, "Performance Analytics (1): Benchmark Comparisons & Scorecard")
    img_bench = CHARTS_DIR / "benchmark_comparison.png"
    if img_bench.exists():
        s7.shapes.add_picture(str(img_bench), Inches(0.8), Inches(1.6), width=Inches(6.2))
    add_card(s7, Inches(7.3), Inches(1.6), Inches(5.2), Inches(5.3))
    tb7 = s7.shapes.add_textbox(Inches(7.5), Inches(1.8), Inches(4.8), Inches(4.9))
    tb7.text_frame.word_wrap = True
    p = tb7.text_frame.paragraphs[0]
    p.text = "Composite Fund Scorecard (0–100)"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = COLOR_NAVY
    for b in [
        "Mirae Asset Large Cap Fund ranked #1 (Score 87.25, 3Y CAGR 14.81%, Sharpe 1.06)",
        "HDFC Mid-Cap Opportunities generated highest manager alpha (+27.11% vs Nifty 100)",
        "Kotak Flexicap ranked #3 (Score 81.50) with balanced multi-cap allocation",
        "Direct plans deliver 0.75% to 1.15% annualized excess compounding vs Regular"
    ]:
        p = tb7.text_frame.add_paragraph()
        p.space_before = Pt(8)
        p.text = "• " + b
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_DARK

    # Slide 8: Advanced Risk
    s8 = prs.slides.add_slide(blank_layout)
    create_header(s8, "Performance Analytics (2): Tail Risk, Rolling Sharpe & Concentration")
    img_rs = CHARTS_DIR / "rolling_sharpe_chart.png"
    if img_rs.exists():
        s8.shapes.add_picture(str(img_rs), Inches(0.8), Inches(1.6), width=Inches(6.2))
    add_card(s8, Inches(7.3), Inches(1.6), Inches(5.2), Inches(5.3))
    tb8 = s8.shapes.add_textbox(Inches(7.5), Inches(1.8), Inches(4.8), Inches(4.9))
    tb8.text_frame.word_wrap = True
    p = tb8.text_frame.paragraphs[0]
    p.text = "Advanced Risk Insights"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = COLOR_NAVY
    for b in [
        "Small Cap schemes exhibit 1-day 95% VaR of -2.69% and CVaR of -3.24% (tail loss)",
        "Liquid schemes preserve capital with daily VaR of only -0.03%",
        "Rolling Sharpe of HDFC Mid-Cap swung from -0.80 to +3.20 across cycles",
        "97.8% of regular SIP investors show cadence gaps > 35 days (mean 64.9 days)",
        "Axis Bluechip shows elevated HHI of 2,967 (48.7% IT concentration)"
    ]:
        p = tb8.text_frame.add_paragraph()
        p.space_before = Pt(6)
        p.text = "• " + b
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_DARK

    # Slide 9: Dashboard 1
    s9 = prs.slides.add_slide(blank_layout)
    create_header(s9, "Power BI Dashboard Showcase (Pages 1 & 2)")
    img_p1 = CHARTS_DIR / "page1_mockup.png"
    img_p2 = CHARTS_DIR / "page2_mockup.png"
    if img_p1.exists():
        s9.shapes.add_picture(str(img_p1), Inches(0.8), Inches(1.6), width=Inches(5.6))
    if img_p2.exists():
        s9.shapes.add_picture(str(img_p2), Inches(6.9), Inches(1.6), width=Inches(5.6))
    add_card(s9, Inches(0.8), Inches(5.4), Inches(5.6), Inches(1.6))
    tb9_1 = s9.shapes.add_textbox(Inches(0.9), Inches(5.5), Inches(5.4), Inches(1.4))
    tb9_1.text_frame.word_wrap = True
    tb9_1.text_frame.paragraphs[0].text = "Page 1: Industry Overview (AUM ₹81L Cr, SIP ₹31K Cr, AMC share)"
    tb9_1.text_frame.paragraphs[0].font.size = Pt(10)
    add_card(s9, Inches(6.9), Inches(5.4), Inches(5.6), Inches(1.6))
    tb9_2 = s9.shapes.add_textbox(Inches(7.0), Inches(5.5), Inches(5.4), Inches(1.4))
    tb9_2.text_frame.word_wrap = True
    tb9_2.text_frame.paragraphs[0].text = "Page 2: Fund Performance (Return vs Risk scatter, Scorecard table, slicers)"
    tb9_2.text_frame.paragraphs[0].font.size = Pt(10)

    # Slide 10: Dashboard 2
    s10 = prs.slides.add_slide(blank_layout)
    create_header(s10, "Power BI Dashboard Showcase (Pages 3 & 4)")
    img_p3 = CHARTS_DIR / "page3_mockup.png"
    img_p4 = CHARTS_DIR / "page4_mockup.png"
    if img_p3.exists():
        s10.shapes.add_picture(str(img_p3), Inches(0.8), Inches(1.6), width=Inches(5.6))
    if img_p4.exists():
        s10.shapes.add_picture(str(img_p4), Inches(6.9), Inches(1.6), width=Inches(5.6))
    add_card(s10, Inches(0.8), Inches(5.4), Inches(5.6), Inches(1.6))
    tb10_1 = s10.shapes.add_textbox(Inches(0.9), Inches(5.5), Inches(5.4), Inches(1.4))
    tb10_1.text_frame.word_wrap = True
    tb10_1.text_frame.paragraphs[0].text = "Page 3: Investor Analytics (State flows, SIP vs Lumpsum donut, Age split)"
    tb10_1.text_frame.paragraphs[0].font.size = Pt(10)
    add_card(s10, Inches(6.9), Inches(5.4), Inches(5.6), Inches(1.6))
    tb10_2 = s10.shapes.add_textbox(Inches(7.0), Inches(5.5), Inches(5.4), Inches(1.4))
    tb10_2.text_frame.word_wrap = True
    tb10_2.text_frame.paragraphs[0].text = "Page 4: SIP & Market Trends (Dual axis SIP vs Nifty 50, Net category heatmap)"
    tb10_2.text_frame.paragraphs[0].font.size = Pt(10)

    # Slide 11: Strategic Recommendations
    s11 = prs.slides.add_slide(blank_layout)
    create_header(s11, "Strategic Recommendations for Bluestock Fintech")
    add_card(s11, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.3))
    tb11 = s11.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.9))
    tb11.text_frame.word_wrap = True
    p = tb11.text_frame.paragraphs[0]
    p.text = "5 Strategic Action Items for Executive Leadership"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = COLOR_NAVY
    for rec in [
        "1. Automated SIP Pre-Debit Reminders: Prevent mandate churn (97.8% at-risk cadence gaps) via WhatsApp/SMS alerts 48h prior.",
        "2. Multi-Factor Scorecard in Client App: Replace simple 1-year leaderboards with our composite 0–100 Scorecard to curb cyclical chasing.",
        "3. Small-Cap Tail-Risk (VaR) Disclosures: Display annualized downside risk gauges before retail investors allocate to high-beta schemes.",
        "4. Automated Sector Concentration Alerts: Warn users when portfolios have HHI > 2500 (e.g. 48.7% IT) and provide diversification swaps.",
        "5. Capitalize on Cohort 2025 Purchasing Power: Target young professionals with higher initial ticket sizes (+22.8%) via curated baskets."
    ]:
        p = tb11.text_frame.add_paragraph()
        p.space_before = Pt(8)
        p.text = "• " + rec
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_DARK

    # Slide 12: Thank You
    s12 = prs.slides.add_slide(blank_layout)
    hero12 = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    hero12.fill.solid()
    hero12.fill.fore_color.rgb = COLOR_NAVY
    hero12.line.fill.background()
    tb12 = s12.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10.3), Inches(3.0))
    tb12.text_frame.word_wrap = True
    p = tb12.text_frame.paragraphs[0]
    p.text = "Thank You!"
    p.font.bold = True
    p.font.size = Pt(44)
    p.font.color.rgb = COLOR_WHITE
    p2 = tb12.text_frame.add_paragraph()
    p2.text = "Bluestock Mutual Fund Analytics Capstone Project Complete"
    p2.font.size = Pt(20)
    p2.font.color.rgb = RGBColor(144, 205, 244)
    p2.space_before = Pt(8)

    prs.save(str(out_file))
    print(f"[OK] Presentation deck successfully saved to {out_file}")
    return str(out_file)

if __name__ == "__main__":
    generate_presentation_deck()
