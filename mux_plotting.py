import csv
import ROOT
import sys
import numpy as np
from collections import OrderedDict
from math import ceil

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetPadTopMargin(0.05)
ROOT.gStyle.SetPadBottomMargin(0.13)
ROOT.gStyle.SetPadLeftMargin(0.10)
ROOT.gStyle.SetPadRightMargin(0.02)

ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickY(1)


def ADCtoVoltage(adc,module,chip):
    module = module[:3]
    chip = chip[-6:]
    offset = {
        'T03': {'chip_0':  8.531, 'chip_1': 15.084, 'chip_2': 11.817, 'chip_3': 16.004},
        'T05': {'chip_0': 18.232, 'chip_1': 12.052, 'chip_2':  6.121, 'chip_3': 14.347},
        'T06': {'chip_0': 13.205, 'chip_1': 18.243, 'chip_2': 19.148, 'chip_3': 22.500},
    }
    slope = {
        'T03': {'chip_0': 0.194, 'chip_1': 0.188, 'chip_2': 0.185, 'chip_3': 0.189},
        'T05': {'chip_0': 0.175, 'chip_1': 0.183, 'chip_2': 0.186, 'chip_3': 0.186},
        'T06': {'chip_0': 0.189, 'chip_1': 0.181, 'chip_2': 0.187, 'chip_3': 0.182},
    }
    #return adc*0.850/4096.
    return (adc * slope[module][chip] + offset[module][chip]) / 1000.


def ADCtoCurrent(adc,module,chip):
    return ADCtoVoltage(adc,module,chip) / 4990.


def Set(obj, **kwargs):
    for key, value in kwargs.iteritems():
        if value is None:
            getattr(obj, 'Set' + key)()
        elif isinstance(value, (list, tuple)):
            getattr(obj, 'Set' + key)(*value)
        else:
            getattr(obj, 'Set' + key)(value)


def read_needlecard(input_dict):
    output_dict = {
        'input_current': list(), 
        'measurements': {'vin': list(), 
        'vdda0': list(), 'vddd0': list(),
        'vdda1': list(), 'vddd1': list(),
        'vdda2': list(), 'vddd2': list(),
        'vdda3': list(), 'vddd3': list()}
        }
    for current,filepath in input_dict.items():
        header = list()
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            for i,row in enumerate(reader): 
                if i==0: header = row
                pass
        output_dict['input_current'].append(current)
        output_dict['measurements']['vin'].append(float(row[header.index('vin')]))
        output_dict['measurements']['vdda0'].append(float(row[header.index('vdda0')]))
        output_dict['measurements']['vddd0'].append(float(row[header.index('vddd0')]))
        output_dict['measurements']['vdda1'].append(float(row[header.index('vdda1')]))
        output_dict['measurements']['vddd1'].append(float(row[header.index('vddd1')]))
        output_dict['measurements']['vdda2'].append(float(row[header.index('vdda2')]))
        output_dict['measurements']['vddd2'].append(float(row[header.index('vddd2')]))
        output_dict['measurements']['vdda3'].append(float(row[header.index('vdda3')]))
        output_dict['measurements']['vddd3'].append(float(row[header.index('vddd3')]))
    return output_dict


def read_muxscan(input_dict):
    mux_list = ['ISHUNTA','ISHUNTD','IINA','IIND','VINA_QUARTER','VIND_QUARTER','VDDA_HALF','VDDD_HALF','VOFS_QUARTER']
    output_dict = {
        'input_current': list(), 
        'chips': list(),
        'measurements': OrderedDict()
        }
    for current,filepath in input_dict.items():
        output_dict['input_current'].append(current)
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            for i,row in enumerate(reader): 
                chip, mux, val = row[0].strip()[-6:], row[2].strip(), row[4].strip()
                if mux not in mux_list:
                    continue
                if chip not in output_dict['chips']:
                    output_dict['chips'].append(chip)
                    output_dict['measurements'][chip] = dict((k,list()) for k in mux_list)
                output_dict['measurements'][chip][mux].append(int(val))
    output_dict['chips'].sort()
    return output_dict


