van_avail_script

import pandas as pd
import numpy as np


# Sort by call time to make processing easier
filtered_cad = filtered_cad.sort_values('Call_Created_Time').reset_index(drop=True)

call_times = filtered_cad['Call_Created_Time'].values
cleared_times = filtered_cad['Unit_Cleared_Time'].values

van_available = np.ones(len(filtered_cad), dtype=bool)

# Use two pointers to efficiently count active units at each call time
j = 0  # pointer for cleared times

for i in range(len(filtered_cad)):
    now = call_times[i]
    
    # Move j forward while cleared_times[j] <= now (units cleared before or at now)
    while j < len(filtered_cad) and cleared_times[j] <= now:
        j += 1
    
    # Active units are those with cleared_times > now and call_times before now (all calls before i)
    # Active units count = i - j
    active_units = i - j
    
    van_available[i] = active_units < 2

filtered_cad['Van_Available'] = van_available

# Drop rows with missing values in key columns
t_data = filtered_cad.dropna(subset=['Arrival_Time', 'Van_Available'])

# Split into two groups based on Van_Available being True or False
available = t_data[t_data['Van_Available'] == True]['Arrival_Time']
not_available = t_data[t_data['Van_Available'] == False]['Arrival_Time']

# Drop rows with missing values in key columns
t_data = filtered_cad.dropna(subset=['Arrival_Time', 'Van_Available'])

# Split into two groups based on Van_Available being True or False
available = t_data[t_data['Van_Available'] == True]['Arrival_Time']
not_available = t_data[t_data['Van_Available'] == False]['Arrival_Time']
