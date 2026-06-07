import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.gridspec as gridspec
import os

# Visual Style Settings (Bluestock Theme)
plt.style.use('seaborn-v0_8-whitegrid')
COLORS = ['#1A365D', '#3182CE', '#63B3ED', '#F6E05E', '#E53E3E', '#38A169', '#805AD5']
sns.set_palette(sns.color_palette(COLORS))
plt.rcParams.update({
    'font.family': 'sans-serif',
    'axes.titlesize': 16,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 22,
    'figure.titleweight': 'bold',
    'axes.titleweight': 'bold'
})

def create_page_1():
    fig = plt.figure(figsize=(16, 9))
    fig.suptitle('Bluestock Mutual Funds Dashboard | Page 1: Industry Overview', color='#1A365D', y=0.98)
    
    gs = gridspec.GridSpec(2, 4, height_ratios=[1, 3])
    
    # KPIs
    kpi_data = [
        ("Total AUM", "₹81L Cr"),
        ("SIP Inflows", "₹31K Cr"),
        ("Total Folios", "26.12 Cr"),
        ("Total Schemes", "1,908")
    ]
    
    for i, (title, value) in enumerate(kpi_data):
        ax = fig.add_subplot(gs[0, i])
        ax.axis('off')
        ax.text(0.5, 0.6, title, ha='center', va='center', fontsize=14, color='#4A5568')
        ax.text(0.5, 0.3, value, ha='center', va='center', fontsize=28, weight='bold', color='#1A365D')
        
        # Add a subtle border/box around KPI
        rect = plt.Rectangle((0, 0), 1, 1, fill=True, facecolor='#E2E8F0', edgecolor='none', alpha=0.3, transform=ax.transAxes)
        ax.add_patch(rect)

    # Line Chart: Industry AUM Trend 2022-2025
    ax_line = fig.add_subplot(gs[1, :2])
    years = ['2022', '2023', '2024', '2025']
    aum_trend = [39.8, 48.5, 62.3, 81.0] # L Cr roughly
    ax_line.plot(years, aum_trend, marker='o', linewidth=3, color='#3182CE', markersize=10)
    ax_line.set_title("Industry AUM Trend (2022-2025)")
    ax_line.set_ylabel("AUM (in ₹Lakh Crores)")
    for i, txt in enumerate(aum_trend):
        ax_line.annotate(f"{txt}L", (years[i], aum_trend[i]), textcoords="offset points", xytext=(0,10), ha='center')

    # Bar Chart: AUM by AMC
    ax_bar = fig.add_subplot(gs[1, 2:])
    amcs = ['SBI MF', 'ICICI Pru', 'HDFC MF', 'Nippon', 'Kotak']
    amc_aum = [10.5, 8.2, 7.8, 5.1, 4.3]
    sns.barplot(x=amcs, y=amc_aum, ax=ax_bar, palette=COLORS)
    ax_bar.set_title("Top 5 AMCs by AUM")
    ax_bar.set_ylabel("AUM (in ₹Lakh Crores)")
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('Page_1_Industry_Overview.png', dpi=300)
    return fig

