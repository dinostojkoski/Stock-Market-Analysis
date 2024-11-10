import pandas as pd
from datetime import datetime, timedelta

# File path for input data
data_file = 'filtered_stock_data.csv'

try:
    stock_data = pd.read_csv(data_file, parse_dates=['Date'], dayfirst=True)
    print("Data successfully loaded from the existing file.")
except FileNotFoundError:
    stock_data = pd.DataFrame()
    print("No prior data found. Proceeding to fetch new data for the past 12 years.")

# List of issuer symbols
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

# Iterate over each issuer and check if additional data is needed
for issuer in issuers:
    if not stock_data.empty and issuer in stock_data['Issuer Name'].values:
        # Retrieve data specific to the issuer
        issuer_data = stock_data[stock_data['Issuer Name'] == issuer]
        most_recent_date = issuer_data['Date'].max()
        print(f"Most recent date for {issuer}: {most_recent_date.strftime('%d.%m.%Y')}")

        # Check if additional data is needed
        if most_recent_date < datetime.now() - timedelta(days=365 * 10):
            print(f"Fetching data for {issuer} from {most_recent_date + timedelta(days=1)} onwards.")
        else:
            print(f"No additional data needed for {issuer}.")
    else:
        # Data does not exist for the issuer, fetch new data
        start_fetch_date = datetime.now() - timedelta(days=365 * 12)
        print(f"No data for {issuer}. Fetching from {start_fetch_date.strftime('%d.%m.%Y')}.")
