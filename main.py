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


@app.route('/everitt/')
def everit():
    return render_template("aboutme/everitt.html")


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

@app.route('/login/', methods=["GET", "POST"])
def main_login():
    # obtains form inputs and fulfills login requirements
    global next_page
    if request.form:
        email = request.form.get("email")
        password = request.form.get("password")
        if login(email, password):
            try:        # try to redirect to next page
                temp = next_page
                next_page = None
                return redirect(url_for(temp))
            except:     # any failure goes to home page
                return redirect(url_for('index'))


    # if not logged in, show the login page
    return render_template("login.html")


# if login url, show phones table only
@app.route('/logout/', methods=["GET", "POST"])
@login_required
def main_logout():
    logout()
    return redirect(url_for('index'))


@app.route('/authorize/', methods=["GET", "POST"])
def main_authorize():
    error_msg = ""
    # check form inputs and creates user
    if request.form:
        # validation should be in HTML
        user_name = request.form.get("user_name")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")  # password should be verified
        if password1 == password2:
            if authorize(user_name, email, password1):
                return redirect(url_for('main_login'))
        else:
            error_msg = "Passwords do not match"
    # show the auth user page if the above fails for some reason
    return render_template("authorize.html", error_msg=error_msg)
# runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True)
