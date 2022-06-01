import os
from __init__ import app, db
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from  model import Uploads

from cruddy.query import user_by_id

# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
app_content = Blueprint('content', __name__,
                        url_prefix='/content',
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='static')
files_uploaded = []

def uploads_all():
    table = Uploads.query.all()
    json_ready = [item.read() for item in table]
    return json_ready

# def uploads_by_studentID(studentID):
#     return Uploads.query.filter_by(studentID=studentID).all()

def upload_by_uploadID(imageID):
    return Uploads.query.filter_by(uploadID=uploadID).first()

def upload_by_home():
    return Uploads.query.filter_by(home=True).first()

# Page to upload content page
@app_content.route('/')
@login_required
def upload():
    # grab user object (uo) based on current login
    uo = user_by_id(current_user.userID)
    user = uo.read()  # extract user record (Dictionary)
    # sortedtable = uploads_by_studentID(current_user.userID)
    # load content page
    return render_template('upload.html', user=user, table=uploads_all())

'''
@app_content.route('/gallery/')
@login_required
def gallery():
    images = images_by_authorID(12)
    return render_template('photograph.html', images=images)
'''

@app_content.route('/delete/', methods=["POST"])
@login_required
def delete():
    uploadID = request.form['delete-value']
    upload = upload_by_uploadID(uploadID)
    os.remove(upload.path[1:])
    upload.delete()
    return redirect(url_for('main.upload'))

@app_content.route('/update/', methods=["POST"])
@login_required
def update():
    uploadID = request.form['update-id-value']
    newCaption = request.form['update-value']
    upload = upload_by_uploadID(uploadID)
    upload.update(newCaption)
    return redirect(url_for('main.upload'))

@app_content.route('/homeupdate/', methods=["POST"])
@login_required
def homeupdate():
    uploadID = request.form['homeupdate-id-value']
    upload = upload_by_uploadID(uploadID)
    try:
        original = upload_by_home()
        original.homeupdate(False)
    except:
        pass
    upload.homeupdate(True)
    return redirect(url_for('main.upload'))


# Notes create/add
@app_content.route('/upload/', methods=["POST"])
@login_required
def upload():
    try:
        # grab file object (fo) from user input
        # The fo variable holds the submitted file object. This is an instance of class FileStorage, which Flask imports from Werkzeug.
        fo = request.files['filename']
        # save file to location defined in __init__.py
        # ... os.path uses os specific pathing for web server
        # ... secure_filename checks for integrity of name for operating system. Pass it a filename and it will return a secure version of it.
        po = Uploads(
            request.form.get("description"),
            url_for('static', filename='uploads/' + fo.filename),
            current_user.userID,
            current_user.name,
            False
        )
        po.create()

        fo.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(fo.filename)))
        # ... add to files_uploaded to give feedback of success on HTML page
        files_uploaded.insert(0, url_for('static', filename='uploads/' + fo.filename))
    except:
        # errors handled, but specific errors are not messaged to user
        pass
    # reload content page
    return redirect(url_for('main.upload'))

if __name__ == "__main__":
    db.create_all()
    po = Uploads(
        "Hello",
        '//image.png',
        '66',
        'Joe',
        False
    )
    db.session.add(po)
    db.session.commit()