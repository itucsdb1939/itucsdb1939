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
class UpdatePerson(FF):
    tc = IntegerField('TC')
    first_name = StringField('First Name', validators = [Length(min = 2, max = 20)])
    last_name = StringField('Last Name', validators = [Length(min = 2, max = 20)] )
    gender = SelectField('Gender', choices = [('.','Select'),('F','Female'),('M','Male')])
    email = StringField('Email', validators = [Email()])
    phone = IntegerField('Phone Number')
    password = PasswordField('Password')
    submit = SubmitField('Update')

class UpdateNurse(FF):
    tc = IntegerField('TC')
    first_name = StringField('First Name', validators = [Length(min = 2, max = 20)])
    last_name = StringField('Last Name', validators = [Length(min = 2, max = 20)] )
    gender = SelectField('Gender', choices = [('.','Select'),('F','Female'),('M','Male')])
    email = StringField('Email', validators = [Email()])
    phone = IntegerField('Phone Number')
    department = SelectField('Department', choices = [('.', 'Select'),('Cardiology','Cardiology'),('ChestDiseases','Chest Diseases'),('Dermatology','Dermatology'),('DietandNutrition','Diet and Nutrition'),('EarNoseThroat','Ear, Nose and Throat'),('Eye','Eye'),('GeneralSurgery','General Surgery'),('Gynecology','Gynecology'),('Nephrology','Nephrology'),('Neurology','Neurology'),('Oncology','Oncology'),('Orthopedics','Orthopedics'),('Pediatrics','Pediatrics'),('Psychiatry','Psychiatry'),('Psychology','Psychology'),('PulmonaryDiseases','Pulmonary Diseases'),('Urology','Urology')])
    password = PasswordField('Password')
    submit = SubmitField('Update')
class RegistrationFormN(FF):
    tc = IntegerField('TC', validators = [DataRequired()])
    first_name = StringField('First Name', validators = [DataRequired(), Length(min = 2, max = 20)])
    last_name = StringField('Last Name', validators = [DataRequired(), Length(min = 2, max = 20)] )
    gender = SelectField('Gender', choices = [('F','Female'),('M','Male')])
    email = StringField('Email', validators = [DataRequired(), Email()])
    phone = IntegerField('Phone Number', validators = [DataRequired()])
    department = SelectField('Department', choices = [('Cardiology','Cardiology'),('ChestDiseases','Chest Diseases'),('Dermatology','Dermatology'),('DietandNutrition','Diet and Nutrition'),('EarNoseThroat','Ear, Nose and Throat'),('Eye','Eye'),('GeneralSurgery','General Surgery'),('Gynecology','Gynecology'),('Nephrology','Nephrology'),('Neurology','Neurology'),('Oncology','Oncology'),('Orthopedics','Orthopedics'),('Pediatrics','Pediatrics'),('Psychiatry','Psychiatry'),('Psychology','Psychology'),('PulmonaryDiseases','Pulmonary Diseases'),('Urology','Urology')])
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
class UpdateDoctor(FF):
    tc = IntegerField('TC')
    first_name = StringField('First Name', validators = [Length(min = 2, max = 20)])
    last_name = StringField('Last Name', validators = [Length(min = 2, max = 20)])
    gender = SelectField('Gender', choices = [('.','Select'),('F','Female'),('M','Male')])
    email = StringField('Email', validators = [Email()])
    phone = IntegerField('Phone Number')
    room = IntegerField('Room')
    department = SelectField('Department', choices = [('.','Select'),('Cardiology','Cardiology'),('ChestDiseases','Chest Diseases'),('Dermatology','Dermatology'),('DietandNutrition','Diet and Nutrition'),('ENT','Ear, Nose and Throat'),('Eye','Eye'),('GeneralSurgery','General Surgery'),('Gynecology','Gynecology'),('Nephrology','Nephrology'),('Neurology','Neurology'),('Oncology','Oncology'),('Orthopedics','Orthopedics'),('Pediatrics','Pediatrics'),('Psychiatry','Psychiatry'),('Psychology','Psychology'),('PD','Pulmonary Diseases'),('Urology','Urology')])
    password = PasswordField('Password')
    submit = SubmitField('Update')

class NewPatient(FF):
    patient_id = IntegerField('Patient ID', validators=[DataRequired()])
    doctor_id = IntegerField('Doctor ID', validators = [DataRequired()])
    pres_id = IntegerField('Prescription ID')
    test_id = IntegerField('Test ID')
    diag = StringField('Diagnosis')
    submit = SubmitField('Submit')
class Operation(FF):
    patient_id = IntegerField('Patient ID', validators=[DataRequired()])
    nurse_id = IntegerField('Nurse ID')
    room = IntegerField('Operating room', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    time = StringField('Time', validators=[DataRequired()])
    blood = StringField('Blood Type', validators=[DataRequired()])
    report = StringField('Operation Report', validators=[DataRequired()])
    submit = SubmitField('Submit')
class OperationU(FF):
    opid = SelectField('Surgery ID', choices=[])
    submit = SubmitField('Submit')

class NewTest(FF):
    patient_id = IntegerField('Patient ID', validators=[DataRequired()])
    doctor_id = IntegerField('Doctor ID', validators = [DataRequired()])
    liver_func = StringField('Liver Func')
    thyroid_func = StringField('Thyroid Func')
    genetic = StringField('Genetic')
    electrolyte = StringField('Electrolyte')
    coagulation = StringField('Coagulation')
    blood_gas = StringField('Blood Gas')
    blood_glucose = StringField('Blood Glucose')
    blood_culture = StringField('Blood Culture')
    full_blood_count = StringField('Full Blood Count')
    submit = SubmitField('Enter')

class TestU(FF):
    t_id = SelectField('Test id', choices=[])
    submit = SubmitField('Submit')

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
    doctor = SelectField('Doctor', choices=[] )
    date = SelectField('Date', choices=[])
    time = SelectField('Time', choices=[] )
    submit = SubmitField('Submit')

class Prescription(FF):
    patient = IntegerField('Patient ID', validators = [DataRequired()])
    pres_type = StringField('Prescription Type',validators = [DataRequired()])
    start_date = StringField('Start Date',validators = [DataRequired()])
    end_date = StringField('End Date',validators = [DataRequired()])
    pill = StringField('Pills',validators = [DataRequired()])
    diag = StringField('Diagnosis',validators = [DataRequired()])
    submit = SubmitField('Submit')