import pandas as pd
import argparse

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Calculate and save mean 'QUANTITY (FAILS)' by SYMBOL.")
    parser.add_argument("--threshold", default=2.0, help="Threshold as std deviations from mean (above only)")
    parser.add_argument("--input", default='ftd_merged.txt.nogit', help="Name of the input FTD file (default: ftd_merged.txt.nogit)")
    parser.add_argument("--output", default="ftd_outliers.csv.nogit", help="Name of the output file to save the results.")
    parser.add_argument("--min_entries", type=int, default=10, help="Minimum number of entries required for a symbol to be included (default: 10)")
    parser.add_argument("--symbol", help="Optional: Specify a symbol to filter results.")
    args = parser.parse_args()

    # Load the data
    df = pd.read_csv(args.input, delimiter='|', encoding='unicode_escape')

    # Filter based on symbol if provided
    if args.symbol:
        filtered_df = df[df['SYMBOL'] == args.symbol].copy()
    else:
        # If no ticker is specified we are going to trim out tickers that only have min_entries
        symbol_counts = df['SYMBOL'].value_counts()
        valid_symbols = symbol_counts[symbol_counts >= args.min_entries].index
        filtered_df = df[df['SYMBOL'].isin(valid_symbols)].copy()

    # Convert 'QUANTITY (FAILS)' to numeric for calculations
    filtered_df['QUANTITY (FAILS)'] = pd.to_numeric(filtered_df['QUANTITY (FAILS)'], errors='coerce')

    # Group by 'SYMBOL' and calculate mean and standard deviation
    symbol_stats = filtered_df.groupby('SYMBOL')['QUANTITY (FAILS)'].agg(['mean', 'std'])

    # Merge statistics back to the original DataFrame
    filtered_df = filtered_df.merge(symbol_stats, on='SYMBOL')

    # Filter rows where 'QUANTITY (FAILS)' is more than threshold standard deviations above the mean
    user_input_float = float(args.threshold)
    outliers = filtered_df[filtered_df['QUANTITY (FAILS)'] > (filtered_df['mean'] + user_input_float * filtered_df['std'])]

    # Display rows that are outliers
    if outliers.empty:
        print("No outliers found.")
    else:
        print(f"Outliers of 'QUANTITY (FAILS)' above {args.threshold} std deviations saved to {args.output}")
        outliers.to_csv(args.output, index=False)
        print("Sample Data:")
        print(outliers)

if __name__ == "__main__":
    main()

