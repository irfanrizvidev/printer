# This application is developed by Syed Irfan Rizvi. The purpose of the app is to allow residents to topup users without physical contact
# with the printer. It is ideal due to COVID-19 pandemic. The application has three user roles super admin, admin and residents. The super
# user could edit all users (admins and residents) alike. The super user could also perform all the funcion an admin can perform.

# The residents could make topup requests from their own dashboards after loggin in. The admins could see the requests in their dashboards
# and approve the requests. The admins could also topup user accounts without users creating requests. it would be ideal in a situaion, 
# where a user requests topup verbally. 

# JAVA APP:
# The topup is done by storing the username and topup amount in a json file. A JAVA application has been developed to access a authenticated 
# route on this website to reset the json file after a succesful topup. The JAVA App is installed on the laptop connected to the printer. 
# When the laptop is turned on the app is run and checks if there is a pending topup in topup.json, if there is, it connects to printer using 
# selenium API for java. It updates users account and connects back to the website using an authenticated route to reset the topup.json to perform
# further topups.

import os
import json
from datetime import date
from flask import Flask, flash, render_template, redirect, request, url_for, session, make_response
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt


# initializing app with DB URL
app = Flask(__name__)
# saved the DB URL for security reasons
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')
mongo = PyMongo(app)


# forcing HTTPS instead of HTTP to secure passwords and usernames
@app.before_request
def before_request():
    scheme = request.headers.get('X-Forwarded-Proto') # gets the header of the request
    if scheme and scheme == 'http' and request.url.startswith('http://'): # if the header has http request
        url = request.url.replace('http://', 'https://', 1) # change it with HTTPS
        code = 301 # set redirect code 301
        return redirect(url, code=code) # redirect to https version


# root route of the app 
@app.route('/')
def index():
    if 'username' in session: # if user is logged in 
        return redirect(url_for('user')) # goto user route for further authentication
        
    return render_template("login.html") # if not logged in show login.html
    

# route to login to user/admin dashboards
@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users # select users table in DB
    login_user = users.find_one({'username' : request.form['username']}) # query to check if user exists

    # if user exists
    if login_user:
        # check if typed password and encrypted password in DB are same
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username'] # if creadentials are correct set the session variables
            session['user_type'] = login_user['admin'] # set variable to know if user is admin or user
            return redirect(url_for('index')) # go back to root for redirection

    # if checks above fail then redirect to login.html with message
    return render_template("login.html", message="Invalid username or password!")


# root to redirect user to their dashboards
@app.route('/user')
def user():
    if 'username' in session: # if user is logged in
        # then check if it is a user or admin
        admin = session['user_type']
        if admin:
            # if it is admin go to admin root for further checks and redering
            return redirect(url_for('admin'))
        else:
            # if it is user go to resident root for further checks and redering
            return redirect(url_for('resident'))

    # if user not logged in go to login.html via root route
    return redirect(url_for("index"))


# route to load specific dashboard for user or superuser
@app.route('/admin/dashboard')
def admin():
    # if user logged in and admin
    if 'username' in session and session['user_type'] == True:
        # check if user if SUPER USER (irfanrizvidev)
        if session['username'] == 'irfanrizvidev':
            # if super user then render admin html with all the users (residents or admins alike) to be edited
            # show all the pending request approvals as well
            return render_template('admin.html', residents=mongo.db.users.find({ "username": { '$ne': "irfanrizvidev" } },
                {'password':0, '_id':0, 'admin':0}), requests=mongo.db.requests.find({'complete': False},
                {'_id':0, 'complete':0}))
        else:
            # if it is not a super user then load only the residents and the pending requests from database
            return render_template('admin.html', residents=mongo.db.users.find({'admin': False},
                {'password':0, '_id':0, 'admin':0}), requests=mongo.db.requests.find({'complete': False},
                {'_id':0, 'complete':0}))

    # if user is not logged in or not an admin simply go to login.html or resident dashboard via root route
    return redirect(url_for("index"))


