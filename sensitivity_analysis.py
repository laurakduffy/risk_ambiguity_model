## Sensitivity Analysis for which variables impact the necessary risk aversion the most
import numpy as np
from SALib.sample import saltelli
from SALib.analyze import sobol
import general_equations as ge
import squigglepy as sq
from squigglepy.numbers import K, M, B

SIMULATIONS = 1*M

def lt_dalys_per_1000_sensitivity():
    problem = {'num_vars': 3,
               'names': ['probability_success', 'bp_per_billion_if_success', 'times_credit_if_success'],
               'bounds': [[0.4, 0.8], [-0.5, 3], [10, 100000]]}
    
    param_values = saltelli.sample(problem, 2**13)
    y = np.array([lt_dalys_per_1000(*params) for params in param_values])
    sobol_indices = sobol.analyze(problem, y)
    influence_list1 = []
    for i, name in enumerate(problem['names']):
        influence_list1.append([name, sobol_indices['S1'][i], sobol_indices['S1_conf'][i]])
    print("[1st Order] Sensitivity analysis for DALYs per $1000 spending on LT")
    print_sensitivity_analysis(influence_list1, "LT DALYs per $1000")
    print("---------------------------------------------------------------------------")   
    influence_list_t = []
    for i, name in enumerate(problem['names']):
        influence_list_t.append([name, sobol_indices['ST'][i], sobol_indices['ST_conf'][i]])
    print("[Total] Sensitivity analysis for DALYs per $1000 spending on LT")
    print_sensitivity_analysis(influence_list_t, "LT DALYs per $1000")
    print("---------------------------------------------------------------------------")   
    return 

def lt_dalys_per_1000(probability_success, bp_per_billion_if_success, times_credit_if_success):
    value_status_quo = ge.years_healthy_per_year()*ge.lifespan_person()*ge.world_population()*times_credit_if_success

    did_intervention_succeed = sq.sample(sq.discrete({0: 1-probability_success, 1: probability_success}), n=1)

    bp_lowered_risk_with_1000 = did_intervention_succeed*bp_per_billion_if_success*1000/(1*10**9)

    risk_reduction = bp_lowered_risk_with_1000*ge.one_basis_point()

    dalys = value_status_quo*risk_reduction
    return dalys

def print_sensitivity_analysis(influence_list, function_name):
    print("{} Sensitivity Analysis".format(function_name))
    for var in influence_list:
        print("{} : {} +/- {}".format(var[0], np.around(var[1], 3), np.around(var[2], 3)))

lt_dalys_per_1000_sensitivity()



