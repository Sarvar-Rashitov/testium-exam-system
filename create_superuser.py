import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ielts_platform.settings')
django.setup()

from organizations.models import Organization

# Superuser credentials
email = 'admin@testium.uz'
password = 'admin123'
username = 'superadmin'
full_name = 'Super Admin'
organization_name = 'Testium Platform'
phone = '+998901234567'

# Check if user with this email exists
if Organization.objects.filter(email=email).exists():
    print(f"User with email {email} already exists!")
    user = Organization.objects.get(email=email)
    # Make existing user superuser
    user.is_staff = True
    user.is_superuser = True
    user.set_password(password)
    user.save()
    print(f"User updated to superuser!")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Password: {password}")
elif Organization.objects.filter(username=username).exists():
    print(f"User with username {username} already exists!")
    user = Organization.objects.get(username=username)
    # Make existing user superuser
    user.is_staff = True
    user.is_superuser = True
    user.set_password(password)
    user.save()
    print(f"User updated to superuser!")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Password: {password}")
else:
    # Create new superuser
    user = Organization.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        full_name=full_name,
        organization_name=organization_name,
        phone=phone
    )
    
    print("Superuser created successfully!")
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Password: {password}")

print(f"\nYou can now login to Django admin at: http://127.0.0.1:8000/admin/")
print(f"Use username: {user.username} or email: {user.email}")
print(f"Password: {password}")
