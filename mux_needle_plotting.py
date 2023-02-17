#!/usr/bin/env python
import csv
import ROOT
import numpy as np
from collections import OrderedDict
from adc_tools import ADCtoVoltage, ADCtoCurrent, read_muxscan, read_needlecard
from plotting_tools import set_style, draw_graphs, draw_histograms
    
ROOT.gROOT.SetBatch(ROOT.kTRUE)
set_style()

input_files = OrderedDict([
    ('T03_standalone', {
        'muxscan': OrderedDict([
            (12.0, 'measurements/T03_standalone/muxscan/MuxScan/muxScan.csv'),
            (11.5, 'measurements/T03_standalone/muxscan/MuxScan_1/muxScan.csv'),
            (11.0, 'measurements/T03_standalone/muxscan/MuxScan_2/muxScan.csv'),
            (10.5, 'measurements/T03_standalone/muxscan/MuxScan_3/muxScan.csv'),
            (10.0, 'measurements/T03_standalone/muxscan/MuxScan_4/muxScan.csv'),
            (9.5, 'measurements/T03_standalone/muxscan/MuxScan_5/muxScan.csv'),
            (9.0, 'measurements/T03_standalone/muxscan/MuxScan_6/muxScan.csv'),
            (8.5, 'measurements/T03_standalone/muxscan/MuxScan_7/muxScan.csv'),
            (8.0, 'measurements/T03_standalone/muxscan/MuxScan_8/muxScan.csv'),
            (7.5, 'measurements/T03_standalone/muxscan/MuxScan_9/muxScan.csv'),
            (7.0, 'measurements/T03_standalone/muxscan/MuxScan_10/muxScan.csv'),
            (6.5, 'measurements/T03_standalone/muxscan/MuxScan_11/muxScan.csv'),
            (6.0, 'measurements/T03_standalone/muxscan/MuxScan_12/muxScan.csv'),
            (5.5, 'measurements/T03_standalone/muxscan/MuxScan_13/muxScan.csv'),
            (5.0, 'measurements/T03_standalone/muxscan/MuxScan_14/muxScan.csv'),
            (4.5, 'measurements/T03_standalone/muxscan/MuxScan_15/muxScan.csv')
            ])
        }),
    ('T05_standalone', {
        'muxscan': OrderedDict([
            (12.0, 'measurements/T05_standalone/muxscan/MuxScan/muxScan.csv'),
            (11.5, 'measurements/T05_standalone/muxscan/MuxScan_1/muxScan.csv'),
            (11.0, 'measurements/T05_standalone/muxscan/MuxScan_2/muxScan.csv'),
            (10.5, 'measurements/T05_standalone/muxscan/MuxScan_3/muxScan.csv'),
            (10.0, 'measurements/T05_standalone/muxscan/MuxScan_4/muxScan.csv'),
            (9.5, 'measurements/T05_standalone/muxscan/MuxScan_5/muxScan.csv'),
            (9.0, 'measurements/T05_standalone/muxscan/MuxScan_6/muxScan.csv'),
            (8.5, 'measurements/T05_standalone/muxscan/MuxScan_7/muxScan.csv'),
            (8.0, 'measurements/T05_standalone/muxscan/MuxScan_8/muxScan.csv'),
            (7.5, 'measurements/T05_standalone/muxscan/MuxScan_9/muxScan.csv'),
            (7.0, 'measurements/T05_standalone/muxscan/MuxScan_10/muxScan.csv'),
            (6.5, 'measurements/T05_standalone/muxscan/MuxScan_11/muxScan.csv'),
            (6.0, 'measurements/T05_standalone/muxscan/MuxScan_12/muxScan.csv'),
            (5.5, 'measurements/T05_standalone/muxscan/MuxScan_13/muxScan.csv'),
            (5.0, 'measurements/T05_standalone/muxscan/MuxScan_14/muxScan.csv'),
            (4.5, 'measurements/T05_standalone/muxscan/MuxScan_15/muxScan.csv')
            ]),
        'needlecard': OrderedDict([
            (12.0, 'measurements/T05_standalone/needlecard/T05_12p0.csv'),
            (11.5, 'measurements/T05_standalone/needlecard/T05_11p5.csv'),
            (11.0, 'measurements/T05_standalone/needlecard/T05_11p0.csv'),
            (10.5, 'measurements/T05_standalone/needlecard/T05_10p5.csv'),
            (10.0, 'measurements/T05_standalone/needlecard/T05_10p0.csv'),
            (9.5, 'measurements/T05_standalone/needlecard/T05_09p5.csv'),
            (9.0, 'measurements/T05_standalone/needlecard/T05_09p0.csv'),
            (8.5, 'measurements/T05_standalone/needlecard/T05_08p5.csv'),
            (8.0, 'measurements/T05_standalone/needlecard/T05_08p0.csv'),
            (7.5, 'measurements/T05_standalone/needlecard/T05_07p5.csv'),
            (7.0, 'measurements/T05_standalone/needlecard/T05_07p0.csv'),
            (6.5, 'measurements/T05_standalone/needlecard/T05_06p5.csv'),
            (6.0, 'measurements/T05_standalone/needlecard/T05_06p0.csv'),
            (5.5, 'measurements/T05_standalone/needlecard/T05_05p5.csv'),
            (5.0, 'measurements/T05_standalone/needlecard/T05_05p0.csv'),
            (4.5, 'measurements/T05_standalone/needlecard/T05_04p5.csv')
            ])
        }),
    ('T06_standalone', {
        'muxscan': OrderedDict([
            (12.0, 'measurements/T06_standalone/muxscan/MuxScan/muxScan.csv'),
            (11.5, 'measurements/T06_standalone/muxscan/MuxScan_1/muxScan.csv'),
            (11.0, 'measurements/T06_standalone/muxscan/MuxScan_2/muxScan.csv'),
            (10.5, 'measurements/T06_standalone/muxscan/MuxScan_3/muxScan.csv'),
            (10.0, 'measurements/T06_standalone/muxscan/MuxScan_4/muxScan.csv'),
            (9.5, 'measurements/T06_standalone/muxscan/MuxScan_5/muxScan.csv'),
            (9.0, 'measurements/T06_standalone/muxscan/MuxScan_6/muxScan.csv'),
            (8.5, 'measurements/T06_standalone/muxscan/MuxScan_7/muxScan.csv'),
            (8.0, 'measurements/T06_standalone/muxscan/MuxScan_8/muxScan.csv'),
            (7.5, 'measurements/T06_standalone/muxscan/MuxScan_9/muxScan.csv'),
            (7.0, 'measurements/T06_standalone/muxscan/MuxScan_10/muxScan.csv'),
            (6.5, 'measurements/T06_standalone/muxscan/MuxScan_11/muxScan.csv'),
            (6.0, 'measurements/T06_standalone/muxscan/MuxScan_12/muxScan.csv'),
            (5.5, 'measurements/T06_standalone/muxscan/MuxScan_13/muxScan.csv'),
            (5.0, 'measurements/T06_standalone/muxscan/MuxScan_14/muxScan.csv'),
            (4.5, 'measurements/T06_standalone/muxscan/MuxScan_15/muxScan.csv'),
            (4.0, 'measurements/T06_standalone/muxscan/MuxScan_16/muxScan.csv')
            ]),
        'needlecard': OrderedDict([
            (12.0, 'measurements/T06_standalone/needlecard/T06_12p0.csv'),
            (11.5, 'measurements/T06_standalone/needlecard/T06_11p5.csv'),
            (11.0, 'measurements/T06_standalone/needlecard/T06_11p0.csv'),
            (10.5, 'measurements/T06_standalone/needlecard/T06_10p5.csv'),
            (10.0, 'measurements/T06_standalone/needlecard/T06_10p0.csv'),
            (9.5, 'measurements/T06_standalone/needlecard/T06_9p5.csv'),
            (9.0, 'measurements/T06_standalone/needlecard/T06_9p0.csv'),
            (8.5, 'measurements/T06_standalone/needlecard/T06_8p5.csv'),
            (8.0, 'measurements/T06_standalone/needlecard/T06_8p0.csv'),
            (7.5, 'measurements/T06_standalone/needlecard/T06_7p5.csv'),
            (7.0, 'measurements/T06_standalone/needlecard/T06_7p0.csv'),
            (6.5, 'measurements/T06_standalone/needlecard/T06_6p5.csv'),
            (6.0, 'measurements/T06_standalone/needlecard/T06_6p0.csv'),
            (5.5, 'measurements/T06_standalone/needlecard/T06_5p5.csv'),
            (5.0, 'measurements/T06_standalone/needlecard/T06_5p0.csv'),
            (4.5, 'measurements/T06_standalone/needlecard/T06_4p5.csv'),
            (4.0, 'measurements/T06_standalone/needlecard/T06_4p0.csv')
            ])
        }),
    ])


