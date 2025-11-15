from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import Tag
import os


def book_cover_path(instance, filename):
    """Generate upload path for book covers"""
    return f"covers/{instance.user.id}/{filename}"


def book_file_path(instance, filename):
    """Generate upload path for book files"""
    return f"books/{instance.book.user.id}/{instance.book.id}/{filename}"


class Book(models.Model):
    """Book model representing a book in the library"""

    STATUS_CHOICES = [
        ('TO_READ', 'To Read'),
        ('READING', 'Reading'),
        ('FINISHED', 'Finished'),
        ('ABANDONED', 'Abandoned'),
    ]

    FORMAT_CHOICES = [
        ('PDF', 'PDF'),
        ('EPUB', 'EPUB'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=300)
    publication_year = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TO_READ')
    overall_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.5), MaxValueValidator(5.0)]
    )
    started_at = models.DateField(null=True, blank=True)
    finished_at = models.DateField(null=True, blank=True)
    primary_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='PDF')
    cover_image = models.ImageField(upload_to=book_cover_path, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='books', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def notes_count(self):
        return self.notes.count()

    @property
    def quotes_count(self):
        return self.quotes.count()

    @property
    def files_count(self):
        return self.files.count()


class BookFile(models.Model):
    """File attachments for books (PDFs, summaries, mindmaps, etc.)"""

    FILE_TYPE_CHOICES = [
        ('SOURCE_PDF', 'Source PDF'),
        ('SOURCE_EPUB', 'Source EPUB'),
        ('SUMMARY', 'Summary'),
        ('MINDMAP', 'Mindmap'),
        ('OTHER', 'Other'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='files')
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default='OTHER')
    file = models.FileField(upload_to=book_file_path)
    original_filename = models.CharField(max_length=500)
    mime_type = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.get_file_type_display()} - {self.original_filename}"

    def save(self, *args, **kwargs):
        if not self.original_filename and self.file:
            self.original_filename = os.path.basename(self.file.name)
        super().save(*args, **kwargs)
