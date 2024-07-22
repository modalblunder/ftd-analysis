import pandas as pd
import argparse

SDATE_TEXT = 'SETTLEMENT DATE'
SYMBOL_TEXT = 'SYMBOL'
QF_TEXT = 'QUANTITY (FAILS)'

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Calculate and save mean 'QUANTITY (FAILS)' by SYMBOL.")
    parser.add_argument("--threshold", default=2.0, help="Threshold as std deviations from mean (above only)")
    parser.add_argument("--input", default='ftd_merged.txt.nogit', help="Name of the input FTD file (default: ftd_merged.txt.nogit)")
    parser.add_argument("--output", default="ftd_outliers.csv.nogit", help="Name of the output file to save the results.")
    parser.add_argument("--nofill", action="store_true", help="Enable nofill mode")
    parser.add_argument("--min_entries", type=int, default=50, help="Minimum number of entries required for a symbol to be included (default: 10)")
    parser.add_argument("--symbol", help="Optional: Specify a symbol to filter results.")
    parser.add_argument("--start", help="A start date using the ftd data format YYYYMMDD.")
    parser.add_argument("--end", help="An end date using the ftd dta format YYYYMMDD.")
    args = parser.parse_args()

    # Load the data
    df = pd.read_csv(args.input, delimiter='|', encoding='unicode_escape')
    df[SDATE_TEXT] = pd.to_datetime(df[SDATE_TEXT], format='%Y%m%d')

    if args.start:
        start_date = pd.to_datetime(args.start, format='%Y%m%d')
        df = df[df[SDATE_TEXT] >= start_date]

    if args.end:
        end_date = pd.to_datetime(args.end, format='%Y%m%d')
        df = df[df[SDATE_TEXT] <= end_date]

    # TODO: Either fix the underlying data or come up with more elegant approach
    df = df.drop_duplicates(subset=[SDATE_TEXT, SYMBOL_TEXT])

    # get symbol counts before we fill zeros
    symbol_counts = df[SYMBOL_TEXT].value_counts()

    # For any combinations of SETTLEMENT DATE and SYMBOL we are missing, let's assume ZERO
    # TODO: Correct logic should only include zeros for entries newer than the oldest entry, per ticker
    if args.nofill:
        print("Nofill mode enabled!")
        # Your code for the nofill scenario here
    else:
        print("Fill mode enabled. Proceeding normally, filling in zeros.")
        # Your code for the default scenario here
        all_combinations = pd.MultiIndex.from_product([df[SDATE_TEXT].unique(), df[SYMBOL_TEXT].unique()],
                                                names=[SDATE_TEXT, SYMBOL_TEXT])
        df = df.set_index([SDATE_TEXT, SYMBOL_TEXT]).reindex(all_combinations, fill_value=0).reset_index()

    # Filter based on symbol if provided
    if args.symbol:
        filtered_df = df[df[SYMBOL_TEXT] == args.symbol].copy()
    else:
        # If no ticker is specified we are going to trim out tickers that only have min_entries
        symbol_counts = df[SYMBOL_TEXT].value_counts()
        valid_symbols = symbol_counts[symbol_counts >= args.min_entries].index
        filtered_df = df[df[SYMBOL_TEXT].isin(valid_symbols)].copy()
    
    # Convert 'QUANTITY (FAILS)' to numeric for calculations
    filtered_df[QF_TEXT] = pd.to_numeric(filtered_df[QF_TEXT], errors='coerce')

    # Group by 'SYMBOL' and calculate mean and standard deviation
    symbol_stats = filtered_df.groupby(SYMBOL_TEXT)[QF_TEXT].agg(['mean', 'std'])

    # Merge statistics back to the original DataFrame
    filtered_df = filtered_df.merge(symbol_stats, on=SYMBOL_TEXT)

    # Filter rows where 'QUANTITY (FAILS)' is more than threshold standard deviations above the mean
    user_input_float = float(args.threshold)
    outliers = filtered_df[filtered_df[QF_TEXT] > (filtered_df['mean'] + user_input_float * filtered_df['std'])]

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

