from flask import Flask,render_template, flash, redirect, url_for, request, session, jsonify
from forms import RegistrationForm, LoginForm, LoginFormP, RegistrationFormD,Operation,Appointment
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
                cur.execute("INSERT INTO person (tc,first_name,last_name,email,phone,pass) VALUES (%s,%s,%s,%s,%s,%s)",
                (request.form['tc'],request.form['first_name'],request.form['last_name'],request.form['email'],request.form['phone'],request.form['password'],))
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
                statement = "INSERT INTO doctor (tc,first_name,last_name,email,phone,room,dep,pass) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"        
                cur.execute(statement,(request.form['tc'],request.form['first_name'],request.form['last_name'],request.form['email'],request.form['phone'],request.form['room'],request.form['department'],request.form['password'],))
                
                conn.commit()
                cur.execute("select extract(dow from now())")
                day = cur.fetchone()
                
                cur.close()
                conn.close()
                return redirect(url_for('login_dr'))
            except:
                return redirect(url_for('home'))
    return render_template("register_dr.html", form = form)

@app.route("/register_nr", methods=['GET', 'POST'])
def register_nr():
    form = RegistrationForm()
    if (request.method =='POST'):
        if form.validate_on_submit():
            try:
                conn = CDB()
                cur = conn.cursor()
                statement = "INSERT INTO nurse (tc,first_name,last_name,email,phone,pass) VALUES (%s,%s,%s,%s,%s,%s)"       
                cur.execute(statement,(request.form['tc'],request.form['first_name'],request.form['last_name'],request.form['email'],request.form['phone'],request.form['password'],))
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
    try:
        conn = CDB()
        cur = conn.cursor()
        cur.execute("SELECT * FROM surgery")
        result = cur.fetchall()
        cur.close()
        conn.close()
    except:
        print("error")
    return render_template("op_view.html", table = result)

@app.route("/prescriptions" , methods=['GET'])
def pres():
    try:
        conn = CDB()
        cur = conn.cursor()
        cur.execute("SELECT * FROM pres WHERE (person = %s)",(session['tc'],))
        p = cur.fetchall() 
        cur.close()
        conn.close()
    except:
        print("error")
    return render_template("pres.html", table = p)



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
    if form.validate_on_submit():
        if form.tc.data == '12345678900' and form.password.data == '1234567890':
            flash('you have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('no login', 'danger')
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
