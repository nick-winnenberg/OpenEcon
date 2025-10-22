# OpenEcon Dashboard

An economic dashboard displaying key US economic indicators using data from the Federal Reserve Economic Data (FRED) API.

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get FRED API Key
1. Visit https://fred.stlouisfed.org/docs/api/api_key.html
2. Create a free account
3. Get your API key

### 3. Set Environment Variable
**Option A: Set environment variable (Recommended)**
```bash
# Windows (PowerShell)
$env:FRED_API_KEY="your_api_key_here"

# Windows (Command Prompt)
set FRED_API_KEY=your_api_key_here

# Linux/Mac
export FRED_API_KEY=your_api_key_here
```

**Option B: Edit the code**
Replace `'YOUR_FRED_API_KEY'` in `app.py` line 11 with your actual API key.

### 4. Run the Application
```bash
streamlit run app.py
```

## Features

The dashboard displays:
- **Workforce Insights**: Employment, open positions, labor force participation
- **Inflation Insights**: Consumer Price Index (CPI) and Producer Price Index (PPI)
- **Economic Growth**: GDP and national debt trends
- **Population Insights**: Fertility rates and demographic trends
- **Income Inequality**: Gini Index analysis

## Data Sources

All data is sourced from the Federal Reserve Economic Data (FRED) database, ensuring reliable and up-to-date economic indicators.

## Fixed Issues

- ✅ Replaced deprecated `pandas-datareader` with `fredapi` for Python 3.13 compatibility
- ✅ Added error handling for data fetching
- ✅ Improved API key management with environment variables
- ✅ Added data caching for better performance