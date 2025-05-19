stat_analysis_script.py

## check for variances in high, med, low priority groups 

import pandas as pd
import scipy.stats as stats

## to check for equal variances in the group
# Extract data by group
groups = [group['Arrival_Time'].dropna() for name, group in filtered_cad.groupby('Priority_Level')]

# Perform Levene's test for equal variance
stat, p_value = stats.levene(*groups)

print(f"Levene’s test statistic: {stat}")
print(f"P-value: {p_value}")

if p_value > 0.05:
    print("Fail to reject null hypothesis: variances are equal across groups.")
else:
    print("Reject null hypothesis: variances are different across groups.")

## welch's anova test

from pingouin import welch_anova
import pandas as pd

# Filter for the three levels
df = filtered_cad[filtered_cad['Priority_Level'].isin(['High', 'Medium', 'Low'])]

# Run Welch's ANOVA
welch_result = welch_anova(data=df, dv='Arrival_Time', between='Priority_Level')
print(welch_result)

## now I want to check the correlation between the priority levels. although the prioirty levels are numeric, they are technically ordinal bc the distance
## does not technically reflect a perfect meaning in terms of distance
## choose to use spearmen

from scipy.stats import spearmanr

corr, p_corr = spearmanr(filtered_cad['Call_Priority'], filtered_cad['Arrival_Time'])
print(f"Spearman correlation between Call Priority and Response Time: {corr:.3f} (p = {p_corr:.5f})")

## measures the strength and direction of association between two ranked variables.

## a linear regression will model how much Response Time increases for every unit increase in Call Priority (e.g., going from priority 2 to 3).

import statsmodels.api as sm

# Define X and y
X = filtered_cad['Call_Priority']
y = filtered_cad['Arrival_Time']

# Add a constant (for the intercept)
X = sm.add_constant(X)

# Fit the model
model = sm.OLS(y, X).fit()

# View summary
##print(model.summary())

# Key values from the model
print(model.params)

print("\nP-values:")
print(model.pvalues)

print(f"\nR-squared: {model.rsquared:.3f}")

import pandas as pd
import scipy.stats as stats

## to check for equal variances in the group
# Extract data by group

# Drop rows with missing values in key columns
t_data = filtered_cad.dropna(subset=['Arrival_Time', 'Van_Available'])

# Split into two groups based on Van_Available being True or False
available = t_data[t_data['Van_Available'] == True]['Arrival_Time']
not_available = t_data[t_data['Van_Available'] == False]['Arrival_Time']

# Variance of arrival times when Van_Available == True
var_available = available.var()

# Variance of arrival times when Van_Available == False
var_not_available = not_available.var()

print(var_available)
print(var_not_available)

stat, p_levene = levene(available, not_available)

print(f"Levene’s test p-value: {p_levene:.4f}")

# Choose appropriate t-test based on Levene's result
if p_levene < 0.05:
    print("Variances are significantly different — use Welch's t-test (equal_var=False).")
    equal_var = False
else:
    print("No significant difference in variances — assume equal_var=True.")
    equal_var = True


## This will tell you if the difference in average response time between those two groups is statistically significant.
## welches t test 
from scipy.stats import ttest_ind

# Perform Welch's t-test (does not assume equal variances)
t_stat, p_val = ttest_ind(available, not_available, equal_var=False)

print(f"Welch's t-test statistic: {t_stat:.4f}")
print(f"Welch's t-test p-value: {p_val:.4f}")

if p_val < 0.05:
    print("Result: Statistically significant difference between groups (reject H0).")
else:
    print("Result: No statistically significant difference between groups (fail to reject H0).")

##cohen's d analysis

import numpy as np

# Calculate means and standard deviations
mean1 = available.mean()
mean2 = not_available.mean()
std1 = available.std()
std2 = not_available.std()

# Sample sizes
n1 = len(available)
n2 = len(not_available)

# Pooled standard deviation
pooled_std = np.sqrt(((n1 - 1)*std1**2 + (n2 - 1)*std2**2) / (n1 + n2 - 2))

# Cohen's d
cohen_d = (mean1 - mean2) / pooled_std
print(f"Cohen's d: {cohen_d:.3f}")


import pingouin as pg

# Drop rows with missing values in key columns
welches_data = filtered_cad.dropna(subset=['Arrival_Time', 'Van_Available'])

# Split into two groups based on Van_Available being True or False
available = welches_data[welches_data['Van_Available'] == True]


welch_avail = pg.welch_anova(dv='Arrival_Time', between='Call_Priority', data=available)
print("[Van Available] Welch's ANOVA")
print(welch_avail)

# VAN NOT AVAILABLE group
not_available = welches_data[welches_data['Van_Available'] == False]

welch_not = pg.welch_anova(dv='Arrival_Time', between='Priority_Level', data=not_available)
print("\n[Van Not Available] Welch's ANOVA")
print(welch_not)

## We can do this by adding:

## A binary column Van_Available

## An interaction term: Call_Priority * Van_Available in the regression model

regression_data = filtered_cad.dropna(subset = ['Call_Priority', 'Van_Available', 'Arrival_Time']).copy()

import statsmodels.formula.api as smf

# Ensure Van_Available is numeric (0/1)
regression_data['Van_Available'] = regression_data['Van_Available'].astype(int)

model = smf.ols('Arrival_Time ~ Call_Priority * Van_Available', data=regression_data).fit()

# Run regression with interaction
model = smf.ols('Arrival_Time ~ Call_Priority * Van_Available', data=regression_data).fit()

# Print summary
print(model.summary())