def create_page_2():
    fig = plt.figure(figsize=(16, 9))
    fig.suptitle('Bluestock Mutual Funds Dashboard | Page 2: Fund Performance', color='#1A365D', y=0.98)
    
    gs = gridspec.GridSpec(2, 2)
    
    # Scatter Plot: Return vs Risk (Std Dev)
    ax_scatter = fig.add_subplot(gs[0, 0])
    np.random.seed(42)
    risk = np.random.uniform(10, 25, 40)
    returns = risk * 0.8 + np.random.normal(0, 3, 40)
    aum = np.random.uniform(100, 5000, 40)
    
    scatter = ax_scatter.scatter(risk, returns, s=aum/5, c=COLORS[0], alpha=0.6, edgecolors='white', linewidth=1)
    ax_scatter.set_title("Fund Performance: Return vs Risk")
    ax_scatter.set_xlabel("Risk (Standard Deviation %)")
    ax_scatter.set_ylabel("Annualized Return (%)")
    
    # Line chart: NAV vs Benchmark
    ax_nav = fig.add_subplot(gs[0, 1])
    dates = pd.date_range(start='1/1/2024', periods=12, freq='ME')
    nav = np.linspace(100, 130, 12) + np.random.normal(0, 2, 12)
    benchmark = np.linspace(100, 125, 12) + np.random.normal(0, 1.5, 12)
    ax_nav.plot(dates, nav, label='Fund NAV', color='#3182CE', linewidth=2)
    ax_nav.plot(dates, benchmark, label='Nifty 50', color='#E53E3E', linestyle='--', linewidth=2)
    ax_nav.set_title("NAV Trend vs Benchmark")
    ax_nav.legend()
    fig.autofmt_xdate()

    # Scorecard Table
    ax_table = fig.add_subplot(gs[1, :])
    ax_table.axis('off')
    table_data = [
        ["SBI Small Cap Fund", "Equity", "24.5%", "18.2", "92"],
        ["HDFC Flexi Cap", "Equity", "21.2%", "14.5", "88"],
        ["ICICI Pru Liquid", "Debt", "7.1%", "1.2", "85"],
        ["Nippon India Large Cap", "Equity", "18.5%", "13.0", "81"],
        ["Kotak Emerging Equity", "Equity", "22.1%", "17.5", "89"]
    ]
    col_labels = ["Fund Name", "Category", "1Y Return", "Risk (StdDev)", "Bluestock Score"]
    table = ax_table.table(cellText=table_data, colLabels=col_labels, loc='center', cellLoc='center')
    table.scale(1, 2)
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor('#1A365D')
            cell.set_text_props(color='white', weight='bold')
        else:
            cell.set_facecolor('#F7FAFC' if row % 2 == 0 else 'white')
            
    ax_table.set_title("Top Funds Scorecard", pad=20)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('Page_2_Fund_Performance.png', dpi=300)
    return fig

def create_page_3():
    fig = plt.figure(figsize=(16, 9))
    fig.suptitle('Bluestock Mutual Funds Dashboard | Page 3: Investor Analytics', color='#1A365D', y=0.98)
    
    gs = gridspec.GridSpec(2, 2)
    
    # Bar Chart: Transaction by State
    ax_state = fig.add_subplot(gs[0, 0])
    states = ['MH', 'KA', 'DL', 'GJ', 'UP', 'TN']
    amounts = [24500, 18200, 15400, 12100, 9500, 8800] # In Crores
    sns.barplot(x=states, y=amounts, ax=ax_state, palette=COLORS)
    ax_state.set_title("Transaction Volume by State (₹ Cr)")
    
    # Donut: Split
    ax_donut = fig.add_subplot(gs[0, 1])
    labels = ['SIP', 'Lumpsum', 'Redemption']
    sizes = [55, 25, 20]
    colors = ['#3182CE', '#F6E05E', '#E53E3E']
    ax_donut.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, pctdistance=0.85, 
                 textprops={'fontsize': 12, 'weight': 'bold'})
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    ax_donut.add_artist(centre_circle)
    ax_donut.set_title("Transaction Type Split")
    
    # Bar: Age Group vs SIP
    ax_age = fig.add_subplot(gs[1, 0])
    age_groups = ['18-25', '26-35', '36-45', '46-55', '55+']
    sip_amounts = [2500, 6500, 12500, 15000, 8500]
    sns.barplot(x=age_groups, y=sip_amounts, ax=ax_age, palette=COLORS)
    ax_age.set_title("Average SIP Amount by Age Group (₹)")
    ax_age.set_ylabel("Avg SIP (₹)")
    
    # Line: Monthly Volume
    ax_monthly = fig.add_subplot(gs[1, 1])
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    vol = [1.2, 1.3, 1.5, 1.4, 1.6, 1.8, 1.7, 1.9, 2.1, 2.0, 2.3, 2.5]
    ax_monthly.plot(months, vol, marker='o', color='#38A169', linewidth=2)
    ax_monthly.set_title("Monthly Transaction Volume (Lakhs)")
    ax_monthly.set_ylabel("Transactions (Lakhs)")
    ax_monthly.tick_params(axis='x', rotation=45)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('Page_3_Investor_Analytics.png', dpi=300)
    return fig

