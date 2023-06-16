# PRICE MOVEMENT ANALYZER
## Video Demo: <"https://youtu.be/zVLs_OkWq3o">
## Description:

An example program for analysing asset prices. Its simplicity demonstrates how quickly tailored analysis models can be built in Python.

### **pma.py**

A class that calculates price movement percentages of tickers in a portfolio and ranks them by biggest daily movers. Tickers that have negative price movements over 1 day, 1 month, and 1 year periods are displayed separately for review. All ticker prices available (regardless of whether they are included in the portfolio) are sorted by daily movers and the top n returned.

NB: This is an example class. It feeds from csv files, not JSON requests. The analysis is as basic as possible; however it serves as a structural demonstration of how algorithmic trading might be included, based on analysis of price performance.

Use case: Compare the top tickers available against the bottom tickers within a portfolio, to inform rebalancing decisions.

Technical details: The class is instantiated from method PMA.analyze, which contains 3 parameters. Argument 1: The ticker list file destination; Argument 2: The ticker price file destination; Argument 3 (optional): defaults to n ticker recommendations in the price analysis.

Unit tests: **test_pma.py** – testing instances and system output.

### **project.py**

Let's revisit the 80s and have some text on a screen as a UI. This module enables a user to:
1) Show all ticker items in their asset portfolio, sorted alphabetically;
2) Delete a ticker from the portfolio;
3) Add a ticker to the portfolio, if it exists in the pricing population.
4) Run the Price Movement Analyzer, which analyses the portfolio against the pricing population.
5) Have a one-sided conversation with the computer if exiting through the interface.

Technical details: I remember doing something like this for computer studies at school: a simple interface operated by key presses that enables the user to change data, run some analysis, and output reports.

Unit tests: **test_project.py** – testing mock input for the interface.

### **requirements.txt**

A list of required libraries.

### **ticker_list.csv and ticker_prices.csv**

These are example data sources, comprising dummy data. Ideally, the data would be pre-processed.

### **Video**

See the demo at the above link.