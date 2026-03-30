from django.urls import path
from .views import check_student_by_phone

urlpatterns = [
    path('api/check-phone/', check_student_by_phone, name='check_student_phone'),
]
