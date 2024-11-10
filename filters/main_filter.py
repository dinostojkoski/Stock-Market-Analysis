import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time


def get_stock_data_for_issuer(issuer_code, start_date, end_date):
    base_url = 'https://www.mse.mk/mk/stats/symbolhistory/' + issuer_code
    payload = {
        'FromDate': start_date.strftime('%d.%m.%Y'),
        'ToDate': end_date.strftime('%d.%m.%Y'),
        'Code': issuer_code
    }

    response = requests.post(base_url, data=payload)

    if response.status_code == 200:
        page_content = BeautifulSoup(response.text, 'html.parser')
        column_names = [
            'Date', 'Last Transaction Price', 'Max.', 'Min.',
            'Average Price', '% Change', 'Quantity',
            'Turnover in BEST in Denars', 'Total Turnover in Denars'
        ]
        table = page_content.find('table')

        if table:
            rows = []
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if cells:
                    row_values = [cell.get_text(strip=True) for cell in cells]
                    row_values.insert(0, issuer_code)  # Add issuer code at the start
                    rows.append(row_values)

            return pd.DataFrame(rows, columns=['Issuer Name'] + column_names)
        else:
            print(f"No table found for {issuer_code}.")
            return pd.DataFrame()
    else:
        print(f"Failed to retrieve data for {issuer_code}. Status code: {response.status_code}")
        return pd.DataFrame()


def fetch_and_process_missing_data():
    input_file = 'filtered_stock_data.csv'
    try:
        stock_data = pd.read_csv(input_file, parse_dates=['Date'], dayfirst=True)
        print("Loaded existing data successfully.")
    except FileNotFoundError:
        stock_data = pd.DataFrame()
        print("No data found. Initiating fetch for the last 12 years of data.")

    issuers = [
        "ADIN", "ALK", "CKB", "DEBA", "DIMI", "EUHA", "EVRO", "FAKM", "FERS",
        "FUBT", "GALE", "GECK", "GECT", "GIMS", "GRNT", "GRZD", "GTC", "GTRG",
        "INB", "KARO", "KDFO", "KJUBI", "KLST", "KMB", "KOMU", "KONF", "KONZ",
        "KPSS", "KVAS", "LOTO", "LOZP", "MAKP", "MAKS", "MB", "MERM", "MKSD",
        "MPOL", "MPT", "MTUR", "MZPU", "NEME", "NOSK", "OKTA", "OTEK", "PKB",
        "POPK", "PPIV", "PROD", "RADE", "REPL", "RZTK", "RZUG", "RZUS", "SBT",
        "SDOM", "SIL", "SKP", "SLAV", "SOLN", "SPAZ", "SPAZP", "STB", "STBP",
        "STIL", "STOK", "TAJM", "TEAL", "TEHN", "TEL", "TETE", "TIKV", "TKPR",
        "TKVS", "TNB", "TRDB", "TRPS", "TSMP", "TTK", "UNI", "USJE", "VITA",
        "VROS", "VTKS", "ZAS", "ZILU", "ZILUP", "ZIMS", "ZKAR", "ZPKO", "OMOS"
    ]

    all_data = pd.DataFrame()
    current_date = datetime.now()

    for issuer in issuers:
        if not stock_data.empty and issuer in stock_data['Issuer Name'].values:
            issuer_data = stock_data[stock_data['Issuer Name'] == issuer]
            latest_date = issuer_data['Date'].max()
            print(f"Most recent data for {issuer} is from {latest_date.strftime('%d.%m.%Y')}")

            if latest_date < current_date - timedelta(days=1):
                start_date = latest_date + timedelta(days=1)
                print(f"Fetching missing data for {issuer} from {start_date.strftime('%d.%m.%Y')} to {current_date.strftime('%d.%m.%Y')}")
                new_data = get_stock_data_for_issuer(issuer, start_date, current_date)
                all_data = pd.concat([all_data, new_data], ignore_index=True)
            else:
                print(f"No missing data for {issuer}.")
        else:
            start_date = current_date - timedelta(days=365 * 12)
            print(f"No prior data for {issuer}. Fetching data from {start_date.strftime('%d.%m.%Y')} to {current_date.strftime('%d.%m.%Y')}")
            new_data = get_stock_data_for_issuer(issuer, start_date, current_date)
            all_data = pd.concat([all_data, new_data], ignore_index=True)

    if not all_data.empty:
        clean_and_save_stock_data(all_data)


def clean_and_save_stock_data(new_data, output_file='filtered_stock_data.csv'):
    cleaned_data = new_data[new_data['Quantity'] != '0']
    if not cleaned_data.empty:
        cleaned_data.to_csv(output_file, mode='a', index=False, header=not pd.io.common.file_exists(output_file))
        print(f"Filtered data appended to '{output_file}'.")
    else:
        print("No filtered data to append.")


def execute():
    start = time.time()  # Start time tracking

    fetch_and_process_missing_data()

    end = time.time()  # End time tracking
    elapsed = end - start
    print(f"Total execution time: {elapsed:.2f} seconds")


if __name__ == "__main__":
    execute()
