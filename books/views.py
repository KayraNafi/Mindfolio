from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import FileResponse, HttpResponseForbidden, Http404
from .models import Book, BookFile
from notes.models import Note
from quotes.models import Quote
from core.models import Tag
from .forms import BookForm, BookFileForm, NoteForm, QuoteForm
import mimetypes


@login_required
def library_view(request):
    """Main library/dashboard view with filters and search"""
    books = Book.objects.filter(user=request.user).select_related('user').prefetch_related('tags', 'files')

    # Get filter parameters
    status_filter = request.GET.get('status', '')
    tag_filter = request.GET.get('tag', '')
    rating_filter = request.GET.get('rating', '')
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '-updated_at')

    # Apply status filter
    if status_filter:
        books = books.filter(status=status_filter)

    # Apply tag filter
    if tag_filter:
        books = books.filter(tags__id=tag_filter)

    # Apply rating filter
    if rating_filter:
        books = books.filter(overall_rating__gte=float(rating_filter))

    # Apply search query
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(notes__body__icontains=search_query) |
            Q(quotes__quote_text__icontains=search_query)
        ).distinct()

    # Apply sorting
    valid_sort_fields = ['-updated_at', '-created_at', 'title', 'author', '-overall_rating', '-finished_at']
    if sort_by in valid_sort_fields:
        books = books.order_by(sort_by)
    else:
        books = books.order_by('-updated_at')

    # Get all tags for the filter dropdown
    user_tags = Tag.objects.filter(user=request.user).annotate(book_count=Count('books'))

    # Get statistics
    stats = {
        'total': Book.objects.filter(user=request.user).count(),
        'reading': Book.objects.filter(user=request.user, status='READING').count(),
        'finished': Book.objects.filter(user=request.user, status='FINISHED').count(),
        'to_read': Book.objects.filter(user=request.user, status='TO_READ').count(),
    }

    context = {
        'books': books,
        'tags': user_tags,
        'stats': stats,
        'current_status': status_filter,
        'current_tag': tag_filter,
        'current_rating': rating_filter,
        'search_query': search_query,
        'sort_by': sort_by,
    }

    # If HTMX request, only return the books list partial
    if request.htmx:
        return render(request, 'books/partials/book_list.html', context)

    return render(request, 'books/library.html', context)


@login_required
def book_create(request):
    """Create a new book"""
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(user=request.user)

    return render(request, 'books/book_form.html', {'form': form, 'action': 'Create'})


@login_required
def book_edit(request, pk):
    """Edit an existing book"""
    book = get_object_or_404(Book, pk=pk, user=request.user)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book, user=request.user)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book, user=request.user)

    return render(request, 'books/book_form.html', {'form': form, 'action': 'Edit', 'book': book})


@login_required
def book_delete(request, pk):
    """Delete a book"""
    book = get_object_or_404(Book, pk=pk, user=request.user)

    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" deleted successfully!')
        return redirect('library')

    return render(request, 'books/book_confirm_delete.html', {'book': book})


@login_required
def book_detail(request, pk):
    """Book detail view with tabs for overview, notes, quotes, and files"""
    book = get_object_or_404(
        Book.objects.select_related('user')
        .prefetch_related('tags', 'notes', 'quotes__tags', 'files'),
        pk=pk,
        user=request.user
    )

    # Get the active tab from query params, default to 'notes'
    active_tab = request.GET.get('tab', 'notes')
    if active_tab not in {'notes', 'quotes', 'files'}:
        active_tab = 'notes'

    context = {
        'book': book,
        'active_tab': active_tab,
    }

    return render(request, 'books/book_detail.html', context)


@login_required
def book_file_upload(request, book_id):
    """Upload a file for a book"""
    book = get_object_or_404(Book, pk=book_id, user=request.user)

    if request.method == 'POST':
        form = BookFileForm(request.POST, request.FILES)
        if form.is_valid():
            book_file = form.save(commit=False)
            book_file.book = book
            book_file.save()
            messages.success(request, 'File uploaded successfully!')

            if request.htmx:
                # Return the updated files list
                context = {'book': book}
                return render(request, 'books/partials/file_list.html', context)

            return redirect('book_detail', pk=book.pk)
    else:
        form = BookFileForm()

    context = {'form': form, 'book': book}

    if request.htmx:
        return render(request, 'books/partials/file_upload_form.html', context)

    return render(request, 'books/book_file_upload.html', context)