def draw_graphs(inputs, filename, xrange=[0.,12.], yrange=None, legend_ncol=4, draw_grid=True, hlines=None, canvas_size=[1000,800]):
    fit_list, i_fit = list(), 0
    for gr in inputs:
        Set(gr['tgraph'], MarkerColor=gr['color'], MarkerStyle=gr['style'])
        if 'fit' in gr.keys():
            gr['fitfunc'] = ROOT.TF1('lin_%s' % i_fit,'[0]+[1]*x', xrange[0]-0.5, xrange[1]+0.5)
            fit = gr['tgraph'].Fit(gr['fitfunc'],'SQ0','', gr['fit'][0], gr['fit'][1])
            gr['fitfunc'].SetParameter(0,fit.Parameter(0))
            gr['fitfunc'].SetParameter(1,fit.Parameter(1))
            gr['fitfunc'].SetLineColor(gr['color'])
            i_fit += 1

    c = ROOT.TCanvas(filename,filename,canvas_size[0],canvas_size[1])
    legend_nentries = len(inputs)
    for gr in inputs:
        if 'fit' in gr.keys(): legend_nentries+=1
    legend_height = ceil(float(legend_nentries)/legend_ncol)*0.05
    legend = ROOT.TLegend(*([0.13, 0.94-legend_height, 0.95, 0.94, '', 'NBNDC']))
    legend.SetNColumns(legend_ncol)
    legend.SetBorderSize(0)
    if draw_grid:
        c.SetGrid(1,1)

    for i,gr in enumerate(inputs):
        if i==0:
            if yrange is not None:
                Set(gr['tgraph'], Minimum=yrange[0], Maximum=yrange[1])
            gr['tgraph'].GetXaxis().SetLimits(xrange[0]-0.1,xrange[1]+0.1)
            gr['tgraph'].Draw('AP')
        else:
            gr['tgraph'].Draw('P same')
        legend.AddEntry(gr['tgraph'], gr['legend'], 'P')
        if 'fitfunc' in gr.keys():
            gr['fitfunc'].Draw('L same')
            legend.AddEntry(gr['fitfunc'], 'fit in range (%s A, %s A)' % (gr['fit'][0], gr['fit'][1]), 'L')
    
    if hlines is not None:
        tlines = list()
        for hline in hlines:
            tlines.append(ROOT.TLine(xrange[0]-0.1,hline,xrange[1]+0.1,hline))
            tlines[-1].SetLineStyle(1 if draw_grid else 2)
            tlines[-1].Draw('L same')

    legend.Draw('same')
    c.Update()
    c.Print(filename)


