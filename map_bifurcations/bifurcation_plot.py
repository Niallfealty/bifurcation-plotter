""" A plotting tool for bifurcation maps
"""

from matplotlib import pyplot as plt
from argparse import ArgumentParser
import numpy as np

class BifurcationPlot:
    """ Code to compute a bifurcation plot for a function

        parameters:
            @fn - the function to be computed (must be callable)
            @initial_val - the initial value to compute the diagram from
            @transition_iterations - how many iterations to ignore to remove transition
            @...
    """
    def __init__(self,
            fn,
            initial_val,
            transition_iterations=1_000,
            fn_sample_count=100,
            param_iterations=1_000,
            **params_range):
        self.fn = fn
        self.initial_val = initial_val
        self.params_range = params_range
        self.fn_sample_count = fn_sample_count
        self.transition_iterations = transition_iterations
        self.total_iterations = transition_iterations + fn_sample_count
        self.param_iterations = param_iterations

    def _compute_param(self, **params):
        ''' Compute the points for a given value of params
            @params: a dict of param values (single, to go into function)
        '''
        points = []
        current_val = self.initial_val
        for i in range(self.total_iterations):
            current_val = self.fn(current_val, **params)
            if i >= self.transition_iterations:
                points.append(current_val)
        return points
    
    def _run_over_params(self):
        ''' Run over all specified ranges of parameters
            
            for now we'll assume one param
        '''
        # for storing data
        points_dict = {}

        # written for extension at the moment this just does one
        param_name = list(self.params_range.keys())[0]
        param_min, param_max = self.params_range[param_name]

        # try to find a stable value for every parameter value
        for param in np.linspace(param_min, param_max, self.param_iterations):
            points_dict[param] = self._compute_param(**{param_name: param})

        return points_dict

    def _plot_diagram(self):
        fig, ax = plt.subplots()
        for param, y_points in self._run_over_params().items():
            ax.plot([param]*len(y_points), y_points, ",", color="blue")

        plt.show()

    def plot(self):
        return self._plot_diagram()

def logistic_map(x, r):
    ''' The logistic map '''
    return r*x*(1-x)

def fn_selection(args):
    """ pick a function, initial value and params in line with args """
    if (args.function=="logistic_map") or (args.function is None):
        return logistic_map, args.initial_val, {"r": [args.start,args.stop]}

def main():
    parser = ArgumentParser("""Bifurcation plotter
            Tool for generating bifurcation plots""")
    parser.add_argument("-f", "--function", help="Pick a function to compute the bifurcation plot for. Supported options are: 'logistic_map'")
    parser.add_argument("-i", "--initial_val", help="Choose an initial value for the calculation, defaults to 0.3", type=float, default=0.3)
    parser.add_argument("--start", help="Pick a start value to plot from, defaults to 1", type=float, default=1.0)
    parser.add_argument("--stop", help="Pick a stop value to plot to, defaults to 3", type=float, default=4.0)

    args = parser.parse_args()
    fn, initial_val, params, = fn_selection(args)
    BifurcationPlot(fn=fn, initial_val=initial_val, **params).plot()

if __name__ == "__main__":
    main()
