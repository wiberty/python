import pandas as pd  # csv files are read and analysed in a DataFrame

""""
# PRICE MOVEMENT ANALYZER

### **pma.py**

Calculates price movement percentages of tickers in a portfolio and ranks them by biggest daily movers. Tickers that have negative price movements over 1 day
, 1 month, and 1 year periods are displayed separately for review. All ticker prices available (regardless of whether they are included in the portfolio) are 
sorted by daily movers and the top n returned.

NB: This is an example class. It feeds from csv files, not JSON requests. The analysis is as basic as possible; however it serves as a structural demonstration 
of how algorithmic trading might be included, based on analysis of price performance.

Use case: Compare the top tickers available against the bottom tickers within a portfolio, to inform rebalancing decisions.

Technical details: The class is instantiated from method PMA.analyze, which contains 3 parameters. Argument 1: The ticker list file destination; Argument 2: 
The ticker price file destination; Argument 3 (optional): defaults to n ticker recommendations in the price analysis.
"""

class PMA:  # Price Movement Analyzer
    def __init__(self, ticker_list, prices, nprices=5):
        self.ticker_list = ticker_list
        self.prices = prices
        self.watchlist_tickers = []
        self.ticker_prices = None
        self.ticker_prices_f = None
        self.ticker_prices_f_s = None
        self.negative_tickers = None
        self.negative_tickers_s = None
        self.ticker_prices_uf = None
        self.ticker_prices_uf_s = None
        self.nprices = nprices  # Number of top price movements to be returned
        self.top_tickers = None

    def read_watchlist(self):
        try:
            # Read watch list
            watchlist = pd.read_csv(self.ticker_list)
            self.watchlist_tickers = watchlist['Ticker'].tolist()
        except FileNotFoundError:
            raise Exception("Error: Watchlist file not found.")
        except Exception as e:
            raise Exception(f"An error occurred while reading the watchlist: {str(e)}")

    def read_ticker_prices(self):
        try:
            # Read ticker prices
            self.ticker_prices = pd.read_csv(self.prices)
        except FileNotFoundError:
            raise Exception("Error: Ticker data file not found.")
        except Exception as e:
            raise Exception(f"An error occurred while reading the ticker data: {str(e)}")

    def filter_data(self):
        try:
            # Filter data by watchlist
            self.ticker_prices_f = self.ticker_prices[self.ticker_prices['Ticker'].isin(self.watchlist_tickers)].copy()
        except KeyError:
            raise Exception("Error: Invalid column name in the ticker data.")
        except Exception as e:
            raise Exception(f"An error occurred while filtering the data: {str(e)}")

    def calculate_percentage_movements(self):
        try:
            # Calculate percentage movements for filtered data
            self.ticker_prices_f['1 Day %'] = ((self.ticker_prices_f['Close'] - self.ticker_prices_f['One_Day_Ago_Close']) / self.ticker_prices_f['One_Day_Ago_Close']) * 100
            self.ticker_prices_f['1 Month %'] = ((self.ticker_prices_f['Close'] - self.ticker_prices_f['One_Month_Ago_Close']) / self.ticker_prices_f['One_Month_Ago_Close']) * 100
            self.ticker_prices_f['1 Year %'] = ((self.ticker_prices_f['Close'] - self.ticker_prices_f['One_Year_Ago_Close']) / self.ticker_prices_f['One_Year_Ago_Close']) * 100
        except KeyError:
            raise Exception("Error: Invalid column name in the filtered data.")
        except Exception as e:
            raise Exception(f"An error occurred while calculating the percentage movements: {str(e)}")

    def sort_filtered_data(self):
        try:
            # Sort filtered data by 1 Day % in descending order
            self.ticker_prices_f_s = self.ticker_prices_f.sort_values('1 Day %', ascending=False).reset_index(drop=True)
            # Add Ranking column for filtered data
            self.ticker_prices_f_s['Ranking'] = range(1, len(self.ticker_prices_f_s) + 1)
        except KeyError:
            raise Exception("Error: Invalid column name in the sorted filtered data.")
        except Exception as e:
            raise Exception(f"An error occurred while sorting the filtered data: {str(e)}")

    def find_negative_tickers(self):
        try:
            # Find tickers with negative percentage values for all three columns in filtered data
            self.negative_tickers = self.ticker_prices_f_s[(self.ticker_prices_f_s['1 Day %'] < 0) & (self.ticker_prices_f_s['1 Month %'] < 0) & (self.ticker_prices_f_s['1 Year %'] < 0)]
            # Sort the negative tickers by the same order as the filtered data
            self.negative_tickers_s = self.negative_tickers.reindex(self.ticker_prices_f_s.columns, axis=1)
        except KeyError:
            raise Exception("Error: Invalid column name in the negative tickers data.")
        except Exception as e:
            raise Exception(f"An error occurred while finding the negative tickers: {str(e)}")

    def process_unfiltered_data(self):
        try:
            # Read ticker_prices.csv again
            self.ticker_prices_uf = pd.read_csv(self.prices)

            # Calculate percentage movements for unfiltered data
            self.ticker_prices_uf['1 Day %'] = ((self.ticker_prices_uf['Close'] - self.ticker_prices_uf['One_Day_Ago_Close']) / self.ticker_prices_uf['One_Day_Ago_Close']) * 100
            self.ticker_prices_uf['1 Month %'] = ((self.ticker_prices_uf['Close'] - self.ticker_prices_uf['One_Month_Ago_Close']) / self.ticker_prices_uf['One_Month_Ago_Close']) * 100
            self.ticker_prices_uf['1 Year %'] = ((self.ticker_prices_uf['Close'] - self.ticker_prices_uf['One_Year_Ago_Close']) / self.ticker_prices_uf['One_Year_Ago_Close']) * 100

            # Sort unfiltered data by 1 Day % in descending order
            self.ticker_prices_uf_s = self.ticker_prices_uf.sort_values('1 Day %', ascending=False).reset_index(drop=True)

            # Select top n tickers from unfiltered data
            self.top_tickers = self.ticker_prices_uf_s.head(self.nprices).copy()

            # Add Ranking column for top n tickers from unfiltered data
            self.top_tickers['Ranking'] = range(1, len(self.top_tickers) + 1)
        except KeyError:
            raise Exception("Error: Invalid column name in the unfiltered data.")
        except Exception as e:
            raise Exception(f"An error occurred while processing the unfiltered data: {str(e)}")

    def print_filtered_data(self):
        # Format the filtered data as a table
        formatted_table_filtered = (
            self.ticker_prices_f_s[['Ranking', 'Ticker', '1 Day %', '1 Month %', '1 Year %']]
            .to_string(index=False, justify='center', col_space=[10, 10, 18, 18, 18], formatters={'1 Day %': '{:.2f}'.format, '1 Month %': '{:.2f}'.format, '1 Year %': '{:.2f}'.format})
        )
        # Print a table for the filtered data
        print("\nPortfolio Performance:")
        print(formatted_table_filtered)

    def print_negative_tickers(self):
        # Format the negative tickers as a table
        formatted_negative_tickers = (
            self.negative_tickers_s[['Ranking', 'Ticker', '1 Day %', '1 Month %', '1 Year %']]
            .to_string(index=False, justify='center', col_space=[10, 10, 18, 18, 18], formatters={'1 Day %': '{:.2f}'.format, '1 Month %': '{:.2f}'.format, '1 Year %': '{:.2f}'.format})
        )
        # Print the table for the tickers with all negative percentage values
        print("\nTickers with All Negative % Movements:")

        # Check if formatted_negative_tickers has data
        if formatted_negative_tickers.strip() and not formatted_negative_tickers.startswith("Empty"):
            print(formatted_negative_tickers)
        else:
            print("None")

    def print_unfiltered_data(self):
        # Format the top n tickers from unfiltered data as a table
        formatted_table_unfiltered = (
            self.top_tickers[['Ranking', 'Ticker', '1 Day %', '1 Month %', '1 Year %']]
            .to_string(index=False, justify='center', col_space=[10, 10, 18, 18, 18], formatters={'1 Day %': '{:.2f}'.format, '1 Month %': '{:.2f}'.format, '1 Year %': '{:.2f}'.format})
        )
        # Print table for the top n tickers from unfiltered data
        print(f"\nTop {self.nprices} Tickers Available:")
        print(formatted_table_unfiltered)

    def analysis(self):
        self.read_watchlist()
        self.read_ticker_prices()
        self.filter_data()
        self.calculate_percentage_movements()
        self.sort_filtered_data()
        self.find_negative_tickers()
        self.process_unfiltered_data()
        self.print_filtered_data()
        self.print_negative_tickers()
        self.print_unfiltered_data()

    @classmethod
    def analyze(cls, ticker_list, prices, nprices=5):
        # Create an instance of PMA
        analyzer = cls(ticker_list, prices, nprices)
        analyzer.analysis()


if __name__ == "__main__":
    # Example
    PMA.analyze("ticker_list.csv", "ticker_prices.csv")