def draw_histograms(inputs, filename, yrange=None, legend_ncol=4, draw_grid=True, vlines=None, canvas_size=[1000,800]):
    for h in inputs:
        Set(h['hist'], MarkerColor=h['color'], MarkerStyle=h['style'])

    c = ROOT.TCanvas(filename,filename,canvas_size[0],canvas_size[1])
    legend_nentries = len(inputs)
    legend_height = ceil(float(legend_nentries)/legend_ncol)*0.05
    legend = ROOT.TLegend(*([0.13, 0.94-legend_height, 0.95, 0.94, '', 'NBNDC']))
    legend.SetNColumns(legend_ncol)
    legend.SetBorderSize(0)
    if draw_grid:
        c.SetGrid(1,1)
    for i,h in enumerate(inputs):
        if i==0:
            if yrange is not None:
                Set(h['hist'], Minimum=yrange[0], Maximum=yrange[1])
            h['hist'].Draw('P')
        else:
            h['hist'].Draw('P same')
        legend.AddEntry(h['hist'], h['legend'], 'P')

    if vlines is not None:
        if yrange is None:
            yrange = [inputs[0]['hist'].GetMinimum(), inputs[0]['hist'].GetMaximum()]
        tlines = list()
        for vline in vlines:
            tlines.append(ROOT.TLine(vline,yrange[0],vline,yrange[1]))
            tlines[-1].SetLineStyle(1 if draw_grid else 2)
            tlines[-1].Draw('L same')

    legend.Draw('same')
    c.Update()
    c.Print(filename)


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
        input_data[module]['needlecard'] = read_needlecard(input_files[module]['needlecard'])
    if 'muxscan' in input_files[module].keys():
        input_data[module]['muxscan'] = read_muxscan(input_files[module]['muxscan'])
        
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
                converted['VDDA_ratio'] = converted['VDDA']/np.array(input_data[module]['needlecard']['measurements']['vdda%s' % chip[-1]])
                converted['VDDD_ratio'] = converted['VDDD']/np.array(input_data[module]['needlecard']['measurements']['vddd%s' % chip[-1]])
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
        for key in measurements.keys():
            histograms[module][key] = ROOT.TGraph(npoints, input_current, np.array(measurements[key]))
            histograms[module][key].SetTitle('h_%s_%s;input current (A);measured voltage (V)' % (module,key))
    if 'muxscan' in input_data[module].keys():
        input_current = np.array(input_data[module]['muxscan']['input_current'])
        chips_list = input_data[module]['muxscan']['chips']
        measurements = input_data[module]['muxscan']['measurements']
        npoints, nchips = len(input_current), len(chips_list)
        
        for chip in chips_list:
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
        inputs.append({'legend': '%s_%s_VIND' % (module[:3],chip), 'tgraph': histograms[module][chip]['VIND'], 
            'color': colors[chip], 'style': 21})
        inputs.append({'legend': '%s_%s_VINA' % (module[:3],chip), 'tgraph': histograms[module][chip]['VINA'], 
            'color': colors[chip], 'style': 20, 'fit': [7.,12.]})
    draw_graphs(inputs, 'plots/VIN_mux_%s.pdf' % module, yrange=[0.0,2.5], legend_ncol=3)

    # VIN vs input current (needle card)
    if 'needlecard' in input_files[module].keys():
        inputs = [
            {'legend': '%s_VIN' % module[:3], 'tgraph': histograms[module]['vin'], 
            'color': ROOT.kRed, 'style': 20, 'fit': [8.,12.]}
            ]
        draw_graphs(inputs, 'plots/VIN_needle_%s.pdf' % module, yrange=[0.0,2.5], legend_ncol=2)


    # VDDA/VDDD vs input current (mux scan)
    inputs = list()
    for chip in input_data[module]['muxscan']['chips']:
        inputs.append({'legend': '%s_%s_VDDD' % (module[:3],chip), 'tgraph': histograms[module][chip]['VDDD'], 
            'color': colors[chip], 'style': 21})
        inputs.append({'legend': '%s_%s_VDDA' % (module[:3],chip), 'tgraph': histograms[module][chip]['VDDA'], 
            'color': colors[chip], 'style': 20})
    
    draw_graphs(inputs, 'plots/VDD_mux_%s.pdf' % module, yrange=[0.6,1.6], legend_ncol=4)

    # VDDA/VDDD vs input current (needle card)
    if 'needlecard' in input_files[module].keys():
        inputs = [
            {'legend': '%s_chip0_VDDD' % module[:3], 'tgraph': histograms[module]['vddd0'], 
            'color': ROOT.kRed, 'style': 21},
            {'legend': '%s_chip0_VDDA' % module[:3], 'tgraph': histograms[module]['vdda0'], 
            'color': ROOT.kRed, 'style': 20},
            {'legend': '%s_chip1_VDDD' % module[:3], 'tgraph': histograms[module]['vddd1'], 
            'color': ROOT.kBlue, 'style': 21},
            {'legend': '%s_chip1_VDDA' % module[:3], 'tgraph': histograms[module]['vdda1'], 
            'color': ROOT.kBlue, 'style': 20},
            {'legend': '%s_chip2_VDDD' % module[:3], 'tgraph': histograms[module]['vddd2'], 
            'color': ROOT.kGreen, 'style': 21},
            {'legend': '%s_chip2_VDDA' % module[:3], 'tgraph': histograms[module]['vdda2'], 
            'color': ROOT.kGreen, 'style': 20},
            {'legend': '%s_chip3_VDDD' % module[:3], 'tgraph': histograms[module]['vddd3'], 
            'color': ROOT.kBlack, 'style': 21},
            {'legend': '%s_chip3_VDDA' % module[:3], 'tgraph': histograms[module]['vdda3'], 
            'color': ROOT.kBlack, 'style': 20}
            ]
        draw_graphs(inputs, 'plots/VDD_needle_%s.pdf' % module, yrange=[0.6,1.6], legend_ncol=4)

    # ISHUNT vs input current (mux scan)
    inputs = list()
    for chip in input_data[module]['muxscan']['chips']:
        inputs.append({'legend': '%s_%s_ISHUNTD' % (module[:3],chip), 'tgraph': histograms[module][chip]['ISHUNTD'], 
            'color': colors[chip], 'style': 21})
        inputs.append({'legend': '%s_%s_ISHUNTA' % (module[:3],chip), 'tgraph': histograms[module][chip]['ISHUNTA'], 
            'color': colors[chip], 'style': 20})
    
    draw_graphs(inputs, 'plots/ISHUNT_mux_%s.pdf' % module, yrange=[0.0,1.0], legend_ncol=4)

    # IIN vs input current (mux scan)
    inputs = list()
    for chip in input_data[module]['muxscan']['chips']:
        inputs.append({'legend': '%s_%s_IIND' % (module[:3],chip), 'tgraph': histograms[module][chip]['IIND'], 
            'color': colors[chip], 'style': 21})
        inputs.append({'legend': '%s_%s_IINA' % (module[:3],chip), 'tgraph': histograms[module][chip]['IINA'], 
            'color': colors[chip], 'style': 20})
    
    draw_graphs(inputs, 'plots/IIN_mux_%s.pdf' % module, yrange=[0.0,2.0], legend_ncol=4)

    # ANALOG/DIGITAL OVERHEAD vs input current (mux scan)
    inputs = list()
    for chip in input_data[module]['muxscan']['chips']:
        inputs.append({'legend': '%s_%s_OVERHEAD_D' % (module[:3],chip), 'tgraph': histograms[module][chip]['OVERHEAD_D'], 
            'color': colors[chip], 'style': 21})
        inputs.append({'legend': '%s_%s_OVERHEAD_A' % (module[:3],chip), 'tgraph': histograms[module][chip]['OVERHEAD_A'], 
            'color': colors[chip], 'style': 20})
    
    draw_graphs(inputs, 'plots/OVERHEAD_AD_%s.pdf' % module, yrange=[0.0,0.7], legend_ncol=4)

    # TOTAL OVERHEAD vs input current (mux scan)
    inputs = list()
    for chip in input_data[module]['muxscan']['chips']:
        inputs.append({'legend': '%s_%s_OVERHEAD' % (module[:3],chip), 'tgraph': histograms[module][chip]['OVERHEAD'], 
            'color': colors[chip], 'style': 20})
    
    draw_graphs(inputs, 'plots/OVERHEAD_%s.pdf' % module, yrange=[0.0,0.7], legend_ncol=4)
    
    # VDDA/VDDD ratio Mux/Needle
    if 'needlecard' in input_files[module].keys():
        inputs = list()
        for chip in input_data[module]['muxscan']['chips']:
            inputs.append({'legend': '%s_%s_VDDD_ratio' % (module[:3],chip), 'tgraph': histograms[module][chip]['VDDD_ratio'], 
                'color': colors[chip], 'style': 21})
            inputs.append({'legend': '%s_%s_VDDA_ratio' % (module[:3],chip), 'tgraph': histograms[module][chip]['VDDA_ratio'], 
                'color': colors[chip], 'style': 20})
        inputs.append({'legend': '%s_VIN_ratio' % module[:3], 'tgraph': histograms[module]['VIN_ratio'], 
            'color': ROOT.kViolet, 'style': 22})
        
        draw_graphs(inputs, 'plots/Mux_Needle_%s.pdf' % module, yrange=[0.9,1.15], legend_ncol=4, draw_grid=False, hlines=[1.])

    # IIN ratio Mux/Power Supply
    inputs = [
        {'legend': '%s_IIN_ratio' % module[:3], 'tgraph': histograms[module]['IIN_ratio'], 
        'color': ROOT.kBlack, 'style': 20}
        ]
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

