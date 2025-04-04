#!/usr/bin/env python3

import os
import argparse
from configparser import ConfigParser

import numpy as np
import pandas as pd

from radiation.prepare_sed import SED
from radiation.parfiles import ParameterFiles

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

        redshift = conf['radiation']['redshift']

        if conf['radiation']['sedfile'] != None:
            sedfile = conf['radiation']['sedfile']
            distance = conf['radiation']['distance']
            age      = conf['radiation']['age']

            sed = SED(sedfile, distance, redshift, age)
            sed.getFile()

        cloudypath = conf['radiation']['cloudypath']
        run_name   = conf['radiation']['runname']
        elements   = conf['radiation']['elements']
        resolution = conf['radiation']['resolution']

        parfiles = ParameterFiles(cloudypath, run_name, elements, redshift, resolution)
        parfiles.getIonFractions()
        parfiles.getHeatingCooling()