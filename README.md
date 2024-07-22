# General
I initially was only focused on analyzing FTD data, but I've started adding little helper scripts in general.

### download_ftd_data.sh
A shell script to download the SEC zip files for FTD data. You can specify year and month ranges.

### outlier_ftd.py
Once you have an FTD data file, run analysis on the file to identify "spikes" of FTDs based on basic std. dev. analysis.

### shares_oustanding.py
A scraper to grab the shares outstanding (in thousands) of a list of specific tickers. Default list is ETFs for GME analysis.

## Getting Started
To attempt to make this as easy as possible, I have set this project up to use devcontainers, so you only have to install Docker and VSCode on your machine, and all other bits of software do not clutter up your operating system.

### Install Docker
[Download](https://www.docker.com/products/docker-desktop/) and install Docker Desktop for the type of machine you are using (Mac, Windows, etc.)

### Install VSCode
[Download](https://code.visualstudio.com/download) and install VSCode for the type of machine you are using (Mac, Windows, etc.)

### Install Git
[Download](https://git-scm.com/downloads) and install Git for your machine (see a trend)?

### Clone the git repository
- Open a terminal/command prompt on your computer (Windows command, Mac terminal, etc.)
```
git clone https://github.com/modalblunder/ftd-analysis.git
```
- This will create a new directory named "ftd-analysis" at the current working directory
- Remember this location, you need to know it for the next step

### Open the repository in VSCode
- There are a few ways to do this but for the gui users:
    - Open VS Code
    - Select "File->Open Folder"
    - Find the "ftd-analysis" folder we cloned from git
    - Open the folder
- VS Code should notify you that it detects "Folder contains a Dev Container configuration..."
- Go ahead and click on the button to "Open in Dev Container" (or "Reopen...")
- The first time will take awhile, but this should be faster next time

### VSCode in the Dev Container
- Now you can run the scripts within VSCode
- In the menu bar, select "Terminal->New Terminal"
- Switch to pipenv shell, by running the following command in the terminal tab
```
pipenv shell
```
- Now you can run the python scripts as you desire. Example
```
python shares_outstanding.py
```

### I have to do all this every time? (NO!)
- Now you have the general environment setup, so next time all you have to do is the following
    - Open VSCode
    - Open the `ftd_analysis` folder
    - VSCode will prompt if you want to Reopen the DevContainer (yes!)
    - Open terminal and run the `pipenv shell` command to run python scripts

# Get Outstanding Shares Data (shares_oustanding.py)
By default, you can run this script without any parameters/arguments and it will grab data for the following ETF tickers: "XRT", "MDY", "FNDA", "IWB", "IWM", "IJH", "VTI", "VBR", "VXF". The output is in thousands.

Note: If you pass in the `--etf` flag, the scraping will be against tipranks.com, but it can only be used for etfs

```
python shares_oustanding.py --etf

XRT Shares Outstanding: 5000226
MDY Shares Outstanding: 41316202
FNDA Shares Outstanding: 127200000
IWB Shares Outstanding: 126150000
IWM Shares Outstanding: 284300000
IJH Shares Outstanding: 267000000
VTI Shares Outstanding: 1383502709
VBR Shares Outstanding: 150493560
VXF Shares Outstanding: 100462953
```

You can also specify any tickers instead, without the `--etf` flag and this will scrape barcharts.com
```
python shares_oustanding.py GME MSFT
GME Shares Outstanding: 351217
MSFT Shares Outstanding: 7432306
```

# Downloading FTD Data Zips for a range (download_ftd_data.sh)
For noobz, this does NOT need python, so you can just run it without going into `pipenv shell`

Note that this is just a helper script to grab zip files. If you want to use this data with the outlier_ftd.py script, then there is some extra work to unzip the files and combine them into a single file. I may write a script, or modify this one, to do all that 'magic' at a later date.

Example, grab 2024-01 through 2024-06
```
./download_ftd_data.sh 2024 01 2024 06
```

The above will download to the current directory, but you can also specific a directory name to keep things organized
```
./download_ftd_data.sh 2024 01 2024 06 temp_zips
```

# Analyzing FTD Data (outlier_ftd.py)
Grabbing data for the past few years, from the SEC Fails-to-Deliver Data site, in order to analyze different stock symbols and their FTD volume.

## Data Set
I've included a sample data set that only contains recent data
- ***Start:*** 2024 - April

- ***End:*** 2024 - June (First Half)

I've also uploaded a larger aggregated dataset (ftd_merged_202012_2024061H.zip) you can [download from GDrive](https://drive.google.com/file/d/10360LRny4McciW89de708ce3_dv0YyEJ/view?usp=sharing)
- ***Start:*** 2020 - December
- ***End:*** 2024 - June (First Half)

> :warning: The data is raw merged from the sec.gov site. I've noticed is has discrepencies and errors, so be careful with results

# How to use
- Unzip the sample data
```
unzip recent_ftds.zip
```
- Install Python3 (search google)
    - Or run in the devcontainer
- Install the dependencies from pip
```
pipenv install
```
- Jump into pipenv shell
```
pipenv shell
```
- Run the python script
```
python outlier_ftd.py
```

Note you can specify a few arguments if you want to play around with it. Take a look at the source for explanation of what the args can do. Example:
```
python outlier_ftd.py --min_entries 100 --threshold 3
python outlier_ftd.py --threshold 2 --symbol GME
```
