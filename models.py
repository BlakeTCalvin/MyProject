from flask import flash, session
from sqlalchemy.sql import func
from config import db, EMAIL_REGEX, bcrypt

muscles_exercises_table = db.Table('muscles_exercises_relationship',
                            db.Column('muscles_id', db.Integer, db.ForeignKey('muscles.id'), primary_key=True),
                            db.Column('exercises_id', db.Integer, db.ForeignKey('exercises.id'), primary_key=True))

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    username = db.Column(db.String(45))
    email = db.Column(db.String(75))
    password = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now())

    @classmethod
    def validate_user(cls, user_data):
        is_valid = True
        if len(user_data['first_name']) < 1:
            is_valid = False
            flash("Enter a First Name")
        if len(user_data['last_name']) < 1:
            is_valid = False
            flash("Enter a Last Name")
        if len(user_data['username']) < 1:
            is_valid = False
            flash("Enter a Username")
        if not EMAIL_REGEX.match(user_data['email']):
            is_valid = False
            flash("Not a Valid Email Address")
        if len(user_data['password']) < 5:
            is_valid = False
            flash("Password Must Be at Least Five Characters")
        if user_data['password'] != user_data['cpassword']:
            is_valid = False
            flash("Password's Do Not Match")
        return is_valid

    @classmethod
    def validate_login(cls, user_data):
        is_valid = True
        get_user = Users.query.filter_by(username=user_data['username']).first()
        if get_user:
            if bcrypt.check_password_hash(get_user.password, user_data['password']):
                return get_user
            else:
                is_valid = False
                flash("Username or Password is Incorrect")
                return is_valid
        else: 
            is_valid = False
            flash("Username or Password is Incorrect")
            return is_valid
    
    @classmethod
    def new_user(cls, user_data):
        hashed_password = bcrypt.generate_password_hash(user_data['password'])
        user_to_add = cls(first_name=user_data['first_name'], last_name=user_data['last_name'], username=user_data['username'], email=user_data['email'], password=hashed_password)
        db.session.add(user_to_add)
        db.session.commit()
        return user_to_add

class Workouts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    exercises_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    description = db.Column(db.String(255))
    intensity = db.Column(db.String(15))
    created_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now())

class Exercises(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    instructions = db.Column(db.String(255))
    muscles_this_exercise_uses = db.relationship('Muscles', secondary=muscles_exercises_table)
    intensity = db.Column(db.String(15))
    created_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now())

    @classmethod
    def validate_exercise(cls, user_data):
        is_valid = True
        if len(user_data['name']) < 1:
            is_valid = False
            flash("Enter a Name")
        if len(user_data['description']) < 1:
            is_valid = False
            flash("Enter a description")
        if len(user_data['instructions']) < 1:
            is_valid = False
            flash("Enter instructions")
        return is_valid

    @classmethod
    def new_exercise(cls, user_data):
        exercise_to_add = cls(name=user_data['name'], description=user_data['description'], instructions=user_data['instructions'], intensity=user_data['intensity'], created_by=session["user_id"])
        db.session.add(exercise_to_add)
        db.session.commit()
        return exercise_to_add

class Muscles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    muscle = db.Column(db.String(45))
    exercises_this_muscle_has = db.relationship('Exercises', secondary=muscles_exercises_table)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now())

    @classmethod
    def new_muscle(cls, user_data):
        muscle_to_add = cls(muscle=user_data['muscle'])
        db.session.add(muscle_to_add)
        db.session.commit()
        return muscle_to_add