from matplotlib import pyplot as plt
from ezfit import FitPDF, Contribution
from ezpdf import plot_single_PDF
from pathlib import Path

path_to_file = Path('../0d/gr/azint_UC1_Al2O3_2_0007_scan0025_pilatus.gr')


Al2O3 = Contribution(cif_name='Tetr_Al2O3', cf_name='sphericalCF', formula='Al2O3')
NiO = Contribution(cif_name='NiO', cf_name='sphericalCF', formula='NiO')
Ni = Contribution(cif_name='Ni', cf_name='sphericalCF', formula='Ni')

fit = FitPDF(path_to_file, contributions=[Ni])

fit.config['rmin'] = 1.5
fit.config['rmax'] = 5
fit.config['rstep'] = 1
fit.update_recipe()
fit.apply_restraints()
#fit.recipe.show()
#fit.run_fit()
fc = fit.recipe.PDF
p = fc.profile
p.setCalculationRange(1, 10, 1)
fit.recipe.free('all')
print(fit.recipe.residual([1, 1, 1, 1, 1, 1]))

#plot_single_PDF(fit.recipe)
#plt.show()
