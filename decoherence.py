import os
import logging.config
from logging.config import fileConfig
import qutip as qt
import numpy as np
import matplotlib.pyplot as plt

if not os.path.isdir('logs'):
    os.makedirs('logs')
if not os.path.isfile('logs/python.log'):
    os.mknod('logs/python.log')

logger = logging.getLogger(__name__)
fileConfig('logger.ini')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logger.info("It's show time")

delta = 0.2 * 2*np.pi
eps0 = 1.0 * 2*np.pi
gamma1 = 0.5

H = - delta/2.0 * qt.sigmax() - eps0/2.0 * qt.sigmaz()


def ohmic_spectrum(w):
    if w == 0.0: # dephasing inducing noise
        return gamma1
    else: # relaxation inducing noise
        return gamma1 / 2 * (w / (2 * np.pi)) * (w > 0.0)


R, ekets = qt.bloch_redfield_tensor(H, [qt.sigmax()], [ohmic_spectrum])

"""
Last part
"""

tlist = np.linspace(0, 15.0, 1000)

psi0 = qt.rand_ket(2)
e_ops = [qt.sigmax(), qt.sigmay(), qt.sigmaz()]
expt_list = qt.bloch_redfield_solve(R, ekets, psi0, tlist, e_ops)

sphere = qt.Bloch()
sphere.add_points([expt_list[0], expt_list[1], expt_list[2]])
sphere.vector_color = ['r']
sphere.add_vectors(np.array([delta, 0, eps0]) / np.sqrt(delta ** 2 + eps0 ** 2))
sphere.make_sphere()

plt.show()

logger.info('You have been terminated')
