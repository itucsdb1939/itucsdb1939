from flask import Flask,render_template, flash, redirect, url_for, request, session, jsonify
from forms import RegistrationForm,UpdateDoctor, LoginForm, LoginFormP, NewPatient,UpdatePerson, UpdateNurse,RegistrationFormD,Operation,OperationU,Appointment,RegistrationFormN,NewTest,Prescription, TestU
import psycopg2
from dbinit import initialize
from os import environ
import datetime 

RELEASE = True

if(not RELEASE):
    environ['DATABASE_URL'] = "postgres://afoeiapd:3N1LWGKtLZAdeI2sEQQR4N0I6GE1EnOM@salt.db.elephantsql.com:5432/afoeiap"
    initialize(environ.get('DATABASE_URL'))
app = Flask(__name__)

app.config['SECRET_KEY'] = 'f5b9ac4eddb1942feeb7d826b76b4a3f'

def CDB():
    try:
        connection = psycopg2.connect(dbname = 'afoeiapd', user = 'afoeiapd', password = '3N1LWGKtLZAdeI2sEQQR4N0I6GE1EnOM', host = 'salt.db.elephantsql.com', port = '5432')
        print("SSS")
        return connection
        
    except:
        print("FFF")


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if (request.method =='POST'):
        if form.validate_on_submit():
            try:
                conn = CDB()
                cur = conn.cursor()
                statement = "INSERT INTO person (tc,first_name,last_name,email,phone,pass,gender) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cur.execute(statement,(request.form['tc'],request.form['first_name'],request.form['last_name'],request.form['email'],request.form['phone'],request.form['password'],request.form['gender'],))
                conn.commit()
                cur.close()
                conn.close()
                flash('New account created.', 'success')
                return redirect(url_for('login'))
            except:
                flash('An error occured.', 'danger')
                render_template("register.html", form = form)
        else:
            flash('An error occured.', 'danger')
            return redirect(url_for('register'))
    return render_template("register.html", form = form)

@app.route("/register_dr", methods=['GET', 'POST'])
def register_dr():
    form = RegistrationFormD()
    day = datetime.date.today()
    date = datetime.date.today()
    if(day.weekday() == 5):
        day = ( date + datetime.timedelta(days=2))
    elif(day.weekday() == 4):
        day = ( date + datetime.timedelta(days=3))
    else:
        day = ( date + datetime.timedelta(days=1))      
    if (request.method =='POST'):
        if form.validate_on_submit():
            try: 
                conn = CDB()
                cur = conn.cursor()
                statement = "INSERT INTO doctor (tc,first_name,last_name,gender,email,phone,room,dep,pass) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"        
                cur.execute(statement,(request.form['tc'],request.form['first_name'],request.form['last_name'],request.form['gender'],request.form['email'],request.form['phone'],request.form['room'],request.form['department'],request.form['password'],))
                statement = "INSERT INTO all_appointments (dep,doctor_id,date,time) VALUES (%s,%s,%s,%s)"
                cur.execute(statement,(request.form['department'],request.form['tc'],day,"08-00",))
                cur.execute(statement,(request.form['department'],request.form['tc'],day,"09-00",))
                cur.execute(statement,(request.form['department'],request.form['tc'],day,"10-00",))
                cur.execute(statement,(request.form['department'],request.form['tc'],day,"11-00",))
                cur.execute(statement,(request.form['department'],request.form['tc'],day,"12-00",))
                cur.execute(statement,(request.form['department'],request.form['tc'],day,"13-00",))
                cur.execute(statement,(request.form['department'],request.form['tc'],day,"14-00",))
                cur.execute(statement,(request.form['department'],request.form['tc'],day,"15-00",))
                cur.execute(statement,(request.form['department'],request.form['tc'],day,"16-00",))
                cur.execute(statement,(request.form['department'],request.form['tc'],day,"17-00",))
                conn.commit()
                
                
                
                cur.close()
                conn.close()
                flash('New account created.', 'success')
                return redirect(url_for('login_dr'))
            except:
                flash('An error occured.', 'danger')
                return redirect(url_for('register_dr'))
        else:
            flash('An error occured.', 'danger')
            return redirect(url_for('register_dr'))
    return render_template("register_dr.html", form = form)

@app.route("/register_nr", methods=['GET', 'POST'])
def register_nr():
    form = RegistrationFormN()
    if (request.method =='POST'):
        if form.validate_on_submit():
            try:
                conn = CDB()
                cur = conn.cursor()
                statement = "INSERT INTO nurse (tc,first_name,last_name,gender,email,phone,dep,pass) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"       
                cur.execute(statement,(request.form['tc'],request.form['first_name'],request.form['last_name'],request.form['gender'],request.form['email'],request.form['phone'],request.form['department'],request.form['password'],))
                conn.commit()
                cur.close()
                conn.close()
                flash('New account created.', 'success')
                return redirect(url_for('login_nr'))
            except:
                flash('An error occured.', 'danger')
                return redirect(url_for('register'))
        else:
            flash('An error occured.', 'danger')
            return redirect(url_for('register'))
    return render_template("register_nr.html", form = form)

