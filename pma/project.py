import sys  # Accept arguments from the command line
import csv  # Validate csv files
from art import text2art  # Make terminal outputs retro pretty
from pma import PMA  # Price Movement Analyzer

""""
# PRICE MOVEMENT ANALYZER

### **project.py**

Let's revisit the 80s and have some text on a screen as a UI. This module enables a user to:
1) Show all ticker items in their asset portfolio, sorted alphabetically;
2) Delete a ticker from the portfolio;
3) Add a ticker to the portfolio, if it exists in the pricing population.
4) Run the Price Movement Analyzer, which analyses the portfolio against the pricing population.
5) Have a one-sided conversation with the computer if exiting through the interface.

Technical details:
I remember doing something like this for computer studies at school: a simple interface operated by key presses that enables the user to 
change data, run some analysis, and output reports.
    
"""

def main():
    show_credits()
    
    list_file, prices_file = get_file_names()
   
    while True:
        try:
            choice = get_user_input()
            if int(choice) == 1:
                show_ticker_list(list_file)
            elif int(choice) == 2:
                delete_ticker(list_file)
            elif int(choice) == 3:
                add_ticker(list_file, prices_file)
            elif int(choice) == 4:
                PMA.analyze(list_file, prices_file)
            elif int(choice) == 5:
                if input("Are you sure you want to exit? (y/n) ").lower() == "y":
                    ok_computer = input("Are you REALLY sure you want to exit!? (y/n) ").strip().lower()
                    if ok_computer == "y":
                        print("Please don't go, you'll hurt my feelings. Never mind, here are all the options again...")
                    elif ok_computer == "open the pod bay doors":
                        break
        except KeyboardInterrupt:
            print("\nCtrl+C detected. Exiting...")
            sys.exit(0)            


def show_credits():
    print(text2art("Price  Movement  Analyzer"))
    print(text2art("(or  back  to  the  1980s)"))
    print(text2art("By  Robert  Walker,  London,  UK"))
    print(text2art("(aged  something  and  a  half)"))
    

def get_file_names():
    # Defaults
    list_file = "ticker_list.csv"
    prices_file = "ticker_prices.csv"

    # Override defaults if applicable
    if len(sys.argv) > 1: # If arguments exist
        if len(sys.argv) >= 2:
            list_file = sys.argv[1]
        if len(sys.argv) >= 3:
            prices_file = sys.argv[2]

    return list_file, prices_file


def get_user_input():
    while True:
        print("\n1. Show ticker list")
        print("2. Delete ticker")
        print("3. Add ticker")
        print("4. Analysis")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice.isdigit() and 1 <= int(choice) <= 5:
            return int(choice)
        else:
            print("Invalid choice. Please try again.")


def show_ticker_list(list_file):
    try:
        with open(list_file, "r") as file:
            print("\nTicker List:")
            reader = csv.reader(file)
            next(reader)  # Skip header row
            ticker_list = [row[0] for row in reader]
            sorted_ticker_list = sorted(ticker_list)
            for ticker in sorted_ticker_list:
                print(ticker)

    except Exception as e:
        handle_error(e, list_file)


def delete_ticker(list_file):
    ticker = input("Enter the ticker to delete: ")
    lines = []
    ticker_exists = False

    try:
        with open(list_file, "r") as file:
            reader = csv.reader(file)
            header = next(reader)  # Read and store the header row
            for row in reader:
                if row[0] == ticker:
                    ticker_exists = True
                else:
                    lines.append(row)

        if ticker_exists:
            with open(list_file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(header)  # Write the header row back
                writer.writerows(lines)
            print(f"The ticker {ticker} has been deleted.")
        else:
            print(f"No ticker has been deleted because {ticker} doesn't exist in the list.")

    except Exception as e:
        handle_error(e, list_file)


def add_ticker(list_file, prices_file):
    ticker = input("Enter the ticker to add: ")
    
    try:
        # Check that ticker exists in the price file
        with open(prices_file, "r") as file:
            reader = csv.DictReader(file)
            tickers = [row["Ticker"] for row in reader]

        if ticker in tickers:  # Found            
            try:
                with open(list_file, "a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([ticker, 1]) # Type_Id is a placeholder column, so default to 1 until live
                print(f"The ticker {ticker} has been added.")
            
            except Exception as e:
                handle_error(e, prices_file)
        else:
            print(f"The ticker does not exist in {prices_file}. Please try again.")

    except Exception as e:
        handle_error(e, list_file)


def handle_error(exception, filename):
    if isinstance(exception, FileNotFoundError):
        print(f"{filename} file not found.")
    elif isinstance(exception, PermissionError):
        print("Permission denied to access {filename} file.")
    else:
        print(f"An error occurred: {str(exception)}")


if __name__ == "__main__":
    main()