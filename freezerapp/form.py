from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, IntegerField, RadioField, HiddenField
from wtforms.validators import DataRequired, Length, Regexp
from flask_wtf.file import FileField, FileRequired

class Add_Replace(FlaskForm):
    project_name = StringField("project name", validators = [DataRequired()])
    plate_name = StringField("plate name",  validators = [DataRequired(),Regexp('[PRD]B?[0-9][0-9]')])
    cell_type = SelectField("cell type", choices = [('glycerin','glyc'),('PPE',"PPE")])
    date = DateField("date",format = '%d/%m/%Y')
    initials = StringField("initials" , validators = [DataRequired()])
    submit = SubmitField("Submit")

class Edit_Box(FlaskForm):
    new_name = StringField("New name", validators = [DataRequired()])
    submit = SubmitField("Submit")

class Remove(FlaskForm):
    plate_name = StringField("plate name",  validators = [DataRequired(),Regexp('.*')])
    position = StringField("position", validators = [DataRequired(),Regexp('[PBTK][0-9][0-9][A-F]')])
    username = StringField("username" , validators = [DataRequired()])
    submit = SubmitField("Submit")
    
class Move(FlaskForm):
    plate_name = StringField("plate name",  validators = [DataRequired(),Regexp('.*')])
    position = StringField("position", validators = [DataRequired(),Regexp('[PBTK][0-9][0-9][A-F]')])
    username = StringField("username" , validators = [DataRequired()])
    submit = SubmitField("Submit")

class Add_Freezer(FlaskForm):
    name = StringField("Freezer name", validators = [DataRequired()])
    mastersheet = FileField("Mastersheet", validators = [FileRequired()])
    submit = SubmitField("Submit")