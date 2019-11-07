from dbinit import initialize
from flask import Flask,render_template, flash, redirect, url_for, request, session, jsonify
from forms import RegistrationForm, LoginForm, LoginFormP, RegistrationFormD,Operation,Appointment,RegistrationFormN
import psycopg2
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
                cur.execute(statement,(request.form['tc'],request.form['first_name'],request.form['last_name'],request.form['gender'],request.form['email'],request.form['phone'],request.form['dep'],request.form['password'],))
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for('login_nr'))
            except:
                return redirect(url_for('home'))
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


@app.route("/patient_view", methods=['GET', 'POST'])
def p_view():
    patients = []
    patient_names = []
    try:
        conn = CDB()
        cur = conn.cursor()
        cur.execute("SELECT * FROM record WHERE (doctor_id = %s)",(session['tc'],))
        patients = cur.fetchall() 
        if(patients != []):
            cur.execute("SELECT first_name, last_name FROM person WHERE (tc = %s)",(patients[0][0],))
            patient = cur.fetchall()
            print(patient)
            for i in range(0,len(patient)):
                print(i)
                patient_names[i] = patient[i][0] + " " + patient[i][1]
                print("hoho")
        cur.close()
        conn.close()
    except:
        print("error")
    return render_template("patient_view.html", table = patients, pt=patient_names)

@app.route("/home_dr", methods=['GET', 'POST'])
def home_dr():
    return render_template("home_dr.html")

@app.route("/home_p", methods=['GET', 'POST'])
def home_p():
    return render_template("home_p.html")

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
                    return redirect(url_for('home_dr'))
                else:
                    flash('no login', 'danger')
                    return redirect(url_for('login_dr'))
                cur.close()
                conn.close()
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
                    return redirect(url_for('home_dr'))
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
        cur.execute("SELECT dep FROM doctor ORDER BY dep ASC")
        dep = cur.fetchall()
        deps = []
        for i in range(0,len(dep)):
            deps.append(tuple((i,dep[i][0])))
        
        form.dep.choices = deps
        if (request.method =='POST'):
            ph = form.dep.data
            url = "/make_appointment/{}".format(dep[int(ph)][0])
            return redirect(url)
    except:
        print("error")
    return render_template("appo.html", form = form)





if __name__ == '__main__':
    if(not RELEASE):
        app.run(debug=True)
    else:
        app.run()
