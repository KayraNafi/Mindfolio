from django import forms
from .models import Book, BookFile
from notes.models import Note
from quotes.models import Quote
from core.models import Tag


class BookForm(forms.ModelForm):
    """Form for creating/editing books"""
    author_name = forms.CharField(
        max_length=300,
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Author name'}),
        label='Author',
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Book
        fields = [
            'title', 'publication_year', 'status',
            'overall_rating', 'started_at', 'finished_at',
            'cover_image', 'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Book title'}),
            'publication_year': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'YYYY'}),
            'status': forms.Select(attrs={'class': 'select'}),
            'overall_rating': forms.NumberInput(attrs={'class': 'input', 'min': '0.5', 'max': '5', 'step': '0.5'}),
            'started_at': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'finished_at': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'cover_image': forms.FileInput(attrs={'class': 'input', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['tags'].queryset = Tag.objects.filter(user=self.user)
        author_initial = ''
        if self.instance and getattr(self.instance, 'author_id', None):
            author_initial = self.instance.author.name
        self.fields['author_name'].initial = author_initial
        self.fields['status'].widget.attrs.update({
            'x-model': 'status',
            '@change': 'handleStatusChange($event.target.value)'
        })
        self.fields['started_at'].widget.attrs.update({
            'x-ref': 'startedInput',
            ':disabled': "status === 'TO_READ'"
        })
        self.fields['finished_at'].widget.attrs.update({
            'x-ref': 'finishedInput',
            ':disabled': "status !== 'FINISHED'"
        })
        self.fields['author_name'].widget.attrs.setdefault('list', 'author-suggestions')

    def _get_author_instance(self, name):
        if not self.user or not name:
            return None
        from .models import Author
        normalized = name.strip()
        if not normalized:
            return None
        author = Author.objects.filter(user=self.user, name__iexact=normalized).first()
        if not author:
            author = Author.objects.create(user=self.user, name=normalized)
        return author

    def save(self, commit=True):
        author_name = self.cleaned_data.get('author_name', '').strip()
        instance = super().save(commit=False)
        author = self._get_author_instance(author_name)
        if author:
            instance.author = author
        if commit:
            instance.save()
            self.save_m2m()
        return instance


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
