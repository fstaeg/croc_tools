#!/usr/bin/env python3
import os
from argparse import ArgumentParser
from adc_tools import ADCtoVoltage, ADCtoCurrent, read_muxscan

parser = ArgumentParser()
parser.add_argument('--module', '-m')
parser.add_argument('--input', '-i')
args = parser.parse_args()

input_file = os.path.join(args.input, 'muxScan.csv')

res = read_muxscan(input_file, muxvals=['VDDA_HALF', 'VDDD_HALF'])

for chip in res.keys():
    vdda = ADCtoVoltage(2*res[chip]['VDDA_HALF'], args.module, chip)
    vddd = ADCtoVoltage(2*res[chip]['VDDD_HALF'], args.module, chip)
    print('\n'+chip)
    print('VDDA = %.3f, VDDD = %.3f' % (vdda, vddd))

