from PEPit.pep import PEP
from PEPit.functions.smooth_convex_function import SmoothConvexFunction


def wc_gradient_descent_lyapunov_1(L, gamma, n, verbose=True):
    """
    Consider the convex minimization problem

    .. math:: f_\\star \\triangleq \\min_x f(x),

    where :math:`f` is :math:`L`-smooth and convex.

    This code verifies a worst-case guarantee for **gradient descent** with fixed step-size :math:`\\gamma`.
    That is, it verifies that the Lyapunov (or potential/energy) function

    .. math:: V_n \\triangleq n (f(x_n) - f_\\star) + \\frac{L}{2} \\|x_n - x_\\star\\|^2

    is decreasing along all trajectories and all smooth convex function :math:`f` (i.e., in the worst-case):

    .. math :: V_{n+1} \\leqslant V_n,

    where :math:`x_{n+1}` is obtained from a gradient step from :math:`x_{n}` with fixed step-size :math:`\\gamma=\\frac{1}{L}`.

    **Algorithm**: Onte iteration of gradient descent is described by

    .. math:: x_{n+1} = x_n - \\gamma \\nabla f(x_n),

    where :math:`\\gamma` is a step-size.

    **Theoretical guarantee**: The theoretical guarantee can be found in e.g., [1, Theorem 3.3]:

    .. math:: V_{n+1} - V_n \\leqslant 0,

    when :math:`\\gamma=\\frac{1}{L}`.

    **References**: The detailed potential function can found in [1] and the SDP approach can be found in [2].

    `[1] N. Bansal, A. Gupta (2019). Potential-function proofs for gradient methods
    (Theory of Computing, 15(1), 1-32).
    <https://arxiv.org/pdf/1712.04581.pdf>`_

    `[2] A. Taylor, F. Bach (2019). Stochastic first-order methods: non-asymptotic and computer-aided analyses
    via potential functions (Conference on Learning Theory (COLT)).
    <https://arxiv.org/pdf/1902.00947.pdf>`_

    Args:
        L (float): the smoothness parameter.
        gamma (float): the step-size.
        n (int): current iteration number.
        verbose (bool): if True, print conclusion.

    Returns:
        pepit_tau (float): worst-case value.
        theoretical_tau (float): theoretical value.

    Examples:
        >>> L = 1
        >>> gamma = 1 / L
        >>> pepit_tau, theoretical_tau = wc_gradient_descent_lyapunov_1(L=L, gamma=gamma, n=10, verbose=True)
        (PEP-it) Setting up the problem: size of the main PSD matrix: 4x4
        (PEP-it) Setting up the problem: performance measure is minimum of 1 element(s)
        (PEP-it) Setting up the problem: initial conditions (0 constraint(s) added)
        (PEP-it) Setting up the problem: interpolation conditions for 1 function(s)
                 function 1 : 6 constraint(s) added
        (PEP-it) Compiling SDP
        (PEP-it) Calling SDP solver
        (PEP-it) Solver status: optimal (solver: MOSEK); optimal value: 2.4580691380721078e-09
        *** Example file: worst-case performance of gradient descent with fixed step-size for a given Lyapunov function***
            PEP-it guarantee:		V_(n+1) - V_(n) <= 2.45807e-09
            Theoretical guarantee:	V_(n+1) - V_(n) <= 0.0

    """

    # Instantiate PEP
    problem = PEP()

    # Declare a smooth convex function
    func = problem.declare_function(SmoothConvexFunction, param={'L': L})

    # Start by defining its unique optimal point xs = x_* and corresponding function value fs = f_*
    xs = func.stationary_point()
    fs = func.value(xs)

    # Then define the starting point x0 of the algorithm as well as corresponding gradient and function value gn and fn
    xn = problem.set_initial_point()
    gn, fn = func.oracle(xn)

    # Run the GD at iteration (n+1)
    xnp1 = xn - gamma * gn
    gnp1, fnp1 = func.oracle(xnp1)

    # Compute the Lyapunov function at iteration n and at iteration n+1
    init_lyapunov = n * (fn - fs) + L / 2 * (xn - xs) ** 2
    final_lyapunov = (n + 1) * (fnp1 - fs) + L / 2 * (xnp1 - xs) ** 2

    # Set the performance metric to the difference between the initial and the final Lyapunov
    problem.set_performance_metric(final_lyapunov - init_lyapunov)

    # Solve the PEP
    pepit_tau = problem.solve(verbose=verbose)

    # Compute theoretical guarantee (for comparison)
    if gamma == 1/L:
        theoretical_tau = 0.
    else:
        theoretical_tau = None


    # Print conclusion if required
    if verbose:
        print('*** Example file:'
              ' worst-case performance of gradient descent with fixed step-size for a given Lyapunov function***')
        print('\tPEP-it guarantee:\t\t'
              'V_(n+1) - V_(n) <= {:.6}'.format(pepit_tau))
        if gamma==1/L:
            print('\tTheoretical guarantee:\t'
                  'V_(n+1) - V_(n) <= {:.6}'.format(theoretical_tau))

    # Return the worst-case guarantee of the evaluated method (and the reference theoretical value)
    return pepit_tau, theoretical_tau


if __name__ == "__main__":

    L = 1
    gamma = 1 / L
    pepit_tau, theoretical_tau = wc_gradient_descent_lyapunov_1(L=L, gamma=gamma, n=10, verbose=True)
