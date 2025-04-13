# Importing libraries
import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import capm_functions

# Streamlit page setup
st.set_page_config(page_title="📈 CAPM Calculator", layout="wide")
st.title("💼 Capital Asset Pricing Model")

# Get user inputs
col1, col2 = st.columns([1, 1])
with col1:
    stock_input = st.text_input(
    "📊 Enter Stock Tickers (comma-separated)", 
    value="TSLA, AAPL"
)
stocks_list = [stock.strip().upper() for stock in stock_input.split(',') if stock.strip()]

with col2:
    year = st.number_input("📆 Number of Years", 1, 10, value=1)

# Date range
end = datetime.date.today()
start = datetime.date(end.year - year, end.month, end.day)

# Download stock data
stock_df = pd.DataFrame()
for stock in stocks_list:
    data = yf.download(stock, start=start, end=end)
    stock_df[stock] = data['Close']
stock_df.reset_index(inplace=True)

# Download and clean SP500 data
SP500 = yf.download('^GSPC', start=start, end=end)

# Flatten columns if needed
if isinstance(SP500.columns, pd.MultiIndex):
    SP500.columns = ['_'.join(col).strip() for col in SP500.columns.values]
SP500.reset_index(inplace=True)

# Find and rename the 'Close' column

# Pick the column that has the word 'Close' in its name (this is the SP500 closing price)
for col in SP500.columns:
    if 'Close' in col:
        sp_close_col = col
        break

# Keep only the 'Date' and 'Close' columns and rename 'Close' to 'SP500'
SP500 = SP500[['Date', sp_close_col]]
SP500.rename(columns={sp_close_col: 'SP500'}, inplace=True)


# Merge stock and SP500 data
merged_df = pd.merge(stock_df, SP500, on='Date', how='inner')

# Show merged data
st.markdown("### 📁 Merged Data Preview")
st.dataframe(merged_df.head(), use_container_width=True)

# Plotting prices
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("### 📈 Stock Prices")
    st.plotly_chart(capm_functions.interactive_plot(stock_df), use_container_width=True)

with col2:
    st.markdown("### 📊 Normalized Prices")
    norm_df = capm_functions.normalize(stock_df)
    st.plotly_chart(capm_functions.interactive_plot(norm_df), use_container_width=True)

# Calculate daily returns
merged_returns = capm_functions.daily_return(merged_df)

# Calculate Beta & Alpha
beta = {}
alpha = {}
for i in stocks_list:
    b, a = capm_functions.calculate_beta(merged_returns, i)
    beta[i] = b
    alpha[i] = a

# Show Beta
beta_df = pd.DataFrame({
    'Stock': list(beta.keys()),
    'Beta Value': [round(val, 2) for val in beta.values()]
})
with col1:
    st.markdown("### 🧮 Beta Values")
    st.dataframe(beta_df, use_container_width=True)

# CAPM Return Calculation
# Get 10-Year Treasury Note Yield (^TNX)
rf_data = yf.download('^TNX', period='1mo', interval='1d')
rf = float(rf_data['Close'].mean()) / 100  # Ensure it's a float


rm = merged_returns['SP500'].mean() * 252  # Annualized market return

with col2:
    st.markdown("### 💹 Expected vs Actual Returns")
    fig_return_compare = capm_functions.expected_vs_actual_plot(beta, merged_returns, rf, rm)
    st.plotly_chart(fig_return_compare, use_container_width=True)


st.markdown(f"#### 📌 Risk-Free Rate (10Y T-Note): `{round(rf * 100, 2)}%`")

returns_df = pd.DataFrame({
    'Stock': list(beta.keys()),
    'Expected Return (CAPM)': [round(rf + b * (rm - rf), 2) for b in beta.values()]
})
with col1:
    st.markdown("### 💰 Expected Return (CAPM)")
    st.dataframe(returns_df, use_container_width=True)

with col2:
    st.markdown("### 📉 Security Characteristic Line (SLR)")
    st.markdown("""
    The **Security Characteristic Line (SCL)** shows the relationship between the stock's excess returns
    and market's excess returns. The **slope** of this line is the **Beta** which shows the stock's sensitivity
    to market movements. A **steeper slope** means more volatility.
    """)
for stock in stocks_list:
    fig = capm_functions.plot_scl(merged_returns, stock)
    st.plotly_chart(fig, use_container_width=True)

with col1:
    st.markdown("### 📐 Security Market Line (SML)")
    st.markdown("""
    The **Security Market Line (SML)** represents the expected return of a stock (Y-axis) given its Beta (X-axis),
    as per CAPM. 

    - Stocks **above** the line are **undervalued** (higher return for given risk).
    - Stocks **below** the line are **overvalued** (lower return for given risk).

    The line starts at the risk-free rate and has a slope equal to the **market risk premium** (`rm - rf`).
    """)
    fig_sml = capm_functions.plot_sml(beta, rf, rm)
    st.plotly_chart(fig_sml, use_container_width=True)
