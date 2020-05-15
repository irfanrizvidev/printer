# Temple Printer Application 
This application is developed by Syed Irfan Rizvi. The purpose of the app is to allow Admins to topup users' accounts without physical touching
the printer. It also enables admins to topup printer remotely which could be helpful so that the users do not need to wait for admins to be onsite.
This app will help asylum seekers who need printing facilities in Temple Accommodation Centre. 
### JAVA APP:
The topup is done by storing the username and topup amount in a json file. A JAVA application has been developed to access a authenticated 
 route on this website to reset the json file after a succesful topup. The JAVA App is installed on the laptop connected to the printer. 
 When the laptop is turned on the app is run automatically and checks after fixed intervals if there is a pending topup in topup.json, if there is,
  it connects to printer using selenium API for java. It updates users account and connects back to the website using an authenticated route to reset
  the topup.json to perform further topups.

<div align="center"> The app is live at: https://printer-application.herokuapp.com/ </div>

## UX
This printer app is very desireable due to COVID-19 pandemic and it can help to redunce the infection chances.
### User Stories
* As the aap user, I want the ability to topup printer accounts remotely.
* As the aap user, I want the ability to create users with different roles.
* As the aap user, I want the ability to create, edit and delete users.
* As the aap user, I want the ability to create and delete topup requests.
* As the aap user, I want users to have ability to make topup requests.
* As the aap user, I want user to have ability to delete active requests created by mistake. 
* As the aap user, I want to use the app on different screen sizes.
* As the aap user, I want the to use HTTPS always to secure usernames and passwords.
* As the aap user, I want users to have ability to see past topups.

### Admin Dashboard Medium/Large Screen

<div align="center"> **A gif demo is below on a large screen:** </div>

![Demo of admin dashboard](/static/images/admin.gif)

### Admin Dashboard Small Screen
![Demo of user dashboard](/static/images/admindash.gif)

### User/Resident Dashboard Medium/Large Screen
![Demo of user dashboard](/static/images/resident.gif)

### User/Resident Dashboard Small Screen
![Demo of user dashboard](/static/images/userdash.gif)

## Features
The app has many features which make it responsive and easy to use. Some of the features could, however be implemented to improve it.
### Existing Features
* HTTPS forced within the app to keep login details secure. 
* The application has three user roles super admin, admin and residents. 
* The super user could edit all users (admins and residents) alike. 
* The super user could also perform all the funcion an admin can perform.
* The residents could make topup requests from their own dashboards after loggin in. 
* The admins could see the requests in their dashboards and approve or delete the requests. 
* The admins could also topup user accounts without users creating requests. it would be ideal in a situaion, 
 where a user requests topup verbally.

### Features left to Implement
* pagination on completed requests
* ability to process all requests automatically in a queue
* Profit/expenses records

## Technologies Used
* [GITPOD IO](https://gitpod.io)
    * GITPOD was used as  the development platform to develop this project.

* [HTML](https://www.wikipedia.com/HTML)
    * HTML 5 is used to make this web project.

* [CSS](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)
    * CSS is used to style the HTML elements

* [JavaScript](https://www.javascript.com/)
    * JavaScript language is used to created the logic of the game and to make game more interactive.

* [Materialize CSS](https://materializecss.com/getting-started.html)
    * Materialize CSS is a UI component library which is created with CSS, JavaScript and HTML. It is created and designed by Google.

* [jQuery](https://jquery.com)
    * JQuery was used for easy manipulation of DOM in javascript.

* [Python 3](https://www.python.org/downloads/)
    * Python is an interpreted, object-oriented, high-level programming language with dynamic semantics. Its high-level built in data structures, combined with dynamic typing and dynamic binding, make it very attractive for Rapid Application Development, as well as for use as a scripting or glue language to connect existing components together.
    * Definition from: https://www.python.org/doc/essays/blurb/

* [Flask ](https://www.fullstackpython.com/flask.html)
    * Flask is a popular, extensible web microframework for building web applications with Python.
    * Definition from: Flask is a popular, extensible web microframework for building web applications with Python.

* [Mongo DB](https://www.mongodb.com/)
    * MongoDB is a document database with the scalability and flexibility that you want with the querying and indexing that you need.
    * Definition from: https://www.mongodb.com/what-is-mongodb


## Testing
The website is tested on Google Chrome for different screen sizes e.g. (S5 mobile, Iphone, Ipad etc.). The website is also tested on Firefox and Internet explorer latest versions.
The website is tested for responsiveness and for all the functions to be working as intended. 
* The html is valid when checkd on w3school
* CSS is valid when tested on validator on w3school
* The database is working fine. 

## Deployment
The project is deployed on Github pages on the following link:
[Live deployed project on Heroku](https://printer-application.herokuapp.com/)

The project is developed using GITPOD IO. GITPOD allows easy to use GIT integration to commit changes on Github. 
Requirements.txt file and procfile where generated and local variables were initialized for Heroku to host the App.
The project is deployed on Heroku.com. The heroku.com is connected to github repository to auto-deploy github repository after every push. 
MongoDB was used to host the collections and tabels. A url was generated and saved as system variable for security. 

<div align="center">Github connection with Heroku under deploy tab of Printer App</div>


![GITHUB pages](/static/images/herokugithub.jpg)

<div align="center">Staging the changes using GIT section on GITPOD</div>

![Gitpod changes staging](/static/images/stage.png)

<div align="center">The changes are commited after a message as shown below</div>

![COmmit changes](/static/images/commit.png)

<div align="center">Pushing changes to Github</div>

![Push on GitPOD](/static/images/push.png)

The same would be achieved using the following git commands:
```
git init

git add file name

git commit -m "comment"

orgin master copied from the github pages

git push orgin master

git status

github username entered

github password entered
```
## Credits
Author: Syed Irfan Haider Rizvi

### Acknowledgements

I got help from following resources for solving problems:

### basic http authentication:
https://www.youtube.com/watch?v=VW8qJxy4XcQ

### Responsive table:
https://codepen.io/team/css-tricks/pen/wXgJww?editors=1100

### Login page form
https://codepen.io/T-P/pen/bpWqrr

### Login Logic 
https://github.com/PrettyPrinted/mongodb-user-login/blob/master/login_example.py

### HTTPS enforcement (ISSUE on heorku sometime http sometimes https due to load balancers)
https://stackoverflow.com/questions/32237379/python-flask-redirect-to-https-from-http/50041843

