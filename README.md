
# File Share App

This is a Django-based file-sharing application that supports two types of users: **Operation Users** and **Client Users**, each with specific functionalities for secure and seamless file sharing.

## User Roles

### 1. Operation User
Operation Users have the following capabilities:

- Login
- Upload Files (Only `.pptx`, `.docx`, and `.xlsx` formats are allowed)

*Note: Only Operation Users can upload files, and only files of the specified formats (pptx, docx, xlsx) are accepted.*

### 2. Client User
Client Users have the following capabilities:

- Sign Up (Returns an encrypted URL)
- Email Verification (A verification email will be sent to the registered email)
- Login
- Download Files
- List all Uploaded Files

## Features

- Role-based access control for file uploads and downloads.
- Secure file sharing with encrypted links and email verification.
- Simple database management with Django ORM.
- Scalable and ready for containerization.

## Prerequisites

Ensure you have the following installed:

- Python 3.8+
- Django 4.x
- SQLite (default) 

## Installation

Clone this repository and navigate to the project directory:

```bash
git clone <repository-url>
cd <project-directory>
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Database Setup

Apply migrations to create the necessary tables in the database:

```bash
python manage.py makemigrations FilesApp
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixtures/groups.json
```

## Running the Server

Start the development server:

```bash
python manage.py runserver 0.0.0.0:8000
```

Access the app at [http://localhost:8000](http://localhost:8000).

## Configuration

- Update settings in `settings.py` for database, allowed hosts, and other configurations.
- By default, the app uses SQLite. To switch to PostgreSQL, update `DATABASES` in `settings.py`.

## Usage

1. Operation User logs in and uploads files (pptx, docx, xlsx).
2. Client User signs up and receives an encrypted URL for email verification.
3. Client User verifies their email, logs in, and can download files or list all uploaded files.

## Troubleshooting

- If you encounter migration issues, try:

  ```bash
  python manage.py makemigrations --merge
  python manage.py migrate --run-syncdb
  ```

- To create a superuser for admin access:

  ```bash
  python manage.py createsuperuser
  ```

