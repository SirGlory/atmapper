# -*- coding: utf-8 -*-
from django.contrib import messages
from flask import Flask, render_template, request, flash, Markup, jsonify
from flask.views import MethodView
from werkzeug.utils import redirect
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

from scrape_last_photos import PhotoUrls

app = Flask(__name__)
app.secret_key = 'devCPT'

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

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/viewerabout', methods=['GET'])
def viewer_about():
    return render_template('viewer_about.html')


@app.route('/explore', methods=['GET'])
def explore():
    return render_template('explore.html')


@app.route('/atviewer')
def at_viewer():
    form = HandleForm()
    return render_template('viewer_index.html', form=form)


@app.route('/photos', methods=['POST'])
def photogen():
    handle_form = HandleForm(request.form)
    data = str(handle_form.handle.data)
    print(data)
    handle = data.replace("@", "").replace(" ", "")  # accounts for @ or space in search field
    linkss = PhotoUrls(handle=handle).photo_links()
    #url = "https://www.picuki.com/app/controllers/proxy_image.php?url=https%3A%2F%2Finstagram.flwo4-2.fna.fbcdn.net%2Fv%2Ft51.2885-15%2Fe35%2F177761008_552220862411476_2642127834352225148_n.jpg%3Ftp%3D1%26_nc_ht%3Dinstagram.flwo4-2.fna.fbcdn.net%26_nc_cat%3D104%26_nc_ohc%3Di3mBDruzVloAX8ef9fy%26edm%3DAP_V10EBAAAA%26ccb%3D7-4%26oh%3D0a4015286338ed1145c5e026ab5e9522%26oe%3D60ADC242%26_nc_sid%3D4f375e"
    url = linkss[0]
    links = linkss[1:-1]
    return render_template('viewer_photos.html', images=links, first_image=url)
    #return render_template('viewer_photos.html', first_image=url)





if __name__ == '__main__':
    app.run()
