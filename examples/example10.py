#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/mystic/browser/mystic/LICENSE
"""
Example:
    - Solve 8th-order Chebyshev polynomial coefficients with DE.
    - Plot (x2) of convergence to Chebyshev polynomial.
    - Monitor (x2) Chi-Squared for Chebyshev polynomial.

Demonstrates:
    - standard models
    - expanded solver interface
    - built-in random initial guess
    - customized monitors and termination conditions
    - customized DE mutation strategies
    - use of solver members to retrieve results information
"""

# Differential Evolution solver
from mystic.solvers import DifferentialEvolutionSolver2

# Chebyshev polynomial and cost function
from mystic.models.poly import chebyshev8, chebyshev8cost
from mystic.models.poly import chebyshev8coeffs

# tools
from mystic.termination import VTR
from mystic.strategy import Best1Exp
from mystic.monitors import VerboseMonitor, Monitor
from mystic.tools import getch, random_seed
from mystic.math import poly1d
import pylab
pylab.ion()

# draw the plot
def plot_frame(label=None):
    pylab.close()
    pylab.title("8th-order Chebyshev coefficient convergence")
    pylab.xlabel("Differential Evolution %s" % label)
    pylab.ylabel("Chi-Squared")
    pylab.draw()
    return
 
# plot the polynomial trajectories
def plot_params(monitor):
    x = range(len(monitor))
    y = monitor.y
    pylab.plot(x,y,'b-')
    pylab.axis([1,0.5*x[-1],0,y[1]],'k-')
    pylab.draw()
    return


if __name__ == '__main__':

    print "Differential Evolution"
    print "======================"

    # set range for random initial guess
    ndim = 9
    x0 = [(-100,100)]*ndim
    random_seed(123)

    # configure monitors
    stepmon = VerboseMonitor(50)
    evalmon = Monitor()

    # use DE to solve 8th-order Chebyshev coefficients
    npop = 10*ndim
    solver = DifferentialEvolutionSolver2(ndim,npop)
    solver.SetRandomInitialPoints(min=[-100]*ndim, max=[100]*ndim)
    solver.SetEvaluationLimits(generations=999)
    solver.SetEvaluationMonitor(evalmon)
    solver.SetGenerationMonitor(stepmon)
    solver.enable_signal_handler()
    solver.Solve(chebyshev8cost, termination=VTR(0.01), strategy=Best1Exp, \
                 CrossProbability=1.0, ScalingFactor=0.9)
    solution = solver.bestSolution

    # get solved coefficients and Chi-Squared (from solver members)
    iterations = solver.generations
    cost = solver.bestEnergy
    print "Generation %d has best Chi-Squared: %f" % (iterations, cost)
    print "Solved Coefficients:\n %s\n" % poly1d(solver.bestSolution)

    # plot convergence of coefficients per iteration
    plot_frame('iterations')
    plot_params(stepmon)
    getch()

    # plot convergence of coefficients per function call
    plot_frame('function calls')
    plot_params(evalmon)
    getch()

# end of file
