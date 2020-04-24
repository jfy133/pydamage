#!/usr/bin/env python3

import numpy as np
from scipy.stats import norm
from pydamage.optim import optim


def vuong_closeness(ref, model_A, model_B, data, wlen, verbose):
    xdata, counts = np.unique(np.sort(data), return_counts=True)
    ydata = list(counts/counts.sum())
    ydata_counts = {i:c for i,c in enumerate(ydata)}
    for i in range(wlen):
        if i not in ydata_counts:
            ydata_counts[i] = np.nan
    res = {}
    optim_A, stdev_A = optim(function=model_A.pmf,
                    parameters=model_A.kwds,
                    xdata=xdata,
                    ydata=ydata,
                    bounds=model_A.bounds)
    optim_B, stdev_B = optim(function=model_B.pmf,
                    parameters=model_B.kwds,
                    xdata=xdata,
                    ydata=ydata,
                    bounds=model_B.bounds)

    LA = model_A.log_pmf(x=data, **optim_A)
    LB = model_B.log_pmf(x=data, **optim_B)
    pdiff = len(model_A.kwds) - len(model_B.kwds)
    LR = LA.sum() - LB.sum() - (pdiff/2)*np.log(len(data))
    omega = np.std(LA-LB)
    Z = LR/(np.sqrt(len(data))*omega)
    pval = norm.cdf(Z)
    if verbose:
        print(f"\nReference: {ref}")
        print(f"Vuong closeness test Z-score for {ref}: {round(Z, 4)}")
        print(f"Vuong closeness test p-value for {ref}: {round(pval, 4)}")
        print(f"Model A parameters for {ref}: {optim_A}")
        print(f"Model B parameters for {ref}: {optim_B}")
    res.update(ydata_counts)
    res.update(optim_A)
    res.update(stdev_A)
    res.update(optim_B)
    res.update(stdev_B)
    res.update({'pvalue': pval})
    return(res)
