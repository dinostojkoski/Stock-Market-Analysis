# Stock Market Analysis Application

## Project Description

The Stock Market Analysis Application is a Python-based application that automates the retrieval, filtering, and saving of historical stock market data for companies listed on the Macedonian Stock Exchange (MSE). The application uses web scraping techniques to collect stock data for various issuers (companies) and processes it to filter out entries with no transaction volume, ensuring the final dataset only includes meaningful stock transactions. The cleaned data is saved into a CSV file for further analysis or reporting.

The application is designed to handle large datasets by fetching historical stock data for up to the past 12 years. It can append new data for issuers based on missing records and save the results in a specified directory. The system makes use of Python libraries like `requests`, `BeautifulSoup`, and `pandas` to fetch and process the data.

## Functional Requirements

### 1. Fetch Stock Data
   - **Description:** The system should be able to fetch historical stock data for specific issuers from the Macedonian Stock Exchange's website.
   - **Input:** Issuer codes (a list of stock symbols for various companies), start date, end date.
   - **Output:** A table with historical stock data, including transaction price, quantity, and turnover details.

### 2. **Filter Stock Data**
   - **Description:** The system should filter out rows where the quantity of stock transactions is zero (i.e., no transaction occurred for that day).
   - **Input:** Raw stock data.
   - **Output:** Cleaned stock data that only includes transactions with a quantity greater than zero.

### 3. **Save Filtered Data**
   - **Description:** After filtering, the cleaned stock data should be saved in a CSV file located in the `filtered_stock_data.csv` directory.
   - **Input:** Filtered stock data.
   - **Output:** A CSV file containing the filtered stock data, saved to the specified directory.

### 4. **Append New Data**
   - **Description:** If new stock data is available (i.e., data for a missing period), it should be appended to the existing dataset without duplicating previously fetched data.
   - **Input:** Newly fetched stock data for missing periods.
   - **Output:** Updated CSV file with appended data.

## Non-Functional Requirements

### 1. **Performance**
   - The application should be able to handle the retrieval and processing of large datasets (up to 12 years of stock data) efficiently.
   - It should ensure that the filtering and data saving operations are performed within a reasonable time frame.

### 2. **Usability**
   - The application should be simple to run. A user only needs to execute the script, and the application will automatically handle fetching, filtering, and saving the data.

### 3. **Scalability**
   - The application should be easily extendable to support additional features, such as fetching data for more issuers or integrating with databases for persistent storage.

### 4. **Error Handling**
   - The application should gracefully handle errors, such as failed network requests or missing files, and provide meaningful error messages.

### 5. **Data Integrity**
   - The application should ensure the integrity of the data, especially when appending new data to the CSV. Duplicate entries should be avoided.

## User Scenarios

### Scenario 1: **Investor Fetching Stock Data**
   **Persona:** Mark, an investor, is interested in tracking the stock performance of Macedonian companies.  
   **Goal:** Mark needs up-to-date historical data to analyze and make investment decisions.  
   **Process:** Mark runs the script, which fetches the latest data for companies he's interested in, cleans up any irrelevant data, and saves it to a CSV file for analysis. Mark can then open the file in Excel or a similar tool to conduct his analysis.

### Scenario 2: **Data Analyst Updating Existing Data**
   **Persona:** Lisa, a data analyst at a financial firm, is maintaining a stock database.  
   **Goal:** Lisa needs to update the existing stock dataset with new data for the past week.  
   **Process:** Lisa runs the script, which checks for missing data for the issuers in the existing dataset. The script fetches the missing data and appends it to the file, ensuring no duplicates. Lisa can then use the updated data for further analysis or reporting.

### Scenario 3: **Administrator Managing Data Files**
   **Persona:** John, an administrator, is responsible for ensuring that the stock data is stored properly.  
   **Goal:** John wants to ensure that the application saves data to the correct location and organizes the data in a structured directory.  
   **Process:** John configures the application to save the filtered stock data to the `filtered_stock_data.csv` file. The application automatically creates the required directories if they do not exist, and stores the data properly.

## Performance Metrics
The time taken to populate the database with the stock data is measured to track the efficiency of the application. The operation completed in 34.46 seconds, providing insight into the performance of the data fetching and processing system.

## Conclusion

This application offers an automated, efficient way to fetch, clean, and save historical stock data from the Macedonian Stock Exchange. It provides an easy-to-use solution for anyone needing clean stock data for analysis or reporting purposes, whether for investment purposes, financial analysis, or data archiving. By automating the process of fetching and cleaning stock data, users can focus on deriving insights from the data instead of spending time on manual data processing tasks.

## Contributors

 - Dino Stojkoski 211226
 - Hristijan Pumpaloski 221264
 - Filip Lokoski 221119
