## Data Prepping Scripts

These scripts are used for the data prepping process for analyzing the Eugene Police Department CAD dataset from 2014–2022.

### Packages Used

The data cleaning process relies on the following Python packages:

- `numpy`
- `pandas`
- `datetime`

### Dataset

The dataset can be accessed via the Eugene PD CAD dataset (2014–2022). This data can be accessed through requests to the police department although is not able to be linked in this GitHub. 

### Steps to Run the Data Prepping Scripts

1. **[data_prep.py](./data_prep.py)**  
   This script contains instructions on how to download and clean the raw CSV data.

2. **[arrival_time.py](./arrival_time.py)**  
   Calculates officer arrival times and categorizes priority levels in the CAD dataset.

3. **[van_avail.py](./van_avail.py)**  
   Determines CAHOOTS van availability at the time each call comes in.

## Next Steps

Once these scripts have been run and the datasets have been processed, you can proceed with your data analysis.
