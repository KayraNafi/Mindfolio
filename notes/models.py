from django.db import models
from django.contrib.auth.models import User
from books.models import Book


class Note(models.Model):
    """Note model for storing summaries, reflections, and general notes about books"""

    NOTE_TYPE_CHOICES = [
        ('SUMMARY', 'Summary'),
        ('REFLECTION', 'Reflection'),
        ('GENERAL', 'General'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    note_type = models.CharField(max_length=20, choices=NOTE_TYPE_CHOICES, default='GENERAL')
    title = models.CharField(max_length=300, blank=True)
    body = models.TextField()
    page_start = models.IntegerField(null=True, blank=True)
    page_end = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_note_type_display()}: {self.title or self.body[:50]}"
