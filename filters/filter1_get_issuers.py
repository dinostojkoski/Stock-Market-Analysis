import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def get_issuer_data(issuer_code, start, end):
    url = f'https://www.mse.mk/mk/stats/symbolhistory/{issuer_code}'
    payload = {
        'FromDate': start.strftime('%d.%m.%Y'),
        'ToDate': end.strftime('%d.%m.%Y'),
        'Code': issuer_code
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        column_headers = [
            'Date', 'Last Transaction Price', 'Max.', 'Min.', 'Average Price',
            '% Change', 'Quantity', 'Turnover in BEST in Denars', 'Total Turnover in Denars'
        ]
        table = soup.find('table')

        if table:
            data_rows = []
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if cells:
                    row_data = [cell.get_text(strip=True) for cell in cells]
                    row_data.insert(0, issuer_code)  # Prepend issuer code
                    data_rows.append(row_data)

            return pd.DataFrame(data_rows, columns=['Issuer Name'] + column_headers)
        else:
            print(f"Table not found for {issuer_code}.")
            return pd.DataFrame()
    else:
        print(f"Error fetching data for {issuer_code}. HTTP Status:", response.status_code)
        return pd.DataFrame()

# Define the time period for the stock data
today = datetime.now()
years_back = timedelta(days=365 * 12)
start_date = today - years_back

# List of issuer codes
issuer_codes = [
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

# Collect data for all issuers
complete_data = pd.DataFrame()

for i in range(12):
    period_start = start_date + timedelta(days=365 * i)
    period_end = period_start + timedelta(days=365)

    for issuer_code in issuer_codes:
        stock_data = get_issuer_data(issuer_code, period_start, period_end)
        complete_data = pd.concat([complete_data, stock_data], ignore_index=True)

# Save the collected data to a CSV file
complete_data.to_csv('stock_data_history.csv', index=False)
print("Data successfully saved to 'stock_data_history.csv'.")
