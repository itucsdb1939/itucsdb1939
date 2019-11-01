from flask import Flask,render_template, flash, redirect, url_for, request
from forms import RegistrationForm, LoginForm, LoginFormP, RegistrationFormD,Operation
import psycopg2

app = Flask(__name__)


DB_NAME = "afoeiapd"
DB_USER = "afoeiapd"
DB_PASS = "3N1LWGKtLZAdeI2sEQQR4N0I6GE1EnOM"
DB_HOST = "salt.db.elephantsql.com"
DB_PORT = "5432"
app.config['SECRET_KEY'] = 'f5b9ac4eddb1942feeb7d826b76b4a3f'

def CDB():
    try:
        connection = psycopg2.connect(dbname = DB_NAME, user = DB_USER, password = DB_PASS, host = DB_HOST, port = DB_PORT)
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
                statement = "INSERT INTO person (tc,first_name,last_name,email,phone,pass) VALUES ('%d','%s','%s','%s','%d','%s');"       
                cur.execute(statement,int(request.form['tc']),request.form['first_name'],request.form['last_name'],request.form['email'],int(request.form['phone']),request.form['password'])
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for('home_p'))
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
                statement = "INSERT INTO doctor (tc,first_name,last_name,email,phone,room,dep,pass) VALUES ('%d','%s','%s','%s','%d','%d','%s','%s');"        
                cur.execute(statement,int(request.form['tc']),request.form['first_name'],request.form['last_name'],request.form['email'],int(request.form['phone']),int(request.form['room']),request.form['department'],request.form['password'])
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for('home_dr'))
            except:
                return redirect(url_for('home'))
    return render_template("register_dr.html", form = form)

@app.route("/register_nr", methods=['GET', 'POST'])
def register_nr():
    form = RegistrationForm()
    if (request.method =='POST'):
        print(form.errors)
        if form.validate_on_submit():
            print(form.errors)
            try:
                conn = CDB()
                cur = conn.cursor()
                statement = "INSERT INTO nurse (tc,first_name,last_name,email,phone,pass) VALUES ('%d','%s','%s','%s','%d','%s');"       
                cur.execute(statement,int(request.form['tc']),request.form['first_name'],request.form['last_name'],request.form['email'],int(request.form['phone']),request.form['password'])
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for('home_d'))
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
                statement = "INSERT INTO surgery (patient_id,doctor_id,nurse_id,op_room,date,time) VALUES ('%d','%d','%d','%d','%s','%s');"
                cur.execute(statement,request.form['patient_id'],request.form['doctor_id'],request.form['nurse_id'],request.form['op_room'],request.form['date'],request.form['time'])
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

@app.route("/home_dr", methods=['GET', 'POST'])
def home_dr():
    return render_template("home_dr.html")

@app.route("/home_p", methods=['GET', 'POST'])
def home_p():
    return render_template("home_p.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginFormP()
    if form.validate_on_submit():
        if form.tc.data == '12345678900' and form.password.data == '1234567890':
            flash('you have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('no login', 'danger')
    return render_template("login.html", form = form)

@app.route("/login_dr", methods=['GET', 'POST'])
def login_dr():
    form = LoginForm()
    if form.validate_on_submit():
        if form.tc.data == '12345678900' and form.password.data == '1234567890':
            flash('you have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('no login', 'danger')
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

if __name__ == '__main__':
    app.run(debug = True)