# READ IN DATA
input_data = OrderedDict()
for module in input_files.keys():
    input_data[module] = dict()
    if 'needlecard' in input_files[module].keys():
        input_data[module]['needlecard'] = {
            'input_current': list(), 
            'chips': ['chip_0', 'chip_1', 'chip_2', 'chip_3'], 
            'measurements': OrderedDict([('vin', list()),
                ('chip_0', {'vdda': list(), 'vddd': list()}),
                ('chip_1', {'vdda': list(), 'vddd': list()}),
                ('chip_2', {'vdda': list(), 'vddd': list()}),
                ('chip_3', {'vdda': list(), 'vddd': list()})])
            }
        for current,filename in input_files[module]['needlecard'].items():
            measurements = read_needlecard(filename)
            input_data[module]['needlecard']['input_current'].append(current)
            input_data[module]['needlecard']['measurements']['vin'].append(measurements['vin'])
            for chip in ['chip_0', 'chip_1', 'chip_2', 'chip_3']:
                input_data[module]['needlecard']['measurements'][chip]['vdda'].append(measurements[chip]['vdda'])
                input_data[module]['needlecard']['measurements'][chip]['vddd'].append(measurements[chip]['vddd'])


    if 'muxscan' in input_files[module].keys():
        input_data[module]['muxscan'] = {'input_current':list(), 'chips':list(), 'measurements':OrderedDict()}
        for current,filename in input_files[module]['muxscan'].items():
            measurements = read_muxscan(filename)
            for chip in measurements.keys():
                if chip not in input_data[module]['muxscan']['chips']:
                    input_data[module]['muxscan']['chips'].append(chip)
                    input_data[module]['muxscan']['measurements'][chip] = dict()
                for key in measurements[chip].keys():
                    if key not in input_data[module]['muxscan']['measurements'][chip].keys():
                        input_data[module]['muxscan']['measurements'][chip][key] = list()
                    input_data[module]['muxscan']['measurements'][chip][key].append(measurements[chip][key])
            input_data[module]['muxscan']['input_current'].append(current)
        
        input_current = np.array(input_data[module]['muxscan']['input_current'])
        vin_sum, iin_sum = np.zeros(len(input_current)), np.zeros(len(input_current))
        chips_list = input_data[module]['muxscan']['chips']
        nchips = len(chips_list)
        
        for chip in chips_list:
            measurements = input_data[module]['muxscan']['measurements'][chip]
            # convert VMUX and IMUX values to volts/ampere
            converted = {
                'VOFS': np.array([4*ADCtoVoltage(m,module,chip) for m in measurements['VOFS_QUARTER']]),
                'VINA': np.array([4*ADCtoVoltage(m,module,chip) for m in measurements['VINA_QUARTER']]),
                'VIND': np.array([4*ADCtoVoltage(m,module,chip) for m in measurements['VIND_QUARTER']]),
                'VDDA': np.array([2*ADCtoVoltage(m,module,chip) for m in measurements['VDDA_HALF']]),
                'VDDD': np.array([2*ADCtoVoltage(m,module,chip) for m in measurements['VDDD_HALF']]),
                'IINA': np.array([21000*ADCtoCurrent(m,module,chip) for m in measurements['IINA']]),
                'IIND': np.array([21000*ADCtoCurrent(m,module,chip) for m in measurements['IIND']]),
                'ISHUNTA': np.array([21520*ADCtoCurrent(m,module,chip) for m in measurements['ISHUNTA']]),
                'ISHUNTD': np.array([21520*ADCtoCurrent(m,module,chip) for m in measurements['ISHUNTD']])
            }
            # calculate current overhead (ishunt/iin)
            converted['OVERHEAD_A'] = converted['ISHUNTA']/converted['IINA']
            converted['OVERHEAD_D'] = converted['ISHUNTD']/converted['IIND']
            converted['OVERHEAD'] = (converted['ISHUNTA']+converted['ISHUNTD'])/(converted['IINA']+converted['IIND'])
            # ratios of VMUX and Needle Card (or IMUX and Power Supply) measurements
            if 'needlecard' in input_data[module].keys():
                converted['VDDA_ratio'] = converted['VDDA']/np.array(input_data[module]['needlecard']['measurements'][chip]['vdda'])
                converted['VDDD_ratio'] = converted['VDDD']/np.array(input_data[module]['needlecard']['measurements'][chip]['vddd'])
            input_data[module]['muxscan']['measurements'][chip] = converted
            vin_sum += converted['VINA']+converted['VIND']
            iin_sum += converted['IINA']+converted['IIND']
        
        iin_sum *= 4./nchips
        input_data[module]['muxscan']['measurements']['IIN_ratio'] = iin_sum/input_current
        if 'needlecard' in input_data[module].keys():
            vin_sum *= 1./(2*nchips)
            input_data[module]['muxscan']['measurements']['VIN_ratio'] = vin_sum/np.array(input_data[module]['needlecard']['measurements']['vin'])


