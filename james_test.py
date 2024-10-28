from bs4 import BeautifulSoup
import pandas as pd

# Read the HTML content from the file
with open('HolderScan.com.html', 'r') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Find the div with the class "TokenListsTables_tokenListTitle__WUjhi" and text "Biggest Gainers"
div_title = soup.find('div', class_='TokenListsTables_tokenListTitle__WUjhi', string='Biggest Gainers')

if div_title:
    # Find the parent element of the title
    table_container = div_title.find_next_sibling('div', class_='TokenListsTables_tokenListContainer__Nxj16')

    if table_container:
        data = []
        headers = ['Token', 'Holders', '24h', '24h %', 'Network']

        # Find all the rows within the container
        rows = table_container.find_all('div', class_='TokenListsTables_tokenListTableRow__7Lmg9')

        for row in rows:
            token_name_div = row.find('div', class_='TokenListsTables_tokenTokenTicker__0jgix')
            token_name = token_name_div.get_text(strip=True) if token_name_div else ''

            holders_div = row.find('div', class_='TokenListsTables_tokenDataHolders___JBbT')
            holders = holders_div.get_text(strip=True) if holders_div else ''

            _24h_divs = row.find_all('div', class_='TokenListsTables_tokenDataPos__OCt9K')
            if len(_24h_divs) >= 2:
                _24h = _24h_divs[0].get_text(strip=True)
                _24h_percent = _24h_divs[1].get_text(strip=True)
            else:
                _24h = ''
                _24h_percent = ''

            network_div = row.find('div', class_='TokenListsTables_tokenData__eBxC8')
            network = network_div.get_text(strip=True) if network_div else ''

            row_data = [token_name, holders, _24h, _24h_percent, network]
            data.append(row_data)

        # Create a DataFrame from the extracted data
        df = pd.DataFrame(data, columns=headers)
        print(df)
    else:
        print("Table container not found.")
else:
    print("Table title not found.")