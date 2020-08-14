#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: juanpelvis
Background computing of BH
"""

import sys
sys.path.append('/home/juanpelvis/Documents/python_code/')
import pandas as pd# Dataframe handling package
import aux_inclino2 as AUX
import numpy as np
import seaborn as sns
import boreholeclass as BC
#import inclinoclass as IC
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.figure as mfigure
from datetime import datetime


def initial_figures():
    figs = {'-FIGTILTAZ-': '',
            '-FIGUD-': '',
           '-FIGDUDZ-' : '' }
    for i in figs:
        figs[i] = mfigure.Figure(figsize=(6, 6))
    return figs

def plot_tilt(start,end,borehole):
    fig,ax = plt.subplots(figsize=borehole.plotsize)
    start = datetime.strptime(start,'%Y-%m-%d')
    end = datetime.strptime(end,'%Y-%m-%d')
    mask = (borehole.data_TS > start) & (borehole.data_TS <= end)
    for i in range(1,1+borehole.get_noi()):
        if borehole.inclinos[i].mask:
            ax.plot_date(mdates.date2num(borehole.data_TS.loc[mask]),borehole.inclinos[i].tilt.loc[mask],label = i)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    ax.legend()
    ax.set_ylabel('Tilt')
    ax.set_title('Tilt vs time per inclinometer')
    return fig,ax

def plot_dudz(borehole):
    plt.subplots(figsize=borehole.plotsize)
    ax = sns.heatmap(borehole.dudz,vmin = 0,vmax = 1.2)#,yticklabels=list(borehole.dudz.index))
    ax.set_title('Internal deformation')
    list_labels = ax.get_yticklabels()
    for i in range(len(list_labels)):
        list_labels[i].set_text(list_labels[i].get_text()[:-19])
    ax.set_yticklabels(list_labels)
    return ax.get_figure()

def plot_ud(borehole,ud_0 = 0):
    figud,axud = plt.subplots(figsize=borehole.plotsize)
    depth = []
    for i in range(1,1+borehole.get_noi()):
        if borehole.inclinos[i].mask:
            depth.append(borehole.inclinos[i].depth)
    axud.set_title('Deformation velocity')
    axud.set_ylim([-250,0])
    axud.set_ylabel('Depth')
    axud.set_xlabel('m a^-1')
    axud.plot(borehole.ud+ud_0,depth)
    axud.legend(borehole.ud.columns)
    return figud,axud

def plot_fitud(udfit,z,axud):
    H,B,n,UD_0 = udfit.params['H'].value,udfit.params['B'].value,udfit.params['n'].value,udfit.params['UD_0'].value
    z = np.append(H,z)
    z = np.append(z,0)
    axud.plot(UD_0+AUX.expo_fit2(z,H,B,n,UD_0),np.multiply(-1,z),'k:')
    return 
            #,label = 'Fit, n='+"{0:.2f}".format(n)+', B='+"{0:.2f}".format(B),linewidth = 4,markersize = 10)

def fit_ud(borehole,key):
    # (NAME VALUE VARY MIN  MAX  EXPR  BRUTE_STEP)
    fixed_vars = []
    depth = []
    for i in range(1,1+borehole.get_noi()):
        if borehole.inclinos[i].mask:
            depth.append(-1*borehole.inclinos[i].depth)
    for k in key:
        if ('-FIT' in k) and (k != '-FITBOOL-'):
            vartup = [k.replace('-FIT','')[:-1],key[k.replace('-FIT','-ini_FIT')],
            key[k], key[k.replace('-FIT','-min_FIT')],
            key[k.replace('-FIT','-max_FIT')]]
            fixed_vars.append(vartup)
    result = AUX.fit_ud(borehole.ud,depth,fixed_vars)
    
    return result,depth

def main_run(values):
    """ Variable declaration """
    bh_list = ['-BH1-','-BH2-','-BH3-','-BH4-','-BH5-']
    start = values['-STARTDATE-']
    end = values['-ENDDATE-']
    dt,DX = values['-dt-'],values['-DX-']
    if values['-FOLDER-'][-1] != '/':
        values['-FOLDER-'] = values['-FOLDER-']+'/'
    initial_figs = initial_figures()
    for k in initial_figs:
        values[k] = initial_figs[k]
    """ Computation inside borehole class """
    for bh_key in bh_list:
        if values[bh_key]:
            borehole = BC.borehole(values['-FOLDER-'],int(bh_key[-2]))
            borehole.load_inclino()
            if values['-TILTAZ-'] or values['-DUDZ-'] or values['-UD-']:
                borehole.compute_tilt_az_alt(start,end,dt)
                if values['-TILTAZ-']:
                    figtilt,axtilt = plot_tilt(start,end,borehole)
                    values['-FIGTILTAZ-'] = figtilt
            if values['-DUDZ-'] or values['-UD-']:
                borehole.compute_dudz(pd.DataFrame(),start,end,dt,DX)
                if values['-DUDZ-']:
                    values['-FIGDUDZ-'] = plot_dudz(borehole)
            if values['-UD-']:
                borehole.compute_ud()
                if values['-FITBOOL-']:
                    fitresult,z = fit_ud(borehole,values)
                    values['-Hfitted-'],values['-Bfitted-'],values['-nfitted-'],values['-UD_0fitted-'] = fitresult.params['H'].value,fitresult.params['B'].value,fitresult.params['n'].value,fitresult.params['UD_0'].value
                    print(values['-Hfitted-'])
                    figud,axud = plot_ud(borehole,fitresult.params['UD_0'].value)
                    plot_fitud(fitresult,z,axud)
                    
                else:
                    figud,axud = plot_ud(borehole)
                axud.set_yticks(np.arange(0,-250,-10))
                values['-FIGUD-'] = figud
            borehole.report()
            values[bh_key] = borehole
    return values



def check_filleddates(values):
    for i in ['-SD-','-ED-','-EM-','-SM-','-EY-','-SY-']:
        if len(str(values[i])) == 0:
            return 0
    return 1


def rebuild_data(values):
    """ Preprocessing """
    dates = [values['-SY-'],values['-SM-'],values['-SD-']]
    datee = [values['-EY-'],values['-EM-'],values['-ED-']]

    for i in range(len(dates)):
        if dates[i] < 10:
            dates[i] = '0'+str(dates[i])
        else:
            dates[i] = str(dates[i])
    for i in range(len(datee)):
        if datee[i] < 10:
            datee[i] = '0'+str(datee[i])
        else:
            datee[i] = str(datee[i])
    dates = dates[0]+'-'+dates[1]+'-'+dates[2]
    datee = datee[0]+'-'+datee[1]+'-'+datee[2]
    values['-STARTDATE-'] = dates
    values['-ENDDATE-'] = datee
    values['-DX-'] = int(values['-DX-'])
    values['-dt-'] = int(values['-dt-'])
    for k in values:
        """
        Initial values ALWAYS inside the domain
        If maxlimit < minlimit, all are set to the initial
        """
        if '-min' in k:
            kini = k.replace('min','ini')
            kmax = k.replace('min','max')
            if values[k] > values[kmax]:
                values[k] = values[kini]
                values[kmax] = values[kini]+1
            if values[kini] > values[kmax]:
                values[kmax] = values[kini]
            if values[kini] < values[k]:
                values[k] = values[kini]

    return values


def default():
    res = {}
    res['-SD-'] = 1
    res['-SM-'] = 4
    res['-SY-'] = 2020
    res['-Sh-'] = 0
    res['-Sm-'] = 0
    #
    res['-ED-'] = 4
    res['-EM-'] = 4
    res['-EY-'] = 2020
    res['-Eh-'] = 0
    res['-Em-'] = 0
    #
    res['-UD-'] = True
    res['-DUDZ-'] = False
    res['-TILTAZ-'] = False
    return res