@app.route("/update_op/", methods=['GET', 'POST'])
def update_op():
    form = OperationU()
    ops = []
    result = []
    try:
        conn = CDB()
        cur = conn.cursor()
        cur.execute("SELECT id FROM surgery")
        result = cur.fetchall()
        ops.append(tuple((".","Select")))
        for i in range(0,len(result)):
            ops.append(tuple((str(result[i][0]),str(result[i][0]))))
        form.opid.choices = ops
    except:
        flash('An error occured.', 'danger')
        return redirect(url_for('update_op'))
    if (request.method =='POST'):
        if form.validate_on_submit():
            if(request.form['opid'] != "."):
                return redirect("/update_op/id/" + str(request.form['opid']))
        else:
            flash('An error occured.', 'danger')
            return redirect(url_for('update_op'))
    return render_template("op_update.html", form = form)

@app.route("/update_op/id/<opid>", methods=['GET', 'POST'])
def update_op_final(opid):
    form = Operation()
    if (request.method =='POST'):
        if form.validate_on_submit():
            try:
                conn = CDB()
                cur = conn.cursor()
                print(opid)
                if opid:

                    statement = "UPDATE surgery SET patient_id = %s,nurse_id = %s,op_room = %s,date = %s,time = %s,blood_type = %s, op_report = %s WHERE id = %s"
                    cur.execute(statement,(request.form['patient_id'],request.form['nurse_id'],request.form['room'],request.form['date'],request.form['time'],request.form['blood'],request.form['report'],opid,))
                    conn.commit()
                cur.close()
                conn.close()
                flash('Surgery update successful.', 'success')
                return redirect(url_for('update_op'))
            except:
                flash('An error occured.', 'danger')
                return redirect(url_for('update_op'))
            else:
                flash('An error occured.', 'danger')
                return redirect(url_for('update_op'))
            return render_template("op_update_final.html", form = form)
    
    return render_template("op_update_final.html", form = form)

@app.route("/op_dr", methods=['GET', 'POST'])
def operation():
    form = Operation()
    if (request.method =='POST'):
        if form.validate_on_submit():
            try:
                conn = CDB()
                cur = conn.cursor()
                statement = "INSERT INTO surgery (patient_id,doctor_id,nurse_id,op_room,date,time,blood_type) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cur.execute(statement,(request.form['patient_id'],session['tc'],request.form['nurse_id'],request.form['room'],request.form['date'],request.form['time'],request.form['blood'],))
                conn.commit()
                cur.close()
                conn.close()
                flash('Surgery registraton successful.', 'success')
                return redirect(url_for('operation'))
            except:
                flash('An error occured.', 'danger')
                return redirect(url_for('operation'))
        else:
            flash('An error occured.', 'danger')
            return redirect(url_for('operation'))
    return render_template("op_dr.html", form = form)

@app.route("/op_delete", methods=['GET', 'POST'])
def delete_op():
    form = OperationU()
    ops = []
    result = []
    try:
        conn = CDB()
        cur = conn.cursor()
        cur.execute("SELECT id FROM surgery")
        result = cur.fetchall()
        ops.append(tuple((".","Select")))
        for i in range(0,len(result)):
            ops.append(tuple((str(result[i][0]),str(result[i][0]))))
        form.opid.choices = ops
    except:
        flash('An error occured.', 'danger')
        return redirect(url_for('update_op'))
    if (request.method =='POST'):
        if form.validate_on_submit():
            if(request.form['opid'] != "."):
                statement = "DELETE FROM surgery WHERE id = %s"
                cur.execute(statement,(request.form['opid'],))
                conn.commit()
                cur.close()
                conn.close()
                flash('Surgery deleted.', 'success')
            return redirect(url_for("delete_op"))
        else:
            flash('An error occured.', 'danger')
            return redirect(url_for('update_op'))
    return render_template("op_delete.html", form = form)

@app.route("/test_delete", methods=['GET', 'POST'])
def test_delete():
    form = TestU()
    tests = []
    result = []
    try:
        conn = CDB()
        cur = conn.cursor()
        cur.execute("SELECT id FROM test")
        result = cur.fetchall()
        tests.append(tuple((".","Select")))
        for i in range(0,len(result)):
            tests.append(tuple((str(result[i][0]),str(result[i][0]))))
        form.t_id.choices = tests
    except:
        flash('An error occured.', 'danger')
        return redirect(url_for('test_delete'))
    if (request.method =='POST'):
        if form.validate_on_submit():
            if(request.form['t_id'] != "."):
                statement = "DELETE FROM test WHERE id = %s"
                cur.execute(statement,(request.form['t_id'],))
                conn.commit()
                cur.close()
                conn.close()
                flash('Test deleted.', 'success')
            return redirect(url_for("test_delete"))
        else:
            flash('An error occured.', 'danger')
            return redirect(url_for('test_delete'))
    return render_template("test_delete.html", form = form)


@app.route("/op_view", methods=['GET'])
def op_view():
    result = []
    try:
        conn = CDB()
        cur = conn.cursor()
        statement = "SELECT * FROM surgery WHERE doctor_id = %s"
        cur.execute(statement,(session['tc'],)) 
        result = cur.fetchall()
        cur.close()
        conn.close()
    except:
        flash('An error occured.', 'danger')
        return redirect(url_for('op_view'))
    return render_template("op_view.html", table = result)

