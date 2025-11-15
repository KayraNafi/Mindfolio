from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'note_type', 'book', 'user', 'created_at']
    list_filter = ['note_type', 'user', 'created_at']
    search_fields = ['title', 'body', 'book__title']