# CREATE GRAPHS
histograms = dict()
for module in input_files.keys():
    histograms[module] = dict()
    if 'needlecard' in input_data[module].keys():
        input_current = np.array(input_data[module]['needlecard']['input_current'])
        npoints = len(input_current)
        measurements = input_data[module]['needlecard']['measurements']
        histograms[module]['vin'] = ROOT.TGraph(npoints, input_current, np.array(measurements['vin']))
        histograms[module]['vin'].SetTitle('h_%s_vin;input current (A);measured voltage (V)' % module)
        for chip in input_data[module]['needlecard']['chips']:
            histograms[module][chip] = dict()
            for key in measurements[chip].keys():
                histograms[module][chip][key] = ROOT.TGraph(npoints, input_current, np.array(measurements[chip][key]))
                histograms[module][chip][key].SetTitle('h_%s_%s_%s;input current (A);measured voltage (V)' % (module,chip,key))
    if 'muxscan' in input_data[module].keys():
        input_current = np.array(input_data[module]['muxscan']['input_current'])
        chips_list = input_data[module]['muxscan']['chips']
        measurements = input_data[module]['muxscan']['measurements']
        npoints, nchips = len(input_current), len(chips_list)
        
        for chip in chips_list:
            if not chip in histograms[module].keys():
                histograms[module][chip] = dict()
            for key in measurements[chip].keys():
                if 'ratio' in key:
                    yaxis = 'VMUX / Needle Card'
                elif key.startswith('V'):
                    yaxis = 'measured voltage (V)'
                elif key.startswith('I'):
                    yaxis = 'measured current (A)'
                elif 'OVERHEAD' in key:
                    yaxis = 'ISHUNT / IIN'
                histograms[module][chip][key] = ROOT.TGraph(npoints, input_current, measurements[chip][key])
                histograms[module][chip][key].SetTitle('h_%s_%s_%s;input current (A);%s' % (module,chip,key,yaxis))
        
        histograms[module]['IIN_ratio'] = ROOT.TGraph(npoints, input_current, measurements['IIN_ratio'])
        histograms[module]['IIN_ratio'].SetTitle('h_%s_iinratio;input current (A);IMUX / Power Supply' % module)
        if 'needlecard' in input_data[module].keys():
            histograms[module]['VIN_ratio'] = ROOT.TGraph(npoints, input_current, measurements['VIN_ratio'])
            histograms[module]['VIN_ratio'].SetTitle('h_%s_vinratio;input current (A);VMUX / Needle Card' % module)