@app.route("/account_view", methods=['GET'])
def account_view():
    result = []
    try:
        conn = CDB()
        cur = conn.cursor()
        statement = "SELECT * FROM nurse WHERE tc = %s"
        cur.execute(statement,(session['tc'],)) 
        result = cur.fetchall()
        cur.close()
        conn.close()
    except:
        flash('An error occured.', 'danger')
        return redirect(url_for('account_view'))
    return render_template("account_view.html", table = result)

@app.route("/op_view_nurse", methods=['GET'])
def op_view_nurse():
    result = []
    try:
        conn = CDB()
        cur = conn.cursor()
        statement = "SELECT * FROM surgery WHERE nurse_id = %s"
        cur.execute(statement,(session['tc'],))
        result = cur.fetchall()
        cur.close()
        conn.close()
    except:
        flash('An error occured.', 'danger')
        return redirect(url_for('op_view_nurse'))
    return render_template("op_view_nurse.html", table = result)

@app.route("/prescriptions" , methods=['GET'])
def pres():
    p = []
    doctor = []
    try:
        conn = CDB()
        cur = conn.cursor()
        statement = "SELECT * FROM prescription WHERE (patient_id = %s)"
        cur.execute(statement,(session['tc'],))
        p = cur.fetchall()
        if(p != []):
            statement = "SELECT first_name, last_name FROM doctor WHERE (tc = %s)"
            cur.execute(statement,(p[0][2],))
            doctor = cur.fetchall()
            doctor = doctor[0][0] + " " + doctor[0][1]
        cur.close()
        conn.close()
    except:
        flash('An error occured.', 'danger')
        return redirect(url_for('pres'))
    return render_template("pres.html", table = p, dr=doctor)

@app.route("/blood_test" , methods=['GET'])
def blood():
    blood = []
    doctor =[]
    try:
        conn = CDB()
        cur = conn.cursor()
        statement = "SELECT * FROM test WHERE (patient_id = %s)"
        cur.execute(statement,(session['tc'],))
        blood = cur.fetchall() 
        if(blood != []):
            statement = "SELECT first_name, last_name FROM doctor WHERE (tc = %s)"
            cur.execute(statement,(blood[0][2],))
            doctor = cur.fetchall()
            doctor = doctor[0][0] + " " + doctor[0][1]
        cur.close()
        conn.close()
    except:
        flash('An error occured.', 'danger')
        return redirect(url_for('blood'))
    return render_template("blood_test.html", table = blood, dr=doctor)

