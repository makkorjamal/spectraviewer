

# app.py

from flask import Flask, render_template, request, jsonify
import os
from createandfilldb import FetchSameYear, FindFilname
from utilfnc import read_cal_spec
import numpy as np
import pandas as pd

# Initialize the Flask application

global intensity, wavenumbers
spimages = os.path.join('static','data', 'images')
app = Flask(__name__, template_folder="webgui")
app.config['UPLOAD_FOLDER'] = spimages
def get_dropdown_values():

    class_entry_relations = FetchSameYear() 
                        
    return class_entry_relations


@app.route('/_update_dropdown')
def update_dropdown():
    """
    Flask function to publich the values from the database in the drop down menu
    """
    selected_year = request.args.get('selected_year', type=str)
    updated_values = get_dropdown_values()[selected_year]
    html_string_selected = ''
    for entry in updated_values:
        html_string_selected += f'<option value="{entry}">{entry}</option>'

    return jsonify(html_string_selected=html_string_selected)


@app.route('/_process_data')
def process_data():
    #selected_year = request.args.get('selected_year', type=str)
    selected_spectrum = request.args.get('selected_spectrum', type=str)
    _,_,_,sp_filename,dg_filename,im_filename=FindFilname(selected_spectrum)
    intensity, wavenumbers = read_cal_spec(sp_filename)
    digitized_spec = np.loadtxt(dg_filename).tolist()
    jsonified = jsonify(intensity = intensity.tolist(),
    wavenumbers=np.round(wavenumbers,1).tolist(), 
    digitized_spec = digitized_spec,
    digitized_lbl = np.arange(len(digitized_spec)).tolist(),
    im_filename = im_filename) # this sends the intensity and the wavelength to be used by js plot functio
    return jsonified

@app.route('/')
def index():

    """
    initialize drop down menus
    """

    class_entry_relations = get_dropdown_values()

    default_years = sorted(class_entry_relations.keys())
    default_spectra = class_entry_relations[default_years[0]]
    return render_template('index.html',
                       years=default_years,
                       spectra=default_spectra,
                       spec_image = '1105_1148.jpg'
                       )