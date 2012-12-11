#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse
from cclib.parser import ccopen
from cclib.parser.utils import PeriodicTable
import logging


def get_xyz_block_from_log(logfile_path):
    myfile = ccopen(logfile_path,loglevel=logging.WARN)
    data   = myfile.parse()
    lines = get_last_coord_block_str(logfile_path, data = data).split('\n')
    scfener = data.scfenergies[-1]
    result = '{0: >5d}\n'.format(len(lines))
    result +=  'scf done:{0: >13.6f}\n'.format(scfener)
    for l in lines:
        result += ' ' + l + '\n'
    return result

def get_last_coord_block_str(log,step=None, data = None):
    """
    Open gaussian log file and prints last coordinates of atoms
    as a block for creating new input file.
    """
    if data == None:
        myfile = ccopen(log,loglevel=logging.WARN)
        data   = myfile.parse()

    if not step:
        coords = data.atomcoords[-1]
    else:
        coords = data.atomcoords[step]
    rows = []
    t = PeriodicTable()
    for i in range(len(coords)):
        strrow_l        = [t.element[data.atomnos[i]]]
        strrow_l.extend(['{0: >12.6f}'.format(x) for x in coords[i]])
        rows.append(''.join(strrow_l))
    coord_block = '\n'.join(rows + [''])
    return coord_block

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, epilog="Documentation will improve.. Promise!")
    parser.add_argument('log', type=str, help='Gaussian logfile')
    parser.add_argument('--step',type=int,default=-1,help='Coordinate step number, starting from 0')
    args = parser.parse_args()
    print get_last_coord_block_str(**vars(args))
