from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAllNotes),
    path('<int:pk>/', views.getSingleNotes),
    path('add/', views.createNotes),
    path('delete/<int:notes_id>', views.deleteSingleNotes),
    path('update/<int:notes_id>/', views.updateSingleNotes, name='update-single-notes')
]