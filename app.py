from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:*****@localhost/hms'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum('male', 'female'), nullable=False)
    specialized_in = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum('male', 'female'), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False)
    medications = db.Column(db.Enum('yes', 'no'), nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    message = db.Column(db.Text, nullable=True)

# Routes
@app.route('/', methods=['GET', 'POST'])  # Login Page
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your email and password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('login'))

@app.route('/home')  # Home Page
@login_required
def home():
    return render_template('home.html')

@app.route('/pdash')  # Patient Dashboard
@login_required
def pdash():
    return render_template('pdash.html')

@app.route('/dash')  # Doctor Dashboard
@login_required
def dash():
    return render_template('dash.html')

@app.route('/sign', methods=['GET', 'POST'])  # SignUp Page
def sign():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pwd']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        print("Form Data Received")
        print(f"Email: {email}")

        new_user = User(email=email, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            print("New User Added to Database")
            flash("SignUp Successful!")
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            flash("SignUp Failed. Please try again.")
        
        return redirect(url_for('sign'))
    
    return render_template('sign.html')

@app.route('/dreg', methods=['GET', 'POST'])  # Doctor Registration
@login_required
def dreg():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        specialized_in = request.form['field']
        contact_number = request.form['contact']
        email = request.form['email']

        print("Form Data Received")
        print(f"Name: {name}")
        print(f"Age: {age}")
        print(f"Gender: {gender}")
        print(f"Specialized In: {specialized_in}")
        print(f"Contact Number: {contact_number}")
        print(f"Email: {email}")
        
        new_doctor = Doctor(
            name=name,
            age=age,
            gender=gender,
            specialized_in=specialized_in,
            contact_number=contact_number,
            email=email
        )
        
        try:
            db.session.add(new_doctor)
            db.session.commit()
            print("New Doctor Added to Database")
            flash("Registration Successful!")
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            flash("Registration Failed. Please try again.")
        
        return redirect(url_for('dash'))
    
    return render_template('dreg.html')

@app.route('/preg', methods=['GET', 'POST'])  # Patient Registration
@login_required
def preg():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        height = request.form['height']
        weight = request.form['weight']
        contact = request.form['contact']
        email = request.form['email']
        address = request.form['address']
        medications = request.form['medications']

        print("Form Data Received")
        print(f"Name: {name}")
        print(f"Age: {age}")
        print(f"Gender: {gender}")
        print(f"Height: {height}")
        print(f"Weight: {weight}")
        print(f"Contact: {contact}")
        print(f"Email: {email}")
        print(f"Address: {address}")
        print(f"Medications: {medications}")
        
        new_patient = Patient(
            name=name, 
            age=age, 
            gender=gender, 
            height=height, 
            weight=weight, 
            contact=contact, 
            email=email, 
            address=address, 
            medications=medications
        )
        
        try:
            db.session.add(new_patient)
            db.session.commit()
            print("New Patient Added to Database")
            flash("Registration Successful!")
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            flash("Registration Failed. Please try again.")
        
        return redirect(url_for('preg'))
    
    return render_template('preg.html')

@app.route('/appoint', methods=['GET', 'POST'])  # Appointment Form
@login_required
def appoint():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        appointment_date = request.form['appointment-date']
        appointment_time = request.form['appointment-time']
        message = request.form.get('message', '')

        print("Appointment Data Received")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Phone: {phone}")
        print(f"Date: {appointment_date}")
        print(f"Time: {appointment_time}")
        print(f"Message: {message}")
        
        new_appointment = Appointment(
            name=name, 
            email=email, 
            phone=phone, 
            appointment_date=appointment_date, 
            appointment_time=appointment_time, 
            message=message
        )
        
        try:
            db.session.add(new_appointment)
            db.session.commit()
            print("New Appointment Added to Database")
            flash("Appointment Booking Successful!")
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            flash("Appointment Booking Failed. Please try again.")
        
        return redirect(url_for('home'))
    
    return render_template('appoint.html')

@app.route('/view_doctors')  # Route to View Doctors
@login_required
def view_doctors():
    doctors = Doctor.query.all()
    return render_template('view_doctors.html', doctors=doctors)

@app.route('/view_patients')  # Route to View Patients
@login_required
def view_patients():
    patients = Patient.query.all() 
    return render_template('view_patients.html', patients=patients)

@app.route('/view_appointments')  # View Appointments
@login_required
def view_appointments():
    appointments = Appointment.query.all() 
    return render_template('view_appointments.html', appointments=appointments)

@app.route('/delete_patient') 
@login_required
def delete_patient():
    patients = Patient.query.all()
    return render_template('delete_patient.html', patients=patients)

@app.route('/delete_patient_by_id/<int:patient_id>', methods=['POST'])
@login_required
def delete_patient_by_id(patient_id):
     patient = Patient.query.get_or_404(patient_id) 
     try: 
        db.session.delete(patient) 
        db.session.commit() 
        flash("Patient deleted successfully!")
     except Exception as e: 
        db.session.rollback() 
        print(f"Error: {e}")
        flash("Error deleting patient. Please try again.") 
     return redirect(url_for('delete_patient'))

@app.route('/delete_doctor') 
def delete_doctor(): 
    doctors = Doctor.query.all()
    return render_template('delete_doctor.html', doctors=doctors)
    
@app.route('/delete_doctor_by_id/<int:doctor_id>', methods=['POST']) 
def delete_doctor_by_id(doctor_id): 
    doctor = Doctor.query.get_or_404(doctor_id)
    try: 
        db.session.delete(doctor) 
        db.session.commit() 
        flash("Doctor deleted successfully!")
    except Exception as e: 
        db.session.rollback() 
        print(f"Error: {e}") 
        flash("Error deleting doctor. Please try again.") 
    return redirect(url_for('delete_doctor'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
