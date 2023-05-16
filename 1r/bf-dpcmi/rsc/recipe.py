from diffpy.srfit.fitbase import FitResults
from diffpy.srfit.pdf import PDFParser
from rsc.fitconfig import FitConfig
from itertools import count
import rsc.diffpyhelper as dh


class CreateRecipe():
    def __init__(self, conf, phases, char_function):
        self.conf = FitConfig(**conf)
        self.char_function = char_function
        self.phases = self._parse_phases(phases)

        self._create_cif_files()
        self._create_equation()
        self._create_functions()

        self.p_f = dict(zip(phases, self.char_function))

    def _phase_counter(self, phase):
        if not hasattr(self, f'{phase}_count'):
            setattr(self, f'{phase}_count', count(1))
            return 0
        else:
            return next(getattr(self, f'{phase}_count'))

    def _parse_phases(self, phases):
        phases_cp = phases.copy()
        for i, phase in enumerate(phases):
            ocur = phases.count(phase)
            if ocur > 1:
                cnt = self._phase_counter(phase)
                phases_cp[i] = f'{phase}Γ{cnt}'

        return phases_cp

    def _create_cif_files(self):
        self.cif_files = {}
        for phase in list(self.phases):
            self.cif_files[f'{phase}'] = f'./cifs/{phase.split("Γ")[0]}.cif' 

    def _create_equation(self):
        equation_list = []
        for phase, function in zip(self.phases, self.char_function):
            equation_list.append(f'{phase} * {phase}{function}')
        self.equation = ' + '.join(equation_list)

    def _create_functions(self):
        self.functions = {}
        for phase, function in zip(self.phases, self.char_function):
            function_definition = self.conf.fetch_function(phase, function)
            self.functions[f'{phase}{function}'] = function_definition

    def update_recipe(self):
        self.recipe, self.pg = dh.create_recipe_from_files(
            meta_data=self.conf(),
            equation=self.equation,
            cif_files=self.cif_files,
            functions=self.functions
        )

    def update_data(self, data_file):
        if not hasattr(self, 'recipe'):
            self.update_recipe()
        pp = PDFParser()
        pp.parseFile(data_file)
        profile = self.recipe._contributions['PDF'].profile
        profile.loadParsedData(pp)
        profile.meta.update(self.conf())

    def default_restraints(self):
        contributions = self.recipe._contributions['PDF']
        recipe = self.recipe
        for phase in self.phases:

            delta2 = getattr(self.recipe, f'{phase}_delta2')
            recipe.restrain(delta2, lb=0, ub=5, sig=1e-3)
            delta2.value = 3.0

            scale = getattr(self.recipe, f'{phase}_scale')
            recipe.restrain(scale, lb=0.001, ub=2, sig=1e-3)
            scale.value = 0.5


            
            
            biso = getattr(contributions, phase)
            for scat in biso.phase.getScatterers():
                recipe.restrain(scat.Biso, lb=0, ub=5)


            for abc in ['a', 'b', 'c']:
                try:
                    lat = getattr(self.recipe, f'{phase}_{abc}')
                    lb_lat = lat.value - 0.2
                    ub_lat = lat.value + 0.2
                    recipe.restrain(lat, lb=lb_lat, ub=ub_lat, sig=1e-3)
                except AttributeError:
                    pass

            for func in self.functions.values():
                params = func[1][1:]
                for p in params:
                    param = getattr(self.recipe, p)
                    recipe.restrain(param, lb=0, ub=5e2, sig=1e-3)

    def create_param_order(self):
        ns = []
        for _ in self.phases:
            for func in self.functions.values():
                for varn in func[1][1:]:
                    ns.append(varn)
        ns = [n for n in ns if n]
        self.param_order = [
            ['free', 'lat', 'scale'],
            ['free', *ns],
            ['free', 'adp', 'delta2'],
        ]

    def remove_phase(self, p):
        if p not in self.phases:
            raise ValueError(f'{p} is not in phases')
        self.phases.remove(p)

        f = self.p_f[p]

        # remove phase from equation
        equation_list = self.equation.split(' + ')
        equation_list.remove(f'{p} * {p}{f}')
        self.equation = ' + '.join(equation_list)

        # remove phase from cif_files
        self.cif_files.pop(f'{p}')

        # remove phase from functions
        self.functions.pop(f'{p}{f}')

    def add_phase(self, p):
        if p in self.phases:
            raise ValueError(f'{p} is already in phases')
        self.phases.append(p)
        
        f = self.p_f[p]
        
        # add phase to equation
        equation_list = self.equation.split(' + ')
        equation_list.append(f'{p} * {p}{f}')
        self.equation = ' + '.join(equation_list)

        # add phase to cif_files
        self.cif_files[f'{p}'] = f'./CIFS/{p}.cif'

        # add phase to functions
        self.functions[f'{p}{f}'] = self.conf.fetch_function(p ,self.p_f[p])

    def get_mol_contribution(self, phase):
        tot_scale = 0 
        for p in self.phases:
            tot_scale += getattr(self.recipe,f'{p}_scale').value
        return getattr(self.recipe,f'{phase}_scale').value#/tot_scale