# CREATE HISTOGRAMS
nchips = 0
for module in input_data.keys():
    nchips += len(input_data[module]['muxscan']['chips'])

histograms['IINA'] = ROOT.TH1D('h_iina', 'h_iina;chip;measured current (A)', nchips, 0, nchips)
histograms['IIND'] = ROOT.TH1D('h_iind', 'h_iind;chip;measured current (A)', nchips, 0, nchips)
histograms['ISHUNTA'] = ROOT.TH1D('h_ishunta', 'h_ishunta;chip;measured current (A)', nchips, 0, nchips)
histograms['ISHUNTD'] = ROOT.TH1D('h_ishuntd', 'h_ishuntd;chip;measured current (A)', nchips, 0, nchips)
histograms['OVERHEAD'] = ROOT.TH1D('h_overhead', 'h_overhead;chip;ISHUNT / IIN', nchips, 0, nchips)
histograms['OVERHEAD_A'] = ROOT.TH1D('h_overhead_a', 'h_overhead_a;chip;ISHUNT / IIN', nchips, 0, nchips)
histograms['OVERHEAD_D'] = ROOT.TH1D('h_overhead_d', 'h_overhead_d;chip;ISHUNT / IIN', nchips, 0, nchips)
histograms['VINA'] = ROOT.TH1D('h_vina', 'h_vina;chip;measured voltage (V)', nchips, 0, nchips)
histograms['VIND'] = ROOT.TH1D('h_vind', 'h_vind;chip;measured voltage (V)', nchips, 0, nchips)
histograms['VDDA'] = ROOT.TH1D('h_vdda', 'h_vdda;chip;measured voltage (V)', nchips, 0, nchips)
histograms['VDDD'] = ROOT.TH1D('h_vddd', 'h_vddd;chip;measured voltage (V)', nchips, 0, nchips)

