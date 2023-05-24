from diffpy.srfit.fitbase import FitResults
from matplotlib import pyplot as plt
from ezfit import FitPDF, Contribution
from ezpdf import plot_PDF
from pathlib import Path
from glob import glob

gr = glob("../../0d/gr30/*.gr")[0]
Al2O3 = Contribution(cif_name="Al2O3", cf_name="sphericalCF", formula="Al2O3")
NiO = Contribution(cif_name="NiO", cf_name="sphericalCF", formula="NiO")
Ni = Contribution(cif_name="Ni", cf_name="sphericalCF", formula="Ni")

fit = FitPDF(path_to_file, contributions=[Ni, Al2O3, NiO])

fit.update_recipe()
fit.run_fit()
fit.res = FitResults(fit.recipe)
fig, ax = plot_PDF(fit, fit.recipe, fit.res)

name = Path(gr).stem
fit.dw.save_results(recipe=fit.recipe,
                    footer=f"Fit of {name}",
                    directory="./res/",
                    file_stem=name,
                    pg_names=fit.phases)
plt.savefig(f"./res/{name}.pdf")
