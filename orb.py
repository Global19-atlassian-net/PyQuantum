from mayavi import mlab
from matplotlib import rcParams
from mpl_toolkits.axes_grid1 import make_axes_locatable
import warnings  # in order to suppress divide_by_zero warnings...
from sympy import symbols, I, latex, pi, diff
from sympy.functions import Abs, sqrt, exp, cos, sin
from sympy import init_printing
from IPython import __version__ as IPython_version
from sympy import re, im, simplify
from sympy import factorial as fac
from sympy.utilities.lambdify import lambdastr
import sympy
import numpy as np
from IPython.display import Latex
import sys  # texting for the right version of Python to use with mayavi
print("Python version = {}".format(sys.version))
print("Machine readable Python version = {}".format(sys.version_info))
sys.version_info[0]

print("The library version numbers used in this notebook are:")
if sys.version_info[0] == 2:
    from mayavi import __version__ as mayavi_version
    from mayavi import mlab
    print("mayavi version:  %s" % mayavi_version)
else:
    print("The use of mayavi.mlab to display the orbital requires the " +
          "use of Python 2.7.3")


init_printing(use_unicode=True)

a_0, z, r = symbols("a_0,z,r")
n, m, l = symbols("n,m,l", integer=True)
int_m = symbols("int_m", integer=True)
theta, phi = symbols("\\theta,\\phi", real=True)

# The variables will used with lambdify...
angle_theta, angle_phi, radius = symbols("angle_theta,angle_phi,radius",
                                         real=True)


print("numpy version:   %s" % np.__version__)
print("sympy version:   %s" % sympy.__version__)

print("IPython version: %s" % IPython_version)


def P_l(l, theta):  # valid for l greater than equal to zero
    """Legendre polynomial"""
    if l >= 0:
        eq = diff((cos(theta)**2-1)**l, cos(theta), l)
    else:
        print("l must be an integer equal to 0 or greater")
        raise ValueError
    return 1/(2**l*fac(l))*eq


def P_l_m(m, l, theta):
    """Legendre polynomial"""
    eq = diff(P_l(l, theta), cos(theta), Abs(m))
    result = sin(theta)**Abs(m)*eq  # note 1-cos^2(theta) = sin^2(theta)
    return result


def Y_l_m(l, m, phi, theta):
    """Spherical harmonics"""
    eq = P_l_m(m, l, theta)
    if m > 0:
        pe = re(exp(I*m*phi))*sqrt(2)
    elif m < 0:
        pe = im(exp(I*m*phi))*sqrt(2)
    elif m == 0:
        pe = 1
    return abs(sqrt(((2*l+1)*fac(l-Abs(m)))/(4*pi*fac(l+Abs(m))))*pe*eq)


def L(l, n, rho):
    """Laguerre polynomial"""
    _L = 0.
    for i in range((n-l-1)+1):  # using a loop to do the summation
        _L += ((-i)**i*fac(n+l)**2.*rho**i)/(fac(i)*fac(n-l-1.-i) *
                                             fac(2.*l+1.+i))
    return _L


def R(r, n, l, z=1., a_0=1.):
    """Radial function"""
    rho = 2.*z*r/(n*a_0)
    _L = L(l, n, rho)
    _R = (2.*z/(n*a_0))**(3./2.)*sqrt(fac(n-l-1.) /
                                      (2.*n*fac(n+l)**3.))*exp(-z/(n*a_0)*r)*rho**l*_L
    return _R


def Psi(r, n, l, m, phi, theta, z=1, a_0=1):
    """Wavefunction"""
    _Y = Y_l_m(l, m, phi, theta)
    _R = R(r, n, l)
    return _R*_Y


def P(r, n, l, m, phi, theta):
    """Returns the symbolic equation probability of the location 
    of an electron"""
    return Psi(r, n, l, m, phi, theta)**2*r**2


def r_fun(_x, _y, _z): return (np.sqrt(_x**2+_y**2+_z**2))


def theta_fun(_x, _y, _z): return (np.arccos(_z/r_fun(_x, _y, _z)))


def phi_fun(_x, _y, _z): return (np.arctan(_y/_x)*(1+_z-_z))


