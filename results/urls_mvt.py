from django.urls import path
from .views_mvt import (
    submit_exam_view, result_view, results_list_view, 
    analytics_view, export_csv_view, export_excel_view, 
    export_word_view, export_pdf_view, download_certificate_view
)

urlpatterns = [
    path('submit/', submit_exam_view, name='submit_exam'),
    path('<int:pk>/', result_view, name='result_detail'),
    path('<int:pk>/certificate/', download_certificate_view, name='download_certificate'),
    path('', results_list_view, name='results_list'),
    path('analytics/', analytics_view, name='analytics'),
    path('export-csv/', export_csv_view, name='export_csv'),
    path('export-excel/', export_excel_view, name='export_excel'),
    path('export-word/', export_word_view, name='export_word'),
    path('export-pdf/', export_pdf_view, name='export_pdf'),
]
