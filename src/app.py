

# app.py
# based on dropdown code from https://stackoverflow.com/questions/25978879/how-to-create-chained-selectfield-in-flask-without-refreshing-the-page

from flask import Flask, render_template, request, jsonify
import os
from createandfilldb import fetchSameYear, findFilname
from utilfnc import read_cal_spec
import numpy as np
# Initialize the Flask application

app = Flask(__name__,
            static_url_path="",
            static_folder="static",
            template_folder="webgui")

@app.route('/_update_dropdown')
def update_dropdown():
    """
    Flask function to publich the values from the database in the drop down menu
    """
    selected_year = request.args.get('selected_year', type=str)
    updated_values = fetchSameYear()[selected_year]
    html_string_selected = ''
    for entry in updated_values:
        html_string_selected += f'<option value="{entry}">{entry}</option>'

    return jsonify(html_string_selected=html_string_selected)


@app.route('/_process_data')
def process_data():
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

@app.route('/')
def index():

    """
    initialize drop down menus
    """

    years_data = fetchSameYear()

    default_years = sorted(years_data.keys())
    default_spectra = years_data[default_years[0]]
    return render_template('index.html',
                       years=default_years,
                       spectra=default_spectra
                       )