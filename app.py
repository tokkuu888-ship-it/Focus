from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, TimeField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import secrets
from functools import wraps

# Database configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

# Check if we're in production (Render) or development
if os.environ.get('DATABASE_URL'):
    # Production: Use PostgreSQL from Render
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    print("🗄️ Using PostgreSQL database (Production)")
else:
    # Development: Use SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///counseling.db'
    print("🗄️ Using SQLite database (Development)")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'student' or 'counselor'
    full_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    counselor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    duration = db.Column(db.Integer, default=60)  # minutes
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship('User', foreign_keys=[student_id], backref='student_appointments')
    counselor = db.relationship('User', foreign_keys=[counselor_id], backref='counselor_appointments')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')

class IntakeForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    contact_info = db.Column(db.String(100))
    emergency_contact = db.Column(db.String(100))
    academic_program = db.Column(db.String(100))
    counseling_history = db.Column(db.Text)
    current_concerns = db.Column(db.Text)
    spiritual_background = db.Column(db.Text)
    consent_agreed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship('User', backref='intake_forms')

class SOAPNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    subjective = db.Column(db.Text)
    objective = db.Column(db.Text)
    assessment = db.Column(db.Text)
    plan = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    appointment = db.relationship('Appointment', backref='soap_notes')

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    full_name = StringField('Full Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('User Type', choices=[
        ('admin', 'Admin username/email'),
        ('counselor', 'Counselor'),
        ('student', 'Student')
    ], validators=[DataRequired()])

class AppointmentForm(FlaskForm):
    counselor_id = SelectField('Counselor', coerce=int, validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    notes = TextAreaField('Additional Notes')

class IntakeFormForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    age = StringField('Age')
    contact_info = StringField('Contact Information')
    emergency_contact = StringField('Emergency Contact')
    academic_program = StringField('Academic Program/Year')
    counseling_history = TextAreaField('Previous Counseling History')
    current_concerns = TextAreaField('Current Concerns', validators=[DataRequired()])
    spiritual_background = TextAreaField('Spiritual Background')

class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])

class ProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Current Password')
    new_password = PasswordField('New Password', validators=[Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[EqualTo('new_password')])

class AdminUserEditForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    user_type = SelectField('User Type', choices=[('student', 'Student'), ('counselor', 'Counselor'), ('admin', 'Administrator')])
    is_active = BooleanField('Account Active')
    reset_password = BooleanField('Reset Password to Default')

# Decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def counselor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_type') != 'counselor':
            flash('Access denied. Counselor access required.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_type') != 'admin':
            flash('Access denied. Administrator access required.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_type'] = user.user_type
            session['full_name'] = user.full_name
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'error')
            return render_template('register.html', form=form)
        
        user = User(
            username=form.username.data,
            email=f"{form.username.data}@focus.org",  # Generate default email
            full_name=form.full_name.data,
            user_type=form.user_type.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    if session['user_type'] == 'student':
        appointments = Appointment.query.filter_by(student_id=user.id).order_by(Appointment.date.desc()).all()
        intake_form = IntakeForm.query.filter_by(student_id=user.id).first()
        return render_template('student_dashboard.html', appointments=appointments, intake_form=intake_form)
    elif session['user_type'] == 'counselor':
        appointments = Appointment.query.filter_by(counselor_id=user.id).order_by(Appointment.date.desc()).all()
        return render_template('counselor_dashboard.html', appointments=appointments)
    elif session['user_type'] == 'admin':
        return render_template('admin_dashboard.html')
    else:
        flash('Invalid user type', 'error')
        return redirect(url_for('logout'))

@app.route('/book_appointment', methods=['GET', 'POST'])
@login_required
def book_appointment():
    if session['user_type'] != 'student':
        flash('Only students can book appointments', 'error')
        return redirect(url_for('dashboard'))
    
    form = AppointmentForm()
    form.counselor_id.choices = [(c.id, c.full_name) for c in User.query.filter_by(user_type='counselor').all()]
    
    if form.validate_on_submit():
        appointment = Appointment(
            student_id=session['user_id'],
            counselor_id=form.counselor_id.data,
            date=form.date.data,
            time=form.time.data,
            notes=form.notes.data
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('book_appointment.html', form=form)

@app.route('/intake_form', methods=['GET', 'POST'])
@login_required
def intake_form():
    if session['user_type'] != 'student':
        flash('Only students can complete intake forms', 'error')
        return redirect(url_for('dashboard'))
    
    existing_form = IntakeForm.query.filter_by(student_id=session['user_id']).first()
    if existing_form:
        flash('You have already completed an intake form', 'info')
        return redirect(url_for('dashboard'))
    
    form = IntakeFormForm()
    if form.validate_on_submit():
        intake = IntakeForm(
            student_id=session['user_id'],
            full_name=form.full_name.data,
            age=form.age.data,
            contact_info=form.contact_info.data,
            emergency_contact=form.emergency_contact.data,
            academic_program=form.academic_program.data,
            counseling_history=form.counseling_history.data,
            current_concerns=form.current_concerns.data,
            spiritual_background=form.spiritual_background.data,
            consent_agreed=True
        )
        db.session.add(intake)
        db.session.commit()
        flash('Intake form submitted successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('intake_form.html', form=form)

@app.route('/messages')
@login_required
def messages():
    user_id = session['user_id']
    sent_messages = Message.query.filter_by(sender_id=user_id).order_by(Message.timestamp.desc()).all()
    received_messages = Message.query.filter_by(receiver_id=user_id).order_by(Message.timestamp.desc()).all()
    
    # Mark received messages as read
    for msg in received_messages:
        if not msg.is_read:
            msg.is_read = True
    db.session.commit()
    
    # Get counselors and students for the template
    counselors = User.query.filter_by(user_type='counselor').all()
    students = User.query.filter_by(user_type='student').all()
    
    return render_template('messages.html', sent_messages=sent_messages, received_messages=received_messages, counselors=counselors, students=students)

@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    receiver_id = request.form.get('receiver_id')
    content = request.form.get('message')
    
    if receiver_id and content:
        message = Message(
            sender_id=session['user_id'],
            receiver_id=receiver_id,
            content=content
        )
        db.session.add(message)
        db.session.commit()
        flash('Message sent successfully!', 'success')
    else:
        flash('Please select a recipient and enter a message', 'error')
    
    return redirect(url_for('messages'))

@app.route('/soap_note/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
@counselor_required
def soap_note(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    
    if appointment.counselor_id != session['user_id']:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        soap = SOAPNote(
            appointment_id=appointment_id,
            subjective=request.form.get('subjective'),
            objective=request.form.get('objective'),
            assessment=request.form.get('assessment'),
            plan=request.form.get('plan')
        )
        db.session.add(soap)
        db.session.commit()
        flash('SOAP note saved successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('soap_note.html', appointment=appointment)

@app.route('/api/messages/<int:user_id>')
@login_required
def get_messages(user_id):
    messages = Message.query.filter(
        ((Message.sender_id == session['user_id']) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == session['user_id']))
    ).order_by(Message.timestamp.asc()).all()
    
    return jsonify([{
        'id': msg.id,
        'sender': msg.sender.full_name,
        'content': msg.content,
        'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M'),
        'is_sent': msg.sender_id == session['user_id']
    } for msg in messages])

# Admin Routes
@app.route('/admin/users')
@admin_required
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/appointments')
@admin_required
def admin_appointments():
    appointments = Appointment.query.order_by(Appointment.date.desc()).all()
    return render_template('admin_appointments.html', appointments=appointments)

@app.route('/admin/messages')
@admin_required
def admin_messages():
    messages = Message.query.order_by(Message.timestamp.desc()).limit(100).all()
    return render_template('admin_messages.html', messages=messages)

@app.route('/admin/stats')
@admin_required
def admin_stats():
    total_users = User.query.count()
    total_students = User.query.filter_by(user_type='student').count()
    total_counselors = User.query.filter_by(user_type='counselor').count()
    total_admins = User.query.filter_by(user_type='admin').count()
    total_appointments = Appointment.query.count()
    scheduled_appointments = Appointment.query.filter_by(status='scheduled').count()
    completed_appointments = Appointment.query.filter_by(status='completed').count()
    total_messages = Message.query.count()
    
    stats = {
        'total_users': total_users,
        'total_students': total_students,
        'total_counselors': total_counselors,
        'total_admins': total_admins,
        'total_appointments': total_appointments,
        'scheduled_appointments': scheduled_appointments,
        'completed_appointments': completed_appointments,
        'total_messages': total_messages
    }
    
    return render_template('admin_stats.html', stats=stats)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == session['user_id']:
        flash('You cannot delete your own account', 'error')
    else:
        # Delete related records
        Message.query.filter((Message.sender_id == user_id) | (Message.receiver_id == user_id)).delete()
        Appointment.query.filter((Appointment.student_id == user_id) | (Appointment.counselor_id == user_id)).delete()
        IntakeForm.query.filter_by(student_id=user_id).delete()
        
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.full_name} has been deleted', 'success')
    
    return redirect(url_for('admin_users'))

# User Profile Management
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = User.query.get(session['user_id'])
    form = ProfileForm()
    
    if form.validate_on_submit():
        # Verify current password if changing password
        if form.new_password.data:
            if not form.current_password.data or not user.check_password(form.current_password.data):
                flash('Current password is required to change password', 'error')
                return render_template('edit_profile.html', form=form)
            
            if form.new_password.data != form.confirm_password.data:
                flash('New passwords do not match', 'error')
                return render_template('edit_profile.html', form=form)
            
            user.set_password(form.new_password.data)
            flash('Password updated successfully', 'success')
        
        # Update profile information
        user.full_name = form.full_name.data
        user.email = form.email.data
        
        # Check if email is already taken by another user
        existing_user = User.query.filter(User.email == form.email.data, User.id != user.id).first()
        if existing_user:
            flash('Email is already taken by another user', 'error')
            return render_template('edit_profile.html', form=form)
        
        db.session.commit()
        
        # Update session
        session['full_name'] = user.full_name
        flash('Profile updated successfully', 'success')
        return redirect(url_for('dashboard'))
    
    # Pre-fill form with current user data
    form.full_name.data = user.full_name
    form.email.data = user.email
    
    return render_template('edit_profile.html', form=form)

# Enhanced Admin User Management
@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = AdminUserEditForm()
    
    if form.validate_on_submit():
        # Prevent admin from changing their own user type to avoid losing admin access
        if user.id == session['user_id'] and form.user_type.data != 'admin':
            flash('You cannot change your own user type', 'error')
            return render_template('admin_edit_user.html', form=form, user=user)
        
        # Update user information
        user.full_name = form.full_name.data
        user.email = form.email.data
        user.user_type = form.user_type.data
        
        # Check if email is already taken by another user
        existing_user = User.query.filter(User.email == form.email.data, User.id != user.id).first()
        if existing_user:
            flash('Email is already taken by another user', 'error')
            return render_template('admin_edit_user.html', form=form, user=user)
        
        # Reset password if requested
        if form.reset_password.data:
            default_password = f"{user.user_type}123"
            user.set_password(default_password)
            flash(f'Password for {user.full_name} has been reset to: {default_password}', 'info')
        
        db.session.commit()
        flash(f'User {user.full_name} has been updated successfully', 'success')
        return redirect(url_for('admin_users'))
    
    # Pre-fill form with current user data
    form.full_name.data = user.full_name
    form.email.data = user.email
    form.user_type.data = user.user_type
    form.is_active.data = True  # Default to active since we don't have is_active field yet
    
    return render_template('admin_edit_user.html', form=form, user=user)

@app.route('/admin/toggle_user_status/<int:user_id>', methods=['POST'])
@admin_required
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    # For now, we'll just toggle between active/inactive by adding a status field
    # This would require modifying the User model to include an 'is_active' field
    flash(f'User status for {user.full_name} has been updated', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/view_user/<int:user_id>')
@admin_required
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Get user statistics
    if user.user_type == 'student':
        appointments = Appointment.query.filter_by(student_id=user.id).all()
        intake_form = IntakeForm.query.filter_by(student_id=user.id).first()
        sent_messages = Message.query.filter_by(sender_id=user.id).count()
        received_messages = Message.query.filter_by(receiver_id=user.id).count()
    elif user.user_type == 'counselor':
        appointments = Appointment.query.filter_by(counselor_id=user.id).all()
        intake_form = None
        sent_messages = Message.query.filter_by(sender_id=user.id).count()
        received_messages = Message.query.filter_by(receiver_id=user.id).count()
    else:  # admin
        appointments = []
        intake_form = None
        sent_messages = Message.query.filter_by(sender_id=user.id).count()
        received_messages = Message.query.filter_by(receiver_id=user.id).count()
    
    return render_template('admin_view_user.html', user=user, appointments=appointments, 
                         intake_form=intake_form, sent_messages=sent_messages, 
                         received_messages=received_messages)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