@app.route("/patient_view/prescription/delete/<pres>", methods=['GET', 'POST'])
def pres_del(pres):
    try:
        conn = CDB()
        cur = conn.cursor()
        statement = "SELECT * FROM record WHERE pres_id  = %s"
        cur.execute(statement, (pres,))
        result = cur.fetchall()
        if(result != ""):
            statement = "DELETE FROM record WHERE pres_id = %s"
            cur.execute(statement, (pres, ))
        statement = "DELETE FROM prescription WHERE (id = %s)"
        cur.execute(statement,(pres,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('p_view'))
    except:
        flash('An error occured.', 'danger')
        return redirect(url_for('p_view'))

@app.route("/patient_view/prescription/update/<pres>", methods=['GET', 'POST'])
def pres_update(pres):
    form = Prescription()
    if (request.method =='POST'):
        if form.validate_on_submit():
            try:
                conn = CDB()
                cur = conn.cursor()
                if pres:
                    statement = "UPDATE prescription SET patient_id = %s,pres_type=%s,date_start=%s,date_end=%s,pills=%s,diagnosis=%s WHERE id=%s"
                    cur.execute(statement,(request.form['patient'],request.form['pres_type'],request.form['start_date'],request.form['end_date'],request.form['pill'],request.form['diag'],pres,))
                    conn.commit()
                cur.close()
                conn.close()
                flash('Prescription update successful.', 'success')
                return redirect(url_for('p_view'))
            except:
                flash('An error occured.', 'danger')
                return redirect(url_for('p_view'))
            else:
                flash('An error occured.', 'danger')
                return redirect(url_for('p_view'))
            
    return render_template("update_pres.html",form=form)

@app.route("/patient_view/prescription/<pres>", methods=['GET', 'POST'])
def pres_view(pres):
    prescriptions = []
    try:
        conn = CDB()
        cur = conn.cursor()
        statement = "SELECT * FROM prescription WHERE (id = %s)"
        cur.execute(statement,(pres,))
        prescriptions = cur.fetchall()
        print(prescriptions)
        cur.close()
        conn.close()
    except:
        flash('An error occured.', 'danger')
        return redirect(url_for('pres_view'))
    return render_template("pres_view.html", pres = prescriptions)


@app.route("/patient_view/test/<test>", methods=['GET', 'POST'])
def test_view(test):
    tests = []
    try:
        conn = CDB()
        cur = conn.cursor()
        statement = "SELECT * FROM test WHERE (id = %s)"
        cur.execute(statement,(test,))
        tests = cur.fetchall()
        cur.close()
        conn.close()
    except:
        flash('An error occured.', 'danger')
        return redirect(url_for('test_view'))
    return render_template("test_view.html", test = tests)

@app.route("/test_update_nurse", methods=['GET', 'POST'])
def test_update_nurse():
    form = TestU()
    tests = []
    result = []
    try:
        conn = CDB()
        cur = conn.cursor()
        cur.execute("SELECT id FROM test ")
        result = cur.fetchall()
        tests.append(tuple((".","Select")))
        for i in range(0,len(result)):
            tests.append(tuple((str(result[i][0]),str(result[i][0]))))
        form.t_id.choices = tests
    except:
        flash('An error occured.', 'danger')
        return redirect(url_for('test_update_nurse'))
    if (request.method =='POST'):
        if form.validate_on_submit():
            if(request.form['t_id'] != "."):
                return redirect("/test_update_nurse/id/" + str(request.form['t_id']))
        else:
            flash('An error occured.', 'danger')
            return redirect(url_for('test_update_nurse'))
    return render_template("test_update_nurse.html", form = form) 

@app.route("/test_update_nurse/id/<t_id>", methods=['GET', 'POST'])
def test_update_final(t_id):
    form = NewTest()
    if (request.method =='POST'):
        if form.validate_on_submit():
            try:
                conn = CDB()
                cur = conn.cursor()
                statement = "UPDATE test SET patient_id = %s,doctor_id = %s,liver_func = %s,thyroid_func = %s,genetic = %s,electrolyte = %s, coagulation = %s, blood_gas = %s,blood_glucose = %s,blood_culture = %s, full_blood_count = %s  WHERE id = %s"
                cur.execute(statement,(request.form['patient_id'],request.form['doctor_id'],request.form['liver_func'],request.form['thyroid_func'], request.form['genetic'],request.form['electrolyte'], request.form['coagulation'], request.form['blood_gas'], request.form['blood_glucose'], request.form['blood_culture'], request.form['full_blood_count'],t_id,))
                conn.commit()
                cur.close()
                conn.close()
                flash('Test update successful.', 'success')
                return redirect(url_for('test_update_nurse'))
            except:
                flash('An error occured.', 'danger')
                return redirect(url_for('test_update_nurse'))
        else:
            flash('An error occured.', 'danger')
            return redirect(url_for('test_update_nurse'))
        return render_template("test_update_final.html", form = form)
    
    return render_template("test_update_final.html", form = form)
 
@app.route("/patient_view", methods=['GET', 'POST'])
def p_view():
    patients = []
    patient_names = []
    patient_pres = []
    patient_test = []
    pres_id = []
    l = 0
    try:
        conn = CDB()
        cur = conn.cursor()
        statement = "SELECT * FROM record WHERE (doctor_id = %s)"
        cur.execute(statement,(session['tc'],))
        patients = cur.fetchall()
        if(patients != []):
            for i in range(0,len(patients)):
                statement = "SELECT first_name, last_name FROM person WHERE (tc = %s)"
                cur.execute(statement,(patients[i][0],))
                patient = cur.fetchall()
                p = patient[0][0] + " " + patient[0][1]
                patient_names.append(p)
                statement = "SELECT * FROM prescription WHERE (patient_id = %s)"
                cur.execute(statement,(patients[i][0],))
                pres = cur.fetchall()
                patient_pres.append([])
                for j in range(0,len(pres)):
                    patient_pres[i].append(pres[j][0])
                statement = "SELECT * FROM test WHERE (patient_id = %s)"
                cur.execute(statement,(patients[i][0],))
                test = cur.fetchall()
                patient_test.append([])
                for j in range(0,len(test)):
                    patient_test[i].append(test[j][0])  
            l = len(patients)
        cur.close()
        conn.close()
    except:
        flash('An error occured.', 'danger')
        return redirect(url_for('p_view'))
    return render_template("patient_view.html", table = patients, pt=patient_names,pres = patient_pres,len = l,test = patient_test)


@app.route("/new_patient", methods=['GET', 'POST'])
def new_pat():
    pres_id = []
    diag = []
    test_id = []
    form = NewPatient()
    if (request.method =='POST'):
        if form.validate_on_submit():
            try:
                conn = CDB()
                cur = conn.cursor()
                pres_id = request.form['pres_id']
                diag = request.form['diag']
                test_id = request.form['test_id']
                statement = "INSERT INTO record (patient_id,doctor_id,pres_id,diagnosis,test_id) VALUES (%s,%s,%s,%s,%s)"
                cur.execute(statement,(request.form['patient_id'],session['tc'],pres_id,diag,test_id,))
                conn.commit()
                cur.close()
                conn.close()
                flash('New record registraton successful.', 'success')
                return redirect(url_for('p_view'))
            except:
                flash('An error occured.', 'danger')
                return redirect(url_for('new_pat'))
        else:
            flash('An error occured.', 'danger')
            return redirect(url_for('new_pat'))
                
    
    return render_template("new_patient.html",form = form)

@app.route("/new_test", methods=['GET', 'POST'])
def new_t():
    form = NewTest()
    if (request.method =='POST'):
        if form.validate_on_submit():
            try:
                conn = CDB()
                cur = conn.cursor()
                statement = "INSERT INTO test (patient_id,doctor_id,liver_func,thyroid_func,genetic,electrolyte,coagulation, blood_gas, blood_glucose, blood_culture, full_blood_count) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cur.execute(statement,(request.form['patient_id'],request.form['doctor_id'],request.form['liver_func'],request.form['thyroid_func'], request.form['genetic'],request.form['electrolyte'], request.form['coagulation'], request.form['blood_gas'], request.form['blood_glucose'], request.form['blood_culture'], request.form['full_blood_count'],))
                conn.commit()
                cur.close()
                conn.close()
                flash('New test registraton successful.', 'success')
                return redirect(url_for('new_t'))
            except:
                flash('An error occured.', 'danger')
                return redirect(url_for('new_t'))
        else:
            flash('An error occured.', 'danger')
            return redirect(url_for('new_t'))
    return render_template("new_test.html",form = form)


@app.route("/home_dr", methods=['GET', 'POST'])
def home_dr():
    return render_template("home_dr.html")

@app.route("/home_p", methods=['GET', 'POST'])
def home_p():
    return render_template("home_p.html")

@app.route("/home_nurse", methods=['GET', 'POST'])
def home_nurse():
    return render_template("home_nurse.html")

@app.route("/sign_out", methods=['GET', 'POST'])
def sign_out():
    session.clear()
    return redirect(url_for('home'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginFormP()
    if (request.method =='POST'):
        if form.validate_on_submit():
            tc = request.form['tc']
            passw = request.form['password']
            try:
                conn = CDB()
                cur = conn.cursor()
                statement = "SELECT pass FROM person WHERE tc=%s"
                cur.execute(statement,(tc,))
                result = cur.fetchone()
                if(result[0] == passw):
                    session['tc'] = tc
                    return redirect(url_for('home_p'))
                else:
                    flash('Wrong password.', 'danger')
                    cur.close()
                    conn.close()
                    return redirect(url_for('login'))
            except:
                flash('An error occured.', 'danger')
                return redirect(url_for('login'))
    return render_template("login.html", form = form)

@app.route("/login_dr", methods=['GET', 'POST'])
def login_dr():
    form = LoginForm()
    if (request.method =='POST'):
        if form.validate_on_submit():
            tc = request.form['tc']
            passw = request.form['password']
            try:
                conn = CDB()
                cur = conn.cursor()
                statement = "SELECT pass FROM doctor WHERE tc=%s"
                cur.execute(statement,(tc,))
                result = cur.fetchone()
                if(result[0] == passw):
                    session['tc'] = tc
                    cur.close()
                    conn.close()
                    return redirect(url_for('home_dr'))
                else:
                    flash('Wrong password.', 'danger')
                    cur.close()
                    conn.close()
                    return redirect(url_for('login_dr'))
                    
            except:
                flash('An error occured.', 'danger')
                return redirect(url_for('login_dr'))
    return render_template("login_doctor.html", form = form)



@app.route("/login_nr", methods=['GET', 'POST'])
def login_nr():
    form = LoginForm()
    if (request.method =='POST'):
        if form.validate_on_submit():
            tc = request.form['tc']
            passw = request.form['password']
            try:
                conn = CDB()
                cur = conn.cursor()
                statement = "SELECT pass FROM nurse WHERE tc=%s"
                cur.execute(statement,(tc,))
                result = cur.fetchone()
                if(result[0] == passw):
                    session['tc'] = tc
                    cur.close()
                    conn.close()
                    return redirect(url_for('home_nurse'))
                else:
                    flash('no login', 'danger')
                    cur.close()
                    conn.close()
                    return redirect(url_for('login_nr'))
               
            except:
                flash('An error occured.', 'danger')
                return redirect(url_for('login_nr'))
    return render_template("login_nurse.html", form = form)

@app.route("/make_appointment", methods=['GET', 'POST'])
def make_appointment():
    form = Appointment()
    try:
        conn = CDB()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT dep FROM all_appointments ORDER BY dep ASC")
        
        dep = cur.fetchall()
        deps = []
        deps.append(tuple((' ','Select')))
        
        for i in range(0,len(dep)):
            deps.append(tuple((dep[i][0],dep[i][0])))
        form.dep.choices = deps
        
        if (request.method =='POST'):
            date = request.form['date']
            tc = session['tc']
            doctor = request.form['doctor']
            time = request.form['time']
            statement = "INSERT INTO taken_appointments (patient_id,doctor_id,date,time) VALUES (%s,%s,%s,%s)"
            cur.execute(statement,(tc,doctor,date,time,))
            statement = "DELETE FROM all_appointments WHERE doctor_id = %s AND date = %s AND time = %s"
            cur.execute(statement,(doctor,date,time,))
            conn.commit()
            cur.close()
            conn.close()
            flash('Appointment saved.', 'success')
            return redirect(url_for('make_appointment'))
    except:
        flash('An error occured.', 'danger')
        return redirect(url_for('make_appointment'))
    return render_template("appo.html", form = form)

@app.route("/make_appointment/<dep>",methods=["GET","POST"])
def select_doc(dep):
    appo_doc = []
    try:
        conn = CDB()
        cur = conn.cursor()
        statement = "SELECT DISTINCT doctor_id FROM all_appointments WHERE dep = %s"
        cur.execute(statement,(dep,))
        result = cur.fetchall()
        for i in range(0,len(result)):
            appo_doc.append(result[i][0])
        doc = []
        docObj = {}
        docObj['tc'] = 0
        docObj['name'] = 'Select'
        doc.append(docObj)
        for i in appo_doc:
            statement = "SELECT first_name,last_name FROM doctor WHERE tc = %s"
            cur.execute(statement,(i,))
            result = cur.fetchall()
            name = result[0][0] + " " + result[0][1]
            docObj = {}
            docObj['tc'] = i
            docObj['name'] = name
            doc.append(docObj)
        cur.close()
        conn.close()
    except:
        pass
    return jsonify({"docs": doc})

@app.route("/make_appointment/<dep>/<doc>",methods=["GET","POST"])
def select_date(dep,doc):
    dates = []
    date = []
    try:
        conn = CDB()
        cur = conn.cursor()
        statement = "SELECT DISTINCT date FROM all_appointments WHERE dep = %s AND doctor_id = %s"
        cur.execute(statement,(dep,doc,))
        result = cur.fetchall()
        for i in range(0,len(result)):
            dates.append(result[i][0])        
        dateObj = {}
        dateObj['id'] = 0
        dateObj['date'] = 'Select'
        date.append(dateObj)
        for i in dates:
            dateObj = {}
            dateObj['id'] = i
            dateObj['date'] = i
            date.append(dateObj)
        cur.close()
        conn.close()
    except:
        pass
    return jsonify({"dates": date})

@app.route("/make_appointment/<dep>/<doc>/<date>",methods=["GET","POST"])
def select_time(dep,doc,date):
    times = []
    time = []
    try:
        conn = CDB()
        cur = conn.cursor()
        statement = "SELECT * FROM all_appointments WHERE dep = %s AND doctor_id = %s AND date = %s"
        cur.execute(statement,(dep,doc,date,))
        result = cur.fetchall()
        for i in range(0,len(result)):
            times.append(result[i][3])
        timeObj = {}
        timeObj['id'] = 0
        timeObj['time'] = 'Select'
        time.append(timeObj)
        for i in times:
            timeObj = {}
            timeObj['id'] = i
            timeObj['time'] = i
            time.append(timeObj)
        cur.close()
        conn.close()
    except:
        pass
    return jsonify({"times": time})


@app.route("/new_pres",methods=["GET","POST"])
def new_pres():
    form = Prescription()
    try:
        conn = CDB()
        cur = conn.cursor()
        if(request.method =='POST'):
            if form.validate_on_submit():
                statement = "INSERT INTO prescription (patient_id,doctor_id,pres_type,date_start,date_end,pills,diagnosis) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cur.execute(statement,(request.form['patient'],session['tc'],request.form['pres_type'],request.form['start_date'],request.form['end_date'],request.form['pill'],request.form['diag'],))
                conn.commit()
                flash('Prescription added successfully.', 'success')
                cur.close()
                conn.close()
                return redirect(url_for('new_pres'))
            else:
                flash('An error occured.', 'danger')
                return redirect(url_for('new_pres'))
    except:
        flash('An error occured.', 'danger')
        return redirect(url_for('new_pres'))
    return render_template("new_pres.html", form = form)
    
@app.route("/appointment_view",methods=["GET","POST"])
def appo_view():
    names = []
    appos = []
    try:
        conn = CDB()
        cur = conn.cursor()
        statement = "SELECT  DISTINCT * FROM taken_appointments WHERE doctor_id = %s"
        cur.execute(statement,(session['tc'],))
        appos = cur.fetchall()
        for i in range(0,len(appos)):
            statement = "SELECT first_name,last_name FROM person WHERE tc = %s"
            cur.execute(statement,(appos[i][0],))
            name = cur.fetchall()
            names.append(name[0][0] + " " + name[0][1])
        l = len(names)
        cur.close()
        conn.close()
    except :
        flash('An error occured.', 'danger')
        return redirect(url_for('appo_view'))
    return render_template("appo_view.html", names = names, appo = appos, len = l)

@app.route("/account_update_nurse", methods=["GET", "POST"])
def nurse_update():
    form = UpdateNurse()
    if (request.method =='POST'):
        tc = request.form['tc']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        email  = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        password = request.form['password']
        try:
            conn = CDB()
            cur = conn.cursor()
            if(tc != ""):
                statement = "UPDATE nurse SET tc = %s WHERE tc = %s"
                cur.execute(statement,(tc,session['tc'],))
            if(first_name != ""):
                statement = "UPDATE nurse SET first_name = %s WHERE tc = %s"
                cur.execute(statement,(first_name,session['tc'],))
            if(last_name != ""):
                statement = "UPDATE nurse SET last_name = %s WHERE tc = %s"
                cur.execute(statement,(last_name,session['tc'],))
            if(gender != "."):
                if(gender == "F"):
                    statement = "UPDATE nurse SET gender = 'F' WHERE tc = %s"
                    cur.execute(statement,(session['tc'],))
                elif(gender == "M"):
                    statement = "UPDATE nurse SET gender = 'M' WHERE tc = %s"
                    cur.execute(statement,(session['tc'],))
            if(email != ""):
                statement = "UPDATE nurse SET email = %s WHERE tc = %s"
                cur.execute(statement,(email,session['tc'],))
            if(phone != ""):
                statement = "UPDATE nurse SET phone = %s WHERE tc = %s"
                cur.execute(statement,(phone,session['tc'],))  
            if(department != "."):
                statement = "UPDATE nurse SET dep = %s WHERE tc = %s"
                cur.execute(statement,(department,session['tc'],))
            if(password != ""):
                statement = "UPDATE nurse SET password = %s WHERE tc = %s"
                cur.execute(statement,(password,session['tc'],))  
            conn.commit()
            cur.close()
            conn.close()
            redirect(url_for("nurse_update"))
        except:
            flash('An error occured.', 'danger')
            return redirect(url_for('nurse_update'))

    return render_template("update_nurse.html", form = form)

@app.route("/account_update",methods=["GET","POST"])
def person_update():
    form = UpdatePerson()
    if (request.method =='POST'):
        tc = request.form['tc']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        try:
            conn = CDB()
            cur = conn.cursor()
            if(tc != ""):
                statement = "UPDATE person SET tc = %s WHERE tc = %s"
                cur.execute(statement,(tc,session['tc'],))
            if(first_name != ""):
                statement = "UPDATE person SET first_name = %s WHERE tc = %s"
                cur.execute(statement,(first_name,session['tc'],))
            if(last_name != ""):
                statement = "UPDATE person SET last_name = %s WHERE tc = %s"
                cur.execute(statement,(last_name,session['tc'],))
            if(gender != "."):
                if(gender == "F"):
                    statement = "UPDATE person SET gender = 'F' WHERE tc = %s"
                    cur.execute(statement,(session['tc'],))
                elif(gender == "M"):
                    statement = "UPDATE person SET gender = 'M' WHERE tc = %s"
                    cur.execute(statement,(session['tc'],))
            if(email != ""):
                statement = "UPDATE person SET email = %s WHERE tc = %s"
                cur.execute(statement,(email,session['tc'],))
            if(phone != ""):
                statement = "UPDATE person SET phone = %s WHERE tc = %s"
                cur.execute(statement,(phone,session['tc'],))
            if(password != ""):
                statement = "UPDATE person SET password = %s WHERE tc = %s"
                cur.execute(statement,(password,session['tc'],))
            
            conn.commit()
            cur.close()
            conn.close()
            redirect(url_for("person_update"))
        except:
            flash('An error occured.', 'danger')
            return redirect(url_for('person_update'))
    
    return render_template("update_person.html", form = form)

@app.route("/account_update_dr",methods=["GET","POST"])
def doctor_update():
    form = UpdateDoctor()
    if (request.method =='POST'):
        tc = request.form['tc']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        room = request.form['room']
        dep = request.form['department']
        password = request.form['password']
        try:
            conn = CDB()
            cur = conn.cursor()
            if(tc != ""):
                statement = "UPDATE doctor SET tc = %s WHERE tc = %s"
                cur.execute(statement,(tc,session['tc'],))
            if(first_name != ""):
                statement ="UPDATE doctor SET first_name = %s WHERE tc = %s"
                cur.execute(statement,(first_name,session['tc'],))
            if(last_name != ""):
                statement = "UPDATE doctor SET last_name = %s WHERE tc = %s"
                cur.execute(statement,(last_name,session['tc'],))
            if(gender != "."):
                if(gender == "F"):
                    statement = "UPDATE doctor SET gender = 'F' WHERE tc = %s"
                    cur.execute(statement,(session['tc'],))
                if(gender == "M"):
                    statement = "UPDATE doctor SET gender = 'M' WHERE tc = %s"
                    cur.execute(statement,(session['tc'],))
            if(email != ""):
                statement = "UPDATE doctor SET email = %s WHERE tc = %s"
                cur.execute(statement,(email,session['tc'],))
            if(phone != ""):
                statement = "UPDATE doctor SET phone = %s WHERE tc = %s"
                cur.execute(statement,(phone,session['tc'],))
            if(room != ""):
                statement = "UPDATE doctor SET room = %s WHERE tc = %s"
                cur.execute(statement,(room,session['tc'],))
            if(dep != "."):
                statement = "UPDATE doctor SET dep = %s WHERE tc = %s"
                cur.execute(statement,(dep,session['tc'],))
            if(password != ""):
                statement = "UPDATE doctor SET password = %s WHERE tc = %s"
                cur.execute(statement,(password,session['tc'],))
            
            conn.commit()
            cur.close()
            conn.close()
            redirect(url_for("doctor_update"))
        except:
            flash('An error occured.', 'danger')
            return redirect(url_for('doctor_update'))
    
    return render_template("update_doctor.html", form = form)

@app.route("/delete_person", methods=['GET', 'POST'])
def delAccountPerson():
    try:
        conn = CDB()
        cur = conn.cursor()
        statement  = "SELECT * FROM record WHERE patient_id = %s"
        cur.execute(statement,(session['tc'],))
        result = cur.fetchall()
        if(result != ""):
            statement = "DELETE FROM record WHERE patient_id = %s"
            cur.execute(statement, (session['tc'],))

        statement = "SELECT * FROM prescription WHERE patient_id = %s"
        cur.execute(statement,(session['tc'],))
        result = cur.fetchall()
        if(result != ""):
            statement = "DELETE FROM prescription WHERE patient_id = %s"
            cur.execute(statement, (session['tc'],))


        statement = "SELECT * FROM surgery WHERE patient_id = %s"
        cur.execute(statement,(session['tc'],))
        result = cur.fetchall()
        if(result != ""):
            statement = "DELETE FROM surgery WHERE patient_id = %s"
            cur.execute(statement, (session['tc'],))


        statement = "SELECT * FROM taken_appointments WHERE patient_id = %s"
        cur.execute(statement,(session['tc'],))
        result = cur.fetchall()
        if(result != ""):
            statement = "DELETE FROM taken_appointments WHERE patient_id = %s"
            cur.execute(statement, (session['tc'],))


        statement = "SELECT * FROM test WHERE patient_id = %s"
        cur.execute(statement,(session['tc'],))
        result = cur.fetchall()
        if(result != ""):
            statement = "DELETE FROM test WHERE patient_id = %s"
            cur.execute(statement, (session['tc'],))


        statement = "SELECT * FROM record WHERE patient_id = %s"
        cur.execute(statement,(session['tc'],))
        result = cur.fetchall()
        if(result != ""):
            statement = "DELETE FROM record WHERE patient_id = %s"
            cur.execute(statement, (session['tc'],))

        conn.commit()
        statement = "DELETE FROM person WHERE tc = %s"
        cur.execute(statement, (session['tc'],))
        conn.commit()

       
        cur.close()
        conn.close()
    except:
        flash('An error occured.', 'danger')
        return redirect(url_for('person_update'))

    return redirect(url_for("home"))

@app.route("/delete_doctor", methods=['GET', 'POST'])
def delAccountDoctor():
    try:
        conn = CDB()
        cur = conn.cursor()
        statement = "SELECT * FROM record WHERE doctor_id = %s"
        cur.execute(statement,(session['tc'],))
        result = cur.fetchall()
        if(result != ""):
            statement = "DELETE FROM record WHERE doctor_id = %s"
            cur.execute(statement, (session['tc'],))

        statement = "SELECT * FROM prescription WHERE doctor_id = %s"
        cur.execute(statement,(session['tc'],))
        result = cur.fetchall()
        if(result != ""):
            statement = "DELETE FROM prescription WHERE doctor_id = %s"
            cur.execute(statement, (session['tc'],))


        statement = "SELECT * FROM surgery WHERE doctor_id = %s"
        cur.execute(statement,(session['tc'],))
        result = cur.fetchall()
        if(result != ""):
            statement = "DELETE FROM surgery WHERE doctor_id = %s"
            cur.execute(statement, (session['tc'],))


        statement = "SELECT * FROM taken_appointments WHERE doctor_id = %s"
        cur.execute(statement,(session['tc'],))
        result = cur.fetchall()
        if(result != ""):
            statement = "DELETE FROM taken_appointments WHERE doctor_id = %s"
            cur.execute(statement, (session['tc'],))
        

        statement = "SELECT * FROM all_appointments WHERE doctor_id = %s"
        cur.execute(statement,(session['tc'],))
        result = cur.fetchall()
        if(result != ""):
            statement = "DELETE FROM all_appointments WHERE doctor_id = %s"
            cur.execute(statement, (session['tc'],))


        statement  ="SELECT * FROM test WHERE doctor_id = %s"
        cur.execute(statement,(session['tc'],))
        result = cur.fetchall()
        if(result != ""):
            statement = "DELETE FROM test WHERE doctor_id = %s"
            cur.execute(statement, (session['tc'],))


        statement = "SELECT * FROM record WHERE doctor_id = %s"
        cur.execute(statement,(session['tc'],))
        result = cur.fetchall()
        if(result != ""):
            statement = "DELETE FROM record WHERE doctor_id = %s"
            cur.execute(statement, (session['tc'],))

        conn.commit()
        statement = "DELETE FROM doctor WHERE tc = %s"
        cur.execute(statement, (session['tc'],))
        conn.commit()

       
        cur.close()
        conn.close()
    except:
        flash('An error occured.', 'danger')
        return redirect(url_for('doctor_update'))

    return redirect(url_for("home"))


@app.route("/delete_nurse", methods=['GET', 'POST'])
def delAccountNurse():
    try:
        conn = CDB()
        cur = conn.cursor()
        statement = "SELECT * FROM surgery WHERE nurse_id = %s"
        cur.execute(statement,(session['tc'],))
        result = cur.fetchall()
        if(result != ""):
            statement = "DELETE FROM surgery WHERE nurse_id = %s"
            cur.execute(statement, (session['tc'],))
        conn.commit()
        statement = "DELETE FROM nurse WHERE tc = %s"
        cur.execute(statement, (session['tc'],))
        conn.commit()
        cur.close()
        conn.close()
    except:
        flash('An error occured.', 'danger')
        return redirect(url_for('delete_nurse'))
    return redirect(url_for("home"))

     
if __name__ == '__main__':
    app.run(debug=True)
    