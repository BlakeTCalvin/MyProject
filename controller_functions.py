from flask import render_template, redirect, request, flash, session
from config import db
from models import Users, Workouts, Exercises, Muscles

def index():
    return redirect("/login")

def loginPage():
    return render_template("loginPage.html")

def processLogin():
    if len(request.form['password']) < 1 and len(request.form['username']) < 1:
        flash("Enter a Username and Password")
        return redirect("/login")
    else: 
        login_check = Users.validate_login(request.form)
        if login_check == False:
            return redirect("/login")
        else:
            session['user_id'] = login_check.id
            session['first_name'] = login_check.first_name
            session['last_name'] = login_check.last_name
            return redirect("/home")

def registerPage():
    return render_template("registerPage.html")

def processUser():
    validation_check = Users.validate_user(request.form)
    if not validation_check:
        return redirect("/register")
    else:
        new_user = Users.new_user(request.form)
        session['user_id'] = new_user.id
        session['first_name'] = new_user.first_name
        session['last_name'] = new_user.last_name
    return redirect("/home")

def home():
    if 'first_name' in session:
        return render_template("homePage.html")
    else:
        return redirect("/login")

def logout():
    session.clear()
    return redirect("/login")