from flask import Flask,render_template, flash, redirect, url_for, request
from forms import RegistrationForm, LoginForm, LoginFormP, RegistrationFormD,Operation
import psycopg2
app = Flask(__name__)


DB_NAME = "dbjrtdrqa9jsc6"
DB_USER = "afxpitnfwcxnoy"
DB_PASS = "4b83fbb00a008227350fee5f8be5f9dc24cd148418e58fa92755aa060998ec72"
DB_HOST = "ec2-54-235-96-48.compute-1.amazonaws.com"
DB_PORT = "5432"

def CDB():
    try:
        connection = psycopg2.connect(dbname = DB_NAME, user = DB_USER, password = DB_PASS, host = DB_HOST, port = DB_PORT)
        print("SSS")
        return connection
        
    except:
        print("FFF")


conn = CDB()
cur = conn.cursor()



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
                cur.execute(f"INSERT INTO person (tc,first_name,last_name,email,phone,pass) VALUES ('{request.form['tc']}','{request.form['first_name']}','{request.form['last_name']}','{request.form['e_mail']}','{request.form['phone']}','{request.form['password']}');")
                return render_template("home_dr.html")
            except:
                return render_template("home.html")
            flash(f'hey {form.first_name.data}', 'success')
            return redirect(url_for('home_dr'))
        
    conn.commit()
    return render_template("register.html", form = form)

@app.route("/register_dr", methods=['GET', 'POST'])
def register_dr():
    form = RegistrationFormD()
    if (request.method =='POST'):
        tc = request.form['tc']
        if(tc == 12345678900):
            return render_template("login.html")
        """
        try:
            cur.execute("INSERT INTO doctor (tc,first_name,last_name,email,phone,room,dep,pass) VALUES ('{tc}','{fn}','{ln}','{mail}','{ph}','{room}','{dep}','{passw}');".format(tc = request.form['tc'],fn = request.form['first_name'],ln = request.form['last_name'],mail = request.form['e_mail'],ph = request.form['phone'],room = request.form['room'],dep = request.form['department'], passw =request.form['password']))
        except:
            return render_template("home.html")
        """
    
    return render_template("register_dr.html", form = form)

@app.route("/register_nr", methods=['GET', 'POST'])
def register_nr():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'hey {form.first_name.data}', 'success')
        return redirect(url_for('home_dr'))
    return render_template("register_nr.html", form = form)

@app.route("/op_dr", methods=['GET', 'POST'])
def operation():
    form = Operation()
    if (request.method =='POST'):
        try:
            cur.execute("""INSERT INTO surgery(patient_id,doctor_id,nurse_id,op_room,date,time)
            VALUES (%d,%d,%d,%d,%s,%s);
            """,(form.patient_id.data,form.doctor_id.data,form.nurse_id.data,form.room.data,form.date.data,form.time.data))
        except:
            print("error")
    conn.commit()
    if form.validate_on_submit():
        flash(f'hey {form.patient_id.data}', 'success')
        return redirect(url_for('home_dr'))
    return render_template("op_dr.html", form = form)

@app.route("/op_view", methods=['GET'])
def op_view():
    try:
        cur.execute("SELECT * FROM surgery")
    except:
        print("error")
    result = cur.fetchall()
    return render_template("op_view.html", table = result)

@app.route("/home_dr", methods=['GET', 'POST'])
def home_dr():
    return render_template("home_dr.html")












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

####randevu zamanınaunique constraint koy
