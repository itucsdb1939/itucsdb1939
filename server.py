from flask import Flask,render_template, flash, redirect, url_for, request, session, jsonify
from forms import RegistrationForm, LoginForm, LoginFormP, NewPatient, RegistrationFormD,Operation,Appointment,RegistrationFormN,NewTest
import psycopg2
from dbinit import initialize
from os import environ

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
                cur.execute("INSERT INTO person (tc,first_name,last_name,email,phone,pass,gender) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (request.form['tc'],request.form['first_name'],request.form['last_name'],request.form['email'],request.form['phone'],request.form['password'],request.form['gender'],))
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for('login'))
            except:
                return redirect(url_for('register'))
    return render_template("register.html", form = form)

@app.route("/register_dr", methods=['GET', 'POST'])
def register_dr():
    form = RegistrationFormD()
    if (request.method =='POST'):
        if form.validate_on_submit():
            try: 
                conn = CDB()
                cur = conn.cursor()
                statement = "INSERT INTO doctor (tc,first_name,last_name,gender,email,phone,room,dep,pass) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"        
                cur.execute(statement,(request.form['tc'],request.form['first_name'],request.form['last_name'],request.form['gender'],request.form['email'],request.form['phone'],request.form['room'],request.form['department'],request.form['password'],))
            
                conn.commit()
                
                cur.close()
                conn.close()
                return redirect(url_for('login_dr'))
            except:
                return redirect(url_for('home'))
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
                return redirect(url_for('login_nr'))
            except:
                print("error")
    return render_template("register_nr.html", form = form)

@app.route("/op_dr", methods=['GET', 'POST'])
def operation():
    form = Operation()
    if (request.method =='POST'):
        if form.validate_on_submit():
            try:
                conn = CDB()
                cur = conn.cursor()
                statement = "INSERT INTO surgery (patient_id,doctor_id,nurse_id,op_room,date,time) VALUES (%s,%s,%s,%s,%s,%s)"
                cur.execute(statement,(request.form['patient_id'],request.form['doctor_id'],request.form['nurse_id'],request.form['room'],request.form['date'],request.form['time'],))
                conn.commit()
                cur.close()
                conn.close()
                flash('Surgery registraton successful.', 'success')
                return redirect(url_for('operation'))
            except:
                print("error")
                return redirect(url_for('operation'))
    return render_template("op_dr.html", form = form)

@app.route("/op_view", methods=['GET'])
def op_view():
    result = []
    try:
        conn = CDB()
        cur = conn.cursor()
        cur.execute("SELECT * FROM surgery WHERE doctor_id = (%s) OR nurse_id = (%s)",(session['tc'],))
        result = cur.fetchall()
        if not result:
            result = []
        cur.close()
        conn.close()
    except:
        print("error")
    return render_template("op_view.html", table = result)

@app.route("/prescriptions" , methods=['GET'])
def pres():
    p = []
    doctor = []
    try:
        conn = CDB()
        cur = conn.cursor()
        cur.execute("SELECT * FROM prescription WHERE (patient_id = %s)",(session['tc'],))
        p = cur.fetchall()
        cur.execute("SELECT first_name, last_name FROM doctor WHERE (tc = %s)",(p[0][2],))
        doctor = cur.fetchall()
        doctor = doctor[0][0] + " " + doctor[0][1]
        cur.close()
        conn.close()
    except:
        print("error")
    return render_template("pres.html", table = p,dr=doctor)

@app.route("/blood_test" , methods=['GET'])
def blood():
    blood = []
    doctor =[]
    try:
        conn = CDB()
        cur = conn.cursor()
        cur.execute("SELECT * FROM test WHERE (patient_id = %s)",(session['tc'],))
        blood = cur.fetchall() 
        cur.execute("SELECT first_name, last_name FROM doctor WHERE (tc = %s)",(blood[0][2],))
        doctor = cur.fetchall()
        doctor = doctor[0][0] + " " + doctor[0][1]
        cur.close()
        conn.close()
    except:
        print("error")
    return render_template("blood_test.html", table = blood, dr=doctor)

@app.route("/patient_view/prescription/<pres>", methods=['GET', 'POST'])
def pres_view(pres):
    prescriptions = []
    try:
        conn = CDB()
        cur = conn.cursor()
        cur.execute("SELECT * FROM prescription WHERE (id = %s)",(pres,))
        prescriptions = cur.fetchall()
        cur.close()
        conn.close()
    except:
        print("error")
    return render_template("pres_view.html", pres = prescriptions)
