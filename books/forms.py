from django import forms
from .models import Book, BookFile
from notes.models import Note
from quotes.models import Quote
from core.models import Tag


class BookForm(forms.ModelForm):
    """Form for creating/editing books"""
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Book
        fields = [
            'title', 'author', 'publication_year', 'status',
            'overall_rating', 'started_at', 'finished_at',
            'primary_format', 'cover_image', 'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Book title'}),
            'author': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Author name'}),
            'publication_year': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'YYYY'}),
            'status': forms.Select(attrs={'class': 'select'}),
            'overall_rating': forms.NumberInput(attrs={'class': 'input', 'min': '0.5', 'max': '5', 'step': '0.5'}),
            'started_at': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'finished_at': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'primary_format': forms.Select(attrs={'class': 'select'}),
            'cover_image': forms.FileInput(attrs={'class': 'input', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['tags'].queryset = Tag.objects.filter(user=user)


class BookFileForm(forms.ModelForm):
    """Form for uploading book files"""
    class Meta:
        model = BookFile
        fields = ['file_type', 'file']
        widgets = {
            'file_type': forms.Select(attrs={'class': 'select'}),
            'file': forms.FileInput(attrs={'class': 'input'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('file'):
            import mimetypes
            instance.mime_type = mimetypes.guess_type(self.cleaned_data['file'].name)[0] or ''
        if commit:
            instance.save()
        return instance


class NoteForm(forms.ModelForm):
    """Form for creating/editing notes"""
    class Meta:
        model = Note
        fields = ['note_type', 'title', 'body', 'page_start', 'page_end']
        widgets = {
            'note_type': forms.Select(attrs={'class': 'select'}),
            'title': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Note title (optional)'}),
            'body': forms.Textarea(attrs={'class': 'textarea', 'rows': 6, 'placeholder': 'Write your note here...'}),
            'page_start': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Start page'}),
            'page_end': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'End page'}),
        }


class QuoteForm(forms.ModelForm):
    """Form for creating/editing quotes"""
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Quote
        fields = ['quote_text', 'page_number', 'my_comment', 'tags']
        widgets = {
            'quote_text': forms.Textarea(attrs={'class': 'textarea', 'rows': 4, 'placeholder': 'Enter the quote...'}),
            'page_number': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Page number'}),
            'my_comment': forms.Textarea(attrs={'class': 'textarea', 'rows': 3, 'placeholder': 'Your thoughts on this quote (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['tags'].queryset = Tag.objects.filter(user=user)
