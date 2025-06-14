arrival_time_script

filtered_cad = filtered_cad.dropna(subset=['Call_Created_Time', 'Unit_OnScene_Time'])

duration = filtered_cad['Unit_OnScene_Time'] - filtered_cad['Call_Created_Time']

filtered_cad['Arrival_Time'] = duration.dt.total_seconds()/60

## Check for any negative durations

filtered_cad = filtered_cad[filtered_cad['Arrival_Time'] >= 0]

## Define a function to group 
def categorize_priority(priority):
    if pd.isna(priority):
        return 'Unknown'
    if priority <= 3:
        return 'High'
    if priority >= 4:
        return 'Low'

# Apply the function to create a new column
filtered_cad['Priority_Level'] = filtered_cad['Call_Priority'].apply(categorize_priority)
