from django.urls import path
from .views_mvt import (
    submit_exam_view, result_view, results_list_view, 
    analytics_view, export_csv_view
)

urlpatterns = [
    path('submit/', submit_exam_view, name='submit_exam'),
    path('result/<int:pk>/', result_view, name='result_detail'),
    path('results/', results_list_view, name='results_list'),
    path('analytics/', analytics_view, name='analytics'),
    path('export-csv/', export_csv_view, name='export_csv'),
]
