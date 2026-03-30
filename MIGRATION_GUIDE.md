# Migration Guide for Updated Authentication System

## Changes Made:

1. **Organization Model Updated:**
   - Added `full_name` field (CharField, max_length=255)
   - Made `email` field unique
   - Made `phone` field unique and required
   - Changed `USERNAME_FIELD` to 'email' for authentication

2. **Registration Form Updated:**
   - Removed `username` field from user input
   - Added `full_name` field
   - Email and phone validation for uniqueness
   - Auto-generates username from email

3. **Login System:**
   - Now uses email instead of username
   - Custom authentication backend added

4. **UI Updates:**
   - Modern, premium design for both login and register pages
   - Professional indigo color scheme
   - Split-screen layout with animations
   - All text in English

## Migration Steps:

### Step 1: Backup your database
```bash
cp db.sqlite3 db.sqlite3.backup
```

### Step 2: Create migrations
```bash
python manage.py makemigrations organizations
```

### Step 3: Apply migrations
```bash
python manage.py migrate
```

### Step 4: Update existing users (if any)
If you have existing users, you'll need to update them manually:

```bash
python manage.py shell
```

Then in the Python shell:
```python
from organizations.models import Organization

# Update existing organizations
for org in Organization.objects.all():
    if not org.full_name:
        org.full_name = org.organization_name
    if not org.email or '@' not in org.email:
        org.email = f"{org.username}@example.com"
    if not org.phone:
        org.phone = f"+998901234567{org.id}"
    org.save()
```

### Step 5: Create superuser (if needed)
```bash
python manage.py createsuperuser
```
Note: You'll be prompted for email (not username)

### Step 6: Run the development server
```bash
python manage.py runserver
```

### Step 7: Test the system
1. Visit http://127.0.0.1:8000/register/
2. Create a new account with:
   - Full Name
   - Email (must be unique)
   - Phone Number (must be unique)
   - Organization Name
   - Password

3. Login at http://127.0.0.1:8000/login/ using:
   - Email
   - Password

## Troubleshooting:

### If migration fails:
1. Delete the migration files in `organizations/migrations/` (except `__init__.py`)
2. Delete `db.sqlite3`
3. Run migrations again:
```bash
python manage.py makemigrations
python manage.py migrate
```

### If you get "email already exists" error:
Check for duplicate emails in the database and remove them.

### If login doesn't work:
Make sure the custom authentication backend is properly configured in settings.py:
```python
AUTHENTICATION_BACKENDS = [
    'organizations.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]
```

## Notes:
- Email is now the primary authentication field
- Username is auto-generated and not visible to users
- Phone numbers must be unique across all organizations
- Full name is not unique (multiple users can have the same name)
