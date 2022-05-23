# import "packages" from flask
from flask import Flask, render_template, request
from flask_login import login_required

from __init__ import app

from cruddy.app_crud import app_crud
from cruddy.app_crud_api import app_crud_api


app.register_blueprint(app_crud)
app.register_blueprint(app_crud_api)
# connects default URL to render index.html
@app.route('/')
@login_required
def index():
    return render_template("index.html")


# connects /kangaroos path to render everit.html
@app.route('/everit/')
def everit():
    return render_template("aboutme/everit.html")


@app.route('/erik/')
def erik():
    return render_template("aboutme/erik.html")


@app.route('/matthew/')
def matthew():
    return render_template("aboutme/mattehw.html")

@app.route('/kurtis/')
def kurtis():
    return render_template("aboutme/kurtis.html")
@app.route('/calendar')
def calender():
    return render_template("calendar.html")

@app.route('/upload')
@login_required
def upload():
    return render_template("upload.html")
@app.route('/blog')
def blog():
    return render_template("blog.html")

@app.route('/stub/')
def stub():
    return render_template("stub.html")
@app.route('/greet', methods=['GET', 'POST'])
def greet():
    # submit button has been pushed
    if request.form:
        name = request.form.get("name")
        if len(name) != 0:  # input field has content
            return render_template("greet.html", name=name)
    # starting and empty input default
    return render_template("greet.html", name="World")


# runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True)
