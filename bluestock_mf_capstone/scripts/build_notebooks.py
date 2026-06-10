import nbformat as nbf
from pathlib import Path

def write_notebook(filename, cells):
    nb = nbf.v4.new_notebook()
    nb_cells = []
    for cell_type, content in cells:
        if cell_type == "markdown":
            nb_cells.append(nbf.v4.new_markdown_cell(content))
        elif cell_type == "code":
            nb_cells.append(nbf.v4.new_code_cell(content))
    nb['cells'] = nb_cells
    
    with open(filename, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Created {filename}")

def main():
    base_path = Path(__file__).resolve().parent.parent / "notebooks"
    base_path.mkdir(exist_ok=True)
    
    # 01 Data Ingestion
    cells_01 = [
        ("markdown", "# Data Ingestion\nThis notebook demonstrates extracting raw CSV files and taking a first look at the dataset shapes and data types."),
        ("code", "import pandas as pd\nimport glob\nfrom pathlib import Path\n\nraw_dir = Path('../data/raw')\nfiles = list(raw_dir.glob('*.csv'))\nfiles"),
        ("code", "for f in files[:3]:\n    print(f'\\n--- {f.name} ---')\n    df = pd.read_csv(f)\n    print(df.info())")
    ]
    write_notebook(base_path / "01_data_ingestion.ipynb", cells_01)
    
    # 02 Data Cleaning
    cells_02 = [
        ("markdown", "# Data Cleaning\nThis notebook cleans the datasets, primarily focusing on `02_nav_history.csv` to forward-fill missing dates for weekends and holidays."),
        ("code", "import pandas as pd\nfrom pathlib import Path\n\nprocessed_dir = Path('../data/processed')\nnav_df = pd.read_csv(processed_dir / '02_nav_history.csv')\nnav_df.head()"),
        ("code", "# Check if we have missing dates after ffill during ETL\nprint(nav_df['date'].isna().sum())")
    ]
    write_notebook(base_path / "02_data_cleaning.ipynb", cells_02)
    
    # 03 EDA Analysis
    cells_03 = [
        ("markdown", "# Exploratory Data Analysis (EDA)\nIn this notebook, we visualize data trends, SIP inflows, and AUM by fund house."),
        ("code", "import pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nfrom pathlib import Path\n\nprocessed_dir = Path('../data/processed')"),
        ("code", "aum = pd.read_csv(processed_dir / '03_aum_by_fund_house.csv')\nsns.barplot(data=aum.head(10), x='aum_crores', y='fund_house')\nplt.title('Top 10 Fund Houses by AUM')\nplt.show()")
    ]
    write_notebook(base_path / "03_eda_analysis.ipynb", cells_03)
    
    # 04 Performance Analytics
    cells_04 = [
        ("markdown", "# Performance Analytics\nHere we compute CAGR, Sharpe Ratio, Beta, and Value at Risk (VaR). \n\n*Important:* We annualize using 252 trading days."),
        ("code", "import pandas as pd\nimport numpy as np\nfrom pathlib import Path\n\nprocessed_dir = Path('../data/processed')\nnav = pd.read_csv(processed_dir / '02_nav_history.csv')\nnav['date'] = pd.to_datetime(nav['date'])"),
        ("code", "def calculate_cagr(start_val, end_val, periods, freq='D'):\n    years = periods / 252 if freq == 'D' else periods\n    if start_val == 0:\n        return np.nan\n    return (end_val / start_val)**(1/years) - 1"),
        ("code", "def calculate_sharpe(returns, risk_free_rate=0.07):\n    excess_return = returns.mean() * 252 - risk_free_rate\n    volatility = returns.std() * np.sqrt(252)\n    if volatility == 0:\n        return 0\n    return excess_return / volatility"),
        ("code", "# Example VaR calculation at 95% confidence\n# var_95 = np.percentile(returns.dropna(), 5)")
    ]
    write_notebook(base_path / "04_performance_analytics.ipynb", cells_04)
    
    # 05 Advanced Analytics
    cells_05 = [
        ("markdown", "# Advanced Analytics\nCohort analysis, recommender logic, Monte Carlo simulations (Bonus 3), and Markowitz Efficient Frontier (Bonus 4)."),
        ("code", "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nfrom pathlib import Path\n\nprocessed_dir = Path('../data/processed')\nnav = pd.read_csv(processed_dir / '02_nav_history.csv')\nnav['date'] = pd.to_datetime(nav['date'])"),
        ("code", "# Bonus 3: Monte Carlo Simulation\ndef monte_carlo_simulation(returns, days=252*5, sims=100):\n    mean_ret = returns.mean()\n    std_ret = returns.std()\n    simulated_paths = np.zeros((days, sims))\n    simulated_paths[0] = 1 # Start at normalized NAV 1\n    for t in range(1, days):\n        rand_shocks = np.random.normal(mean_ret, std_ret, sims)\n        simulated_paths[t] = simulated_paths[t-1] * (1 + rand_shocks)\n    return simulated_paths"),
        ("code", "# Bonus 4: Markowitz Efficient Frontier\n# Use scipy.optimize to find minimum variance portfolio or max Sharpe portfolio")
    ]
    write_notebook(base_path / "05_advanced_analytics.ipynb", cells_05)

if __name__ == '__main__':
    main()
