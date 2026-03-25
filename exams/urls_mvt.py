from django.urls import path
from .views_mvt import (
    exam_list_view, exam_create_view, exam_detail_view, exam_edit_view, exam_delete_view,
    section_create_view, question_group_create_view, question_group_detail_view,
    question_create_view, question_mcq_single_create_view, question_delete_view,
    generate_link_view, exam_start_view, exam_take_view
)

urlpatterns = [
    # Exam URLs
    path('exams/', exam_list_view, name='exam_list'),
    path('exams/create/', exam_create_view, name='exam_create'),
    path('exams/<int:pk>/', exam_detail_view, name='exam_detail'),
    path('exams/<int:pk>/edit/', exam_edit_view, name='exam_edit'),
    path('exams/<int:pk>/delete/', exam_delete_view, name='exam_delete'),
    
    # Section URLs
    path('exams/<int:exam_pk>/sections/create/', section_create_view, name='section_create'),
    
    # Question Group URLs
    path('sections/<int:section_pk>/groups/create/', question_group_create_view, name='question_group_create'),
    path('groups/<int:pk>/', question_group_detail_view, name='question_group_detail'),
    
    # Question URLs
    path('groups/<int:group_pk>/questions/create/', question_create_view, name='question_create'),
    path('groups/<int:group_pk>/questions/mcq-single/create/', question_mcq_single_create_view, name='question_mcq_single_create'),
    path('questions/<int:pk>/delete/', question_delete_view, name='question_delete'),
    
    # Link URLs
    path('exams/<int:exam_pk>/generate-link/', generate_link_view, name='generate_link'),
    
    # Public URLs
    path('start/<uuid:token>/', exam_start_view, name='exam_start'),
    path('take/<uuid:token>/<int:student_id>/', exam_take_view, name='exam_take'),
]