def display_orbital(n, l, m_, no_of_contours=16, Opaque=0.5):
    """Diplays a 3D view of electron orbitals"""
    # The plot density settings (don't mess with unless you are sure)
    rng = 12*n*1.5  # This determines the size of the box
    _steps = 55j  # (it needs to be bigger with n).
    _x, _y, _z = np.ogrid[-rng:rng:_steps, -rng:rng:_steps, -rng:rng:_steps]

    # Plot tweaks
    color = (0, 1.0, 1.0)  # relative RGB color (0-1.0 vs 0-255)
    mlab.figure(bgcolor=color)  # set the background color of the plot

    P_tex = ""  # initialize the LaTex string of the probabilities

    # Validate the quantum numbers
    # validate the value of n
    assert(n >= 1), "n must be greater or equal to 1"
    # validate the value of l
    assert(0 <= l <= n-1), "l must be between 0 and n-1"
    # validate the value of p
    assert(-l <= max(m_) <= l), "p must be between -l and l"
    # validate the value of p
    assert(-l <= min(m_) <= l), "p must be between -l and l"

    for m in m_:
        # Determine the probability equation symbolically and convert
        # it to a string
        prob = lambdastr((radius, angle_phi, angle_theta), P(radius, n, l, m,
                                                             angle_phi,
                                                             angle_theta))

        # record the probability equation as a LaTex string
        P_eq = simplify(P(r, n, l, m, phi, theta))
        P_tex += "$$P ="+latex(P_eq)+"$$ \n\n "

        # print("prob before substitution = \n\n".format(prob)) #for debugging

        if '(nan)' in prob:  # Check for errors in the equation
            print("There is a problem with the probability function.")
            raise ValueError

        # Convert the finctions in the probability equation from the sympy
        # library to the numpy library to allow for the use of matrix
        # calculations
        prob = prob.replace('sin', 'np.sin')  # convert to numpy
        prob = prob.replace('cos', 'np.cos')  # convert to numpy
        prob = prob.replace('Abs', 'np.abs')  # convert to numpy
        prob = prob.replace('pi', 'np.pi')  # convert to numpy
        prob = prob.replace('exp', 'np.exp')  # convert to numpy

        # print("prob after substitution = \n\n".format(prob)) #for debugging

        # convert the converted string to a callable function
        Prob = eval(prob)

        # generate a set of data to plot the contours of.
        w = Prob(r_fun(_x, _y, _z), phi_fun(_x, _y, _z), theta_fun(_x, _y, _z))

        # add the generated data to the plot
        mlab.contour3d(w, contours=no_of_contours,
                       opacity=Opaque, transparent=True)

    mlab.colorbar()
    mlab.outline()
    mlab.show()  # this pops up a interactive window that allows you to
    #            rotate the view

    # Information used for the 2D slices below
    limits = []
    lengths = []
    for cor in (_x, _y, _z):
        limit = (np.min(cor), np.max(cor))
        limits.append(limit)
        # print(np.size(cor))
        lengths.append(np.size(cor))
        # print(limit)
    return (limits, lengths, _x, _y, _z, P_tex)


def r_fun(_x, _y, _z): return (np.sqrt(_x**2+_y**2+_z**2))


def theta_fun(_x, _y, _z): return (np.arccos(_z/r_fun(_x, _y, _z)))


def phi_fun(_x, _y, _z): return (np.arctan(_y/_x)*(1+_z-_z))


