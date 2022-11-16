

from flask_sqlalchemy  import SQLAlchemy
import sqlalchemy

# app.py

from flask import Flask, render_template, request, jsonify
import json

# Initialize the Flask application
app = Flask(__name__, template_folder="webgui")

def get_dropdown_values():

    """
    dummy function, replace with e.g. database call. If data not change, this function is not needed but dictionary
could be defined globally
    """

    # Create a dictionary (myDict) where the key is 
    # the name of the brand, and the list includes the names of the car models
    # 
    # Read from the database the list of cars and the list of models. 
    # With this information, build a dictionary that includes the list of models by brand. 
    # This dictionary is used to feed the drop down boxes of car brands and car models that belong to a car brand.
    # 
    # Example:
    #
    # {'Toyota': ['Tercel', 'Prius'], 
    #  'Honda': ['Accord', 'Brio']}

    #carbrands = Carbrands.query.all()
    # Create an empty dictionary
    myDict = {}
    for p in carbrands:
    
        key = p.brand_name
        brand_id = p.brand_id

        # Select all car models that belong to a car brand
        q = Carmodels.query.filter_by(brand_id=brand_id).all()
    
        # build the structure (lst_c) that includes the names of the car models that belong to the car brand
        lst_c = []
        for c in q:
            lst_c.append( c.car_model )
        myDict[key] = lst_c
    
    
    class_entry_relations = myDict
                        
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

    # process the two selected values here and return the response; here we just create a dummy string

    return jsonify(random_text="You selected the car brand: {} and the model: {}.".format(selected_class, selected_entry))




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