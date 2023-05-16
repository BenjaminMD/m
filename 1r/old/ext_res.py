#!/usr/bin/python3
import pandas as pd
import fire






def main(files):
    vertical_seperator = '-'*78    
    parameters = [
                'file_name',
                'Rw',
                'Al2O3_Al1_Biso',  
                'Al2O3_Al2_Biso',  
                'Al2O3_Al3_Biso',  
                'Al2O3_O1_Biso ',  
                'Al2O3_a',  
                'Al2O3_c',  
                'Al2O3_delta2',  
                'Al2O3_psize',  
                'Al2O3_scale',  
                'NiO_Ni0_Biso',  
                'NiO_O1_Biso',  
                'NiO_a',  
                'NiO_delta2',  
                'NiO_psize',  
                'NiO_scale', 
                'Ni_Ni0_Biso',  
                'Ni_O1_Biso',  
                'Ni_a',  
                'Ni_delta2',  
                'Ni_psize',  
                'Ni_scale',  
            ]
    df = pd.DataFrame(columns=parameters)
    
    for f in files:





if __name__ == '__main__':
    fire.Fire(main)
