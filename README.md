# Group Project

## Description
This is a Flask-based web application that uses SQLAlchemy for database management. The project includes multiple routes and blueprints for modularity and scalability.

## Features
- **Flask Framework**: Backend development.
- **SQLAlchemy**: Database ORM for managing MySQL.
- **Flask-CORS**: Cross-Origin Resource Sharing support.
- **Blueprints**: Modular route organization.

## Prerequisites
- Python 3.10+
- MySQL installed and running locally.
- `pip` for managing Python packages.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd project

### 2. Create a Virtual Environment
```bash
python -m venv venv

### 3. Activate the Virtual Environment
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```
### 4. Install Dependencies
```bash
pip install -r requirements.txt
```
### 5. Configure Database
Make sure MySQL is running and create a database named `Group_Project`. Update the database URI in `app.py` if necessary.
If you don't have the DB running you need to first run the create tables script and all of the mock data scripts within DBeaver or MYSQLWorkbench

### 6. Run the Application
```bash
python app.py
```
### 7. Access the Application
Open your web browser and navigate to `http://localhost:5000` to access the application.

### 8. Test DB Connection
You can test the database connection by navigating to `http://localhost:5000/test_db` in your web browser. This route will attempt to connect to the MySQL database and return a success message if the connection is successful.

## Team Workflow

### Working on Features

1. **Always pull latest changes before starting work:**
   ```bash
   git pull origin main
   ```

2. **Create a new branch for your feature:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes and test them**

4. **Commit with clear messages:**
   ```bash
   git add .
   git commit -m "Add workout builder form component"
   ```

5. **Push your branch:**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** for team review
