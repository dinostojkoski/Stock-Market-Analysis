import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time


def get_stock_data_for_today():
    def retrieve_data_for_issuer(issuer_code, start_date, end_date):
        url = f'https://www.mse.mk/mk/stats/symbolhistory/{issuer_code}'
        params = {
            'FromDate': start_date.strftime('%d.%m.%Y'),
            'ToDate': end_date.strftime('%d.%m.%Y'),
            'Code': issuer_code
        }

        response = requests.post(url, data=params)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            columns = [
                'Date', 'Last Transaction Price', 'Max.', 'Min.',
                'Average Price', '% Change', 'Quantity',
                'Turnover in BEST in Denars', 'Total Turnover in Denars'
            ]
            table = soup.find('table')

            if table:
                rows = []
                for row in table.find_all('tr'):
                    cells = row.find_all('td')
                    if cells:
                        row_data = [cell.get_text(strip=True) for cell in cells]
                        row_data.insert(0, issuer_code)  # Insert issuer code as the first column
                        rows.append(row_data)

                stock_df = pd.DataFrame(rows, columns=['Issuer Name'] + columns)
                return stock_df
            else:
                print(f"Table not found for {issuer_code}.")
                return pd.DataFrame()
        else:
            print(f"Error fetching data for {issuer_code}. HTTP Status Code: {response.status_code}")
            return pd.DataFrame()

    current_time = datetime.now()
    end_date = current_time
    start_date = current_time

    issuers = [
        "ADIN", "ALK", "CKB", "DEBA", "DIMI", "EUHA", "EVRO", "FAKM", "FERS", "FUBT",
        "GALE", "GECK", "GECT", "GIMS", "GRNT", "GRZD", "GTC", "GTRG", "INB", "KARO",
        "KDFO", "KJUBI", "KLST", "KMB", "KOMU", "KONF", "KONZ", "KPSS", "KVAS", "LOTO",
        "LOZP", "MAKP", "MAKS", "MB", "MERM", "MKSD", "MPOL", "MPT", "MTUR", "MZPU",
        "NEME", "NOSK", "OKTA", "OTEK", "PKB", "POPK", "PPIV", "PROD", "RADE", "REPL",
        "RZTK", "RZUG", "RZUS", "SBT", "SDOM", "SIL", "SKP", "SLAV", "SOLN", "SPAZ",
        "SPAZP", "STB", "STBP", "STIL", "STOK", "TAJM", "TEAL", "TEHN", "TEL", "TETE",
        "TIKV", "TKPR", "TKVS", "TNB", "TRDB", "TRPS", "TSMP", "TTK", "UNI", "USJE",
        "VITA", "VROS", "VTKS", "ZAS", "ZILU", "ZILUP", "ZIMS", "ZKAR", "ZPKO"
    ]

    combined_data = pd.DataFrame()

    start_timer = time.time()

    for issuer in issuers:
        issuer_data = retrieve_data_for_issuer(issuer, start_date, end_date)
        combined_data = pd.concat([combined_data, issuer_data], ignore_index=True)

    if not combined_data.empty:
        combined_data.to_csv('stock_data_today.csv', index=False)
        print("Data for today has been written to 'stock_data_today.csv'.")
    else:
        print("No data fetched for today.")

    end_timer = time.time()
    elapsed_duration = end_timer - start_timer
    print(f"Time taken to fetch and save the data: {elapsed_duration:.2f} seconds.")


def filter_and_save_today_stock_data(input_file='stock_data_today.csv', output_file='filtered_stock_data.csv'):
    stock_df = pd.read_csv(input_file)

    filtered_stock_df = stock_df[stock_df['Quantity'] != 0]

    if not filtered_stock_df.empty:
        filtered_stock_df.to_csv(output_file, mode='a', index=False, header=not pd.io.common.file_exists(output_file))
        print(f"Filtered data has been appended to '{output_file}'.")
    else:
        print("No data to append.")


def run():
    get_stock_data_for_today()
    filter_and_save_today_stock_data()


if __name__ == "__main__":
    run()
