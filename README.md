# 📝 Django Enrollment System

A lightweight **student enrollment management system** built with Django, designed to mimic real university operations.
It supports **students, teachers, registrars, departments, programs, courses, sections, and enrollments** with realistic relationships.
The system includes role-based permissions, GPA and grade tracking, and can **automatically populate the database with realistic sample data** using `manage.py populate`.

## 🚀 Quick Start

### Prerequisites

* Python 3.8+
* Git

### Installation

```bash
# 1. Clone repository
git clone https://github.com/yourusername/enrollment-system.git
cd enrollment-system

# 2. Create virtual environment
python -m venv venv

# 3. Activate environment
# Linux/Mac:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate

# 4. Install Faker for realistic data population
pip install Faker

# images
pip install Pillow 

# 5. Setup database
python manage.py migrate

# 6. Create admin account
python manage.py createsuperuser

# 7. (Optional) Populate database with realistic sample data
python manage.py populate

# 8. Run development server
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## ✨ Key Features

| Feature                           | Description                                                                          |
| --------------------------------- | ------------------------------------------------------------------------------------ |
| 👨‍💼 **User Roles**              | Admin, Teacher, Registrar, and Student access levels with automatic group assignment |
| 📚 **Course Management**          | Create and manage courses, prerequisites, programs, and curricula                    |
| 🎓 **Enrollment System**          | Student registration, section management, and grade tracking                         |
| 🧑‍🏫 **Teacher & Advisor Roles** | Teachers can manage sections and advise students                                     |
| 📊 **Admin Dashboard**            | Centralized interface for departments, programs, and user management                 |
| 🔄 **Database Population**        | `manage.py populate` can reset and fill the database with realistic sample data      |

## 🛠️ Technologies

* Python & Django
* Django ORM with relational models
* PostgreSQL / SQLite (configurable)
* Bootstrap / Tailwind (optional for UI)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

