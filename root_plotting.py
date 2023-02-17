#!/usr/bin/env python
import ROOT
import argparse
import os

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetStatX(0.8)
ROOT.gStyle.SetStatY(0.9)
ROOT.gStyle.SetPadLeftMargin(0.13)
ROOT.gStyle.SetPadRightMargin(0.19)

def make_filename(input_name):
    replace = [(' ','_'), ('.',''), ('(',''), (')',''), ('^','')]
    output_name = input_name
    for r in replace: output_name = output_name.replace(*r)
    return output_name

parser = argparse.ArgumentParser()
parser.add_argument('input') # path of directory where the root file is saved
parser.add_argument('--tdirectories', nargs='+', default=None) # only save plots from these TDirectories (default: all plots)
parser.add_argument('--png', action='store_true') # save plots as .png (default: .pdf)
args = parser.parse_args()

basepath = args.input
rfile = ROOT.TFile(os.path.join(basepath,'results.root'), 'READ')

dirs = [key.GetName() for key in rfile.GetListOfKeys() if key.ReadObj().IsA().InheritsFrom('TDirectoryFile')]
hists = [key.GetName() for key in rfile.GetListOfKeys() if key.ReadObj().IsA().InheritsFrom('TH1')]

if args.tdirectories is not None:
    dirs = [name for name in dirs if make_filename(name) in args.tdirectories]
    hists = []

# loop through all subdirectories to create a list of all histogram paths
while len(dirs)>0:
    newdirs = []
    for dir in dirs:
        for key in rfile.Get(dir).GetListOfKeys():
            if key.ReadObj().IsA().InheritsFrom('TDirectoryFile'):
                newdirs.append('%s/%s' % (dir, key.GetName()))
            elif key.ReadObj().IsA().InheritsFrom('TH1'):
                hists.append('%s/%s' % (dir, key.GetName()))
    dirs = [dir for dir in newdirs]

# plot histograms
canv_counter = 0
for hpath in hists:
    hpath_external = make_filename(os.path.join(basepath, hpath))
    if not os.path.isdir(os.path.split(hpath_external)[0]):
        os.makedirs(os.path.split(hpath_external)[0])
    
    c = ROOT.TCanvas('c_%s' % canv_counter, '', 1000, 1000)
    canv_counter += 1
    
    h = rfile.Get(hpath)
    if h.IsA().InheritsFrom('TH2'):
        ROOT.gStyle.SetOptStat(0)
        h.Draw('colz')
        c.SetLogz()
    else:
        ROOT.gStyle.SetOptStat(1)
        h.Draw('hist')

    c.Update()
    c.Print('%s.png' % hpath_external if args.png else '%s.pdf' % hpath_external)

rfile.Close()
