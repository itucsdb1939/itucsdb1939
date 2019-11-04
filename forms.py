from flask_wtf import FlaskForm as FF
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField, TimeField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FF):
    tc = IntegerField('TC', validators = [DataRequired()])
    first_name = StringField('First Name', validators = [DataRequired(), Length(min = 2, max = 20)])
    last_name = StringField('Last Name', validators = [DataRequired(), Length(min = 2, max = 20)] )
    gender = SelectField('Gender', choices = [('F','Female'),('M','Male')])
    email = StringField('Email', validators = [DataRequired(), Email()])
    phone = IntegerField('Phone Number', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
class RegistrationFormN(FF):
    tc = IntegerField('TC', validators = [DataRequired()])
    first_name = StringField('First Name', validators = [DataRequired(), Length(min = 2, max = 20)])
    last_name = StringField('Last Name', validators = [DataRequired(), Length(min = 2, max = 20)] )
    gender = SelectField('Gender', choices = [('F','Female'),('M','Male')])
    email = StringField('Email', validators = [DataRequired(), Email()])
    phone = IntegerField('Phone Number', validators = [DataRequired()])
    department = SelectField('Department', choices = [('Cardiology','Cardiology'),('ChestDiseases','Chest Diseases'),('Dermatology','Dermatology'),('DietandNutrition','Diet and Nutrition'),('ENT','Ear, Nose and Throat'),('Eye','Eye'),('GeneralSurgery','General Surgery'),('Gynecology','Gynecology'),('Nephrology','Nephrology'),('Neurology','Neurology'),('Oncology','Oncology'),('Orthopedics','Orthopedics'),('Pediatrics','Pediatrics'),('Psychiatry','Psychiatry'),('Psychology','Psychology'),('PD','Pulmonary Diseases'),('Urology','Urology')])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
class RegistrationFormD(FF):
    tc = IntegerField('TC', validators = [DataRequired()])
    first_name = StringField('First Name', validators = [DataRequired(), Length(min = 2, max = 20)])
    last_name = StringField('Last Name', validators = [DataRequired(), Length(min = 2, max = 20)])
    gender = SelectField('Gender', choices = [('F','Female'),('M','Male')])
    email = StringField('Email', validators = [DataRequired(), Email()])
    phone = IntegerField('Phone Number', validators = [DataRequired()])
    room = IntegerField('Room', validators = [DataRequired()])
    department = SelectField('Department', choices = [('Cardiology','Cardiology'),('ChestDiseases','Chest Diseases'),('Dermatology','Dermatology'),('DietandNutrition','Diet and Nutrition'),('ENT','Ear, Nose and Throat'),('Eye','Eye'),('GeneralSurgery','General Surgery'),('Gynecology','Gynecology'),('Nephrology','Nephrology'),('Neurology','Neurology'),('Oncology','Oncology'),('Orthopedics','Orthopedics'),('Pediatrics','Pediatrics'),('Psychiatry','Psychiatry'),('Psychology','Psychology'),('PD','Pulmonary Diseases'),('Urology','Urology')])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class Operation(FF):
    patient_id = IntegerField('Patient ID', validators=[DataRequired()])
    doctor_id = IntegerField('Doctor ID', validators = [DataRequired()])
    nurse_id = IntegerField('Nurse ID')
    room = IntegerField('Operating room', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    submit = SubmitField('Enter')

class LoginFormP(FF):
    tc = IntegerField('TC', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
class LoginForm(FF):
    tc = IntegerField('TC', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class Appointment(FF):
    dep = SelectField('Department', choices=[])
    submit = SubmitField('Submit')

   