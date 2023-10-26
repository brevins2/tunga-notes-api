from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAllNotes),
    path('<int:pk>/', views.getSingleNotes),
    path('export-pdf', views.export_pdf),
    path('export-csv', views.download_csv),
    path('add/', views.createNotes),
    path('delete/<int:notes_id>', views.deleteSingleNotes),
    path('update/<int:notes_id>/', views.updateSingleNotes, name='update-single-notes'),
    path('download/csv/', views.download_csv, name='download_csv'),
    path('categorysearch/', views.unfinnishedNotes, name='unfinished_notes'),
    path('reverseorder/', views.getReversNotes)
]