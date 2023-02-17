import numpy as np
import squigglepy as sq
from squigglepy.numbers import K, M, B


SIMULATIONS = 10*M
percentiles = [0.15, 1, 2.5, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 97.5, 99, 99.85]

def get_pctiles(sample, percentiles):
    pctiles = []
    for pct in percentiles:
        pctiles.append(np.percentile(sample, pct))
        print("{}%: {}".format(pct, np.percentile(sample, pct)))
    print("Mean: {}".format(np.mean(sample)))
    return pctiles

print("Lognorm(0.001, 0.1)")
model1 = sq.lognorm(10, 1000)
sample1 = sq.sample(model1, n=SIMULATIONS)
get_pctiles(sample1, percentiles)

print("Lognorm(1, 3)")
model2= sq.lognorm(47.5, 40000)
sample2 = sq.sample(model2, n=SIMULATIONS)
get_pctiles(sample2, percentiles)

print("Mixture")
model_mix = sq.mixture([model1, model2], [0.9,0.1])
sample_mix = sq.sample(model_mix, n=SIMULATIONS, lclip = 10, rclip=100000)
get_pctiles(sample_mix, percentiles)


