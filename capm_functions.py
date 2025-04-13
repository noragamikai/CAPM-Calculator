import plotly.express as px
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Function to plot interactive plotly chart
def interactive_plot(df):
    fig = px.line()
    for col in df.columns[1:]:  # skip 'Date'
        fig.add_scatter(x=df['Date'], y=df[col], mode='lines', name=col)
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        height=450
    )
    return fig

# Normalize stock prices relative to the first day
def normalize(df):
    df_norm = df.copy()
    for col in df.columns[1:]:  # skip 'Date'
        df_norm[col] = df_norm[col] / df_norm[col].iloc[0]
    return df_norm

# Calculate daily returns (% change from previous day)
def daily_return(df):
    df_ret = df.copy()
    for col in df.columns[1:]:  # skip 'Date'
        df_ret[col] = df_ret[col].pct_change()
    df_ret.dropna(inplace=True)
    return df_ret

# Function to calculate beta and alpha using linear regression
def calculate_beta(df_return, stock):
    x = df_return['SP500']
    y = df_return[stock]
    b, a = np.polyfit(x, y, deg=1)  # beta = slope, alpha = intercept
    return b, a



# Plot Security Characteristic Line for a stock
def plot_scl(df_return, stock):
    x = df_return['SP500']
    y = df_return[stock]
    beta, alpha = np.polyfit(x, y, deg=1)

    fig = go.Figure()

    # Scatter plot of returns
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Daily Returns'))

    # Regression line (SCL)
    regression_line = alpha + beta * x
    fig.add_trace(go.Scatter(x=x, y=regression_line, mode='lines', name='SCL (Regression Line)', line=dict(color='red')))

    fig.update_layout(
        title=f"📈 Security Characteristic Line: {stock}",
        xaxis_title='Market Return (S&P 500)',
        yaxis_title=f'{stock} Return',
        height=500
    )
    return fig

def expected_vs_actual_plot(beta_dict, merged_returns, rf, rm):
    # Calculate expected and actual returns
    expected = {stock: rf + beta_dict[stock] * (rm - rf) for stock in beta_dict}
    actual = {stock: merged_returns[stock].mean() * 252 for stock in beta_dict}

    # Determine bar colors based on performance
    colors = []
    for stock in beta_dict:
        if actual[stock] >= expected[stock]:
            colors.append('green')  # Outperformed
        else:
            colors.append('red')    # Underperformed

    # Create bar chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=list(beta_dict.keys()),
        y=[round(expected[s], 2) for s in beta_dict],
        name='Expected Return (CAPM)',
        marker_color='blue'
    ))

    fig.add_trace(go.Bar(
        x=list(beta_dict.keys()),
        y=[round(actual[s], 2) for s in beta_dict],
        name='Actual Return',
        marker_color=colors  # Green if outperformed, red if not
    ))

    fig.update_layout(
        barmode='group',
        title="📊 Expected Return (CAPM) vs Actual Return",
        xaxis_title="Stock",
        yaxis_title="Annual Return",
        height=500
    )

    return fig

import plotly.graph_objects as go

def plot_sml(beta_dict, rf, rm):
    """
    Plot the Security Market Line (SML) using CAPM formula:
    Expected Return = rf + beta * (rm - rf)
    """
    betas = list(beta_dict.values())
    stocks = list(beta_dict.keys())

    # Calculate expected returns using CAPM
    expected_returns = [rf + b * (rm - rf) for b in betas]

    # Create the SML line (from beta 0 to max_beta + 0.5)
    beta_range = [0, max(betas) + 0.5]
    sml_returns = [rf + b * (rm - rf) for b in beta_range]

    fig = go.Figure()

    # Plot the SML line
    fig.add_trace(go.Scatter(
        x=beta_range,
        y=sml_returns,
        mode='lines',
        name='Security Market Line',
        line=dict(color='blue', width=3, dash='dash')
    ))

    # Plot each stock's beta and expected return
    fig.add_trace(go.Scatter(
        x=betas,
        y=expected_returns,
        mode='markers+text',
        name='Stocks',
        text=stocks,
        textposition='top center',
        marker=dict(size=10, color='red')
    ))

    fig.update_layout(
        title="📉 Security Market Line (SML)",
        xaxis_title="Beta",
        yaxis_title="Expected Return (CAPM)",
        height=500
    )

    return fig
