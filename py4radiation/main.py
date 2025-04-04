#!/usr/bin/env python3

import os
import argparse
from configparser import ConfigParser

import numpy as np
import pandas as pd

from .simload import simload
from radiation.prepare_sed import SED
from radiation.parfiles import ParameterFiles
from synthetic.observables import SyntheticObservables

def main():
    parser = argparse.ArgumentParser(
        prog = 'py4radiation',
        description = 'UV radiation effects into HD/MHD wind-cloud simulations'
    )

    parser.add_argument('-f', type='str', required=True, help='CONFIG file')

    file = parser.parse_args()
    conf = ConfigParser()
    conf.read(file.f)

    mode = int(conf['MODE']['mode'])

    if mode == 0:
        print('PHOTOIONISATION + RADIATIVE HEATING & COOLING mode')

        redshift = conf['RADIATION']['redshift']

        if conf['RADIATION']['sedfile'] != None:
            sedfile = conf['RADIATION']['sedfile']
            distance = conf['RADIATION']['distance']
            age      = conf['RADIATION']['age']

            sed = SED(sedfile, distance, redshift, age)
            sed.getFile()

        cloudypath = conf['RADIATION']['cloudypath']
        run_name   = conf['RADIATION']['runname']
        elements   = conf['RADIATION']['elements']
        resolution = conf['RADIATION']['resolution']

        parfiles = ParameterFiles(cloudypath, run_name, elements, redshift, resolution)
        parfiles.getIonFractions()
        parfiles.getHeatingCooling()

    elif mode == 1:
        print('SYNTHETIC OBSERVABLES mode')

        simpath = conf['SYNTHETIC']['simpath']
        simfile = conf['SYNTHETIC']['simfile']
        ions    = pd.read_csv(conf['SYNTHETIC']['ionsfile'], sep=r'\s+', header=None).to_numpy()
        units   = pd.read_csv(conf['SYNTHETIC']['unitsfile'], sep=r'\s+', header=None).to_numpy()[1]

        fields, shape = simload(simfile)
        observables = SyntheticObservables(fields, shape, ions, units)
        observables.get_column_densities()
        observables.get_mock_spectra()