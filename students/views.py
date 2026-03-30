from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Student


@require_http_methods(["GET"])
def check_student_by_phone(request):
    """Check if student exists by phone number and return their data"""
    phone = request.GET.get('phone', '').strip()
    
    if not phone:
        return JsonResponse({'exists': False})
    
    try:
        # Find the most recent student with this phone number
        student = Student.objects.filter(phone=phone).order_by('-created_at').first()
        
        if student:
            return JsonResponse({
                'exists': True,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'telegram_username': student.telegram_username or '',
                'email': student.email or '',
                'student_type': student.student_type,
                'teacher_id': student.teacher.id if student.teacher else None
            })
        else:
            return JsonResponse({'exists': False})
    except Exception as e:
        return JsonResponse({'exists': False, 'error': str(e)})
