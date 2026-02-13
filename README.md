# DV Report Management System

A professional Django-based Diminished Value Report Management System with automated PDF generation, approval workflow (WAD system), duplicate prevention, and full admin lifecycle control.

This system allows users and administrators to create, review, approve, reject, and manage vehicle diminished value reports in a structured workflow.

---

## Overview

The DV Report Management System provides a complete solution for managing diminished value reports including:

* Report creation
* Automatic PDF generation
* Approval workflow
* Admin review and control
* Duplicate prevention
* Secure file storage
* Soft delete functionality

---

## Features

### Core Features

* Create diminished value reports
* Automatic PDF generation using ReportLab
* Professional report format
* Secure database storage
* Admin management interface

### Workflow Features (WAD System)

* Draft status
* Waiting for Approval
* Approved status
* Rejected status
* Soft Delete functionality
* Admin-controlled lifecycle

### Data Integrity

* Duplicate report prevention
* Strict field validation
* Unique report number generation
* Safe file handling using Django FileField

### File Management

* Automatic PDF storage
* Organized media structure
* Admin download support

---

## Tech Stack

**Backend**

* Python 3.9+
* Django 4.x

**Frontend**

* HTML5
* Bootstrap 5
* JavaScript

**PDF Generation**

* ReportLab

**Database**

* SQLite (default)
* PostgreSQL (recommended for production)

**File Storage**

* Django FileField
* Local media storage

---

## Project Structure

```
dv-report-management-system/
│
├── documents/
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   │   └── documents/
│   │       └── home.html
│   └── static/
│       └── documents/
│           ├── header.png
│           └── signature.png
│
├── media/
│   └── dv_reports/
│
├── project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── db.sqlite3
├── manage.py
└── README.md
```

---

## Installation Guide

### Step 1: Clone Repository

```
git clone https://github.com/yourusername/dv-report-management-system.git
cd dv-report-management-system
```

### Step 2: Create Virtual Environment

**Windows**

```
python -m venv venv
venv\Scripts\activate
```

**Linux / Mac**

```
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```
pip install django reportlab
```

### Step 4: Apply Database Migrations

```
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Admin User

```
python manage.py createsuperuser
```

### Step 6: Run Server

```
python manage.py runserver
```

Open browser:

User Interface

```
http://127.0.0.1:8000/
```

Admin Panel

```
http://127.0.0.1:8000/admin/
```

---

## Workflow System (WAD)

The system follows a structured workflow:

1. Report Created
2. Status → Waiting for Approval
3. Admin reviews report
4. Admin can:

   * Approve
   * Reject
   * Soft delete

---

## Status Definitions

| Status   | Description             |
| -------- | ----------------------- |
| Draft    | Initial state           |
| Waiting  | Awaiting admin approval |
| Approved | Final approved report   |
| Rejected | Rejected by admin       |
| Deleted  | Soft deleted            |

---

## PDF Storage

Generated PDFs are stored in:

```
media/dv_reports/
```

Example:

```
media/dv_reports/DV-2026-000001.pdf
```

---

## Duplicate Prevention

System prevents duplicates using:

* Claim Number
* VIN

If duplicate exists, system updates existing record instead of creating a new one.

---

## Admin Capabilities

Admin can:

* View reports
* Approve reports
* Reject reports
* Soft delete reports
* Download PDF reports
* Search reports
* Filter reports
* Manage report lifecycle

---

## Security Features

* Django ORM protection
* FileField secure storage
* Soft delete protection
* Admin access control
* Validation using full_clean()

---

## Production Deployment Recommendations

Recommended production stack:

* PostgreSQL database
* Gunicorn
* Nginx
* Linux server
* HTTPS enabled

---

## Future Improvements

Potential enhancements:

* Email notification system
* User roles and permissions
* REST API integration
* Audit logs
* Dashboard analytics
* Cloud storage integration (AWS S3, Azure Blob)

---

## Requirements

Minimum:

* Python 3.9+
* Django 4+
* ReportLab

Recommended:

* Python 3.11+
* PostgreSQL
* Linux server

---

## Author

Sagnik Sen

---

## License

MIT License

This project is open source and free to use.

---

## Version

Current Version: 1.0.0
Stable Production Release
