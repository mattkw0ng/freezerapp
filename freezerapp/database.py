from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import itertools
import os

PEOPLE_FOLDER = os.path.join('static', 'uploads')
SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

# freezer
# cabinets
# compartments
# racks
# samples

class Freezer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30)) 
    # list of cabinets in freezer for the freezer map
    cabinets = db.relationship("Cabinet", backref="freezer")
    # essentially the mastersheet, containing locations and names of samples
    samples = db.relationship("Sample", backref="freezer")
    def __repr__(self):
        return '<Freezer %r>' % self.name

class Cabinet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Identifier for each cabinet (not zero indexed)
    number = db.Column(db.Integer)
    freezer_id = db.Column(db.Integer, db.ForeignKey('freezer.id'))
    # 10 compartments per cabinet 
    compartments = db.relationship("Compartment", backref="cabinet")

class Compartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cabinet_id = db.Column(db.Integer, db.ForeignKey('cabinet.id'))
    # plate, box, or tube rack
    rack_type = db.Column(db.String(5))
    vacancy = db.Column(db.Integer)
    # placement within the cabinet (zero indexed)
    ordering = db.Column(db.Integer)
    # 2-4 racks per compartment
    racks = db.relationship("Rack", backref="compartment")

class Rack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4))
    compartment_id = db.Column(db.Integer, db.ForeignKey('compartment.id'))
    # samples = db.relationship("Sample", backref="rack")

class Sample(db.Model):
    # location P01A1 - rack P01
    loc = db.Column(db.String(5), primary_key=True)
    rack = db.Column(db.String(3))
    name = db.Column(db.String(100), nullable=False)
    freezer_id = db.Column(db.Integer, db.ForeignKey('freezer.id'))

    def __repr__(self):
        return '<Sample %r>' % self.name

# class UpdateLog(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     # remove, add, edit, validate
#     action = db.Column(db.String(6))
#     message = db.Column(db.String(75))
#     time_stamp = db.Column(db.DateTime)
#     freezer_id = db.Column(db.Integer, db.ForeignKey('freezer.id'))

# ------------------------------------------------------------------------------------------------------

def import_mastersheet(mastersheet, db, freezer_name):
    # read in mastersheet, and skip first row, with the second row as the header
    df = pd.read_excel(mastersheet, skiprows=[0])
    print(df.head)
    num_cols = len(df.columns)
    print("---number of columns---", num_cols)
    # iterate through each column in pairs (skip the last three)
    freezer = Freezer.query.filter_by(name = freezer_name).first()
    if not freezer:
        freezer = Freezer(name = freezer_name)
        db.session.add(freezer)
        db.session.commit()

    empty_list = ['#REF!', '-', 'Name', '']

    x = 0
    while x < (num_cols - 3):
        # take each column
        locations = df.iloc[:, x]
        names = df.iloc[:, x+1]
        print("---names---",names.tolist()[:10])
        print("---locations---", locations.tolist()[:10])
        # iterate through each column simultaneously
        for loc, name in zip(locations, names):
            if name in empty_list:
                name = 'Empty'
            if pd.isna(loc):
                break
            add_sample(loc, name, freezer)
        # skip a row in order to keep in pairs
        x+=2
    # commit changes to the database
    db.session.commit()

def add_sample(loc, name, freezer):
    # if name is null, change it to "empty"
    if pd.isna(name):
        name = 'Empty'
    rack_loc = str(loc)[:3]

    # check if the name is in the database and edit it .. else add to database
    match = Sample.query.filter_by(loc=loc).first()
    if match:
        match.name = name 
    else:
        sample = Sample(loc = loc, rack = rack_loc, name = name, freezer = freezer)
        db.session.add(sample)
    db.session.commit()


# simple query mapping funtion that grabs all samples from a certain rack and returns a dictionary
def get_samples(freezer_name, rack_name):
    freezer = Freezer.query.filter_by(name = freezer_name).first()
    samples = Sample.query.filter(Sample.freezer_id == freezer.id).filter_by(rack = rack_name).all()
    dictionary = {}
    for sample in samples:
        dictionary[sample.loc] = sample.name
    return dictionary

