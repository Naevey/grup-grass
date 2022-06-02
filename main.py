# import "packages" from flask
from flask import render_template, redirect, request, url_for, send_from_directory
from flask_login import login_required

from __init__ import app

from krug.app_crud import app_krug
from cruddy.app_crud import app_crud
from cruddy.app_crud_api import app_crud_api
from krug.query import students_all
from content import app_content
from uploady.app_upload import app_upload

app.register_blueprint(app_upload)
app.register_blueprint(app_krug)
app.register_blueprint(app_crud)
app.register_blueprint(app_crud_api)
# app.register_blueprint(app_content)
# connects default URL to render index.html

@app.route('/')
@login_required
def index():
    return render_template("index.html")

@app.route('/calendar')
def calender():
    return render_template("calendar.html")

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

# serve uploaded files so they can be downloaded by users.
@app.route('/uploads/<name>')
def uploads_endpoint(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


# register "uploads_endpoint" endpoint so url_for will find all uploaded files
app.add_url_rule(
    "/" + app.config['UPLOAD_FOLDER'] + "/<name>", endpoint="uploads_endpoint", build_only=True
)


if __name__ == "__main__":
    app.run(debug=True)
