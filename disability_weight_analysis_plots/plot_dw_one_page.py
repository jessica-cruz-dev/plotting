"""
Create disability weight plots. Plots include:
-Age pattern for every national and subnational per acause

Example:
    python plot_dw_one_page.py \
"""

import math
import matplotlib
import matplotlib.gridspec as gridspec
import seaborn as sns
import pandas as pd
import numpy as np
import xarray as xr

from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from queries import get_age_metadata
from textwrap import wrap
from numpy import arange


matplotlib.use("Agg")

SEXES = {
    1: "Male",
    2: "Female",
}

SEX_COLORS = dict(
    Male="blue",
    Female="red",
)

LINE_DICT = {
    1: "-",
    2: ":",
}

LINE_WIDTH = 0.9

# Versions where files will be pulled from
version6 = "version6"
version5 = "version5"
stage = "disability_weight"
gbd_round_id = 6
output_filename = "cause.pdf"

plot_dir = FBDPath(f'/{gbd_round_id}/past/{stage}/{"cause"}/', root_dir="plot")
plot_dir.mkdir(parents=True, exist_ok=True)

dw_dir = FBDPath(f'/{gbd_round_id}/past/{stage}/{version6}')
dw_dir_roud5 = FBDPath(f'/5/past/{stage}/{version5}')

# Retrieving the correct cause list for given cause set
acauses = get_stage_cause_set(stage, gbd_round_id)
acauses.sort()

# Setting up ages to plot
age_meta = get_age_metadata(round=6)
age_meta['age_mid'] = (
    age_meta['age_group_years_start'] + age_meta['age_group_years_end']
) / 2
age_meta.drop(
    columns=[
        'age_group_years_start',
        'age_group_years_end',
        'age_group_weight_value'
    ],
    inplace=True
)

# Setting up location list and order
location_mapping = pd.concat([
    db.get_locations_by_level(3),
    db.get_locations_by_level(4).query(
        "parent_id in [44533, 6, 102, 163, 135]"
    )
])
location_order = pd.read_csv('/path/to/locaton_order.csv').location_id.tolist()
sorterIndex = dict(zip(location_order,range(len(location_order))))
location_mapping['location_order'] = location_mapping[
    'location_id'
].map(sorterIndex)
location_mapping.sort_values('location_order', inplace=True)
location_mapping.drop('location_order', 1, inplace = True)
nrow = 14
ncol = 14

def plot_location(ix, loc):

    # Round 6 data to plot
    dw_sub = dw_da.sel(location_id = loc).mean("draw").squeeze()
    df = dw_sub.to_dataset().to_dataframe().reset_index()
    df = df.merge(age_meta, left_on='age_group_id', right_on='age_group_id')

    # Round 5 data to plot
    dw_sub5 = dw_da5.sel(location_id=loc).mean("draw").squeeze()
    df5 = dw_sub5.to_dataset().to_dataframe().reset_index()
    df5 = df5.merge(age_meta, left_on='age_group_id', right_on='age_group_id')

    # location name for figure
    loc_name = location_mapping[
        location_mapping['location_id']==loc
    ]['location_name'].iloc[0]

    # start the next figure
    ax = fig.add_subplot(grid[ix])

    # calculate the ylimits
    top = df5.value.max() if df5.value.max() > df.value.max() else df.value.max()
    ax.set_ylim(bottom=0, top=top+.1) # top is +.1 to better see 

    # Round 5 lines plotting
    if 1 in df5.sex_id.unique():
        sex=SEXES[1]
        col=SEX_COLORS[sex]
        ax.plot(
            df5.age_mid.unique(),
            df5.loc[df5.location_id == loc][df5.sex_id == 1]['value'].values,
            color=col, label='Round 5',
            linestyle=LINE_DICT[2]
        )
    if 2 in df5.sex_id.unique():
        sex=SEXES[2]
        col=SEX_COLORS[sex]
        ax.plot(
            df5.age_mid.unique(),
            df5.loc[df5.location_id == loc][df5.sex_id == 2]['value'].values,
            color=col,
            linestyle=LINE_DICT[2]
        )

    # Round 6 lines plotting
    if 1 in df.sex_id.unique():
        sex=SEXES[1]
        col=SEX_COLORS[sex]
        ax.plot(
            df.age_mid.unique(),
            df.loc[df.location_id == loc][df.sex_id == 1]['value'].values,
            color=col,
            label='Round 6',
            linestyle=LINE_DICT[1]
        )
    if 2 in df.sex_id.unique():
        sex=SEXES[2]
        col=SEX_COLORS[sex]
        ax.plot(
            df.age_mid.unique(),
            df.loc[df.location_id == loc][df.sex_id == 2]['value'].values,
            color=col,
            linestyle=LINE_DICT[1]
        )
    
    # Final labels
    ax.set_title('\n'.join(wrap(f"{loc_name}",25)),  fontsize=45)
    ax.set_xlabel("Age midpoint")
    ax.set_ylabel("Disability Weight")
    ax.legend()

    return ax

with PdfPages(plot_dir / output_filename) as pdf:
    for acause in remaining:

        print(f"Plotting {acause}")
        # global veriables for both rounds datasets
        dw_da = open_xr(dw_dir / f"{acause}.nc").data
        dw_da5 = open_xr(dw_dir_roud5 / f"{acause}.nc").data

        # plot national location ids
        nat_location_ids = location_mapping[
            location_mapping.level==3
        ].location_id.tolist()

        # Figure specs
        fig = plt.figure(figsize=(150,100))
        nrow = math.floor(math.sqrt(len(nat_location_ids)))
        ncol = math.ceil(len(nat_location_ids) / nrow)
        grid = gridspec.GridSpec(nrow, ncol)
        loc = nat_location_ids[0]
        ax1 = plot_location(ix=0, loc=loc)
        nat_location_ids.pop(0)
    
        # National page plotting
        for ix, loc in enumerate(nat_location_ids):
            plot_location(ix=ix+1, loc=loc)
        fig.suptitle(
            f'{acause} national disability weights',
            fontsize=50,
            y=0.92
        )
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

        # Suvnational location ids
        subnat_location_ids = location_mapping[
            location_mapping.level==4
        ].location_id.tolist()

        # Prepend parent location ids 
        subnat_location_ids[:0] = [102, 163, 6, 135]
        fig = plt.figure(figsize=(150,100))
        nrow = math.floor(math.sqrt(len(subnat_location_ids)))
        ncol = math.ceil(len(subnat_location_ids) / nrow)
        grid = gridspec.GridSpec(nrow, ncol)
        loc = subnat_location_ids[0]
        ax1 = plot_location(ix=0, loc=loc)
        subnat_location_ids.pop(0)

        # Subnatinal page plotting
        for ix, loc in enumerate(subnat_location_ids):
            plot_location(ix=ix+1, loc=loc)
        fig.suptitle(
            f'{acause} subnational disability weights',
            fontsize=50, y=0.92
        )
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

great_job.congratulations()  # You did it!