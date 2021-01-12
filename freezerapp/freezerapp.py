from flask import Flask, request,render_template,redirect,url_for,send_file
from form import Add_Replace, Remove, Move, Edit_Box, Add_Freezer
from database import import_mastersheet, get_samples, add_sample, Rack, Sample, Freezer, app, db, get_freezer_map, get_freezers, save_layout, create_blank_cabinet
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
import matplotlib
import sys


matplotlib.use('Agg')

@app.route("/home")
def home_page():
    addReplace =  Add_Replace()
    freezer_list = get_freezers()
    return render_template('home.html', add_replace = addReplace, freezer_list = freezer_list)

@app.route("/freezer-map/<freezer_name>")
def freezer_map(freezer_name = None):
    addReplace =  Add_Replace()
    print("freezer name: ", freezer_name, file=sys.stdout)
    f_map = get_freezer_map(freezer_name)
    return render_template('freezermap.html', add_replace = addReplace, f_map = f_map, freezer_name = freezer_name)

@app.route("/box-display/<freezer_name>/<box_ids>", methods=['GET','POST'])
def box_display(freezer_name = None, box_ids = None):
    addReplace =  Add_Replace()
    if request.method == 'POST':
        name = request.form['new_name']
        loc = request.form['loc']
        freezer = Freezer.query.filter_by(name = freezer_name).first()
        add_sample(loc, name, freezer)

        return redirect(request.url)
    else:
        start, end = box_ids.split('-')
        i = int(start[1:3])
        j = int(end[1:3])
        print(i,j,file=sys.stdout)
        # safety
        if i > j:
            temp = i 
            i = j
            j = temp

        # dictionary of dictionaries
        boxes = {}
        for x in range(i, (j+1)):
            box_name = ''
            if(x < 10):
                box_name = "B0{}".format(x)
            else:
                box_name = "B{}".format(x)
            print(box_name, file=sys.stdout)
            boxes[box_name] = get_samples(freezer_name, box_name)
        
        print(boxes, file=sys.stdout)
        letters = ['A','B','C','D','E']
        edit_box = Edit_Box()

        return render_template('box_rack_display.html', add_replace = addReplace, title = box_ids, letters = letters, boxes = boxes, freezer_name = freezer_name, edit_box = edit_box)

@app.route("/plate-display/<freezer_name>/<plate_ids>", methods=['GET','POST'])
def plate_display(freezer_name = None, plate_ids = None):
    if request.method == 'POST':
        # gather data into variables
        project_name = request.form['project_name']
        plate_name = request.form['plate_name']
        cell_type = request.form['cell_type']
        date = request.form['date']
        initials = request.form['initials']
        name = "{}_{} {} {} {}".format(project_name, plate_name, cell_type, date, initials)
        loc = request.form['loc']

        # print(name,loc, file=sys.stdout)
        freezer = Freezer.query.filter_by(name = freezer_name).first()
        add_sample(loc, name, freezer)
        
        # plate_name_1 , plate_name_2 = plate_ids.split('-')
        # print( Sample.query.filter_by(loc = loc).all(), file=sys.stdout)
        return redirect(request.url)
    else:
        testing = "hello"
        addReplace =  Add_Replace()
        letters = ['A','B','C','D','E','F','G']
        plate_name_1 , plate_name_2 = plate_ids.split('-')
        print(plate_name_1, plate_name_2, file=sys.stdout)
        rack_1 = get_samples(freezer_name, plate_name_1)
        rack_2 = get_samples(freezer_name, plate_name_2)

        # print(rack_1, rack_2, file=sys.stdout)
        
        return render_template('plate_display.html',test_name = testing, add_replace = addReplace, letters = letters, plate_name_1 = plate_name_1, plate_name_2 = plate_name_2, p1_dict = rack_1, p2_dict = rack_2)

@app.route("/edit-freezer/<freezer_name>", methods=['GET','POST'])
def edit_freezer(freezer_name = None):
    if request.method == 'POST':
        data = request.get_json()
        print(data, file=sys.stdout)
        if 'command' in data:
            print('add new freezer', file=sys.stdout)
            freezer = Freezer.query.filter_by(name = freezer_name).first()
            create_blank_cabinet(freezer)
            return request.url
        else:
            save_layout(freezer_name, data)
            url = "/freezer-map/{}".format(freezer_name)
            return url
    else :
        addReplace =  Add_Replace()
        f_map = get_freezer_map(freezer_name)
        return render_template('map_editor.html', add_replace = addReplace, f_map = f_map, freezer_name = freezer_name)

@app.route("/add-freezer", methods=['GET','POST'])
def add_freezer():
    if request.method == 'GET':
        addReplace =  Add_Replace()
        add_freezer = Add_Freezer()
        return render_template('add_freezer.html', add_replace = addReplace, add_freezer = add_freezer)
    else:
        mastersheet = request.form['mastersheet']
        name = request.form['name']
        import_mastersheet(mastersheet, db, name)
        return redirect(url_for('home_page'))

if __name__ == "__main__":        # on running python app.py
    # db.create_all()
    # import_mastersheet("mastersheet-demo.xlsx", db, "Banana")
    app.run(debug=True)  


