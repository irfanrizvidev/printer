import os
import json
from flask import Flask, flash, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt


app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')
mongo = PyMongo(app)


@app.before_request
def before_request():
    scheme = request.headers.get('X-Forwarded-Proto')
    if scheme and scheme == 'http' and request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('user'))
        
    return render_template("login.html")
    

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'username' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            session['user_type'] = login_user['admin']
            return redirect(url_for('index'))

    return render_template("login.html", message="Invalid username or password!")


@app.route('/user')
def user():
    if 'username' in session:
        admin = session['user_type']
        if admin:
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('resident'))

    return redirect(url_for("index"))


@app.route('/admin/dashboard')
def admin():
    if 'username' in session and session['user_type'] == True:
        if session['username'] == 'irfanrizvidev':
            return render_template('admin.html', residents=mongo.db.users.find({ "username": { '$ne': "irfanrizvidev" } },
                {'password':0, '_id':0, 'admin':0}), requests=mongo.db.requests.find({'complete': False},
                {'_id':0, 'complete':0}))
        else:
            return render_template('admin.html', residents=mongo.db.users.find({'admin': False},
                {'password':0, '_id':0, 'admin':0}), requests=mongo.db.requests.find({'complete': False},
                {'_id':0, 'complete':0}))

    return redirect(url_for("index"))

@app.route('/topup', methods=['POST'])
def topup():
    if request.method == 'POST' and 'username' in session and session['user_type'] == True:
        user = request.form['usertopup']
        topup = request.form['topup']
        with open('topup.json') as f:
            data = json.load(f)
        if(data["name"] == "" and data["topup"] == ""):
            data["name"] = user
            data["topup"]= topup
            with open('topup.json', 'w') as json_file:
                json.dump(data, json_file)
            flash('Topup in Queue.')
            return redirect(url_for('admin', _anchor='test2'))
        else:
            flash('Another topup in Queue already.')
            return redirect(url_for('admin', _anchor='test2'))

    return redirect(url_for("index"))
               

@app.route('/deleteuser', methods=['POST'])
def deleteuser():
    if request.method == 'POST' and 'username' in session and session['user_type'] == True:
        user = request.form['userdelete']
        queryResponse = mongo.db.users.delete_one({'username': user})
        flash('User Delete Successfuly.')
        return redirect(url_for('admin', _anchor='test2'))

    return redirect(url_for("index"))

@app.route('/admin/dashboard')
def edituser():
    if 'username' in session and session['user_type'] == True:
        if session['username'] == 'irfanrizvidev':
            return render_template('admin.html', residents=mongo.db.users.find({},
                {'password':0, '_id':0, 'admin':0}), requests=mongo.db.requests.find({'complete': False},
                {'_id':0, 'complete':0}))
        else:
            return render_template('admin.html', residents=mongo.db.users.find({'admin': False},
                {'password':0, '_id':0, 'admin':0}), requests=mongo.db.requests.find({'complete': False},
                {'_id':0, 'complete':0}))

    return redirect(url_for("index"))   


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST' and 'username' in session and session['user_type'] == True:
        users = mongo.db.users
        existing_user = users.find_one({'username' : request.form['username']})

        if existing_user is None:
            if(request.form.get('adminorresident')):
                adminorresident = True
            else:
                adminorresident = False
            # generates bytes instead of a string
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            # converting password to string to match when loggin in
            hashpass = str(hashpass.decode('utf-8'))
            users.insert({'username' : request.form['username'], 'password' : hashpass, 'admin': adminorresident})
            
            flash('User Created Successfully.')
            return redirect(url_for('admin', _anchor='test4'))
        elif "edit" in request.form:
            if(request.form['edit'] == 'edit'):
                return request.form['edit']

        flash('User Already Exists.')
        return redirect(url_for('admin', _anchor='test4'))
        
    return redirect(url_for('admin', _anchor='test4'))


@app.route('/user/dashboard')
def resident():
    if 'username' in session and session['user_type'] == False:
        return render_template('resident.html')

    return redirect(url_for("index"))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = os.getenv('PRINTER_FLASK_KEY')
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
    
