import ROOT
from math import ceil

def set_style():
    ROOT.gStyle.SetPadTopMargin(0.05)
    ROOT.gStyle.SetPadBottomMargin(0.13)
    ROOT.gStyle.SetPadLeftMargin(0.10)
    ROOT.gStyle.SetPadRightMargin(0.02)

    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPadTickY(1)


def draw_graphs(inputs, filename, xrange=[0.,12.], yrange=None, legend_ncol=4, draw_grid=True, hlines=None, canvas_size=[1000,800]):
    fit_list, i_fit = list(), 0
    for gr in inputs:
        gr['tgraph'].SetMarkerColor(gr['color'])
        gr['tgraph'].SetMarkerStyle(gr['style'])
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
                gr['tgraph'].SetMinimum(yrange[0])
                gr['tgraph'].SetMaximum(yrange[1])
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
        h['hist'].SetMarkerColor(h['color'])
        h['hist'].SetMarkerStyle(h['style'])

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
                h['hist'].SetMinimum(yrange[0])
                h['hist'].SetMaximum(yrange[1])
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

