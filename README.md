# NGO Enterprise System

A modular, enterprise-level web application designed for NGOs to efficiently manage various internal operations and sub-projects. This system includes role-based dashboards, workplace injury claim management, accounting functionalities, and reporting tools.

## 🔧 Technologies Used

- **Backend:** Django (Python)
- **Frontend:** HTML, Bootstrap 5
- **Database:** SQLite (development), PostgreSQL (recommended for production)
- **Authentication:** Django built-in auth system with custom user roles

## 📦 Features

- 🧑‍💼 **Role-based Dashboards**
  - Admin
  - Project Manager
  - Accountant
  - Reporter
  - Staff

- 🧾 **Accounting Module**
  - Expense and income tracking
  - Financial reporting dashboard

- 🚨 **Workplace Injury Claims**
  - Submit, review, and track claims
  - Admin and manager oversight tools

- 📊 **Reports & Analytics**
  - Project-level performance stats
  - Organization-wide summary reports

## 🧰 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/phindulo12/NGO-Enterprise-System.git
cd NGO-Enterprise-System
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

### 6. Create a Superuser

```bash
python manage.py createsuperuser
```

## 🛠️ Future Improvements

- REST API with Django REST Framework
- Real-time notifications and alerts
- Exporting reports (PDF/Excel)
- Multi-language support

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/XYZ`)
3. Commit your changes (`git commit -m 'Add XYZ'`)
4. Push to the branch (`git push origin feature/XYZ`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

---

**Maintainer:** [@phindulo12](https://github.com/phindulo12)
