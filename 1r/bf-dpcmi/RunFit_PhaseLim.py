
from multiprocessing import Process, Queue
from rsc.recipe import CreateRecipe
from rsc.util import read_config
import rsc.diffpyhelper as dh
from rsc.diffpyfit import DiffpyFit
import numpy as np
from glob import glob

from datetime import datetime
startTime = datetime.now()


OUT_DIR ='../../0d/res/'
CONF_PATH = './FitConfig.json'


conf = read_config(CONF_PATH)


def RunFit(dat_file):
    Fit = DiffpyFit(
            conf,
            ['Ni', 'NiO', 'Al2O3'],
            ['sphericalCF']*3
        )
    Fit.run_molarcontribution_fit(dat_file, OUT_DIR, 0.10)
    name = dat_file.split('/')[-1].split('.')[0]


data_files = glob('../../0d/gr/*.gr')



res_files = glob('../../0d/res/*.res')

res_files_names = ['_'.join(res.split('/')[-1].split('.')[0].split('_')[:6]) for res in res_files]
filtered_data_files = []

for dat_file in data_files:
    name = dat_file.split('/')[-1].split('.')[0]
    if name not in res_files_names:
        filtered_data_files.append(dat_file)
    else:
        print('File {} already fitted'.format(name))
data_files = filtered_data_files

if __name__ == "__main__":
    queue = Queue()

    #for chunk in np.array_split(data_files[1:], len(data_files[1:])//8):
    processes = [Process(target=RunFit(df), args=(df,)) for df in
                 data_files]
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    print(datetime.now() - startTime)
