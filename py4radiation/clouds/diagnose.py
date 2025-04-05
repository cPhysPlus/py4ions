#!/usr/bin/env python3

import os
import numpy as np

from .cloud_cuts import CloudCuts
from .cloud_diagnostics import CloudDiagnostics

class Diagnose():
    """

    Get a diagnosis of cloud gas in a VTK simulation file

    """

    def __init__(self, fields_sim1, shape, box):
        self.shape
        box_x, box_y, box_z = box

        x = np.linspace(box_x[0], box_x[1], shape[0])
        y = np.linspace(box_y[0], box_y[1], shape[1])
        z = np.linspace(box_z[0], box_z[1], shape[2])

        self.j3D = [x.reshape(-1, 1, 1), y.reshape(1, -1, 1), z.reshape(1, 1, -1)]

        self.dV = ((np.max(x) - np.min(x)) / shape[0])**3

        rho, tr1, _, _, _, _ = fields_sim1

        self.M0 = np.sum(rho * tr1) * divmod

    def get_sim_diagnostics(self, fields):
        diagnostics = CloudDiagnostics(self.j3D, self.dV, self.M0)
        return diagnostics.diagnose(fields)

    def get_cuts(self, fields, sinnum):
        cuts = CloudCuts(fields, sinnum, self.shape)
        cuts.get_ncuts()
        cuts.get_vcuts()