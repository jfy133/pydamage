#!/usr/bin/env python3


from scipy.optimize import curve_fit


def optim(function, parameters, xdata, ydata, bounds):
    """Find optimal parameters given data

    Args:
        function (function): function to optimize
        xdata (np array): x values
        ydata (np array): y values
        bounds (tuple of tuple): optimization bounds
                    ((par1_min, par2_min), (par1_max, par2_max))
    Returns:
        (dict): 'parameter_name':'parameter_value'
    """
    op_par = curve_fit(function, xdata=xdata, ydata=ydata, bounds=bounds)
    op_par_dict = {k: v for (k, v) in zip(parameters, op_par[0])}
    return(op_par_dict)