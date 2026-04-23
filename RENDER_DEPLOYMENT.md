# FOCUS Counseling Platform - Render Deployment Guide

## 🚀 Render Deployment Configuration

This platform is configured for deployment on Render with PostgreSQL database.

### 📋 Files Created for Render Deployment:

1. **`app_render.py`** - Production-ready Flask application
2. **`render.yaml`** - Render service configuration
3. **`.env.example`** - Environment variables template
4. **Updated `app.py`** - PostgreSQL support
5. **Updated `requirements.txt`** - psycopg2-binary added

### 🔧 Render Configuration Details:

#### Python Version
- **Specified**: Python 3.11.7
- **Location**: `render.yaml` > `envVars`

#### Application Entry Point
- **File**: `app_render.py` (not `app.py`)
- **Command**: `python app_render.py`
- **Location**: `render.yaml` > `startCommand`

#### Database Configuration
- **Type**: PostgreSQL (cloud-hosted)
- **Provider**: Render Database Service
- **Auto-provisioned**: Yes
- **Connection**: Via `DATABASE_URL` environment variable

### 🗄️ Database Setup:

#### Production (Render)
```yaml
- type: postgres
  name: focus-db
  plan: free
```

#### Environment Variables
- `DATABASE_URL` - Automatically set by Render
- `PYTHON_VERSION` - Set to 3.11.7
- `FLASK_ENV` - Set to production

### 📦 Requirements Update:
```
psycopg2-binary==2.9.7  # Added for PostgreSQL support
```

### 🚀 Deployment Steps:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Configure for Render deployment"
   git push origin master
   ```

2. **Connect to Render**
   - Go to [render.com](https://render.com)
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`

3. **Automatic Setup**
   - Render creates PostgreSQL database
   - Sets `DATABASE_URL` environment variable
   - Deploys using Python 3.11.7
   - Runs `app_render.py` as entry point

### 🔍 Database Detection Logic:

```python
# app.py - Automatic database detection
if os.environ.get('DATABASE_URL'):
    # Production: PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    # Development: SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///counseling.db'
```

### ✅ Expected Results:

1. **Python 3.11.7** ✅ (not 3.14)
2. **Runs app_render.py** ✅ (not app.py)
3. **PostgreSQL database** ✅ (from .env/DATABASE_URL)
4. **Deploy successfully** ✅ (no SQLAlchemy errors)

### 🌐 Production Features:

- **24/7 Availability**: Render's cloud infrastructure
- **Automatic SSL**: HTTPS provided by default
- **Custom Domain**: Optional domain configuration
- **Environment Management**: Secure variable handling
- **Database Backups**: Automatic PostgreSQL backups

### 📊 Admin Access:

Once deployed:
- **URL**: `https://your-app.onrender.com`
- **Admin Login**: `admin` / `admin123`
- **Dashboard**: `/admin`

### 🔧 Local Development:

For local testing with SQLite:
```bash
python app.py
```

For local testing with PostgreSQL:
```bash
# Set DATABASE_URL to your local PostgreSQL
export DATABASE_URL="postgresql://user:pass@localhost/dbname"
python app_render.py
```

### 📝 Notes:

- Render automatically provisions PostgreSQL database
- No need to manually set `DATABASE_URL` in production
- Application automatically detects environment
- Sample data created on first deployment
- Admin user created automatically
