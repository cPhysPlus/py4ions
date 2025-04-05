#!/usr/bin/env python3

import numpy as np

class CloudCuts():
    """

    Create velocity and number density cuts from a VTK simulation file

    :fields: numpy array

        Scalar/vector fields from a VTK simulation file

    :shape: tuple

        Shape of the computational box of the simulation file

    """

    def __init__(self, simnum, fields, shape):
        rho, _, _, vx, vy, vz = fields
        self.rho = rho
        self.v   = np.sqrt(vx**2 + vy**2 + vz**2)

        self.cut = int((shape[2] / 2) - 1)

    def get_ncuts(self):
        """

        Get a number density cut of a single simulation file

        """
        mu = 0.6724418
        mm = 1.660e-24

        n = self.rho / (mm * mu)
        nz0 = n[:, :, self.cut]

        nfile = 'ncut_' + self.nsim + '.dat'
        n_arr = '\n'.join(['\t'.join(map(str, row)) for row in nz0])
        with open(nfile, 'w') as fn:
            fn.write(n_arr)

    def get_vcuts(self):
        """

        Get a velocity cut of a single simulation file
        
        """
        v = self.v
        vz0 = v[:, :, self.cut]

        vfile = 'vcut_' + self.nsim + '.dat'
        v_arr = '\n'.join(['\t'.join(map(str, row)) for row in vz0])
        with open(vfile, 'w') as fv:
            fv.write(v_arr)