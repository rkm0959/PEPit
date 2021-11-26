from PEPit.pep import PEP
from PEPit.operators.monotone import MonotoneOperator
from PEPit.primitive_steps.proximal_step import proximal_step


def wc_ppm(alpha, n, verbose=True):
    """
    Consider the monotone inclusion problem

        .. math:: \\text{Find} \ x, 0 \in Ax,

    where :math:`A` is maximally monotone. We denote :math:`J_A = (I + A)^{-1}` the resolvents of :math:`A`.

    This code computes a worst-case guarantee for the **accelerated proximal point** method, that is the smallest
    possible :math:`\\tau(n)` such that the guarantee

        .. math:: ||x_n - y_n||^2 \\leqslant \\tau(n) || x_0 - x_\star||^2,

    is valid, where :math:`x_\star` is such that :math:`0 \\in Ax_\star`.

    **Algorithm**:

        .. math:: x_{i+1} = J_{\\alpha A}(y_i)

        .. math y_{i+1} = x_{i+1} + \\frac{i}{i+2}(x_{i+1} - x_{i}) - \\frac{i}{i+1}(x_i - y_{i-1})

    **Theoretical guarantee**:

    Theoretical rates can be found in the following paper (section 4, Theorem 4.1)

        .. math:: ||x_n - y_n||^2 \\leqslant  \\frac{1}{n^2}  || x_0 - x_\star||^2

    **Reference**:

    [1] Donghwan Kim. "Accelerated Proximal Point Method  and Forward Method
    for Monotone Inclusions." (2019)

    Args:
        alpha (float): the step size
        n (int): number of iterations.
        verbose (bool, optional): if True, print conclusion

    Returns:
        tuple: worst_case value, theoretical value

    Example:
        >>> pepit_tau, theoretical_tau = wc_ppm(2, 10)
        (PEP-it) Setting up the problem: size of the main PSD matrix: 12x12
        (PEP-it) Setting up the problem: performance measure is minimum of 1 element(s)
        (PEP-it) Setting up the problem: initial conditions (1 constraint(s) added)
        (PEP-it) Setting up the problem: interpolation conditions for 1 function(s)
                 function 1 : 110 constraint(s) added
        (PEP-it) Compiling SDP
        (PEP-it) Calling SDP solver
        (PEP-it) Solver status: optimal (solver: SCS); optimal value: 0.010001764316228073
        *** Example file: worst-case performance of the Accelerated Proximal Point Method***
            PEP-it guarantee:	 ||x_n - y_n||^2 <= 0.0100018 ||x_0 - x_s||^2
            Theoretical guarantee :	 ||x_n - y_n||^2 <= 0.01 ||x_0 - x_s||^2
    """

    # Instantiate PEP
    problem = PEP()

    # Declare a monotone operator
    A = problem.declare_function(MonotoneOperator, param={})

    # Start by defining its unique optimal point xs = x_*
    xs = A.stationary_point()

    # Then define the starting point x0 of the algorithm and its function value f0
    x0 = problem.set_initial_point()

    # Set the initial constraint that is the distance between x0 and x^*
    problem.set_initial_condition((x0 - xs) ** 2 <= 1)

    # Compute n steps of the Proximal Gradient method starting from x0
    x = [x0 for _ in range(n + 1)]
    y = [x0 for _ in range(n + 1)]
    for i in range(0, n - 1):
        x[i + 1], _, _ = proximal_step(y[i + 1], A, alpha)
        y[i + 2] = x[i + 1] + i / (i + 2) * (x[i + 1] - x[i]) - i / (i + 2) * (x[i] - y[i])
    x[n], _, _ = proximal_step(y[n], A, alpha)

    # Set the performance metric to the distance between xn and yn
    problem.set_performance_metric((x[n] - y[n]) ** 2)

    # Solve the PEP
    pepit_tau = problem.solve(verbose=verbose)

    # Compute theoretical guarantee (for comparison)
    theoretical_tau = 1 / n ** 2

    # Print conclusion if required
    if verbose:
        print('*** Example file: worst-case performance of the Accelerated Proximal Point Method***')
        print('\tPEP-it guarantee:\t ||x_n - y_n||^2 <= {:.6} ||x_0 - x_s||^2'.format(pepit_tau))
        print('\tTheoretical guarantee :\t ||x_n - y_n||^2 <= {:.6} ||x_0 - x_s||^2 '.format(theoretical_tau))

    # Return the worst-case guarantee of the evaluated method ( and the reference theoretical value)
    return pepit_tau, theoretical_tau


if __name__ == "__main__":
    alpha = 2
    n = 10

    pepit_tau, theoretical_tau = wc_ppm(alpha=alpha,
                                        n=n)
