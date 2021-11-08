# PEP-it: Performance Estimation in Python

This code comes jointly with the following [`reference`](.pdf):

> [1] B. Goujaud, C. Moucer, F. Glineur, J. Hendrickx, A. Taylor, A. Dieuleveut. "PEP-it: computer-assisted worst-case analyses of first-order optimization methods in Python." 

please refer to this note when using the toolbox in a project.

Version: November 2021

#### Authors

- [**Baptiste Goujaud**]() (main contributor #1) 
- [**Céline Moucer**]() (main contributor #2)
- [**Julien Hendrickx**](https://perso.uclouvain.be/julien.hendrickx/index.html) (project supervision)
- [**François Glineur**](https://perso.uclouvain.be/francois.glineur/) (project supervision)
- [**Adrien Taylor**](http://www.di.ens.fr/~ataylor/) (contributor & main project supervision)
- [**Aymeric Dieuleveut**](http://www.cmap.polytechnique.fr/~aymeric.dieuleveut/) (contributor & main project supervision)

#### Acknowledgments


The authors would like to thank [**Rémi Flamary**](https://remi.flamary.com/) for his feedbacks on preliminary versions of the toolbox, as well as for support regarding the continuous integration and overall organization.


## Installing the toolbox

This code runs under Python 3.6+.
- Please run ``pip install -r Infrastructure.requirements.txt``
- Then run ``pip install -e .``

You are all set; it remains to test the installation by running the tests:
- ``python -m unittest``

## When to use PEP-it?

The general purpose of the toolbox is to help the researchers producing worst-case guarantees for their favorite first-order methods. A gentle introduction to the toolbox is provided in [1].

The toolbox implements the performance estimation approach, pioneered by Drori and Teboulle [2]. The PEP-it implementation is in line with the framework as exposed in [3,4] and follow-up works (for which proper references are provided in the example files). A gentle introduction to performance estimation problems is provided in this [blog post](https://francisbach.com/computer-aided-analyses/).

 > [2] Drori, Yoel, and Marc Teboulle. "Performance of first-order methods for smooth convex minimization: a novel approach." Mathematical Programming 145.1-2 (2014): 451-482
 >
 > [3] Taylor, Adrien B., Julien M. Hendrickx, and François Glineur. "Smooth strongly convex interpolation and exact worst-case performance of first-order methods." Mathematical Programming 161.1-2 (2017): 307-345.
 >
 > [4] Taylor, Adrien B., Julien M. Hendrickx, and François Glineur. "Exact worst-case performance of first-order methods for composite convex optimization." SIAM Journal on Optimization 27.3 (2017): 1283-1313

 
 
## Example

The folder [Examples](/examples) contains numerous introductory examples to the toolbox.


Among the other examples, the following code (see [`GradientMethod`](PEPit/examples/a_methods_for_unconstrained_convex_minimization/gradient_descent.py)) generates a worst-case scenario for <img src="https://render.githubusercontent.com/render/math?math=N"> iterations of the gradient method, applied to the minimization of a smooth (possibly strongly) convex function f(x). More precisely, this code snippet allows computing the worst-case value of <img src="https://render.githubusercontent.com/render/math?math=f(x_N)-f_\star"> when <img src="https://render.githubusercontent.com/render/math?math=x_N"> is generated by gradient descent, and when <img src="https://render.githubusercontent.com/render/math?math=\|x_0-x_\star\|=1">.


```Python
from PEPit.pep import PEP
from PEPit.functions.smooth_strongly_convex_function import SmoothStronglyConvexFunction


def wc_gd(mu, L, gamma, n, verbose=True):
    """
    Consider the minimization problem
        f_* = min_x f(x),
    where f is L-smooth and mu-strongly convex.
    This code computes a worst-case guarantee for the gradient method with fixed step size. That is, it computes
    the smallest possible tau(n, L, mu) such that the guarantee
        f(x_n) - f_* <= tau(n, L, mu) * || x_0 - x_* ||^2
    is valid, where x_n is the output of the gradient descent with fixed step size,
    and where x_* is the minimizer of f.
    Result to be compared with that of
    [1] Yoel Drori. "Contributions to the Complexity Analysis of
        Optimization Algorithms." PhD thesis, Tel-Aviv University, 2014.
    :param mu: (float) the strong convexity parameter.
    :param L: (float) the smoothness parameter.
    :param gamma: (float) step size.
    :param n: (int) number of iterations.
    :param verbose: (bool) if True, print conclusion
    :return: (tuple) worst_case value, theoretical value
    """

    # Instantiate PEP
    problem = PEP()

    # Declare a strongly convex smooth function
    func = problem.declare_function(SmoothStronglyConvexFunction,
                                    {'mu': mu, 'L': L})

    # Start by defining its unique optimal point xs = x_* and corresponding function value fs = f_*
    xs = func.optimal_point()
    fs = func.value(xs)

    # Then define the starting point x0 of the algorithm
    x0 = problem.set_initial_point()

    # Set the initial constraint that is the distance between x0 and x^*
    problem.set_initial_condition((x0 - xs) ** 2 <= 1)

    # Run n steps of the GD method
    x = x0
    for _ in range(n):
        x = x - gamma * func.gradient(x)

    # Set the performance metric to the function values accuracy
    problem.set_performance_metric(func.value(x) - fs)

    # Solve the PEP
    pepit_tau = problem.solve()

    # Compute theoretical guarantee (for comparison)
    theoretical_tau = L/2/(2*n+1)

    # Print conclusion if required
    if verbose:
        print('*** Example file: worst-case performance of gradient descent with fixed step sizes ***')
        print('\tPEP-it guarantee:\t\t f(x_n)-f_* <= {:.6} ||x_0 - x_*||^2'.format(pepit_tau))
        print('\tTheoretical guarantee:\t f(x_n)-f_* <= {:.6} ||x_0 - x_*||^2'.format(theoretical_tau))

    # Return the worst-case guarantee of the evaluated method (and the reference theoretical value)
    return pepit_tau, theoretical_tau


```

## Code: conventions and external contributions

**Convention of the code**

- The ``PEPit`` directory contains the main code while ``Tests`` directory contains all the associated tests. 
- We use PEP8 convention rules.

**Convention of the VCS**

- The ``master`` branch is exclusively used for deployed versions of the code.
- The ``develop`` branch must be the main one and must not be broken at any time.
- The other branches are named either ``feature/...`` or ``fix/..`` or eventually ``hotfix/..`` to highlight the importance of the PR.
- All branches must be approved before merge. We use PRs and the ``git rebase`` command to sync any branch on ``develop``.

## Documentation
