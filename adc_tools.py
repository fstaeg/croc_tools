import csv
from collections import OrderedDict

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


def read_muxscan(input_file, muxvals=['ISHUNTA','ISHUNTD','IINA','IIND','VINA_QUARTER','VIND_QUARTER','VDDA_HALF','VDDD_HALF','VOFS_QUARTER']):
    output_dict = OrderedDict()
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        for i,row in enumerate(reader): 
            chip, mux, val = row[0].strip()[-6:], row[2].strip(), row[4].strip()
            if mux not in muxvals:
                continue
            if chip not in output_dict.keys():
                output_dict[chip] = dict()
            output_dict[chip][mux] = int(val)
    return output_dict


def read_needlecard(input_file):
    output_dict = OrderedDict([('chip_0',{}),('chip_1',{}),('chip_2',{}),('chip_3',{})])
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        for i,row in enumerate(reader): 
            if i==0: header = row
            if row[0] == 'average': break
    output_dict['vin'] = float(row[header.index('vin')])
    output_dict['chip_0']['vdda'] = float(row[header.index('vdda0')])
    output_dict['chip_0']['vddd'] = float(row[header.index('vddd0')])
    output_dict['chip_1']['vdda'] = float(row[header.index('vdda1')])
    output_dict['chip_1']['vddd'] = float(row[header.index('vddd1')])
    output_dict['chip_2']['vdda'] = float(row[header.index('vdda2')])
    output_dict['chip_2']['vddd'] = float(row[header.index('vddd2')])
    output_dict['chip_3']['vdda'] = float(row[header.index('vdda3')])
    output_dict['chip_3']['vddd'] = float(row[header.index('vddd3')])
    return output_dict

