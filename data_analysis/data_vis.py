## Imports for the plots
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from matplotlib.patches import Rectangle


### PLOT 1 - FREQUENCY OF CALL TYPES 

# Count and sort priorities
priority_counts = filtered_cad['Call_Priority'].value_counts().sort_index()

# Set figure size and color palette
plt.figure(figsize=(10, 6))
barplot = sns.barplot(
    x=priority_counts.index,
    y=priority_counts.values,
)

# Add annotations on top of bars
for i, value in enumerate(priority_counts.values):
    plt.text(i, value + 0.5, f'{value:,}', ha='center', va='bottom', fontsize=10)

# Titles and labels
plt.title('Frequency of Each Call Priority', fontsize=20)
plt.xlabel('Call Priority', fontsize=12)
plt.ylabel('Number of Calls', fontsize=12)


plt.tight_layout()
plt.show()


## PLOT 2 - WORD CLOUD OF INCIDENT TYPES IN EACH PRIORITY

# Get the unique priority levels
priority_levels = sorted(filtered_cad['Call_Priority'].unique())

# Set up the figure
fig, axes = plt.subplots(3, 3, figsize=(20, 15))
axes = axes.flatten()

# Loop through each priority level
for i, level in enumerate(priority_levels):
    # Filter data for this level
    level_df = filtered_cad[filtered_cad['Call_Priority'] == level]

    # Count top 5 most frequent incident types
    top5 = level_df['InitialIncidentTypeDescription'].value_counts().nlargest(5)

   
    # Generate the word cloud
    wordcloud = WordCloud(
        width=900,
        height=900,
        relative_scaling=0.5,
        background_color='white',
        margin = 1,
        colormap='Dark2',
        max_font_size=100, 
        prefer_horizontal=1.0     # Avoid rotated words
    ).generate_from_frequencies(top5)

    # Plot
    ax = axes[i]
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_title(f'Priority Level {level}', fontsize=30)
    ax.axis('off')
    
    rect = Rectangle(
        (0, 0),                # bottom-left corner
        900, 900,              # width and height of the wordcloud
        linewidth=3,
        edgecolor='black',
        facecolor='none',
        transform=ax.transData
    )
    ax.add_patch(rect)

plt.tight_layout()
plt.show()

## PLOT 3 - BOX PLOTS OF ALL PRIORITIES VS ARRIVAL TIMES 

plt.figure(figsize=(10, 10))
sns.boxplot(data=filtered_cad, x='Call_Priority', y='Arrival_Time', showfliers=False)

