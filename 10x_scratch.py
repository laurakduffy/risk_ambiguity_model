import numpy as np
import squigglepy as sq
from squigglepy.numbers import K, M, B


SIMULATIONS = 1*M
percentiles = [0.15, 1, 2.5, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 97.5, 99, 99.85]


def get_pctiles(sample, percentiles):
    pctiles = []
    for pct in percentiles:
        pctiles.append(np.percentile(sample, pct))
        print("{}%: {}".format(pct, np.percentile(sample, pct)))
    print("Mean: {}".format(np.mean(sample)))
    return pctiles

print("Lognorm(0.001, 0.1)")
model1 = sq.lognorm(0.1, 1)
sample1 = sq.sample(model1, n=SIMULATIONS)

print("Lognorm(1, 3)")
model2= sq.lognorm(1, 23)
sample2 = sq.sample(model2, n=SIMULATIONS)

print("Lognorm(1, 3)")
model2n= -1*sq.lognorm(0.5, 5)

print("Overall Mixture")
model_mixo = sq.mixture([model1, model2, model2n], [0.238, 0.262, 0.5])
sample_mixo = sq.sample(model_mixo, n=SIMULATIONS, lclip=-5, rclip=30)
get_pctiles(sample_mixo, percentiles)