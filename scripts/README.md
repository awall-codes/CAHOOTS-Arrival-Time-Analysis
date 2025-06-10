## Data Prepping Scripts

These scripts are used for the data prepping process for analyzing the Eugene Police Department (PD) CAD dataset from 2014–2022.

### Dependencies

The data cleaning process relies on the following Python packages:

- `numpy`
- `pandas`
- `datetime`

### Dataset

The dataset can be accessed via the Eugene PD CAD dataset (2014–2022). Instructions on how to obtain and prepare this data are included in the first script.

### Steps to Run the Data Prepping Scripts

1. **[data_prep.py](./scripts/data_prep.py)**  
   This script contains instructions on how to download and clean the raw CSV data.

2. **[arrival_time.py](./scripts/arrival_time.py)**  
   Calculates officer arrival times and categorizes priority levels in the CAD dataset.

3. **[van_avail.py](./scripts/van_avail.py)**  
   Determines CAHOOTS van availability at the time each call comes in.

## Next Steps

Once these scripts have been run and the datasets have been processed, you can proceed with your data analysis.
