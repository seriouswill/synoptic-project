# WebbiSkools Ltd

# User Stories

### As a Client
### I want a web based quiz application
### In order to field quizzes out to Users

### As a Client
### I want to be able to view, edit and delete the quizzes, and questions
### In order to have a maintable and customisable quiz app

### As a User
### In order to test my programming knowledge
### I would like to view and answer quiz questions

# Design Specs

_ In this section I may link to the relevent design docs that I will create as I go along _

### Requirements include:
###     Log in functionality - I will most likely make this in a Flask application as the in built werkzeug security is very good
###     User pages for stats on quiz results, maybe even a graph
###     Admin page for administaror priviledge holders to upload, edit and delete quiz questions and quizzes.
###     The quiz pages themselves, with a way of storing scores and saving them to the relevent User database.


# ! Admin Access

### I have implemented Flask Security, so access to the Admin portal and some restricted view are only achievable by logging in as admin.webbiskools.ltd with password 'admin123' (no apostrophes) 

### NOTE I will alter these passwords even though they are sha256 encrypted, whenever I deploy this site.

### this will grant access to adding and editing quizzes!
### 