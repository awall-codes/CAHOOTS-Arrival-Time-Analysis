## script for data cleaning
## First loading in the CAD data
cad = pd.read_csv("call_data_from_CAD.csv")

## then doing the columns that we want
filtered_columns = [
    "Call_Created_Time", 
    "Call_First_Dispatched_Time", 
    "Call_Cleared", 
    "Call_Priority", 
    "Unit_Dispatched_Time", 
    "Unit_OnScene_Time", 
    "Unit_Cleared_Time",
    "InitialIncidentTypeDescription", 
]

cahoots_pattern = r"\b(1J77|3J79|3J78|4J79|3J81|3J76|2J28|2J29|CAHOOT|CAHOT|CAHO)\b"

# Filter the DataFrame for the regex pattern

filtered_data = cad[
    cad['RespondingUnitCallSign'].fillna('').apply(lambda x: bool(re.match(cahoots_pattern, x)))
]

filtered_cad = filtered_data[filtered_columns]
filtered_cad = filtered_cad.dropna()

# For the sake of analysis, since P is not less important, going to drop it

filtered_cad = filtered_cad[filtered_cad['Call_Priority'] != 'P']

# Ensure they are set as integers

filtered_cad['Call_Priority'] = filtered_cad['Call_Priority'].astype(int)



## converting to a datetime format
time_columns = [
    'Call_Created_Time', 
    'Call_First_Dispatched_Time',
    'Call_Cleared',
    'Unit_Dispatched_Time', 
    'Unit_OnScene_Time', 
    'Unit_Cleared_Time',
]

# Convert columns to datetime

for col in time_columns:
    filtered_cad[col] = pd.to_datetime(filtered_cad[col], format='%m/%d/%y %H:%M')



