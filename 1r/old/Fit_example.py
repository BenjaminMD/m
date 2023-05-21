from diffpy.srfit.fitbase import FitResults, initializeRecipe
from matplotlib import pyplot as plt
from ezfit import FitPDF, Contribution
from ezpdf import plot_PDF
from pathlib import Path
from glob import glob

names = glob("../../0d/gr30/*.gr")
for name in names:
    path_to_file = name
    name = Path(name).stem
    print(name)
    path_to_res = glob(f"../../0d/res/{name}*.res")[0]
    Al2O3 = Contribution(cif_name="Al2O3", cf_name="sphericalCF", formula="Al2O3")
    NiO = Contribution(cif_name="NiO", cf_name="sphericalCF", formula="NiO")
    Ni = Contribution(cif_name="Ni", cf_name="sphericalCF", formula="Ni")
    fit = FitPDF(path_to_file, contributions=[Ni, Al2O3, NiO])
    fit.config["rmin"] = 1
    fit.config["rmax"] = 5
    fit.config["rstep"] = 0.1
    fit.update_recipe()
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