# route to process topup requests
@app.route('/topup', methods=['POST'])
def topup():
    # if method is POST and user is logged in and user is admin
    if request.method == 'POST' and 'username' in session and session['user_type'] == True:
        user = request.form['usertopup'] # get name of user to topup from form
        topup = request.form['topup'] # get the amount to topup from form
        with open('topup.json') as f: # open topup.json as data dictionary
            data = json.load(f)
        if(data["name"] == "" and data["topup"] == ""): # check if name and topup fields are empty to verify there is no pending topup
            data["name"] = user # set the name field to user received from topup form
            data["topup"]= topup # set the topup field to amount received from topup form
            with open('topup.json', 'w') as json_file: # open topup.json to write this time the changed variables
                json.dump(data, json_file, indent=4) # with pretty printing
            # There are two methods to approve a topup, 1. approve a user request 
            # 2. admin could also topup without an electronic request made from user
            if "requestTopup" in request.form: # check if this is electronic request from user
                requests = mongo.db.requests # select the requests table from DB
                # update the status of request to completed
                requests.update_one({'user' : user, "complete" : False}, {"$set": { 'complete': True }})
                flash('Topup in Queue..')
                return redirect(url_for('admin', _anchor='test3')) # flash a message back to admin dashboard
            # if request is not electronic but verbal the admin could still topup
            else:
                # select requests table from DB
                requests = mongo.db.requests
                # create a new request with username, current date, amount of topup and the status completed
                requests.insert({'user' : user, 'date' : str(date.today().strftime('%d-%m-%Y')), 'amount': topup, 'complete': True})
                flash('Topup in Queue.')
                return redirect(url_for('admin', _anchor='test2')) # flash message of success to admin dashboard
        # if the name and topup fields are not empty means there is a unprocessed topup
        else:
            # if electronic request flash the message to admin dashboard tab 3
            if "requestTopup" in request.form:
                flash('Another topup in Queue already..')
                return redirect(url_for('admin', _anchor='test3'))
             # if verbal request flash the message to admin dashboard tab 2
            else:
                flash('Another topup in Queue already.')
                return redirect(url_for('admin', _anchor='test2'))
    # if user not logged in or method not POST or user not admin go to root for redirection
    return redirect(url_for("index"))
               

# route to clear an uprocessed topup from topup.json
@app.route('/admin/clear/topup', methods=['POST'])
def clearpending():
    # check that user is logged in and admin when the request is made
    if 'username' in session and session['user_type'] == True:
        # make blank dictionary to overwrite topup.json
        blank = {"name": "", "topup": ""}
        with open('topup.json', 'w') as json_file:
            json.dump(blank, json_file, indent=4)
        # flash message back to admin dashboard tab 2.
        flash("Pending topup cleared.")
        return redirect(url_for('admin', _anchor='test2'))
    # if not logged and admin go to root for redirection
    return redirect(url_for("index"))


# route to delete the user
@app.route('/deleteuser', methods=['POST'])
def deleteuser():
    # check if method is post and user logged in and admin
    if request.method == 'POST' and 'username' in session and session['user_type'] == True:
        user = request.form['userdelete'] # save user to be deleted as user
        queryResponse = mongo.db.users.delete_one({'username': user}) # make db query to delete the user
        # flash to admin dashboard tab 2
        flash('User Delete Successfuly.')
        return redirect(url_for('admin', _anchor='test2'))

    # if not admin or logged in redirect to root
    return redirect(url_for("index"))


# root to render admin dashboard
@app.route('/admin/dashboard')
def edituser():
    # if username and admin
    if 'username' in session and session['user_type'] == True:
        # check if user name is SUPER USER
        if session['username'] == 'irfanrizvidev':
            # if super user then show all the users to edit (admins and users) and show all pending topup requests
            return render_template('admin.html', residents=mongo.db.users.find({},
                {'password':0, '_id':0, 'admin':0}), requests=mongo.db.requests.find({'complete': False},
                {'_id':0, 'complete':0}))
        # if not super user but admin
        else:
            # only show the users/residents to edit and show all pending topup requests
            return render_template('admin.html', residents=mongo.db.users.find({'admin': False},
                {'password':0, '_id':0, 'admin':0}), requests=mongo.db.requests.find({'complete': False},
                {'_id':0, 'complete':0}))
    # if not logged in or admin go to root for redirectino
    return redirect(url_for("index"))   


# route to register new users or edit users
@app.route('/register', methods=['POST'])
def register():
    # if method is post user logged in and admin
    if request.method == 'POST' and 'username' in session and session['user_type'] == True:
        users = mongo.db.users # select users table in DB
        existing_user = users.find_one({'username' : request.form['username']}) # check if user exists already

        if existing_user is None: # if user does not exist
            # check the admin or resident switch in the form
            if(request.form.get('adminorresident')):
                adminorresident = True
            else:
                adminorresident = False
            # hash the passwords for security, generates bytes instead of a string
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            # converting password to string to match when loggin in
            hashpass = str(hashpass.decode('utf-8'))
            # insert a new user in users table with username hashed password and role of user
            users.insert({'username' : request.form['username'], 'password' : hashpass, 'admin': adminorresident})
            
            # flash the message of success to admin dashboard tab 4
            flash('User Created Successfully.')
            return redirect(url_for('admin', _anchor='test4'))
        # check if the same form was used to edit the user instead of creating user (Javascript used to achieve editing of users)
        elif "edit" in request.form:
            # making sure edit of the user is required
            if(request.form['edit'] == 'edit'):
                # check if role of the user is changed
                if(request.form.get('adminorresident')):
                    adminorresident = True
                else:
                    adminorresident = False

                # check if password is left empty which tells the intention to leave the password same
                if request.form['password'] and request.form['password'] != "" and request.form['password'] is not None:
                    # has the password if something was typed in password input field, generates bytes instead of a string
                    hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
                    # converting password to string to match when loggin in
                    hashpass = str(hashpass.decode('utf-8'))
                    # update the user with new information received from edit form
                    users.update_one({'username' : request.form['username']}, {"$set": { 'password' : hashpass, 'admin': adminorresident }})
                    # flash the success message to admin dashboard tab 2
                    flash('User Details Updated.')
                    return redirect(url_for('admin', _anchor='test2'))
                # if password is not entered then leave the password same and update the user
                users.update_one({'username' : request.form['username']}, {"$set": { 'admin': adminorresident }})
                # flash the message to admin dashboard tab 2
                flash('User Details Updated.')
                return redirect(url_for('admin', _anchor='test2'))
        # if the intention is to create new user but user already in database
        # flash message to admin dashboard tab 4
        flash('User Already Exists.')
        return redirect(url_for('admin', _anchor='test4'))
    # if user not logged in or not admin go to admin route for redirection
    return redirect(url_for('admin', _anchor='test4'))


