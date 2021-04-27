# -*- coding: utf-8 -*-
from django.contrib import messages
from flask import Flask, render_template, request, flash, Markup, jsonify
from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from mapgen import GenMap
from data_check import DataCheck
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField, TextField,\
    FormField, SelectField, FieldList
from wtforms.validators import DataRequired, Length
from wtforms.fields import *

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '420dev710'

#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

# set default button style and size, will be overwritten by macro parameters
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'
# app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'lumen'  # uncomment this line to test bootswatch theme

bootstrap = Bootstrap(app)
#db = SQLAlchemy(app)
#csrf = CSRFProtect(app)


class HandleForm(FlaskForm):
    handle = StringField(render_kw={'placeholder': 'Enter Instagram Handle'})
    submit = SubmitField("Generate Map")


@app.route('/')
def index():
    form = HandleForm()
    return render_template('index.html', form=form)


@app.route('/map', methods=['POST'])
def mapgen():
    # draw inputs, get handle, scrape location addresses,
    handle_form = HandleForm(request.form)
    data = str(handle_form.handle.data)
    handle = data.replace("@","").replace(" ","") #accounts for @ or space in search field
    try:
        print("-----")
        print(handle)
        print("-----")
        DataCheck(handle).db_check()
        my_map = GenMap(handle)
        my_map.gen_map()
        map_name = f"map_{handle}.html"
        return render_template(map_name)
    except:
        error = "Please Try again"
        return render_template('index.html', error=error)


# @app.route('/map_page/<handle>', methods=['GET'])
# def handles(handle):
#   return render_template(f"map_{handle}.html", handle=handle)

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/at_viewer', methods=['GET', 'POST'])
def at_viewer():
    return redirect("https://atviewer.herokuapp.com/")

@app.route('/explore', methods=['GET', 'POST'])
def explore():
    return render_template('explore.html')




if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
