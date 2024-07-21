import requests
import argparse
from bs4 import BeautifulSoup

def scrape_shares_outstanding(url):
    """Scrapes the shares outstanding value from a webpage with the given structure."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)

    # Parse the HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the relevant <li> element using CSS selectors
    target_li = soup.select_one('li span.left:-soup-contains("Shares Outstanding, K") ~ span.right')
    if target_li:
        # Extract and clean the number
        shares_str = target_li.get_text(strip=True).replace(',', '')  # Remove commas
        shares_outstanding = int(shares_str) if shares_str.isdigit() else None
        return shares_outstanding
    else:
        return None

def scrape_multiple_symbols(base_url, symbols):
    """Scrapes shares outstanding for multiple symbols using the base URL."""

    results = {}
    for symbol in symbols:
        url = base_url.replace("[SYMBOL]", symbol)
        shares = scrape_shares_outstanding(url)
        results[symbol] = shares

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape shares outstanding for stock symbols.")
    parser.add_argument("symbols", nargs="*", help="List of stock symbols (optional)")
    args = parser.parse_args()

    base_url = "https://barchart.com/stocks/quotes/[SYMBOL]"

    if args.symbols:  # If symbols were provided on the command line
        symbols_to_lookup = args.symbols
    else:  # Use a default list if none are provided
        symbols_to_lookup = ["XRT", "MDY", "FNDA", "IWB", "IWM", "IJH", "VTI", "VBR", "VXF"]

    shares_data = scrape_multiple_symbols(base_url, symbols_to_lookup)

    for symbol, shares in shares_data.items():
        if shares:
            print(f"{symbol} Shares Outstanding: {shares}")
        else:
            print(f"{symbol} Shares Outstanding not found")
