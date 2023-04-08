

# app.py
# based on dropdown code from 
#https://stackoverflow.com/questions/25978879/
#how-to-create-chained-selectfield-in-flask-without-refreshing-the-page

from flask import Flask, render_template, request, jsonify
import os
from createandfilldb import fetchSameYear, findFilname
from utilfnc import read_cal_spec
import numpy as np
import pandas as pd
# Initialize the Flask application

app = Flask(__name__,
            static_url_path="",
            static_folder="static",
            template_folder="webgui")

@app.route('/_update_dropdown')
def update_dropdown():

    selected_year = request.args.get('selected_year', type=str)
    updated_values = fetchSameYear()[selected_year]
    shtml = ''
    for opt in updated_values:
        shtml += f'<option value="{opt}">{opt}</option>'

    return jsonify(shtml=shtml)


@app.route('/_plot_data')
def plot_data():
    selected_spectrum = request.args.get('selected_spectrum', type=str)
    _,_,_,sp_filename,dg_filename,im_filename, imheight=findFilname(selected_spectrum)
    intensity, wavenumbers = read_cal_spec(sp_filename)
    digitized_in = np.loadtxt(dg_filename).tolist()
    jsonified = jsonify(calibrated_in = intensity.tolist(),
    wavenumber_lbl=np.round(wavenumbers,1).tolist(), 
    digitized_in = digitized_in,
    pixel_lbl = np.arange(len(digitized_in)).tolist(),
    im_filename = im_filename,
    imheight = imheight
    ) # this sends the intensity and the wavelength to be used by js plot functio
    return jsonified
@app.route('/_draw_table')
def draw_table():
    selected_spectrum = request.args.get('selected_spectrum', type=str)
    tabs = os.path.join('static/data/tables.dat')
    dataf = pd.read_csv(tabs, sep = '\s+')
    data_table = dataf.loc[(dataf['Date'].isin(selected_spectrum.split())) 
                           & (dataf['Start Time']
                              .isin(selected_spectrum.split()))].to_dict('list')
    shtml = ''
    for ke,va in data_table.items():
        shtml += f'<tr><th>{ke}</th><td>{va[0]}</td></tr>'
    return jsonify(shtml = shtml)

@app.route('/')
def index():
    years_data = fetchSameYear()
    default_years = sorted(years_data.keys())
    default_spectra = years_data[default_years[0]]
    stemp = render_template('spec_select.html',
                       years=default_years,
                       spectra=default_spectra,
                       table_data = {})    
    return stemp