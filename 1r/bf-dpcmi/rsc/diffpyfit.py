from diffpy.srfit.fitbase import FitResults
from rsc.recipe import CreateRecipe
import rsc.diffpyhelper as dh
import numpy

class DiffpyFit(CreateRecipe):
    def __init__(self, conf, phases, char_function):
        super().__init__(conf, phases, char_function)

    def run_simple_fit(self, data_file, out_dir):
        self.name = data_file.split('/')[-1].split('.')[0]
        if not hasattr(self, 'recipe'):
            self.update_data(data_file)
            self.update_recipe()
            self.default_restraints()
            self.create_param_order()
            self.recipe.show()
        else:
            self.update_data(data_file)
        try:
            self.recipe.constrain('delta4_Al2O3_Al2_Biso', 'delta4_Al2O3_Al1_Biso')
            self.recipe.constrain('delta4_Al2O3_Al3_Biso', 'delta4_Al2O3_Al1_Biso')
            self.recipe.constrain('delta4_Al2O3_Al4_Biso', 'delta4_Al2O3_Al1_Biso')
            self.recipe.constrain('delta4_Al2O3_Al5_Biso', 'delta4_Al2O3_Al1_Biso')
            self.recipe.constrain('delta4_Al2O3_Al6_Biso', 'delta4_Al2O3_Al1_Biso')
            self.recipe.constrain('delta4_Al2O3_Al7_Biso', 'delta4_Al2O3_Al1_Biso')
            self.recipe.constrain('delta4_Al2O3_Al8_Biso', 'delta4_Al2O3_Al1_Biso')
            self.recipe.constrain('delta4_Al2O3_Al9_Biso', 'delta4_Al2O3_Al1_Biso')
            self.recipe.constrain('delta4_Al2O3_Al10_Biso', 'delta4_Al2O3_Al1_Biso')
            self.recipe.constrain('delta4_Al2O3_Al11_Biso', 'delta4_Al2O3_Al1_Biso')
            self.recipe.constrain('delta4_Al2O3_Al12_Biso', 'delta4_Al2O3_Al1_Biso')
            self.recipe.constrain('delta4_Al2O3_Al13_Biso', 'delta4_Al2O3_Al1_Biso')
            self.recipe.constrain('delta4_Al2O3_Al14_Biso', 'delta4_Al2O3_Al1_Biso')
            self.recipe.constrain('delta4_Al2O3_Al15_Biso', 'delta4_Al2O3_Al1_Biso')
            self.recipe.constrain('delta4_Al2O3_Al16_Biso', 'delta4_Al2O3_Al1_Biso')
            self.recipe.constrain('delta4_Al2O3_Al17_Biso', 'delta4_Al2O3_Al1_Biso')
            self.recipe.constrain('delta4_Al2O3_Al18_Biso', 'delta4_Al2O3_Al1_Biso')
            self.recipe.constrain('delta4_Al2O3_O2_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O3_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O4_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O5_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O6_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O7_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O8_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O9_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O10_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O11_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O12_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O13_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O14_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O15_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O16_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O17_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O18_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O19_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O20_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O21_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O22_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O23_Biso', 'delta4_Al2O3_O1_Biso')
            self.recipe.constrain('delta4_Al2O3_O24_Biso', 'delta4_Al2O3_O1_Biso')
        except ValueError:
                pass
        dh.optimize_params_manually(
            self.recipe,
            self.param_order,
            rmin=self.conf.rmin,
            rmax=self.conf.rmax,
            rstep=self.conf.rstep,
            ftol=1e-3,
            print_step=False
        )

        #res = FitResults(self.recipe)
        #res.saveResults(f'{out_dir}{self.name}.res')

    def get_gr(recipe):
        """
        Get the gr of a recipe and for each phase contribution
        returns:
        - r: list of floats
        - gobs: list of floats
        - gcalc: list of floats
        - gdiff: list of floats
        - baseline: float 
        - gr_composition: dict of list of floats
        """
        def remove_consecutive_duplicates(string, char):
            indices = [m.start() for m in re.finditer(char * 2, string)]
            if indices:
                for i in indices:
                    string = string[:i] + string[i+1:]
                return remove_consecutive_duplicates(string, char)
            else:
                return string

        equation = recipe.PDF.getEquation()        
        for char in ['\)', '\(']:
            equation = (remove_consecutive_duplicates(equation, char))
    

        prof = recipe._contributions['PDF'].profile
        r = prof.x
        gobs = prof.y
        gcalc = recipe._contributions['PDF'].evaluate()
        baseline = 1.35 * gobs.min()
        gdiff = gobs - gcalc


        gr_composition = {}
        for eq in equation.split(' + '):
            gr = recipe.PDF.evaluateEquation(eq[1:])
            gr_composition[eq[1:]] = gr

        return r, gobs, gcalc, gdiff, baseline, gr_composition


    def save_results(self, out_dir, name_ext=''):
        #self.recipe.show()
        res = FitResults(self.recipe)
        res.saveResults(f'{out_dir}{self.name}{name_ext}.res')

    def save_fits(self, out_dir, name_ext=''):
        get_gr(recipe)
        dataout = numpy.column_stack([r, gobs, gcalc, gdiff, gr_composition])
        numpy.savetxt(f'{out_dir}{self.name}{name_ext}.fit', dataout)

    def complete_recipe(self, data_file):
        self.update_recipe()
        self.update_data(data_file)
        self.create_param_order()
        self.default_restraints()
        
        

    def _run_molarcontribution_fit(self, data_file, out_dir, molar_limit):
        self.complete_recipe(data_file)
        self.run_simple_fit(data_file, out_dir)

        self.removed_phase = []
        print(self.phases)
        for phase in self.phases:
            mol_contrib = self.get_mol_contribution(phase)
            print(f'{phase} scale: {mol_contrib}')
            
            if mol_contrib < molar_limit:
                print(f'{phase}', "removed")
                self.remove_phase(phase)
                self.removed_phase.append(phase)

        self.complete_recipe(data_file)
        self.run_simple_fit(data_file, out_dir)


        if self.removed_phase:
            [self.add_phase(phase) for phase in self.removed_phase]
            
        
        self.update_data(data_file)
        self.name = data_file.split('/')[-1].split('.')[0]
        self.save_results(out_dir, name_ext='_'.join(self.removed_phase))


        self.complete_recipe(data_file)
        self.run_simple_fit(data_file, out_dir)
        self.removed_phase = []
        print(self.phases)
    
    def run_molarcontribution_fit(self, data_file, out_dir, limit):
        if not hasattr(self, 'recipe'):
            self.update_recipe()
            self.create_param_order()
            self.default_restraints()
        self.removed_phase = []
        def drop_phases():
            self.update_recipe()
            self.create_param_order()
            self.default_restraints()
            self.run_simple_fit(data_file, out_dir)
            for phase in self.phases:
                scale = self.get_mol_contribution(phase)
                if scale < limit and len(self.phases) != 1:
                    self.remove_phase(phase)
                    self.removed_phase.append(phase)
                    drop_phases()
        drop_phases()
        self.save_results(out_dir, name_ext='_rm_'+'_'.join(self.removed_phase))
        if self.removed_phase:
            [self.add_phase(phase) for phase in self.removed_phase]