@login_required
def book_file_delete(request, pk):
    """Delete a book file"""
    book_file = get_object_or_404(BookFile, pk=pk, book__user=request.user)
    book = book_file.book

    if request.method == 'POST':
        book_file.delete()
        messages.success(request, 'File deleted successfully!')

        if request.htmx:
            context = {'book': book}
            return render(request, 'books/partials/file_list.html', context)

        return redirect('book_detail', pk=book.pk)

    context = {'book_file': book_file, 'book': book}
    return render(request, 'books/partials/file_confirm_delete.html', context)


@login_required
def book_file_view(request, pk):
    """View/download a book file"""
    book_file = get_object_or_404(BookFile, pk=pk, book__user=request.user)

    # Security check: ensure the file belongs to the current user
    if book_file.book.user != request.user:
        return HttpResponseForbidden("You don't have permission to access this file.")

    try:
        # Determine the content type
        content_type = book_file.mime_type or mimetypes.guess_type(book_file.file.name)[0] or 'application/octet-stream'

        # For PDFs, render inline. For others, trigger download.
        if content_type == 'application/pdf':
            return render(request, 'books/pdf_viewer.html', {'book_file': book_file, 'book': book_file.book})
        else:
            response = FileResponse(book_file.file.open('rb'), content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename="{book_file.original_filename}"'
            return response
    except FileNotFoundError:
        raise Http404("File not found")


@login_required
def note_create(request, book_id):
    """Create a note for a book"""
    book = get_object_or_404(Book, pk=book_id, user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.book = book
            note.user = request.user
            note.save()
            messages.success(request, 'Note created successfully!')

            if request.htmx:
                context = {'book': book}
                return render(request, 'books/partials/note_list.html', context)

            return redirect('book_detail', pk=book.pk)
    else:
        form = NoteForm()

    context = {'form': form, 'book': book}

    if request.htmx:
        return render(request, 'books/partials/note_form.html', context)

    return render(request, 'books/note_form.html', context)


@login_required
def note_edit(request, pk):
    """Edit a note"""
    note = get_object_or_404(Note, pk=pk, user=request.user)
    book = note.book

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully!')

            if request.htmx:
                context = {'book': book}
                return render(request, 'books/partials/note_list.html', context)

            return redirect('book_detail', pk=book.pk)
    else:
        form = NoteForm(instance=note)

    context = {'form': form, 'note': note, 'book': book}

    if request.htmx:
        return render(request, 'books/partials/note_form.html', context)

    return render(request, 'books/note_form.html', context)


@login_required
def note_delete(request, pk):
    """Delete a note"""
    note = get_object_or_404(Note, pk=pk, user=request.user)
    book = note.book

    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully!')

        if request.htmx:
            context = {'book': book}
            return render(request, 'books/partials/note_list.html', context)

        return redirect('book_detail', pk=book.pk)

    context = {'note': note, 'book': book}
    return render(request, 'books/partials/note_confirm_delete.html', context)


@login_required
def quote_create(request, book_id):
    """Create a quote for a book"""
    book = get_object_or_404(Book, pk=book_id, user=request.user)

    if request.method == 'POST':
        form = QuoteForm(request.POST, user=request.user)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.book = book
            quote.user = request.user
            quote.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Quote created successfully!')

            if request.htmx:
                context = {'book': book}
                return render(request, 'books/partials/quote_list.html', context)

            return redirect('book_detail', pk=book.pk)
    else:
        form = QuoteForm(user=request.user)

    context = {'form': form, 'book': book}

    if request.htmx:
        return render(request, 'books/partials/quote_form.html', context)

    return render(request, 'books/quote_form.html', context)


@login_required
def quote_edit(request, pk):
    """Edit a quote"""
    quote = get_object_or_404(Quote, pk=pk, user=request.user)
    book = quote.book

    if request.method == 'POST':
        form = QuoteForm(request.POST, instance=quote, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quote updated successfully!')

            if request.htmx:
                context = {'book': book}
                return render(request, 'books/partials/quote_list.html', context)

            return redirect('book_detail', pk=book.pk)
    else:
        form = QuoteForm(instance=quote, user=request.user)

    context = {'form': form, 'quote': quote, 'book': book}

    if request.htmx:
        return render(request, 'books/partials/quote_form.html', context)

    return render(request, 'books/quote_form.html', context)


@login_required
def quote_delete(request, pk):
    """Delete a quote"""
    quote = get_object_or_404(Quote, pk=pk, user=request.user)
    book = quote.book

    if request.method == 'POST':
        quote.delete()
        messages.success(request, 'Quote deleted successfully!')

        if request.htmx:
            context = {'book': book}
            return render(request, 'books/partials/quote_list.html', context)

        return redirect('book_detail', pk=book.pk)

    context = {'quote': quote, 'book': book}
    return render(request, 'books/partials/quote_confirm_delete.html', context)
