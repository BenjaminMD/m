from matplotlib import pyplot as plt
from ezfit import FitPDF, Contribution
from ezpdf import plot_PDF 
from pathlib import Path

path_to_file = Path('../0d/gr/azint_UC1_Al2O3_2_0007_scan0025_pilatus.gr')


Al2O3 = Contribution(cif_name='Tetr_Al2O3', cf_name='sphericalCF', formula='Al2O3')
NiO = Contribution(cif_name='NiO', cf_name='sphericalCF', formula='NiO')
Ni = Contribution(cif_name='Ni', cf_name='sphericalCF', formula='Ni')

fit = FitPDF(path_to_file, contributions=[Ni, Al2O3, NiO])

fit.config['rmin'] = 1
fit.config['rmax'] = 5
fit.config['rstep'] = 0.1
fit.update_recipe()
fit.apply_restraints()
fit.run_fit()

plot_PDF(fit, fit.recipe, fit.res)
plt.show()