# given a freezer name, returns a nested array of the 
def get_freezer_map(freezer_name):
    freezer = Freezer.query.filter_by(name = freezer_name).first()

    # if the map has not been created yet
    if not freezer.cabinets:
        create_blank_cabinet(freezer)

    # freezer || n cabinets --> 10 Compartments --> 2-4 Racks
    freezer_map = [] # n cabinets
    for cabinet in freezer.cabinets:
        compartment_list = [] # 10 compartments

        for compartment in cabinet.compartments:
            compartment_dict = {}
            compartment_dict['vacancy'] = compartment.vacancy

            rack_list = [] # 2-4 items
            for rack in compartment.racks:
                rack_list.append(rack.name)
            compartment_dict['list'] = rack_list
            compartment_dict['type'] = compartment.rack_type
            compartment_list.append(compartment_dict)
        
        print(cabinet.number , str(compartment_list))
        freezer_map.append(compartment_list)
    
    return freezer_map

def get_freezers():
    all_freezers = Freezer.query.all()
    freezer_list = []
    for freezer in all_freezers:
        name = freezer.name
        type_count = {}

        for cabinet in freezer.cabinets:
            for compartment in cabinet.compartments:
                rack_type = compartment.rack_type
                if rack_type not in type_count:
                    type_count[rack_type] = 1
                else:
                    type_count[rack_type] = type_count[rack_type] + 1
        temp_list = [name,type_count]
        freezer_list.append(temp_list)
    return freezer_list

def create_blank_cabinet(freezer):
    print("creating cabinet")
    cabinet_number = len(freezer.cabinets)+1
    cabinet = Cabinet(freezer = freezer, number = cabinet_number)
    db.session.add(cabinet)
    for x in range(10):
        compartment = Compartment(cabinet = cabinet, rack_type = 'empty', vacancy = 1, ordering = x)
        db.session.add(compartment)
    db.session.commit()


def get_cabinet_dict(freezer_name):
    freezer = Freezer.query.filter_by(name = freezer_name).first()
    cabinet_dict = {}
    for cabinet in freezer.cabinets:
        cabinet_dict[cabinet.number] = cabinet
    return cabinet_dict

def delete_cabinet(freezer_name, cabinet_number):
    cabinet_dict = get_cabinet_dict(freezer_name)
    deleted = cabinet_dict.get(cabinet_number)
    db.session.delete(deleted)
    db.session.commit()
    


# calculates the available space in the rack and returns an integer
# (1-10) where 1 means empty and 10 means full
def calculate_vacancy(rack_list, freezer):
    total = 0
    filled = 0
    for rack in rack_list:
        samples = Sample.query.filter_by(freezer = freezer).filter_by(rack = rack).all()
        for sample in samples:
            total += 1
            if sample.name != 'Empty':
                filled += 1

    if total == 0:
        # if its completely empty return 1
        return 1

    vacancy = round((filled/total)*9) + 1
    return vacancy

# save the layout of the freezer
def save_layout(freezer_name, layout):
    freezer = Freezer.query.filter_by(name=freezer_name).first()
    cabinet_dict = get_cabinet_dict(freezer_name)
    cabinet_index = 1;
    # iterate through each cabinet
    for cabinet in layout:
        # find cabinet in the database
        db_cabinet = cabinet_dict.get(cabinet_index)

        compartment_index = 0;
        # iterate through each compartment
        for compartment in cabinet:
            # find compartment in the database
            db_compartment = db_cabinet.compartments[compartment_index]
            
            db_compartment.rack_type = compartment['type']
            db_compartment.vacancy = calculate_vacancy(compartment['list'], freezer)
            # delete previous rows
            Rack.query.filter_by(compartment = db_compartment).delete()
            db.session.commit()
            # add new rows
            for rack in compartment['list']:
                new_rack = Rack(name = rack, compartment = db_compartment)
                db.session.add(new_rack)
            compartment_index += 1
        cabinet_index += 1
    db.session.commit()




     