plt.title('Arrival Time by Call Priority')
plt.xlabel('Call Priority')
plt.ylabel('Arrival Time (minutes)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

## PLOT 4 - BOX PLOTS OF TOP 5 COMMON PRIORITIES VS ARRIVAL TIMES 

import matplotlib.pyplot as plt
import seaborn as sns

# Get top 5 most frequent Call_Priority values
top_5 = (
    filtered_cad['Call_Priority']
    .value_counts()
    .nlargest(5)       
    .index
)

# Filter the dataset to include only those top 5
top_priority = filtered_cad[filtered_cad['Call_Priority'].isin(top_5)]

# Plot
plt.figure(figsize=(10, 6))
sns.boxplot(data=top_priority, x= 'Call_Priority', y='Arrival_Time', hue='Call_Priority', showfliers=False, palette='Set2', legend=False)

plt.title('Arrival Time by Priority - Top 5 Most Frequent Calls')
plt.xlabel('Call Priority')
plt.ylabel('Arrival Time (minutes)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

## PLOT 5 - BOX PLOTS OF HIGH PRIORITY VS LOW PRIORITY ARRIVAL TIMES
## now plotting

sns.boxplot(x='Priority_Level', y='Arrival_Time', data=filtered_cad,showfliers=False)
plt.title("Arrival Time by Priority Level")
plt.xlabel("Priority Level")
plt.ylabel("Arrival Time")
plt.tight_layout()
plt.show()

## PLOT 6 - ARRIVAL TIME VS VAN AVAILABILITY 

## violin plots
# Compute IQR
Q1 = filtered_cad['Arrival_Time'].quantile(0.25)
Q3 = filtered_cad['Arrival_Time'].quantile(0.75)
IQR = Q3 - Q1

# Filter out outliers
filtered_no_outliers = filtered_cad[
    (filtered_cad['Arrival_Time'] >= Q1 - 1.5 * IQR) &
    (filtered_cad['Arrival_Time'] <= Q3 + 1.5 * IQR)
]
import seaborn as sns

plt.figure(figsize=(10, 10))
sns.violinplot(x='Van_Available', y='Arrival_Time', data=filtered_no_outliers)

# Customize plot
plt.title('Arrival Time by Van Availability')
plt.xlabel('Van Available')
plt.ylabel('Response Time (minutes)')
plt.xticks([1, 0], [ 'Available', 'Not Available'])  # Optional: clearer labels
plt.grid(True)
plt.show()

## PLOT 7 A - VAN AVAILABILE HIGH VS LOW PRIORITY ARRIVAL TIME

# Filter for van available
van_not_available = filtered_cad[filtered_cad['Van_Available'] == 1]

# Keep only Low and High priority levels 
subset = van_not_available[van_not_available['Priority_Level'].isin(['Low', 'High'])]

# Plot
plt.figure(figsize=(8, 6))
sns.boxplot(x='Priority_Level', y='Arrival_Time', data=subset, palette='Set2', 
            showfliers = False,  order=['High', 'Low']))


plt.title('Arrival Time by Priority Level (Van Available)')
plt.xlabel('Priority Level')
plt.ylabel('Arrival Time')
plt.grid(True)
plt.tight_layout()
plt.show()

## PLOT 7 B - VAN NOT AVAILABILE HIGH VS LOW PRIORITY ARRIVAL TIME

import seaborn as sns
import matplotlib.pyplot as plt

# Step 1: Filter for van not available
van_not_available = filtered_cad[filtered_cad['Van_Available'] == 0]

# Step 2: Keep only Low and High priority levels (adjust as needed)
subset = van_not_available[van_not_available['Priority_Level'].isin(['Low', 'High'])]

# Step 3: Plot
plt.figure(figsize=(8, 6))
sns.boxplot(x='Priority_Level', y='Arrival_Time', data=subset, palette='Set2', 
            showfliers = False,  order=['High', 'Low'])  # explicitly set order)

 

plt.title('Arrival Time by Priority Level (Van Not Available)')
plt.xlabel('Priority Level')
plt.ylabel('Arrival Time')
plt.grid(True)
plt.tight_layout()
plt.show()

## PLOT 8 - T STATISTIC FOR VAN AVAILABILITY ACROSS LOW AND HIGH PRIORITY

import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import pandas as pd

# Compute t-stats and p-values
tstat_df = (
    filtered_cad.groupby('Priority_Level')
    .apply(lambda df: pd.Series(ttest_ind(
        df[df['Van_Available'] == 1]['Arrival_Time'],
        df[df['Van_Available'] == 0]['Arrival_Time'],
        equal_var=False)))
    .reset_index()
    .rename(columns={0: 't_stat', 1: 'p_val'})
)

tstat_df['t_stat'] = tstat_df['t_stat'].abs()
tstat_df = tstat_df.sort_values('Priority_Level')

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(x='Priority_Level', y='t_stat', data=tstat_df, palette='coolwarm')

plt.axhline(0, color='gray', linewidth=0.8)
plt.title('T-Statistic Comparing Arrival Time by Van Availability\nAcross Priority Levels')
plt.ylabel('Absolute T-Statistic')
plt.xlabel('Priority Level')

for i, row in enumerate(tstat_df.itertuples()):
    plt.text(i, row.t_stat + 0.5, f"{row.t_stat:.2f}", ha='center')

plt.tight_layout()
plt.show()
