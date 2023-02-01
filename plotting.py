"""
Format model outputs to be plotted using plotting.R
"""

import pickle
import numpy as np
import pandas as pd
import os

from fhs_lib_year_range_manager.lib import YearRange
from mrtool import MRData
from scipy.special import expit
from db_queries import get_location_metadata


# Set up for a given indicator
indicator = "malaria"
pickle_file = "malaria_incidence"
covariate = "ldi"

output_path = f"/path/to/{indicator}/exemplar_plots/"
input_path = f"/path/to/{indicator}/coefficients/{pickle_file}.pickle"
years = YearRange.parse_year_range("1990:2021:2050")

os.makedirs(output_path, exist_ok=True)

# Read in Pickle and expit data
fit = pickle.load(open(input_path, "rb"))
cov_list = fit.node_models[0].cov_names.copy()
cov_list.remove("intercept")
cov_name = cov_list[0]
fit_df = fit.node_models[0].result_to_df()
fit_df["obs_exp"] = expit(fit_df["obs"])
fit_df["prediction_exp"] = expit(fit_df["prediction"])
fit_df.rename(columns={"obs_exp": "indicator"}, inplace=True)

# Isolate to both sex
if len(fit_df.sex_id.unique()) is not 1:
    fit_df = fit_df[fit_df.sex_id == 3]

# Year id treated uniquely 
fit_df["study_id"] = fit_df["study_id"].astype(str).astype(int)
cov_df = pd.DataFrame()
if cov_name == "year_id":
    cov_df[cov_name] = np.linspace(years.past_end, years.past_end, 100)
    data_pred = MRData(
        covs={cov_name: np.linspace(years.past_end, years.past_end, 100)}
    )
else:
    cov_max = np.ceil(fit_df[cov_name].max())
    cov_df[cov_name] = np.linspace(0, cov_max, 100)
    data_pred = MRData(covs={cov_name: np.linspace(0, cov_max, 100)})

# Set up Spline data
fit_df.rename(columns={covariate: "covariate"}, inplace=True)
cov_df["spline"] = fit.node_models[0].predict(data_pred)
spline_df = cov_df
spline_df["spline_exp"] = expit(spline_df.spline)
spline_df["location_id"] = ""
spline_df.rename(columns={covariate: "covariate"}, inplace=True)
spline_df = spline_df[["covariate", "spline_exp", "location_id"]]
spline_df.to_csv(output_path + 'spline_df.csv', index=False)

# Add on iso codes for plotting
df = fit_df
df = df[["study_id", "year_id", "covariate", "indicator"]]
df.rename(columns={"study_id": "location_id"}, inplace=True)
df_loc = get_location_metadata(location_set_id=39, release_id=9)
df_loc = df_loc[['location_id', 'ihme_loc_id']]
final = pd.merge(df, df_loc, how="left", on="location_id")
final.to_csv(output_path + f'{indicator}.csv', index=False)
