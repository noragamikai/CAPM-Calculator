# 📈 CAPM Calculator using Streamlit

This is a web app that calculates and visualizes the **Capital Asset Pricing Model (CAPM)** for any selected stocks using historical data.

## 🚀 Features
- Download stock and S&P 500 data automatically
- Normalize and plot stock prices
- Calculate Beta, Alpha, and Expected Returns
- Compare Expected vs Actual Returns
- Plot Security Characteristic Line (SCL)
- Plot Security Market Line (SML)

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/noragamikai/capm-calculator.git
cd capm-calculator

2.Install the dependencies:
pip install -r requirements.txt

3.Run the Streamlit app:
streamlit run capm_return.py

## 🛠️ Files
capm_functions.py: Contains helper functions (normalization, beta calculation, plots)

capm_return.py: Main Streamlit application file

requirements.txt: Lists all Python libraries required

README.md: Project documentation

## Usage:
-  Open the app in your browser after running streamlit run capm_return.py.
-   Enter stock tickers (e.g., TSLA, AAPL) in the input field, separated by commas.
-   Select the number of years for historical data (1-10 years).
-   Explore the results, including:
-   Merged data preview.
-   Stock price and normalized price charts.
-   Beta values for each stock.
-   Expected vs. actual return comparisons.
-   SCL and SML plots with explanations.

📋 Notes
Make sure you have an internet connection as it downloads live data using Yahoo Finance.

If you see any API limits from Yahoo, just wait a few minutes and retry.

Contact
For questions or feedback, open an issue on GitHub or mail me at: rohitrajsinha88@gmail.com 
