import pandas as pd
import numpy as np


df = pd.read_csv('FelixStinkt.csv')
df = df[[f.startswith('azint_UC1_Al2O3_2') for f in df.file_name]]
df.reset_index(inplace=True)

switch = df["file_name"].values 

switch = [f.split('Al2O3_2_')[-1] for f in switch]
switch = [f.split('_scan')[0] for f in switch]
switch = [int(f) for f in switch]

# get id when scan number changes
switch = np.where(np.diff(switch) != 0)[0] + 1

def fill_list_with_blocks(indices, length):
    result = []
    current_value = 1  # Start with 1
    for i in range(length):
        if i in indices:
            result.append(current_value)
        else:
            result.append(1 - current_value)  # Alternate between 0 and 1
        if i + 1 in indices:
            current_value = 1 - current_value  # Flip the value for the next block
    return result


df.dt = pd.to_datetime(df.dt)
t = df.dt - df.dt[0]
t = t.dt.total_seconds() / 3600
t = t.values
df.loc[df.rw > 1, 'rw'] = np.nan

switch = fill_list_with_blocks(switch[1:], len(df))

df['scan'] = switch

df["T"] = df['T_avg / °C']
