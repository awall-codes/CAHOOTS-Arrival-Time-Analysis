from scipy.stats import ttest_ind

## T test to assess difference in high and low priority calls arrival times 

low = filtered_cad[filtered_cad['Priority_Level'] == 'Low']['Arrival_Time']
high = filtered_cad[filtered_cad['Priority_Level'] == 'High']['Arrival_Time']

t_stat, p_val = ttest_ind(low, high, equal_var=False)
print(f"Welch's t-test: t = {t_stat:.2f}, p = {p_val:.4f}")


## T test to assess difference in arrival times across van availabilities

# Split into two groups based on Van_Available being True or False
available = t_data[t_data['Van_Available'] == True]['Arrival_Time']
not_available = t_data[t_data['Van_Available'] == False]['Arrival_Time']

t_stat, p_val = ttest_ind(available, not_available, equal_var=False)

print(f"Welch's t-test statistic: {t_stat:.4f}")
print(f"Welch's t-test p-value: {p_val:.4f}")

if p_val < 0.05:
    print("Result: Statistically significant difference between groups (reject H0).")
else:
    print("Result: No statistically significant difference between groups (fail to reject H0).")

## T-Test to see how both priority level and van availability differ in significance 

for level in filtered_cad['Priority_Level'].unique():
    subset = filtered_cad[filtered_cad['Priority_Level'] == level]
    group1 = subset[subset['Van_Available'] == 1]['Arrival_Time']
    group0 = subset[subset['Van_Available'] == 0]['Arrival_Time']
    
    t_stat, p_val = stats.ttest_ind(group1, group0, equal_var=False)
    print(f"Priority {level} — t = {t_stat:.2f}, p = {p_val:.4f}")
    
