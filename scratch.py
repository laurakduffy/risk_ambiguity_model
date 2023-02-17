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
model1 = sq.lognorm(0.001, 0.001)
sample1 = sq.sample(model1, n=SIMULATIONS)

print("Lognorm(1, 3)")
model2= sq.lognorm(0.001, 2.2)
sample2 = sq.sample(model2, n=SIMULATIONS)

print("Mixture")
model_mix = sq.mixture([model1, model2], [0.9,0.1])
sample_mix = sq.sample(model_mix, n=SIMULATIONS, lclip = 0.001, rclip=3)


print("Lognorm(0.001, 0.1)")
model1n = sq.uniform(-0.0005, -0.00005)

print("Lognorm(1, 3)")
model2n= sq.norm(-.5, -0.0005)

print("Overall Mixture")
model_mixo = sq.mixture([model1, model2, model1n, model2n], [0.9/2, 0.1/2, 0.95/2, 0.05/2])
sample_mixo = sq.sample(model_mixo, n=SIMULATIONS, lclip=-0.5, rclip=3)
get_pctiles(sample_mixo, percentiles)