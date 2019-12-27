Parts Implemented by Seda Sugur
================================

.. note:: All table creations exist in dbinit.py file.

**************
Nurse
**************

1. Create
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

        CREATE TABLE IF NOT EXISTS nurse(
        tc BIGINT NOT NULL PRIMARY KEY UNIQUE,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        gender VARCHAR(1) NOT NULL,
        email TEXT,
        phone BIGINT,
        dep TEXT NOT NULL,
        pass TEXT NOT NULL
    )

2. Read
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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

.. code-block:: python

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



.. code-block:: python

    class LoginForm(FF):
        tc = IntegerField('TC', validators = [DataRequired()])
        password = PasswordField('Password', validators = [DataRequired()])
        remember = BooleanField('Remember Me')
        submit = SubmitField('Login')
    

3. Adding
~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: python

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


.. code-block:: python

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

4. Update
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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


.. code-block:: python

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

5. Delete
~~~~~~~~~~~~~~~~~~~~~~~~




.. code-block:: python

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

*******************
Test
*******************

1. Create
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

        CREATE TABLE IF NOT EXISTS test(
                id BIGSERIAL PRIMARY KEY NOT NULL,
                patient_id BIGINT REFERENCES person(tc) ON DELETE RESTRICT ON UPDATE CASCADE,
                doctor_id BIGINT REFERENCES doctor(tc) ON DELETE RESTRICT ON UPDATE CASCADE,
                liver_func TEXT,
                thyroid_func TEXT,
                genetic TEXT,
                electrolyte TEXT,
                coagulation TEXT,
                blood_gas TEXT,
                blood_glucose TEXT,
                blood_culture TEXT,
                full_blood_count TEXT
            )


3. Read
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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



3. Adding
~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: python

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



.. code-block:: python

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


4. Update
~~~~~~~~~~~~~~~~~~~~~~~~




.. code-block:: python

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


.. code-block:: python

    class TestU(FF):
        t_id = SelectField('Test id', choices=[])
        submit = SubmitField('Submit')

.. code-block:: python

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

.. code-block:: python


5.Delete
~~~~~~~~~~~~~~~~~~


.. code-block:: python

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
    
*******************
Prescription
*******************

1. Create
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

        CREATE TABLE IF NOT EXISTS prescription(
            id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
            patient_id BIGINT REFERENCES person(tc) ON DELETE RESTRICT ON UPDATE CASCADE,
            doctor_id BIGINT REFERENCES doctor(tc) ON DELETE RESTRICT ON UPDATE CASCADE,
            type TEXT NOT NULL,
            date_start TEXT NOT NULL,
            date_end TEXT NOT NULL,
            pills TEXT NOT NULL,
            diagnosis TEXT NOT NULL
        )



2. Read
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
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



3. Adding
~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: python

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



.. code-block:: python

        class Prescription(FF):
            patient = IntegerField('Patient ID', validators = [DataRequired()])
            pres_type = StringField('Prescription Type',validators = [DataRequired()])
            start_date = StringField('Start Date',validators = [DataRequired()])
            end_date = StringField('End Date',validators = [DataRequired()])
            pill = StringField('Pills',validators = [DataRequired()])
            diag = StringField('Diagnosis',validators = [DataRequired()])
            submit = SubmitField('Submit')


4. Update
~~~~~~~~~~~~~~~~~~~~~~~~




.. code-block:: python

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





5.Delete
~~~~~~~~~~~~~~~~~~


.. code-block:: python

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



