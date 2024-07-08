# Analyzing FTD Data
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