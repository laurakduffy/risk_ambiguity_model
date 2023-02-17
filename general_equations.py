## Equations needed by both the Buchak model and my models

import squigglepy as sq
from squigglepy.numbers import K, M, B
import numpy as np
import copy

SIMULATIONS = 100*K

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

def one_model_dalys_per_1000_by_reducing_risk(p_x_risk, power, probability_success, bp_per_billion_if_success, times_credit_if_success):
    value_status_quo = years_healthy_per_year()*lifespan_person()*world_population()*times_credit_if_success # TODO: Fix this to match the cross-cause model
    bp_lowered_risk = probability_success*bp_per_billion_if_success*1*K/(1*B)

    risk_reduction = bp_lowered_risk*one_basis_point()

    dalys_with_risk_aversion = value_gained_by_reducing_x_risk(p_x_risk, risk_reduction, value_status_quo, power)
    return dalys_with_risk_aversion

## GHD Intervention

def cost_per_daly_ghd():
    return 50

def dalys_per_1000_certain_intervention():
    return 1000/cost_per_daly_ghd()

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