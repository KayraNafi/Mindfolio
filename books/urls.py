from django.urls import path
from . import views

urlpatterns = [
    # Library/Dashboard
    path('', views.library_view, name='library'),

    # Book CRUD
    path('book/create/', views.book_create, name='book_create'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),

    # Book file operations
    path('book/<int:book_id>/file/upload/', views.book_file_upload, name='book_file_upload'),
    path('file/<int:pk>/delete/', views.book_file_delete, name='book_file_delete'),
    path('file/<int:pk>/view/', views.book_file_view, name='book_file_view'),

    # Note operations
    path('book/<int:book_id>/note/create/', views.note_create, name='note_create'),
    path('note/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('note/<int:pk>/delete/', views.note_delete, name='note_delete'),

    # Quote operations (on book detail page)
    path('book/<int:book_id>/quote/create/', views.quote_create, name='quote_create'),
    path('quote/<int:pk>/edit/', views.quote_edit, name='quote_edit'),
    path('quote/<int:pk>/delete/', views.quote_delete, name='quote_delete'),
]
