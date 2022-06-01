# import "packages" from flask
from flask import Flask, render_template, request
from flask_login import login_required

from __init__ import app

from krug.app_crud import app_krug
from cruddy.app_crud import app_crud
from cruddy.app_crud_api import app_crud_api
from krug.query import students_all
from content import app_content


app.register_blueprint(app_krug)
app.register_blueprint(app_crud)
app.register_blueprint(app_crud_api)
# connects default URL to render index.html

@app.route('/')
@login_required
def index():
    return render_template("index.html")

@app.route('/calendar')
def calender():
    return render_template("calendar.html")

@app.route('/upload')
@login_required
def upload():
    return render_template("upload.html", table=students_all() )
@app.route('/studentworks')
@login_required
def studentworks():
    return render_template("studentworks.html", table=students_all() )

@app.route('/blog')
@login_required
def blog():
    return render_template("blog.html")

@app.route('/thread')
def thread():
    return render_template("thread.html")

@app.route('/resources')
def resources():
    return render_template("resources.html")

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

if __name__ == "__main__":
    app.run(debug=True)
