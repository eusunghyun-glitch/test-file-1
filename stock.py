import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
import seaborn as sb
import yfinance as yf  # Assuming yfinance for data API

sb.set_theme()

"""
STUDENT CHANGE LOG & AI DISCLOSURE:
----------------------------------
1. Did you use an LLM (ChatGPT/Claude/etc.)? [Yes/No]
2. If yes, what was your primary prompt?
----------------------------------
"""

DEFAULT_START = dt.date.isoformat(dt.date.today() - dt.timedelta(365))
DEFAULT_END = dt.date.isoformat(dt.date.today())


class Stock:
    def __init__(self, symbol, start=DEFAULT_START, end=DEFAULT_END):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.data = self.get_data()

    def get_data(self):
        """Downloads data from yfinance and triggers return calculation."""
        df = yf.download(self.symbol, start=self.start, end=self.end, progress=False)
        df.index = pd.to_datetime(df.index)
        df = self.calc_returns(df)
        return df


    def calc_returns(self, df):
        """Adds 'Change', close to close and 'Instant_Return' columns to the dataframe."""
        # Requirement: Use vectorized pandas operations, not loops.
        df['change'] = df['Close'].pct_change()
        df['instant_return'] = np.log(df['Close']).diff().round(4)
        return df

    
    def add_technical_indicators(self, windows=[20, 50]):
        """
        Add Simple Moving Averages (SMA) for the given windows
        to the internal DataFrame. Produce a plot showing the closing price and SMAs. 
        """
        for window in windows:
            self.data[f'SMA_{window}'] = self.data['Close'].rolling(window=window).mean()
        plt.figure(figsize=(12, 6))
        plt.plot(self.data.index, self.data['Close'], label='Close Price', color='black', linewidth=1.5)

        for window in windows:
            plt.plot(self.data.index, self.data[f'SMA_{window}'], label=f'{window}-Day SMA', linestyle='--')

        plt.title(f"{self.symbol} - Price and Simple Moving Averages")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.legend()
        plt.tight_layout()
        plt.show()


    def plot_return_dist(self):
        plt.figure(figsize=(10, 6))

        clean_returns = self.data['instant_return'].dropna()

        sb.histplot(clean_returns, kde=True, bins=50, color='purple')
        plt.title(f"{self.symbol} - Distribution of Instantaneous Returns")
        plt.xlabel("Instantaneous Return (Log Return)")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()



    def plot_performance(self):
        """Plots cumulative growth of $1 investment."""
        first_price = self.data['Close'].dropna().iloc[0]
        performance = ((self.data['Close'] / first_price) - 1) * 100

        plt.figure(figsize=(12, 6))
        plt.plot(self.data.index, performance, label='Cumulative Performance', color='green', linewidth=2)

        plt.axhline(0, color='red', linestyle='--', linewidth=1)

        plt.title(f"{self.symbol} - Cumulative Performance")
        plt.xlabel("Date")
        plt.ylabel("Percent Gain/Loss (%)")

        # 요구사항: Y축을 퍼센트 형식으로 표시
        ax = plt.gca()
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())

        plt.legend()
        plt.tight_layout()
        plt.show()



def main():

    ticker_symbol = input("Enter the stock symbol you want to analyze (e.g., NVDA): ").upper()

    stock_obj = Stock(ticker_symbol)

    print(f"\n--- Historical Data for {ticker_symbol} ---")
    print(stock_obj.data.head())

    print(f"\nGenerating plots for {ticker_symbol}...")
    stock_obj.add_technical_indicators()
    stock_obj.plot_return_dist()
    stock_obj.plot_performance()


if __name__ == "__main__":
    main()