def display_orbital(n, l, m_, no_of_contours=16, Opaque=0.5):
    """Diplays a 3D view of electron orbitals"""
    # The plot density settings (don't mess with unless you are sure)
    rng = 12*n*1.5  # This determines the size of the box
    _steps = 55j  # (it needs to be bigger with n).
    _x, _y, _z = np.ogrid[-rng:rng:_steps, -rng:rng:_steps, -rng:rng:_steps]

    # Plot tweaks
    color = (0, 1.0, 1.0)  # relative RGB color (0-1.0 vs 0-255)
    mlab.figure(bgcolor=color)  # set the background color of the plot

    P_tex = ""  # initialize the LaTex string of the probabilities

    # Validate the quantum numbers
    # validate the value of n
    assert(n >= 1), "n must be greater or equal to 1"
    # validate the value of l
    assert(0 <= l <= n-1), "l must be between 0 and n-1"
    # validate the value of p
    assert(-l <= max(m_) <= l), "p must be between -l and l"
    # validate the value of p
    assert(-l <= min(m_) <= l), "p must be between -l and l"

    for m in m_:
        # Determine the probability equation symbolically and convert
        # it to a string
        prob = lambdastr((radius, angle_phi, angle_theta), P(radius, n, l, m,
                                                             angle_phi,
                                                             angle_theta))

        # record the probability equation as a LaTex string
        P_eq = simplify(P(r, n, l, m, phi, theta))
        P_tex += "$$P ="+latex(P_eq)+"$$ \n\n "

        # print("prob before substitution = \n\n".format(prob)) #for debugging

        if '(nan)' in prob:  # Check for errors in the equation
            print("There is a problem with the probability function.")
            raise ValueError

        # Convert the finctions in the probability equation from the sympy
        # library to the numpy library to allow for the use of matrix
        # calculations
        # prob = prob.replace('sin', 'np.sin')  # convert to numpy
        # prob = prob.replace('cos', 'np.cos')  # convert to numpy
        # prob = prob.replace('Abs', 'np.abs')  # convert to numpy
        # prob = prob.replace('pi', 'np.pi')  # convert to numpy
        # prob = prob.replace('exp', 'np.exp')  # convert to numpy

        # print("prob after substitution = \n\n".format(prob)) #for debugging

        # convert the converted string to a callable function
        Prob = eval(prob)

        # generate a set of data to plot the contours of.
        w = Prob(r_fun(_x, _y, _z), phi_fun(_x, _y, _z), theta_fun(_x, _y, _z))

        # add the generated data to the plot
        mlab.contour3d(w, contours=no_of_contours,
                       opacity=Opaque, transparent=True)

    mlab.colorbar()
    mlab.outline()
    mlab.show()  # this pops up a interactive window that allows you to
    #            rotate the view

    # Information used for the 2D slices below
    limits = []
    lengths = []
    for cor in (_x, _y, _z):
        limit = (np.min(cor), np.max(cor))
        limits.append(limit)
        # print(np.size(cor))
        lengths.append(np.size(cor))
        # print(limit)
    return (limits, lengths, _x, _y, _z, P_tex)


#    Set the quantum numbers for the orbitals (all in one spot)

print("n must be greater or equal to 1.")
n = int(input("Entry the quantum number for n = "))

print("")
l_str = input(
    "Enter a value for l such that it is less than n (default l=n-1) l = ")
if l_str == "":
    l = n-1
else:
    l = int(l_str)

print("\nThe next value, m, determines which specific orbital will be displayed.")
print("Enter a value(s) for m such that -l <= m <= l.\n" +
      "m can be a single number for a single orbital or a range for multiple.")
m_str = input("Enter a number like, 2, or a range like, -2, 2.  m = ")
if "," in m_str:
    _m = eval("("+m_str+")")
    m_ = range(_m[0], _m[1]+1, 1)
else:
    m_ = [int(m_str)]

print("\nElectron orbitals are traditionally displayed at a 95% confidence interval.  ")
print("The isosurface you would see is at a P value that depends on the principal ")
print("quantum number and the shape of the orbital.  They are analogous to the height ")
print("on a normal probability density function plot.  In displaying this surface ")
print("the mayavi library is picking the confidence interval value for you, however ")
print("some control can be had by setting number of isosuface contours.  ")
print
print("I have found that 16 is a good place to start, however on older computers there ")
print("may be a problem rendering more than 7.")
n_o_c = input(
    "\nEnter the number of isosurface contours to be displayed:[Default = 16] ")
if n_o_c == "":
    n_o_c = 16
else:
    n_o_c = abs(int(n_o_c))
print("\nIn order to see the various probability surfaces you can set the opacity of the ")
print("plot from 0 to 1")
opacity = input(
    "Enter the opacity of the orbital plot:[Range 0 - 1, Default = 0.5] ")
if opacity == "":
    opacity = 0.5
else:
    opacity = abs(float(opacity))
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    limits, lengths, _x, _y, _z, P_tex = display_orbital(
        n, l, m_, n_o_c, opacity)

txt = r"$$\textbf{The symbolic expression for the resulting probability equation is:}$$ "
Latex(txt+P_tex)


# rcParams.update({'font.size': 12, 'font.family': 'serif'})
length = max(lengths)
# print(length)
x0, x1, y0, y1 = (-length/2, length/2)*2


def demo():
    # Figure sizes
    fig_x = 12
    fig_y = 24

    fig1 = plt.figure(1, figsize=(fig_x, fig_y))
    ax = []
    for index, plane in enumerate(['xy', 'yz', 'xz']):
        ax.append(fig1.add_subplot(3, 1, index+1))
        ax[index].set_title('%s Plane' % plane)
        ax[index].set_xlabel(plane[0])
        ax[index].set_ylabel(plane[1])
        result, Prob = orbital_plane(plane)
        im = ax[index].imshow(result, origin='lower',
                              extent=[x0, x1, y0, y1])

        plt.colorbar(im)
        plt.tight_layout()

    plt.draw()
    plt.show()
    return result


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    result = demo()
