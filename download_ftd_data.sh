#!/bin/zsh

# Check for correct number of arguments (either 4 or 5)
if [[ $# -lt 4 || $# -gt 5 ]]; then
    echo "Usage: $0 start_year start_month end_year end_month [destination_folder]"
    exit 1
fi

# Get parameters from command-line arguments
start_year=$1
start_month=$2
end_year=$3
end_month=$4

# Set destination_folder to "." if not provided
if [[ $# -eq 4 ]]; then
    destination_folder="."
else
    destination_folder=$5
fi

# Check if destination folder exists and create if necessary
if [[ ! -d $destination_folder ]]; then
    echo "Destination folder '$destination_folder' does not exist. Creating it..."
    mkdir -p "$destination_folder" || { 
        echo "Error: Could not create destination folder."
        exit 1
    }
fi

# Basic input validation
for arg in start_year start_month end_year end_month; do
    if [[ ! ${(P)arg} =~ ^[0-9]+$ ]]; then   # Use (P) for parameter expansion
        echo "Error: Invalid input for $arg. Please provide a number."
        exit 1
    fi
done

# Validate date range
if [[ $start_year -gt $end_year || ($start_year -eq $end_year && $start_month -gt $end_month) ]]; then
    echo "Error: Invalid date range. Start date must be before or equal to end date."
    exit 1
fi

current_year=$start_year
current_month=$start_month

while [[ $current_year -le $end_year ]]; do
    while [[ $current_month -le 12 ]]; do
        if [[ $current_year -eq $end_year && $current_month -gt $end_month ]]; then
            break  # Reached end of desired date range
        fi

        for file_type in a b; do
            # TODO: Might want to add a random sleep as you don't want to hammer the site
            # sleep_duration=$(( ($RANDOM % 2) + 1 ))
            # sleep $sleep_duration
            # cnsfails201502b.zip is the format
            filename="cnsfails${current_year}$(printf "%02d" $current_month)$file_type.zip"

            # Change URL based on date
            if [[ ($current_year -eq 2020 && $current_month -ge 2 && $current_month -le 4 ) ]]; then
                url="https://www.sec.gov/files/node/add/data_distribution/$filename"
            elif [[ $current_year -gt 2017 || 
                    ($current_year -eq 2017 && $current_month -gt 6) ||
                    ($current_year -eq 2017 && $current_month -eq 6 && $file_type == "b") ]]; then
                url="https://www.sec.gov/files/data/fails-deliver-data/$filename"
            else
                url="https://www.sec.gov/files/data/frequently-requested-foia-document-fails-deliver-data/$filename"
            fi

            # Using a distinct user agent because...SEC blocks wget (kinda against terms o.O)
            wget -P "$destination_folder" --user-agent="Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0" "$url"
        done

        ((current_month++))
    done

    ((current_year++))
    current_month=1  # Reset to January for next year
done
