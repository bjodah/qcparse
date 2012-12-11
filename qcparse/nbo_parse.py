#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script for parsing spin density per atom from Natural Bond Orbitals population
analysis (Natural Population Analysis) generated by NBO 3.0 using Gaussian 09.
Written by Björn Dahlgren for use in MSc Thesis at KTH Royal Institute of Technology
"""

import sys
import numpy as np


def parse_atoms(src):
    trigger = ' Summary of Natural Population Analysis:'

    res = []

    recording = -1
    for line in file(src):
        if recording > 0:
            # Hadle lines between trigger and data
            recording -= 1
            continue
        if line.startswith(trigger):
            recording = 5
        if recording == 0:
            if '===' in line:
                # End of parsing
                recording = -1
                break
            splt = line.split()
            res.append(str(splt[0]).strip())
    return res

def parse_partial_charge_per_atom(src):
    trigger = ' Summary of Natural Population Analysis:'

    res = []

    recording = -1
    for line in file(src):
        if recording > 0:
            # Hadle lines between trigger and data
            recording -= 1
            continue
        if line.startswith(trigger):
            recording = 5
        if recording == 0:
            if '===' in line:
                # End of parsing
                recording = -1
                break
            splt = line.split()
            res.append(float(splt[2]))
    return np.array(res)


def parse_ab_pop_per_atom(src):
    trigger = ' Summary of Natural Population Analysis:'
    #tokens = ['Atom', 'No', 'Natural Electron Configuration']

    a = 'Alpha spin orbitals'
    b = 'Beta  spin orbitals'
    a_or_b = ''

    res = {}
    res['a'] = []
    res['b'] = []

    recording = -1
    for line in file(src):
        if recording > 0:
            # Hadle lines between trigger and data
            recording -= 1
            continue
        if a in line:
            assert recording == -1
            a_or_b = 'a'
        elif b in line:
            assert recording == -1
            a_or_b = 'b'
        if line.startswith(trigger):
            if a_or_b in ['a', 'b']:
                recording = 5
        if recording == 0:
            if '===' in line:
                # End of parsing
                recording = -1
                continue
            splt = line.split()
            res[a_or_b].append(float(splt[6]))
    return np.array(res['a']) - np.array(res['b'])

if __name__ == '__main__':
    print parse_ab_pop_per_atom(sys.argv[1])
