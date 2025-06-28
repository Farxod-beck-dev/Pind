from django.urls import path
from . import views

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('create/', views.note_create, name='note_create'),
    path('update/<int:pk>/', views.note_update, name='note_update'),
    path('delete/<int:pk>/', views.note_delete, name='note_delete'),
    path('note/<int:pk>/', views.note_detail, name='note_detail'),
    path('notes/<int:note_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('search/', views.search_notes, name='search_notes'),

]
