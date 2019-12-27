Parts Implemented by Buket Akgun
================================

.. note:: All table creations exist in dbinit.py file.

**************
Doctor
**************

1. Create
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS doctor(
            tc BIGINT NOT NULL PRIMARY KEY UNIQUE,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            gender VARCHAR(1) NOT NULL,
            email TEXT,
            phone BIGINT,
            room INTEGER NOT NULL,
            dep TEXT NOT NULL,
            pass TEXT NOT NULL 
        )
   

2. Read
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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




.. code-block:: python

    class LoginForm(FF):
        tc = IntegerField('TC', validators = [DataRequired()])
        password = PasswordField('Password', validators = [DataRequired()])
        remember = BooleanField('Remember Me')
        submit = SubmitField('Login')
        

3. Adding
~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: python

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


.. code-block:: python

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

4. Update
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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


.. code-block:: python

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

5. Delete
~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: python

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


        

*******************
Surgery
*******************

1. Create
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS surgery(
            id BIGSERIAL PRIMARY KEY NOT NULL,
            patient_id BIGINT REFERENCES person(tc) ON DELETE RESTRICT ON UPDATE CASCADE,
            doctor_id BIGINT REFERENCES doctor(tc) ON DELETE RESTRICT ON UPDATE CASCADE,
            nurse_id BIGINT REFERENCES nurse(tc) ON DELETE RESTRICT ON UPDATE CASCADE,
            op_room INTEGER NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            blood_type TEXT NOT NULL,
            op_report TEXT,
            UNIQUE(date,time,op_room)
        )

        


2. Read
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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
        


3. Insert
~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: python

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
    

.. code-block:: python

    class Operation(FF):
        patient_id = IntegerField('Patient ID', validators=[DataRequired()])
        nurse_id = IntegerField('Nurse ID')
        room = IntegerField('Operating room', validators=[DataRequired()])
        date = StringField('Date', validators=[DataRequired()])
        time = StringField('Time', validators=[DataRequired()])
        blood = StringField('Blood Type', validators=[DataRequired()])
        report = StringField('Operation Report', validators=[DataRequired()])
        submit = SubmitField('Submit')   

4. Update
~~~~~~~~~~~~~~~~~~~~~~~~




.. code-block:: python

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
    


.. code-block:: python

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
    
.. code-block:: python

    class OperationU(FF):
        opid = SelectField('Surgery ID', choices=[])
        submit = SubmitField('Submit')


5.Delete
~~~~~~~~~~~~~~~~~~


.. code-block:: python

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

    
    
*******************
Person
*******************

1. Create
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS person(
        tc BIGINT NOT NULL PRIMARY KEY UNIQUE,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        gender VARCHAR(1) NOT NULL,
        email TEXT,
        phone BIGINT,
        pass TEXT NOT NULL
    )
       


2. Read
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
    
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


3. Insert
~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: python

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
        

.. code-block:: python

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


4. Update
~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: python

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
    


.. code-block:: python

    class UpdatePerson(FF):
        tc = IntegerField('TC')
        first_name = StringField('First Name', validators = [Length(min = 2, max = 20)])
        last_name = StringField('Last Name', validators = [Length(min = 2, max = 20)] )
        gender = SelectField('Gender', choices = [('.','Select'),('F','Female'),('M','Male')])
        email = StringField('Email', validators = [Email()])
        phone = IntegerField('Phone Number')
        password = PasswordField('Password')
        submit = SubmitField('Update')



5.Delete
~~~~~~~~~~~~~~~~~~


.. code-block:: python

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

    



