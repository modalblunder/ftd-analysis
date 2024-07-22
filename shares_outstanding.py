import requests
import argparse
from bs4 import BeautifulSoup

def scrape_shares_outstanding(url, span_text):
    """Scrapes the shares outstanding value from a webpage with the given structure."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)

    # Parse the HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find first span that matches text
    shares_outstanding_span = soup.find('span', string=span_text)
    
    if shares_outstanding_span:
        # Find the next sibling span, which contains the number
        number_span = shares_outstanding_span.find_next_sibling('span')

        if number_span:
            # Extract and clean the number
            number_str = number_span.get_text(strip=True).replace(',', '')
            return int(number_str)
    
    return None

def scrape_multiple_symbols(base_url, span_text, symbols):
    """Scrapes shares outstanding for multiple symbols using the base URL."""

    results = {}
    for symbol in symbols:
        url = base_url.replace("[SYMBOL]", symbol)
        shares = scrape_shares_outstanding(url, span_text)
        results[symbol] = shares

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape shares outstanding for stock symbols.")
    parser.add_argument("--etf", action="store_true", help="Search specifically for ETF data against tipranks.com")
    parser.add_argument("symbols", nargs="*", help="List of stock symbols (optional)")
    args = parser.parse_args()

    if args.etf:
        base_url = "https://www.tipranks.com/etf/[SYMBOL]"
        span_text = "Shares Outstanding"
    else:
        base_url = "https://barchart.com/stocks/quotes/[SYMBOL]"
        span_text = "Shares Outstanding, K"

    if args.symbols:  # If symbols were provided on the command line
        symbols_to_lookup = args.symbols
    else:  # Use a default list if none are provided
        symbols_to_lookup = ["XRT", "MDY", "FNDA", "IWB", "IWM", "IJH", "VTI", "VBR", "VXF"]

    shares_data = scrape_multiple_symbols(base_url, span_text, symbols_to_lookup)

    for symbol, shares in shares_data.items():
        if shares:
            share_output =  shares if args.etf else shares * 1000
            print(f"{symbol} Shares Outstanding: {share_output}")
        else:
            print(f"{symbol} Shares Outstanding not found")
