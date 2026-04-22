# FOCUS Counseling Platform

A Christ-centered online counseling platform for the FOCUS Ministry Counseling Team at Addis Ababa Christian Fellowship Students.

## Features

- **User Authentication**: Secure login system for students and counselors
- **Appointment Booking**: Schedule counseling sessions online
- **Digital Intake Forms**: Complete counseling intake forms digitally
- **Secure Messaging**: Private messaging between students and counselors
- **SOAP Notes**: Digital SOAP note documentation for counselors
- **Mobile Responsive**: Works on both desktop and mobile devices
- **Ngrok Integration**: Public access for testing and remote access

## Quick Start

### Prerequisites

1. Python 3.7 or higher
2. ngrok account and authtoken (for public access)

### Setup Instructions

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup ngrok** (if you want public access)
   ```bash
   # Download ngrok from https://ngrok.com/download
   # Extract and add to PATH, or place in this directory
   
   # Authenticate with your authtoken
   ngrok authtoken YOUR_AUTH_TOKEN
   ```

3. **Run the Platform**
   ```bash
   python start_with_ngrok.py
   ```

   This will:
   - Install required packages
   - Start the Flask application
   - Create an ngrok tunnel for public access
   - Create sample user accounts for testing

### Test Accounts

After starting the platform, you can login with these test accounts:

**Counselor Account:**
- Username: `counselor1`
- Password: `counselor123`

**Student Account:**
- Username: `student1`
- Password: `student123`

## Manual Setup

If you prefer to run without the startup script:

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Database**
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

3. **Run Flask App**
   ```bash
   python app.py
   ```

4. **Start ngrok Separately** (optional)
   ```bash
   ngrok http 5000
   ```

## Platform Features

### For Students

- **Dashboard**: View appointments and counseling progress
- **Book Appointments**: Schedule sessions with available counselors
- **Intake Forms**: Complete initial counseling assessment
- **Messaging**: Communicate securely with counselors
- **Spiritual Resources**: Access biblical guidance and encouragement

### For Counselors

- **Dashboard**: Manage appointments and view student progress
- **SOAP Notes**: Create and manage session documentation
- **Messaging**: Communicate with students
- **Resource Library**: Access counseling manual and templates
- **Student Management**: View student information and history

## Security Features

- **Password Hashing**: Secure password storage using Werkzeug
- **Session Management**: Secure user sessions
- **Input Validation**: Form validation using WTForms
- **Confidentiality**: Built-in confidentiality guidelines and consent
- **Crisis Support**: Integrated crisis information and resources

## Mobile Access

The platform is fully responsive and works on:
- Desktop browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Android Chrome)
- Tablets (iPad, Android tablets)

When using ngrok, the same URL works on all devices - just share the ngrok URL with users.

## Database Schema

The platform uses SQLite with the following main tables:

- **Users**: Student and counselor accounts
- **Appointments**: Counseling session scheduling
- **Messages**: Secure messaging between users
- **IntakeForms**: Student assessment forms
- **SOAPNotes**: Counselor session documentation

## Configuration

### Environment Variables

You can configure these environment variables:

```bash
export FLASK_SECRET_KEY=your-secret-key
export DATABASE_URL=sqlite:///counseling.db
export FLASK_ENV=development
```

### Customization

- **Styling**: Modify the CSS in `templates/base.html`
- **Forms**: Update form fields in `app.py`
- **Database**: Modify models in `app.py`
- **Features**: Add new routes and templates as needed

## Troubleshooting

### Common Issues

1. **Port 5000 already in use**
   ```bash
   # On Windows
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   
   # On Mac/Linux
   lsof -ti:5000 | xargs kill -9
   ```

2. **ngrok not working**
   - Ensure ngrok is in your PATH or in the same directory
   - Check your authtoken is valid
   - Verify internet connection

3. **Database errors**
   ```bash
   # Reset database
   rm counseling.db
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

4. **Import errors**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

## Development

### Adding New Features

1. Add new routes in `app.py`
2. Create corresponding templates in `templates/`
3. Update database models if needed
4. Test with both user types

### Code Structure

```
Focus/
|-- app.py                 # Main Flask application
|-- start_with_ngrok.py    # Startup script with ngrok
|-- requirements.txt       # Python dependencies
|-- counseling.db         # SQLite database (auto-created)
|-- templates/            # HTML templates
|   |-- base.html        # Base template with styling
|   |-- index.html       # Home page
|   |-- login.html       # Login page
|   |-- register.html    # Registration page
|   |-- student_dashboard.html
|   |-- counselor_dashboard.html
|   |-- book_appointment.html
|   |-- intake_form.html
|   |-- messages.html
|   |-- soap_note.html
```

## Privacy and Confidentiality

This platform is designed with Christian counseling ethics in mind:

- All data is stored securely and confidentially
- Users must consent to counseling terms
- Crisis support information is readily available
- Biblical integration is optional but encouraged
- Professional boundaries are maintained

## Support

For technical support or questions about the platform:

1. Check this README file
2. Review the code comments in `app.py`
3. Test with the provided sample accounts
4. Contact the development team for additional help

## License

This platform is developed for the FOCUS Ministry Counseling Team and follows Christian counseling principles and ethical guidelines.

---

**FOCUS Ministry - Addis Ababa Christian Fellowship Students**  
*Christ-Centered Counseling for Student Growth*
