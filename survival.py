import numpy as np
import pandas as pd
import lifelines
from matplotlib import pyplot as plt
from lifelines.statistics import KaplanMeierFitter
from lifelines.statistics import logrank_test
from lifelines import WeibullFitter
from lifelines import WeibullAFTFitter
from lifelines.plotting import qq_plot
from lifelines import CoxPHFitter

survival_df = pd.read_csv('survival_final.csv')
survival_df['duration'] = [(x.split(' ')[0]) for x in survival_df['Duration']]
survival_df['duration'] = pd.to_numeric(survival_df["duration"], downcast="float")
print(survival_df.head())

kmf_has_lad = KaplanMeierFitter()
kmf_has_lcx = KaplanMeierFitter()
kmf_has_rca = KaplanMeierFitter()
kmf_has_mvd = KaplanMeierFitter()

# Fit Kaplan Meier estimators to each DataFrame
kmf_has_lad.fit(durations=survival_df[survival_df['LAD_perf']==1]['duration'],
               event_observed=survival_df[survival_df['LAD_perf']==1]['Event'])
kmf_has_lcx.fit(durations=survival_df[survival_df['LCx_perf']==1]['duration'],
               event_observed=survival_df[survival_df['LCx_perf']==1]['Event'])
kmf_has_rca.fit(durations=survival_df[survival_df['RCA_perf']==1]['duration'],
               event_observed=survival_df[survival_df['RCA_perf']==1]['Event'])
kmf_has_mvd.fit(durations=survival_df[survival_df['MVD']==1]['duration'],
               event_observed=survival_df[survival_df['MVD']==1]['Event'])

# Print out the median survival duration of each group
print("The median survival duration (days) of patients with LAD ischaemia: ", kmf_has_lad.median_survival_time_)
print("The median survival duration (days) of patients with LCx ischaemia: ", kmf_has_lcx.median_survival_time_)
print("The median survival duration (days) of patients with RCA ischaemia: ", kmf_has_rca.median_survival_time_)
print("The median survival duration (days) of patients with MVD ischaemia: ", kmf_has_mvd.median_survival_time_)

lad = (survival_df['LAD_perf']==1)
lcx = (survival_df['LCx_perf']==1)
rca = (survival_df['RCA_perf']==1)
ax = plt.subplot(111)
lad_km = KaplanMeierFitter()
lcx_km = KaplanMeierFitter()
rca_km = KaplanMeierFitter()
lad_km.fit(durations=survival_df[lad]['duration'],
               event_observed=survival_df[lad]['Event'], label="LAD ischaemia")
lad_km.plot_survival_function(ax=ax)
lcx_km.fit(durations=survival_df[lcx]['duration'],
               event_observed=survival_df[lcx]['Event'], label="LCx ischaemia")
lcx_km.plot_survival_function(ax=ax)
rca_km.fit(durations=survival_df[rca]['duration'],
               event_observed=survival_df[rca]['Event'], label="RCA ischaemia")
rca_km.plot_survival_function(ax=ax)
plt.show()
patient_results = logrank_test(durations_A = survival_df[lad]['duration'],
                               durations_B = survival_df[lcx]['duration'],
                               duration_C = survival_df[rca]['duration'],
                               event_observed_A = survival_df[lad]['Event'],
                               event_observed_B = survival_df[lcx]['Event'],
                               event_observed_C = survival_df[rca]['Event'])
# Print out the p-value of log-rank test results
print(patient_results.p_value)

mvd = (survival_df['MVD']==1)
no_mvd = (survival_df['MVD']==0)
mvd_km = KaplanMeierFitter()
nomvd_km = KaplanMeierFitter()
mvd_km.fit(durations=survival_df[mvd]['duration'],
               event_observed=survival_df[mvd]['Event'], label="MVD ischaemia")
mvd_km.plot_survival_function(ax=ax)
nomvd_km.fit(durations=survival_df[no_mvd]['duration'],
               event_observed=survival_df[no_mvd]['Event'], label="No MVD ischaemia")
nomvd_km.plot_survival_function(ax=ax)
plt.show()
patient_results = logrank_test(durations_A = survival_df[mvd]['duration'],
                               durations_B = survival_df[no_mvd]['duration'],
                               event_observed_A = survival_df[mvd]['Event'],
                               event_observed_B = survival_df[no_mvd]['Event'])
# Print out the p-value of log-rank test results
print(patient_results.p_value)

pos = (survival_df['Positive_perf']==1)
neg = (survival_df['Positive_perf']==0)
pos_km = KaplanMeierFitter()
neg_km = KaplanMeierFitter()
pos_km.fit(durations=survival_df[pos]['duration'],
               event_observed=survival_df[pos]['Event'], label="Positive ischaemia")
pos_km.plot_survival_function(ax=ax)
neg_km.fit(durations=survival_df[neg]['duration'],
               event_observed=survival_df[neg]['Event'], label="Negative ischaemia")
neg_km.plot_survival_function(ax=ax)
plt.show()
patient_results = logrank_test(durations_A = survival_df[pos]['duration'],
                               durations_B = survival_df[neg]['duration'],
                               event_observed_A = survival_df[pos]['Event'],
                               event_observed_B = survival_df[neg]['Event'])
# Print out the p-value of log-rank test results
print(patient_results.p_value)