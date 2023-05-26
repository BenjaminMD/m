from diffpy.srfit.fitbase import FitResults, initializeRecipe
from matplotlib import pyplot as plt
from ezfit import FitPDF, Contribution
from ezpdf import plot_PDF
from pathlib import Path
from glob import glob

name = glob("../../0d/gr30/*.gr")[0]
name = Path(name).stem
path_to_res = glob(f"../../0d/res/{name}*.res")[0]
Al2O3 = Contribution(cif_name="Al2O3", cf_name="sphericalCF", formula="Al2O3")
NiO = Contribution(cif_name="NiO", cf_name="sphericalCF", formula="NiO")
Ni = Contribution(cif_name="Ni", cf_name="sphericalCF", formula="Ni")
fit = FitPDF(name, contributions=[Ni, Al2O3, NiO])


fit.config["rmin"] = 1
fit.config["rmax"] = 5
fit.config["rstep"] = 0.1
fit.update_recipe()
fit.recipe.Al2O3.Al1_occ = 0.5
fit.recipe.free("all")
initializeRecipe(fit.recipe, path_to_res)
fit.res = FitResults(fit.recipe)
fig, ax = plot_PDF(fit, fit.recipe, fit.res)
fit.dw.save_results(recipe=fit.recipe,
                    footer=f"Fit of {name}",
                    directory="./res/",
                    file_stem=name,
                    pg_names=fit.phases)
plt.savefig(f"./res/{name}.pdf")