@app.route("/patient_view/test/<test>", methods=['GET', 'POST'])
def test_view(test):
    tests = []
    try:
        conn = CDB()
        cur = conn.cursor()
        cur.execute("SELECT * FROM test WHERE (id = %s)",(test,))
        tests = cur.fetchall()
        cur.close()
        conn.close()
    except:
        print("error")
    return render_template("test_view.html", test = tests)

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
        cur.execute("SELECT * FROM record WHERE (doctor_id = %s)",(session['tc'],))
        patients = cur.fetchall()
        if(patients != []):
            for i in range(0,len(patients)):
                cur.execute("SELECT first_name, last_name FROM person WHERE (tc = %s)",(patients[i][0],))
                patient = cur.fetchall()
                p = patient[0][0] + " " + patient[0][1]
                patient_names.append(p)
                cur.execute("SELECT * FROM prescription WHERE (patient_id = %s)",(patients[i][0],))
                pres = cur.fetchall()
                patient_pres.append([])
                for j in range(0,len(pres)):
                    patient_pres[i].append(pres[j][0])
                cur.execute("SELECT * FROM test WHERE (patient_id = %s)",(patients[i][0],))
                test = cur.fetchall()
                patient_test.append([])
                for j in range(0,len(test)):
                    patient_test[i].append(test[j][0])  
            l = len(patients)
            print(patient_test)
        cur.close()
        conn.close()
    except:
        print("error")
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
                print("error")
                
    
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
                return redirect(url_for('new_test'))
            except:
                print("error")
                
    
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
                cur.execute("SELECT pass FROM person WHERE tc=%s",(tc,))
                result = cur.fetchone()
                if(result[0] == passw):
                    session['tc'] = tc
                    return redirect(url_for('home_p'))
                else:
                    flash('no login', 'danger')
                    return redirect(url_for('login'))
                cur.close()
                conn.close()
            except:
                print("error")
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
                cur.execute("SELECT pass FROM doctor WHERE tc=%s",(tc,))
                result = cur.fetchone()
                if(result[0] == passw):
                    session['tc'] = tc
                    cur.close()
                    conn.close()
                    return redirect(url_for('home_dr'))
                else:
                    flash('no login', 'danger')
                    cur.close()
                    conn.close()
                    return redirect(url_for('login_dr'))
                
            except:
                print("error")
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
                cur.execute("SELECT pass FROM nurse WHERE tc=%s",(tc,))
                result = cur.fetchone()
                if(result[0] == passw):
                    return redirect(url_for('home_nurse'))
                else:
                    flash('no login', 'danger')
                    return redirect(url_for('login_nr'))
                cur.close()
                conn.close()
            except:
                print("error")
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
            cur.execute("INSERT INTO taken_appointments (patient_id,doctor_id,date,time) VALUES (%s,%s,%s,%s)",(tc,doctor,date,time,))
            cur.execute("DELETE FROM all_appointments WHERE doctor_id = %s AND date = %s AND time = %s",(doctor,date,time,))
            conn.commit()
            
        cur.close()
        conn.close()
    except:
        print("error")
    return render_template("appo.html", form = form)

@app.route("/make_appointment/<dep>",methods=["GET","POST"])
def select_doc(dep):
    appo_doc = []
    try:
        conn = CDB()
        cur = conn.cursor()
        cur.execute("SELECT doctor_id FROM all_appointments WHERE dep = %s",(dep,))
        result = cur.fetchall()
        for i in range(0,len(result)):
            appo_doc.append(result[i][0])
        doc = []
        docObj = {}
        docObj['tc'] = 0
        docObj['name'] = 'Select'
        doc.append(docObj)
        for i in appo_doc:
            cur.execute("SELECT first_name,last_name FROM doctor WHERE tc = %s",(i,))
            result = cur.fetchall()
            name = result[0][0] + " " + result[0][1]
            docObj = {}
            docObj['tc'] = i
            docObj['name'] = name
            doc.append(docObj)
            
        cur.close()
        conn.close()
    except:
        print("error")
    return jsonify({"docs": doc})

@app.route("/make_appointment/<dep>/<doc>",methods=["GET","POST"])
def select_date(dep,doc):
    dates = []
    try:
        conn = CDB()
        cur = conn.cursor()
        cur.execute("SELECT date FROM all_appointments WHERE dep = %s AND doctor_id = %s",(dep,doc,))
        result = cur.fetchall()
      
        for i in range(0,len(result)):
            dates.append(int(result[i][0]))
       
        date = []
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
        print("error")
    return jsonify({"dates": date})

@app.route("/make_appointment/<dep>/<doc>/<date>",methods=["GET","POST"])
def select_time(dep,doc,date):
    times = []
    try:
        conn = CDB()
        cur = conn.cursor()
        cur.execute("SELECT date FROM all_appointments WHERE dep = %s AND doctor_id = %s AND date = %s",(dep,doc,date,))
        result = cur.fetchall()
   
        for i in range(0,len(result)):
            times.append(int(result[i][0]))
        
        time = []
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
        print("error")
    return jsonify({"times": time})






if __name__ == '__main__':
    if(not RELEASE):
        app.run(debug=True)
    else:
        app.run()