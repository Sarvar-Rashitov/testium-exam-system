# IELTS Mock Exam Platform - Django MVT

Production-ready IELTS mock exam platform built with Django MVT (Model-View-Template) architecture.

## 🎯 Features

### For Organizations (Admin)
- ✅ Secure registration and authentication
- ✅ Create, edit, and delete exams
- ✅ 4 question types (Multiple Choice, Writing, Listening, Reading)
- ✅ Generate unique exam links with expiration and usage limits
- ✅ View comprehensive analytics and student results
- ✅ Export results to CSV
- ✅ Automatic IELTS band score calculation

### For Students (No Registration Required)
- ✅ Access exams via unique links
- ✅ Simple registration form before exam
- ✅ Timed exams with auto-submit
- ✅ View results immediately after completion
- ✅ Tab switch tracking (anti-cheat)

## 🛠️ Tech Stack

- **Backend**: Django 5.0 (MVT Architecture)
- **Frontend**: Bootstrap 5 + Vanilla JavaScript
- **Database**: SQLite3 (development)
- **Authentication**: Django Session Authentication
- **Deployment**: Gunicorn + Nginx

## 📦 Quick Start

### 1. Clone and Setup

```bash
# Clone repository
git clone <repository-url>
cd ielts-exam-system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 3. Run Development Server

```bash
python manage.py runserver
```

Visit:
- **Main**: http://localhost:8000/
- **Login**: http://localhost:8000/login/
- **Admin**: http://localhost:8000/admin/

## 📚 Usage Guide

### Admin Workflow

1. **Register/Login**: Create organization account
2. **Create Exam**: Add title, description, duration
3. **Add Questions**: Choose from 4 question types
4. **Generate Link**: Create unique link with expiration
5. **Share Link**: Send to students
6. **View Results**: Check analytics and export CSV

### Student Workflow

1. **Open Link**: Access exam via unique URL
2. **Register**: Fill in name, phone, telegram
3. **Take Exam**: Answer questions with timer
4. **Submit**: Automatic or manual submission
5. **View Result**: See score and IELTS band

## 🎨 Question Types

1. **Multiple Choice**: A, B, C, D options with auto-grading
2. **Writing**: Text input for essays (manual review)
3. **Listening**: Audio URL with MCQ answers
4. **Reading**: Text-based questions with MCQ

## 📊 IELTS Band Score

Automatic calculation based on percentage:

| Percentage | Band Score |
|------------|------------|
| 90-100%    | 9.0        |
| 80-89%     | 8.0        |
| 70-79%     | 7.0        |
| 60-69%     | 6.0        |
| 50-59%     | 5.0        |
| 40-49%     | 4.0        |
| 30-39%     | 3.0        |
| 20-29%     | 2.0        |
| 10-19%     | 1.0        |
| 0-9%       | 0.0        |

## 🔐 Security Features

- Password hashing (bcrypt)
- CSRF protection
- XSS protection
- SQL injection protection (Django ORM)
- Session authentication
- Input validation
- Tab switch tracking
- Copy-paste disabled during exam

## 📁 Project Structure

```
ielts-exam-system/
├── organizations/          # Organization management
├── exams/                 # Exam and question management
├── students/              # Student registration
├── results/               # Results and analytics
├── templates/             # HTML templates
├── static/                # CSS, JavaScript
├── ielts_platform/        # Main project settings
├── db.sqlite3             # SQLite database
├── manage.py              # Django CLI
└── requirements.txt       # Python dependencies
```

## 🚀 Production Deployment

### 1. Update Settings

```env
DEBUG=False
SECRET_KEY=your-strong-secret-key
ALLOWED_HOSTS=yourdomain.com
```

### 2. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 3. Run with Gunicorn

```bash
gunicorn ielts_platform.wsgi:application --bind 0.0.0.0:8000
```

## 📝 License

MIT License

## 👥 Support

For issues and questions, please open an issue on GitHub.

## 🎉 Ready to Use!

The platform is fully functional with:
- ✅ Complete CRUD operations
- ✅ 4 question types
- ✅ Automatic grading
- ✅ Analytics and statistics
- ✅ CSV export
- ✅ Responsive design
- ✅ Anti-cheat features

**Good luck with your IELTS mock exams! 🚀**
