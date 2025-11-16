from django.contrib import admin
from .models import Book, BookFile, Author


class BookFileInline(admin.TabularInline):
    model = BookFile
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'overall_rating', 'user', 'created_at']
    list_filter = ['status', 'user', 'created_at']
    search_fields = ['title', 'author__name']
    filter_horizontal = ['tags']
    inlines = [BookFileInline]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at']
    search_fields = ['name', 'user__username']


@admin.register(BookFile)
class BookFileAdmin(admin.ModelAdmin):
    list_display = ['book', 'file_type', 'original_filename', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at']
    search_fields = ['original_filename', 'book__title']
