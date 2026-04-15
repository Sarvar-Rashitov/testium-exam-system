from django.urls import path
from .views_mvt import (
    auth_view, register_view, login_view, logout_view, dashboard_view,
    teacher_list_view, teacher_create_view, teacher_edit_view, teacher_delete_view,
    teacher_statistics_view,
    group_list_view, group_create_view, group_detail_view, group_edit_view, group_delete_view
)
from .views_settings import (
    settings_view, update_profile_view, update_settings_view, change_password_view
)

urlpatterns = [
    path('auth/', auth_view, name='auth'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # Teacher URLs
    path('teachers/', teacher_list_view, name='teacher_list'),
    path('teachers/create/', teacher_create_view, name='teacher_create'),
    path('teachers/<int:pk>/edit/', teacher_edit_view, name='teacher_edit'),
    path('teachers/<int:pk>/delete/', teacher_delete_view, name='teacher_delete'),
    path('teachers/statistics/', teacher_statistics_view, name='teacher_statistics'),
    
    # Group URLs
    path('groups/', group_list_view, name='group_list'),
    path('groups/create/', group_create_view, name='group_create'),
    path('groups/<int:pk>/', group_detail_view, name='group_detail'),
    path('groups/<int:pk>/edit/', group_edit_view, name='group_edit'),
    path('groups/<int:pk>/delete/', group_delete_view, name='group_delete'),
    
    # Settings URLs
    path('settings/', settings_view, name='settings'),
    path('settings/profile/update/', update_profile_view, name='update_profile'),
    path('settings/update/', update_settings_view, name='update_settings'),
    path('settings/password/change/', change_password_view, name='change_password'),
]
