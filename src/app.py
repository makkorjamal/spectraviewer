

from flask_sqlalchemy  import SQLAlchemy
import sqlalchemy

# app.py

from flask import Flask, render_template, request, jsonify
import json
import plotly
import plotly.express as px
from createandfilldb import FetchSameYear, FindFilname
from utilfnc import read_cal_spec
import numpy as np
import pandas as pd

# Initialize the Flask application

global intensity, wavenumbers
app = Flask(__name__, template_folder="webgui")
def get_dropdown_values():

    class_entry_relations = FetchSameYear() 
                        
    return class_entry_relations


@app.route('/_update_dropdown')
def update_dropdown():

    # the value of the first dropdown (selected by the user)
    selected_class = request.args.get('selected_class', type=str)

    # get values for the second dropdown
    updated_values = get_dropdown_values()[selected_class]

    # create the value sin the dropdown as a html string
    html_string_selected = ''
    for entry in updated_values:
        html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)

    return jsonify(html_string_selected=html_string_selected)


@app.route('/_process_data')
def process_data():
    selected_class = request.args.get('selected_class', type=str)
    selected_entry = request.args.get('selected_entry', type=str)
    _,_,filename=FindFilname(selected_entry)
    #jsonified = jsonify(random_text="Year {} file {} and filename {} selected.".format(selected_class, selected_entry, filename))
    #sp_plotter(filename)
    intensity, wavenumbers = read_cal_spec(filename)
    jsonified = jsonify(intensity = intensity.tolist(), wavenumbers=np.round(wavenumbers,1).tolist())
    return jsonified

def sp_plotter(filename):

    intensity, wavenumbers = read_cal_spec(filename)
    sptuples = list(zip(wavenumbers, intensity))
    df = pd.DataFrame(sptuples, columns = ['wavenumber', 'intensity'])
    fig = px.line(df, x="wavenumber", y="intensity", title='Blah')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/')
def index():

    """
    initialize drop down menus
    """

    class_entry_relations = get_dropdown_values()

    default_classes = sorted(class_entry_relations.keys())
    default_values = class_entry_relations[default_classes[0]]
    return render_template('index.html',
                       all_classes=default_classes,
                       all_entries=default_values)