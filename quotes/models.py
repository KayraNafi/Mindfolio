from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from core.models import Tag


class Quote(models.Model):
    """Quote model for storing quotes from books"""

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='quotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quotes')
    quote_text = models.TextField()
    page_number = models.IntegerField(null=True, blank=True)
    my_comment = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, related_name='quotes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.quote_text[:50]}..." if len(self.quote_text) > 50 else self.quote_text