# route to render user dashboard
@app.route('/user/dashboard')
def resident():
    # check that user is logged in and not admin
    if 'username' in session and session['user_type'] == False:
        # render resident.html with history of approved/successful topups and if there is an active pending request
        return render_template('resident.html', history=mongo.db.requests.find({ "user": session['username'], 'complete': True },
                {'complete':0, '_id':0}), activerequest=mongo.db.requests.find_one({"user": session['username'], 'complete': False},
                {'_id':0, 'complete':0}))
    # if not username or user go to root for redirection
    return redirect(url_for("index"))


# route to process resident/user topup request
@app.route('/resident/topup', methods=['POST'])
def residentTopUp():
    # check if user logged in and not admin
    if 'username' in session and session['user_type'] == False:
        topup = request.form['amount'] # get amount to topup from request form
        requests = mongo.db.requests # select requests table from DB
        # check if a pending request is already created for the current user
        existing_req = requests.find_one({'user' : session['username'], 'complete': False}) 

        if existing_req is None: # there is no active request
            # create a request with username, current date amount and status incomplete. 
            requests.insert({'user' : session['username'], 'date' : str(date.today().strftime('%d-%m-%Y')), 'amount': topup, 'complete': False})
            # flash the message of success to user dashboard tab 2
            flash('Topup request Created!')
            return redirect(url_for('resident', _anchor='test2'))
        
        # if there is already one active request flash the message to resident dashboard tab 2
        flash('Avtive request Pending Approval.')
        return redirect(url_for('resident', _anchor='test2'))

    # if user not logged in and admin go to root for reidrection
    return redirect(url_for("index"))


# route to delete an active topup request (helpful if request created by mistake or change of mind)
@app.route('/resident/delete', methods=['POST'])
def requestDelete():
    # if user logged in
    if 'username' in session:
        # if the delete request initiated from resident dashboard
        if "resident" in request.form:
            user = request.form['requestDelete'] # save the user from the form
            mongo.db.requests.delete_one({"user": user, 'complete': False}) # delete the request with db query
            # flash the success message to residents dashboard tab 4
            flash('Request Deleted.')
            return redirect(url_for('resident', _anchor='test4'))
        # if the delete request is originating from admin dashboard
        elif "admin" in request.form:
            user = request.form['requestDelete'] # get the user name to delete the request for
            mongo.db.requests.delete_one({"user": user, 'complete': False}) # delete the request
            # flash the message to admin dashboard tab 3
            flash('Request Deleted.')
            return redirect(url_for('admin', _anchor='test3'))
    # if user is not logged in then go to root for redirection
    return redirect(url_for("index"))


# route to logout the user
@app.route('/logout')
def logout():
    # if user logged in
    if 'username' in session:
        session.clear() # destroy the session to logout the user
        return redirect(url_for('index')) # goto root for redirection


# route to clear the process topup from the JAVA APP installed on the laptop connected to laptop
@app.route('/clear/from/laptop/connected/to/printer')
def clearaftersuccess():
    # basic HTTP authentication to stop unauthorized connection to this route
    # checks if there is authorization and the credentials are correct
    if request.authorization and request.authorization.username == 'irfanrizvidevfromotherside' and request.authorization.password == 'ihopenobodyW!ll':
        blank = {"name": "", "topup": ""}
        # reset the topup.json with blank dictionary and pretty print
        with open('topup.json', 'w') as json_file:
            json.dump(blank, json_file, indent=4)
        return 'topup cleared'
    # if authorization fails make the following response
    return make_response('Count not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})


# setting the variables required to run the flask app
# the variables stored in .bashrc for security
if __name__ == '__main__':
    app.secret_key = os.getenv('PRINTER_FLASK_KEY')
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
    
