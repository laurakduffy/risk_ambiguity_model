## Equations needed by both the Buchak model and my models

import squigglepy as sq
from squigglepy.numbers import K, M, B
import numpy as np

SIMULATIONS = 10*M

def mix_models(models, weights=None):
    if weights is None:
        weights = [1/len(models) for model in models]
    
    model_mix = sq.mixture(models, weights)
    sample = sq.sample(model_mix, n=SIMULATIONS)
    return sample


def create_variables(models_dict, weights_dict):
    p_success_models = models_dict['p_success']
    risk_models = models_dict['risk']
    bp_per_billion_models = models_dict['bp_per_billion_if_success']
    times_credit_if_success_models = models_dict['times_credit_if_success']

    p_success_weights = weights_dict['p_success']
    risk_weights = weights_dict['risk']
    bp_per_billion_weights = weights_dict['bp_per_billion_if_success']
    times_credit_if_success_weights = weights_dict['times_credit_if_success']


    p_success = mix_models(p_success_models, p_success_weights)
    risk = mix_models(risk_models, risk_weights)
    bp_per_billion_if_success = mix_models(bp_per_billion_models, bp_per_billion_weights)
    times_credit_if_success = mix_models(times_credit_if_success_models, times_credit_if_success_weights)

    return p_success, risk, bp_per_billion_if_success, times_credit_if_success

def get_pct(num):
    return "{:.2%}".format(num)

def probability_weight(p, r):
    ## takes probabilities of getting at least a certain level of DALYs and returns an adjusted coefficient to multiply by in doing EV calculations
    probability_weight = p**r
    return probability_weight

def utility_status_quo(p_x_risk, value_of_status_quo, power):
    # define disvalue of having everyone die as 0 
    p_survive = 1 - p_x_risk
    risk_wt = probability_weight(p_survive, power)
    u_sq = 0*(1) + risk_wt*value_of_status_quo

    return u_sq

def utility_world_with_less_x_risk(p_x_risk, x_risk_reduction, value_of_status_quo, power):
    p_survive = 1 - p_x_risk + x_risk_reduction
    risk_wt = probability_weight(p_survive, power)
    u_less_x_risk = 0*(1) + risk_wt*value_of_status_quo
    return u_less_x_risk

def value_gained_by_reducing_x_risk(p_x_risk, x_risk_reduction, value_of_status_quo, power):
    u_sq = utility_status_quo(p_x_risk, value_of_status_quo, power)
    u_less_x_risk = utility_world_with_less_x_risk(p_x_risk, x_risk_reduction, value_of_status_quo, power)
    value_gained = u_less_x_risk - u_sq
    return value_gained

## X-risk Model

def years_healthy_per_year():
    return 0.8

def world_population():
    return 8*B

def lifespan_person():
    return 80

def one_basis_point():
    return 0.0001

def generate_success_bernoullis(probability_success):
    successes = []
    for i in range(SIMULATIONS):
        p_success_i = sq.sample(sq.discrete({0: 1-probability_success[i], 1: probability_success[i]}), n=1)
        successes.append(p_success_i)
    return np.array(successes)

def one_model_dalys_per_1000_by_reducing_risk(p_x_risk, power, probability_success, bp_per_billion_if_success, times_credit_if_success):
    value_status_quo = years_healthy_per_year()*lifespan_person()*world_population()*times_credit_if_success 
    
    did_intervention_succeed = generate_success_bernoullis(probability_success)
    
    bp_lowered_risk_with_1000 = did_intervention_succeed*bp_per_billion_if_success*1*K/(1*B)

    risk_reduction = bp_lowered_risk_with_1000*one_basis_point()

    dalys_with_risk_aversion = value_gained_by_reducing_x_risk(p_x_risk, risk_reduction, value_status_quo, power)
    return dalys_with_risk_aversion

## GHD Intervention

def dalys_per_1000_ghd_intervention():
    return sq.sample(sq.lognorm(9, 24), n=SIMULATIONS)

## Ambiguity Aversion Modeling

def sample_model(model):
    p_success = sq.sample(model['p_success'], n=SIMULATIONS)
    risk = sq.sample(model['risk'], n=SIMULATIONS)
    bp_per_billion_if_success = sq.sample(model['bp_per_billion_if_success'], n=SIMULATIONS)
    years_credit_if_success = sq.sample(model['years_credit_if_success'], n=SIMULATIONS)
    return (p_success, risk, bp_per_billion_if_success, years_credit_if_success)
    
def get_list_of_evs_by_model(power, models):
    evs = []
    for model in models:
        p_success, risk, bp_per_billion, years_credit_if_success = sample_model(model)
        risk_weighted_dalys = one_model_dalys_per_1000_by_reducing_risk(risk, power, p_success, bp_per_billion, years_credit_if_success)[0]
        ev_risk_weighted_dalys = np.mean(risk_weighted_dalys)
        evs.append(ev_risk_weighted_dalys)
    return evs

def dalys_per_1000_by_reducing_risk_ambiguity_aversion(a, power, models):
    evs = get_list_of_evs_by_model(power, models)
    ev_dalys_risk_and_ambiguity_weighted = (1-a)*min(evs) + a*max(evs)

    return ev_dalys_risk_and_ambiguity_weighted

def define_model(p_success, risk, bp_per_billion_if_success, years_credit_if_success, net_negative):
    model = {'p_success': p_success, 
            'risk': risk,
            'bp_per_billion_if_success': bp_per_billion_if_success,
            'years_credit_if_success': years_credit_if_success, 
            'net_negative': net_negative
            }
    return model