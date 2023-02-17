#!/usr/bin/env python3
import time
import requests
import csv
import os
from argparse import ArgumentParser
from math import sqrt

def get_voltages_pi():
    IP_pi = '130.60.164.209'
    return requests.get('http://%s:8080/read' % IP_pi).json()

def get_average(measurements):
    n = len(measurements)
    return sum(measurements)/n

def get_stdev(measurements):
    average = get_average(measurements)
    diffs_squared = [(m-average)**2 for m in measurements]
    n = len(measurements)
    return sqrt(sum(diffs_squared)/(n-1))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--filename', '-f', default=None)
    args = parser.parse_args()

    if args.filename is not None and args.filename[-4:] != '.csv': 
        args.filename += '.csv'

    header_str  = '    Time-stamp     '
    header_str += '     VIN '
    header_str += '     vdda0'
    header_str += '     vddd0'
    header_str += '     vdda1'
    header_str += '     vddd1'
    header_str += '     vdda2'
    header_str += '     vddd2'
    header_str += '     vdda3'
    header_str += '     vddd3'

    voltages_to_csv = [['time-stamp','vin','vdda0','vddd0','vdda1','vddd1','vdda2','vddd2','vdda3','vddd3']]

    if args.filename is None: max_printouts = 100
    else: max_printouts = 5

    n_printouts = 0
    while n_printouts < max_printouts:
        if not n_printouts%10:
            print('-'*110)
            print(header_str)
            print('-'*110)
        n_printouts += 1
        time.sleep(3)
        localtime = time.localtime()
        time_str = time.strftime("%Y/%m/%d %H:%M:%S", localtime)
        voltages = get_voltages_pi()
        vin   = (voltages[ '7'] - voltages[ '8'])*1e-3
        vdda0 = (voltages['13'] - voltages['14'])*1e-3
        vddd0 = (voltages['12'] - voltages['14'])*1e-3
        vdda1 = (voltages['10'] - voltages['11'])*1e-3
        vddd1 = (voltages[ '9'] - voltages['11'])*1e-3
        vdda2 = (voltages[ '5'] - voltages[ '6'])*1e-3
        vddd2 = (voltages[ '4'] - voltages[ '6'])*1e-3
        vdda3 = (voltages[ '2'] - voltages[ '3'])*1e-3
        vddd3 = (voltages[ '1'] - voltages[ '3'])*1e-3
        voltages_str = f'{time_str}    {vin:4.3f}    '
        voltages_str+= f'{vdda0:4.3f}    {vddd0:4.3f}    '
        voltages_str+= f'{vdda1:4.3f}    {vddd1:4.3f}    '
        voltages_str+= f'{vdda2:4.3f}    {vddd2:4.3f}    '
        voltages_str+= f'{vdda3:4.3f}    {vddd3:4.3f}    '
        print(voltages_str)
        voltages_to_csv.append([time_str,vin,vdda0,vddd0,vdda1,vddd1,vdda2,vddd2,vdda3,vddd3])
    
    if args.filename is not None:
        averages = [0. for icol in range(len(voltages_to_csv[-1]))]
        stdevs = [0. for icol in range(len(voltages_to_csv[-1]))]
        averages[0] = 'average'
        stdevs[0] = 'stdev'
        for icol in range(1,len(averages)):
            col = [voltages_to_csv[irow][icol] for irow in range(1,len(voltages_to_csv))]
            averages[icol] = get_average(col)
            stdevs[icol] = get_stdev(col)
        voltages_to_csv.append(averages)
        voltages_to_csv.append(stdevs)
        print('-'*110)
        averages_str = f'average               {averages[1]:4.3f}+/-{stdevs[1]:4.3f}   '
        averages_str+= f'{averages[2]:4.3f}+/-{stdevs[2]:4.3f}    {averages[3]:4.3f}+/-{stdevs[3]:4.3f}    '
        averages_str+= f'{averages[4]:4.3f}+/-{stdevs[4]:4.3f}    {averages[5]:4.3f}+/-{stdevs[5]:4.3f}    '
        averages_str+= f'{averages[6]:4.3f}+/-{stdevs[6]:4.3f}    {averages[7]:4.3f}+/-{stdevs[7]:4.3f}    '
        averages_str+= f'{averages[8]:4.3f}+/-{stdevs[8]:4.3f}    {averages[9]:4.3f}+/-{stdevs[9]:4.3f}    '
        print(averages_str)
        if os.path.isfile(args.filename):
            filename = args.filename.replace('.csv','_%s.csv')  
            i_file = 1
            while os.path.isfile(filename % i_file):
                i_file += 1
            filename = filename % i_file
        else:
            filename = args.filename
        with open(filename,'w') as f:
            writer = csv.writer(f)
            for row in voltages_to_csv:
                writer.writerow(row)
        print('-'*110)
        print('saved output to "%s"\n' % filename)
