# import "packages" from flask
from flask import Flask, render_template, request

# create a Flask instance
app = Flask(__name__)


# connects default URL to render index.html
@app.route('/')
def index():
    return render_template("index.html")


# connects /kangaroos path to render everit.html
@app.route('/everit/')
def everit():
    return render_template("everit.html")


@app.route('/erik/')
def erik():
    return render_template("erik.html")


@app.route('/matthew/')
def matthew():
    return render_template("mattehw.html")

@app.route('/kurtis/')
def kurtis():
    return render_template("kurtis.html")
@app.route('/calendar')
def calender():
    return render_template("calendar.html")

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
