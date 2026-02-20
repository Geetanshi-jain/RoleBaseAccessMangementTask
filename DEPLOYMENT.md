# Deployment Guide: Task Management Project

This document provides instructions on how to deploy this Django application to a production environment.

## 1. Prerequisites
- Python 3.10+
- `pip` (Python package manager)
- A hosting provider (e.g., PythonAnywhere, Render, Railway, or Heroku)
- A domain name (optional)

## 2. Configuration for Production

### Environment Variables
For security, do **not** hardcode sensitive information. Create a `.env` file in the project root:
```env
DEBUG=False
SECRET_KEY=your-very-secret-key-here
EMAIL_HOST_PASSWORD=your-app-password
ALLOWED_HOSTS=your-domain.com,your-app.herokuapp.com
```

### Static Files
Ensure `whitenoise` is installed and configured in `settings.py` to serve static files efficiently.
1. Install: `pip install whitenoise`
2. Add to `MIDDLEWARE` (immediately after `SecurityMiddleware`):
   ```python
   'whitenoise.middleware.WhiteNoiseMiddleware',
   ```

## 3. Deployment Options

### Option A: PythonAnywhere (Recommended for Beginners)
1. **Upload Code**: Upload your project files or `git clone` them into your PythonAnywhere account.
2. **Virtualenv**: Create a virtualenv and install dependencies:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 my-virtualenv
   pip install -r requirements.txt
   ```
3. **Web Tab**:
   - Set the Source code and Working directory.
   - Set the Virtualenv path.
   - Edit the WSGI configuration file to point to your `task_management.wsgi` application.
4. **Database & Static**:
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```

### Option B: Render (Highly Recommended)
1. **Connect Repository**: Connect your GitHub/GitLab repository to Render.
2. **New Web Service**: Select "Web Service".
3. **Environment Settings**:
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn task_management.wsgi`
4. **Environment Variables**: Add the following in the Render dashboard:
   - `DEBUG`: `False`
   - `SECRET_KEY`: (Generate a new secure key)
   - `PYTHON_VERSION`: `3.10.x` (or your version)
   - `EMAIL_HOST_PASSWORD`: (Your Gmail App Password)
5. **Database (SQLite)**: 
   > [!WARNING]
   > SQLite on Render is transient. Every time the service restarts, data is reset. To keep data, adding a **Persistent Disk** to your service is required (e.g., Mount Path: `/data`, and change `settings.py` DB path to `/data/db.sqlite3`).

## 4. Post-Deployment Checklist
- [ ] Ensure `DEBUG = False` in production.
- [ ] Check if email notifications are working (Gmail SMTP).
- [ ] Verify that styles (CSS) are loading correctly (Static files).
- [ ] Change the `SECRET_KEY` to something unique.

---
**Note**: This project currently uses SQLite. For high-traffic production, it is highly recommended to migrate to PostgreSQL.