i_bin = 0
for module in input_data.keys():
    input_current = np.array(input_data[module]['muxscan']['input_current'])
    chips_list = input_data[module]['muxscan']['chips']
    measurements = input_data[module]['muxscan']['measurements']
    index = np.where(input_current == 8.0)[0][0] # input_current.index(8.0) but for numpy arrays

    for chip in chips_list:
        i_bin += 1
        for key in ['IINA','IIND','ISHUNTA','ISHUNTD','VINA','VIND','VDDA','VDDD','OVERHEAD','OVERHEAD_A','OVERHEAD_D']:
            histograms[key].GetXaxis().SetBinLabel(i_bin, module+'_'+chip)
            histograms[key].SetBinContent(i_bin, measurements[chip][key][index])


# MAKE PLOTS
colors = {'chip_0': ROOT.kRed, 'chip_1': ROOT.kBlue, 'chip_2': ROOT.kGreen, 'chip_3': ROOT.kBlack}

for module in input_files.keys():
    # VIN vs input current (mux scan)
    inputs = list()
    for chip in input_data[module]['muxscan']['chips']:
        inputs.append({'legend': '%s_%s_VIND' % (module[:3],chip), 
            'tgraph': histograms[module][chip]['VIND'], 'color': colors[chip], 'style': 21})
        inputs.append({'legend': '%s_%s_VINA' % (module[:3],chip), 
            'tgraph': histograms[module][chip]['VINA'], 'color': colors[chip], 'style': 20, 'fit': [7.,12.]})
    draw_graphs(inputs, 'plots/VIN_mux_%s.pdf' % module, yrange=[0.0,2.5], legend_ncol=3)

    # VIN vs input current (needle card)
    if 'needlecard' in input_files[module].keys():
        inputs = [{'legend': '%s_VIN' % module[:3], 
            'tgraph': histograms[module]['vin'], 'color': ROOT.kRed, 'style': 20, 'fit': [8.,12.]}]
        draw_graphs(inputs, 'plots/VIN_needle_%s.pdf' % module, yrange=[0.0,2.5], legend_ncol=2)


    # VDDA/VDDD vs input current (mux scan)
    inputs = list()
    for chip in input_data[module]['muxscan']['chips']:
        inputs.append({'legend': '%s_%s_VDDD' % (module[:3],chip), 
            'tgraph': histograms[module][chip]['VDDD'], 'color': colors[chip], 'style': 21})
        inputs.append({'legend': '%s_%s_VDDA' % (module[:3],chip), 
            'tgraph': histograms[module][chip]['VDDA'], 'color': colors[chip], 'style': 20})
    draw_graphs(inputs, 'plots/VDD_mux_%s.pdf' % module, yrange=[0.6,1.6], legend_ncol=4)

    # VDDA/VDDD vs input current (needle card)
    if 'needlecard' in input_files[module].keys():
        inputs = list()
        for chip in input_data[module]['needlecard']['chips']:
            inputs.append({'legend': '%s_%s_VDDD' % (module[:3],chip), 
                'tgraph': histograms[module][chip]['vddd'], 'color': colors[chip], 'style': 21})
            inputs.append({'legend': '%s_%s_VDDA' % (module[:3],chip), 
                'tgraph': histograms[module][chip]['vdda'], 'color': colors[chip], 'style': 20})
        draw_graphs(inputs, 'plots/VDD_needle_%s.pdf' % module, yrange=[0.6,1.6], legend_ncol=4)

    # ISHUNT vs input current (mux scan)
    inputs = list()
    for chip in input_data[module]['muxscan']['chips']:
        inputs.append({'legend': '%s_%s_ISHUNTD' % (module[:3],chip), 
            'tgraph': histograms[module][chip]['ISHUNTD'], 'color': colors[chip], 'style': 21})
        inputs.append({'legend': '%s_%s_ISHUNTA' % (module[:3],chip), 
            'tgraph': histograms[module][chip]['ISHUNTA'], 'color': colors[chip], 'style': 20})
    draw_graphs(inputs, 'plots/ISHUNT_mux_%s.pdf' % module, yrange=[0.0,1.0], legend_ncol=4)

    # IIN vs input current (mux scan)
    inputs = list()
    for chip in input_data[module]['muxscan']['chips']:
        inputs.append({'legend': '%s_%s_IIND' % (module[:3],chip), 
            'tgraph': histograms[module][chip]['IIND'], 'color': colors[chip], 'style': 21})
        inputs.append({'legend': '%s_%s_IINA' % (module[:3],chip), 
            'tgraph': histograms[module][chip]['IINA'], 'color': colors[chip], 'style': 20})
    draw_graphs(inputs, 'plots/IIN_mux_%s.pdf' % module, yrange=[0.0,2.0], legend_ncol=4)

    # ANALOG/DIGITAL OVERHEAD vs input current (mux scan)
    inputs = list()
    for chip in input_data[module]['muxscan']['chips']:
        inputs.append({'legend': '%s_%s_OVERHEAD_D' % (module[:3],chip), 
            'tgraph': histograms[module][chip]['OVERHEAD_D'], 'color': colors[chip], 'style': 21})
        inputs.append({'legend': '%s_%s_OVERHEAD_A' % (module[:3],chip), 
            'tgraph': histograms[module][chip]['OVERHEAD_A'], 'color': colors[chip], 'style': 20})
    draw_graphs(inputs, 'plots/OVERHEAD_AD_%s.pdf' % module, yrange=[0.0,0.7], legend_ncol=4)

    # TOTAL OVERHEAD vs input current (mux scan)
    inputs = list()
    for chip in input_data[module]['muxscan']['chips']:
        inputs.append({'legend': '%s_%s_OVERHEAD' % (module[:3],chip), 
            'tgraph': histograms[module][chip]['OVERHEAD'], 'color': colors[chip], 'style': 20})
    draw_graphs(inputs, 'plots/OVERHEAD_%s.pdf' % module, yrange=[0.0,0.7], legend_ncol=4)
    
    # VDDA/VDDD ratio Mux/Needle
    if 'needlecard' in input_files[module].keys():
        inputs = list()
        for chip in input_data[module]['muxscan']['chips']:
            inputs.append({'legend': '%s_%s_VDDD_ratio' % (module[:3],chip), 
                'tgraph': histograms[module][chip]['VDDD_ratio'], 'color': colors[chip], 'style': 21})
            inputs.append({'legend': '%s_%s_VDDA_ratio' % (module[:3],chip), 
                'tgraph': histograms[module][chip]['VDDA_ratio'], 'color': colors[chip], 'style': 20})
        inputs.append({'legend': '%s_VIN_ratio' % module[:3], 
            'tgraph': histograms[module]['VIN_ratio'], 'color': ROOT.kViolet, 'style': 22})
        draw_graphs(inputs, 'plots/Mux_Needle_%s.pdf' % module, yrange=[0.9,1.15], legend_ncol=4, draw_grid=False, hlines=[1.])

    # IIN ratio Mux/Power Supply
    inputs = [{'legend': '%s_IIN_ratio' % module[:3], 
        'tgraph': histograms[module]['IIN_ratio'], 'color': ROOT.kBlack, 'style': 20}]
    draw_graphs(inputs, 'plots/Mux_PowerSupply_%s.pdf' % module, yrange=[0.5,1.2], legend_ncol=2, draw_grid=False, hlines=[1.])


    # IIN, ISHUNT at input current = 8 A
    inputs = [
        {'legend': 'IINA', 'hist': histograms['IINA'], 'color': ROOT.kRed, 'style': 20},
        {'legend': 'IIND', 'hist': histograms['IIND'], 'color': ROOT.kBlue, 'style': 21},
        {'legend': 'ISHUNTA', 'hist': histograms['ISHUNTA'], 'color': ROOT.kGreen, 'style': 22},
        {'legend': 'ISHUNTD', 'hist': histograms['ISHUNTD'], 'color': ROOT.kViolet, 'style': 23}
        ]
    draw_histograms(inputs, 'plots/CURRENTS_8A.pdf', yrange=[0,1.6], legend_ncol=4, vlines=[4,8])

    # VIN, VDD at input current = 8 A
    inputs = [
        {'legend': 'VINA', 'hist': histograms['VINA'], 'color': ROOT.kRed, 'style': 20},
        {'legend': 'VIND', 'hist': histograms['VIND'], 'color': ROOT.kBlue, 'style': 21},
        {'legend': 'VDDA', 'hist': histograms['VDDA'], 'color': ROOT.kGreen, 'style': 22},
        {'legend': 'VDDD', 'hist': histograms['VDDD'], 'color': ROOT.kViolet, 'style': 23}
        ]
    draw_histograms(inputs, 'plots/VOLTAGES_8A.pdf', yrange=[0,2], legend_ncol=4, vlines=[4,8])

    # Current Overhead at input current = 8 A
    inputs = [
        {'legend': 'OVERHEAD', 'hist': histograms['OVERHEAD'], 'color': ROOT.kRed, 'style': 20},
        {'legend': 'OVERHEAD_A', 'hist': histograms['OVERHEAD_A'], 'color': ROOT.kBlue, 'style': 21},
        {'legend': 'OVERHEAD_D', 'hist': histograms['OVERHEAD_D'], 'color': ROOT.kGreen, 'style': 22}
        ]
    draw_histograms(inputs, 'plots/OVERHEAD_8A.pdf', yrange=[0,0.5], legend_ncol=3, vlines=[4,8])

