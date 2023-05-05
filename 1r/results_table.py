import matplotlib.pyplot as plt 
import pandas as pd
from collections import defaultdict
import fnmatch
import numpy as np
from glob import glob

def get_Rw(lines):
    for line in lines.split('\n'):
        if line.startswith('Rw'):
            return float(line.split()[-1])
def get_param(lines, param):
    param_list = fnmatch.filter(lines.split('\n'), f'*{param}*')
    param_list = [p.split('+/-')[0] for p in param_list]
    param_dict = {p.split()[0]: float(p.split()[1]) for p in param_list}
    return param_dict


def get_lat(lines):
    lat_list = fnmatch.filter(lines.split('\n'), '*_a*')
    lat_list = [lat.split('+/-')[0] for lat in lat_list]
    lat_dict = {lat.split()[0]: float(lat.split()[1]) for lat in lat_list}
    return lat_dict

def get_scale(lines):
    lat_list = fnmatch.filter(lines.split('\n'), '*_scale*')
    lat_list = [lat.split('+/-')[0] for lat in lat_list]
    lat_dict = {lat.split()[0]: float(lat.split()[1]) for lat in lat_list}
    return lat_dict

def get_size(lines):
    lat_list = fnmatch.filter(lines.split('\n'), '*size*')
    lat_list = [lat.split('+/-')[0] for lat in lat_list]
    lat_dict = {lat.split()[0]: float(lat.split()[1]) for lat in lat_list}
    return lat_dict

def get_param(lines, param):
    param_list = fnmatch.filter(lines.split('\n'), f'*{param}*')
    param_list = [p.split('+/-')[0] for p in param_list]
    param_dict = {p.split()[0]: float(p.split()[1]) for p in param_list}
    param_set = set() | {*param_dict.keys()}

    return param_dict, param_set 

res_file_paths = glob('./results/*res')

data = []
cleaned_data = []

lat = {}
lat_names = set()

scale = {}
scale_names = set()

size = {}
size_names = set()


d2_names = set()

for res in res_file_paths:
    name = res.split('/')[-1].split('.')[0]
    with open(res, 'r') as f:
        lines = '\n'.join(f.readlines())
        
        lines = lines.split(''.join(['-']*78))[1:]
        Rw = get_Rw(lines[0])
        lat = get_lat(lines[1])
        lat_names |= {*lat.keys()}

        scale = get_scale(lines[1])
        scale_names |= {*scale.keys()}
        
        size = get_size(lines[1])
        size_names |= {*size.keys()}

        delta2, d2_set = get_param(lines[1], 'delta2')
        d2_names |= d2_set

        data.append([name, Rw, lat, scale, size, delta2])

for dat in data:
    name, Rw, lat, scale, size, delta2 = dat
    dlat = defaultdict(lambda : np.nan) | lat
    dscale = defaultdict(lambda : np.nan) | scale
    dsize = defaultdict(lambda : np.nan) | size
    d2 = defaultdict(lambda : np.nan) | delta2
    cleaned_data.append([
        name, 
        Rw, 
        *[dlat[key] for key in lat_names],
        *[dscale[key] for key in scale_names],   
        *[dsize[key] for key in size_names],
        *[d2[key] for key in d2_names]   
        ])


df = pd.DataFrame(
        columns=['name',
                 'Rw',
                 *lat_names,
                 *scale_names,
                 *size_names,
                 *d2_names
                 ], data=cleaned_data)
col = df.columns
print(col)
plt.subplot(321)
for i in ['Fe_fcc_a', 'Ni_fcc_a']:
    plt.scatter(df.index, df[i], label=i)
plt.legend()
plt.subplot(323)
for i in ['Fe_fcc_scale', 'Ni_fcc_scale']:
    plt.scatter(df.index, df[i], label=i)
plt.legend()
plt.subplot(324)
for i in ['Fe_fcc_psize', 'Ni_fcc_psize']:
    plt.scatter(df.index, df[i], label=i)
plt.legend()
plt.subplot(325)
for i in ['Fe_fcc_delta2', 'Ni_fcc_delta2']:
    plt.scatter(df.index, df[i], label=i)
plt.legend()
plt.subplot(326)
plt.scatter(df.index, df['Rw'], label='Rw')
plt.legend()
plt.show()
