#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 16:14:16 2020

@author: juanpelvis
"""

import PySimpleGUI as sg
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sys
sys.path.append('/home/juanpelvis/Documents/python_code/')
import bg_GUI as BG
#!/usr/bin/env python
import numpy as np

"""
Demonstrates one way of embedding Matplotlib figures into a PySimpleGUI window.
Basic steps are:
 * Create a Canvas Element
 * Layout form
 * Display form (NON BLOCKING)
 * Draw plots onto convas
 * Display form (BLOCKING)
 
 Based on information from: https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html
 (Thank you Em-Bo & dirck)
"""
""" Auxiliary functions  """
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg
def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    plt.close('all')

sg.theme('Dark Blue 3')
res = BG.default()
# Layout
layout = []
frame1 = [[sg.Text('Folder containing the data:'), sg.Text(size=(15,1), key='-OUTPUT-')]]

frame1.append([sg.In(key='-FOLDER-',default_text='/home/juanpelvis/Documents/Inclino'), sg.FolderBrowse()])
# add date finder
frame1.append([sg.Text('Initial Date:'),sg.InputCombo(values=[i for i in range(2019,2021)],key='-SY-',default_value=res['-SY-']),sg.Text('y'),
           sg.InputCombo(values=[i for i in range(1,13)],key='-SM-',default_value=res['-SM-']),sg.Text('m'),
           sg.InputCombo(values=[i for i in range(1,32)],key='-SD-',default_value=res['-SD-']),sg.Text('d'),
           sg.Text('Time:'),sg.InputCombo(values=[i for i in range(24)],key='-Sh-',default_value=res['-Sh-']),
           sg.Text('h'),sg.Spin(values=[i for i in range(0,31,30)],initial_value=res['-Sm-'],key='-Sm-'),sg.Text('min')])

frame1.append([sg.Text('End Date:    '),sg.InputCombo([i for i in range(2019,2021)],key='-EY-',default_value=res['-EY-']),sg.Text('y'),
               sg.InputCombo([i for i in range(1,13)],key='-EM-',default_value=res['-EM-']),sg.Text('m'),
               sg.InputCombo([i for i in range(1,32)],key='-ED-',default_value=res['-ED-']),sg.Text('d'),
           sg.Text('Time:'),sg.InputCombo([i for i in range(24)],key='-Eh-',default_value=res['-Eh-']),
           sg.Text('h'),sg.Spin([i for i in range(0,31,30)],initial_value=res['-Em-'],key='-Em-'),sg.Text('min')])
# add select borehole.
frame1.append([sg.Text('Select Borehole:'), sg.Checkbox('1',key='-BH1-'), sg.Checkbox('2',key='-BH2-',default=True),
             sg.Checkbox('3',key='-BH3-'), sg.Checkbox('4',key='-BH4-'), sg.Checkbox('5',key='-BH5-')])
# add time_steps
frame1.append([sg.Text('Averaging window: '),sg.InputText(default_text='48',key='-DX-',size=(2,1)),
              sg.Text(', Timestep (keep 1): '),sg.InputText(default_text='1',key='-dt-',size=(2,1))])
# add checkbox for data computation
frame1.append([sg.Text('Plot: '),sg.Checkbox('Tilt,Azimuth',default=res['-TILTAZ-'],key='-TILTAZ-'),
              sg.Checkbox('DUDZ',default=res['-DUDZ-'],key='-DUDZ-'),sg.Checkbox('UD',default=res['-UD-'],key='-UD-'),
              sg.Checkbox('Fit?',key='-FITBOOL-',default=True),
              sg.Text('Variables: '), sg.Checkbox('B',key='-FITB-'),sg.Checkbox('n',key='-FITn-',default=True),
              sg.Checkbox('UD_0',key='-FITUD_0-'),sg.Checkbox('H',key='-FITH-')])#,sg.Checkbox('More options',key='-FITMORE-')])
# Columns for the fit
Cola = [[sg.Text('Var',size = (4,2)),sg.Text('       B',size = (18,2)),sg.Text('       n',size = (18,2)),
         sg.Text('    ud_0',size = (18,2)),sg.Text('     H',size = (18,2))],
# initial sliders    
    [sg.Text('Initial',size = (4,2)),sg.Slider(range=(1.0,100.),resolution=10,
         default_value=7,size = (20,10),
         orientation='h', key = '-ini_FITB-',
         font=('Helvetica', 8)),sg.Slider(range=(1,5.),resolution=0.1,
         default_value=3,size = (20,10),
         orientation='h',key = '-ini_FITn-',
         font=('Helvetica', 8)),sg.Slider(range=(0,30),resolution=1,
         default_value=0,size = (20,10),
         orientation='h',key = '-ini_FITUD_0-',
         font=('Helvetica', 8)),sg.Slider(range=(180,250),resolution=5,
         default_value=235,size = (20,10),
         orientation='h',key = '-ini_FITH-',
         font=('Helvetica', 8))],
# min sliders
         [sg.Text('min',size = (4,2)),sg.Slider(range=(1.0,100.),resolution=10,
         default_value=1,size = (20,10),
         orientation='h', key = '-min_FITB-',
         font=('Helvetica', 8)),sg.Slider(range=(1,5.),resolution=0.1,
         default_value=1,size = (20,10),
         orientation='h',key = '-min_FITn-',
         font=('Helvetica', 8)),sg.Slider(range=(0,30),resolution=1,
         default_value=0,size = (20,10),
         orientation='h',key = '-min_FITUD_0-',
         font=('Helvetica', 8)),sg.Slider(range=(180,250),resolution=5,
         default_value=230,size = (20,10),
         orientation='h',key = '-min_FITH-',
         font=('Helvetica', 8))],
# max sliders
         [sg.Text('max',size = (4,2)),sg.Slider(range=(1.0,100),resolution=10,
         default_value=100,size = (20,10),
         orientation='h',key = '-max_FITB-',
         font=('Helvetica', 8)),sg.Slider(range=(1,5.),resolution=0.1,
         default_value=5,size = (20,10),
         orientation='h',key = '-max_FITn-',
         font=('Helvetica', 8)),sg.Slider(range=(0,30),resolution=1,
         default_value=0,size = (20,10),
         orientation='h',key = '-max_FITUD_0-',
         font=('Helvetica', 8)),sg.Slider(range=(180,250),resolution=5,
         default_value=235,size = (20,10),
         orientation='h',key = '-max_FITH-',
         font=('Helvetica', 8))]]
frame2 = [[sg.Column(Cola)]]
# Frame 3
frame3 = [[sg.Text('B   '),sg.Output(size=(5,1),key='-OUTPUTB-')],
           [sg.Text('n   '),sg.Output(size=(5,1),key='-OUTPUTn-')],
           [sg.Text('UD_0'),sg.Output(size=(5,1),key='-OUTPUTUD_0-')],
           [sg.Text('H   '),sg.Output(size=(5,1),key='-OUTPUTH-')]]
#
layout.append([sg.Frame('PARAMETERS',frame1),
               sg.Frame('FIT',frame2),
               sg.Frame('RESULT',frame3), 
               sg.Frame('OUTPUT',[[sg.Output(size=(60,12),key='-ALLOUTPUT-')]])]) #keep as last output element 
# Final line
layout.append([sg.Button('Run'), sg.Button('Reset'), sg.Button('Exit')])

# Line for graphs
layout.append([sg.Canvas(key='-CANVAS1-'),
               sg.Canvas(key='-CANVAS2-'),
               sg.Canvas(key='-CANVAS3-')])
# Create Window
figures = {}
window = sg.Window('Borehole', layout,resizable = True,size=sg.Window.get_screen_size(),finalize = True)
fig_canvas_agg1,fig_canvas_agg2,fig_canvas_agg3 = None, None, None
figcanvases = [fig_canvas_agg1,fig_canvas_agg2,fig_canvas_agg3]
canvases = [window['-CANVAS1-'].TKCanvas,window['-CANVAS2-'].TKCanvas,window['-CANVAS3-'].TKCanvas]

# Event
while True:  # Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Run':
        # ** IMPORTANT ** Clean up previous drawing before drawing again
        for i in figcanvases:
            if i is not None:
                delete_figure_agg(i)
        # Update the "output" text element to be the value of "input" element.
        values = BG.rebuild_data(values)
        values = BG.main_run(values)
        for k in values:
            if 'FIT' in k:
                window[k].update(values[k])
        rolling = 0
        for k in values:
            if '-FIG' in k:
                figures[k] = values[k]
                checkbox = k.replace('FIG','')
                if values[checkbox]:
                    figcanvases[rolling] = draw_figure(canvases[rolling],values[k])
                    rolling = rolling + 1
        borehole = values['-BH2-']
        if values['-FITBOOL-']:
            window['-OUTPUTB-'].update("{0:.3f}".format(values['-Bfitted-']))
            window['-OUTPUTn-'].update("{0:.3f}".format(values['-nfitted-']))
            window['-OUTPUTUD_0-'].update("{0:.3f}".format(values['-UD_0fitted-']))
            window['-OUTPUTH-'].update("{0:.3f}".format(values['-Hfitted-']))
    if event == 'Reset':
        for k in res:
            window[k].update(res[k])
    print(event, values)


window.close()