def create_page_4():
    fig = plt.figure(figsize=(16, 9))
    fig.suptitle('Bluestock Mutual Funds Dashboard | Page 4: SIP & Market Trends', color='#1A365D', y=0.98)
    
    gs = gridspec.GridSpec(2, 2)
    
    # Dual Axis: SIP Inflow + Nifty 50
    ax_dual_1 = fig.add_subplot(gs[0, :])
    months_dual = pd.date_range(start='1/1/2023', periods=12, freq='ME').strftime('%b %y')
    sip_inflow = [13.5, 14.1, 14.5, 13.8, 14.9, 15.2, 15.8, 16.0, 16.5, 17.1, 17.5, 18.2] # K Cr
    nifty = np.linspace(17500, 21500, 12) + np.random.normal(0, 500, 12)
    
    ax_dual_1.bar(months_dual, sip_inflow, color='#3182CE', alpha=0.7, label='SIP Inflow (₹K Cr)')
    ax_dual_1.set_ylabel("SIP Inflow (₹K Cr)", color='#3182CE')
    
    ax_dual_2 = ax_dual_1.twinx()
    ax_dual_2.plot(months_dual, nifty, color='#E53E3E', marker='o', linewidth=2, label='Nifty 50')
    ax_dual_2.set_ylabel("Nifty 50 Index", color='#E53E3E')
    
    ax_dual_1.set_title("SIP Inflow vs Market Trend")
    
    lines_1, labels_1 = ax_dual_1.get_legend_handles_labels()
    lines_2, labels_2 = ax_dual_2.get_legend_handles_labels()
    ax_dual_1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

    # Category Inflow Heatmap
    ax_heat = fig.add_subplot(gs[1, 0])
    heat_data = pd.DataFrame(
        np.random.randint(500, 5000, size=(5, 4)),
        columns=['Q1', 'Q2', 'Q3', 'Q4'],
        index=['Small Cap', 'Mid Cap', 'Large Cap', 'Flexi Cap', 'Debt']
    )
    sns.heatmap(heat_data, annot=True, fmt="d", cmap="Blues", ax=ax_heat)
    ax_heat.set_title("Category Inflow Heatmap (₹ Cr)")
    
    # Top 5 Categories
    ax_bar = fig.add_subplot(gs[1, 1])
    categories = ['Small Cap', 'Sectoral', 'Mid Cap', 'Flexi Cap', 'Multi Cap']
    net_inflow = [42000, 35000, 28000, 22000, 15000]
    sns.barplot(y=categories, x=net_inflow, ax=ax_bar, palette="viridis")
    ax_bar.set_title("Top 5 Categories by Net Inflow FY25 (₹ Cr)")
    ax_bar.set_xlabel("Net Inflow (₹ Cr)")
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('Page_4_SIP_Market_Trends.png', dpi=300)
    return fig

def main():
    print("Generating Page 1...")
    p1 = create_page_1()
    print("Generating Page 2...")
    p2 = create_page_2()
    print("Generating Page 3...")
    p3 = create_page_3()
    print("Generating Page 4...")
    p4 = create_page_4()
    
    print("Saving to Dashboard.pdf...")
    with PdfPages('Dashboard.pdf') as pdf:
        pdf.savefig(p1)
        pdf.savefig(p2)
        pdf.savefig(p3)
        pdf.savefig(p4)
    print("Done! Check your folder for Dashboard.pdf and the 4 PNG files.")

if __name__ == "__main__":
    main()
