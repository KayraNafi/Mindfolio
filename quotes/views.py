from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Quote
from books.models import Book
from core.models import Tag


@login_required
def quotes_list(request):
    """Global quotes page with filtering and search"""
    quotes = Quote.objects.filter(user=request.user).select_related('book', 'user').prefetch_related('tags')

    # Get filter parameters
    book_filter = request.GET.get('book', '')
    tag_filter = request.GET.get('tag', '')
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '-created_at')

    # Apply book filter
    if book_filter:
        quotes = quotes.filter(book__id=book_filter)

    # Apply tag filter
    if tag_filter:
        quotes = quotes.filter(tags__id=tag_filter)

    # Apply search query
    if search_query:
        quotes = quotes.filter(
            Q(quote_text__icontains=search_query) |
            Q(my_comment__icontains=search_query) |
            Q(book__title__icontains=search_query) |
            Q(book__author__icontains=search_query)
        ).distinct()

    # Apply sorting
    valid_sort_fields = ['-created_at', 'created_at', 'book__title', 'page_number']
    if sort_by in valid_sort_fields:
        quotes = quotes.order_by(sort_by)
    else:
        quotes = quotes.order_by('-created_at')

    # Get all books and tags for filter dropdowns
    user_books = Book.objects.filter(user=request.user).order_by('title')
    user_tags = Tag.objects.filter(user=request.user).order_by('name')

    context = {
        'quotes': quotes,
        'books': user_books,
        'tags': user_tags,
        'current_book': book_filter,
        'current_tag': tag_filter,
        'search_query': search_query,
        'sort_by': sort_by,
    }

    # If HTMX request, only return the quotes list partial
    if request.htmx:
        return render(request, 'quotes/partials/quote_list.html', context)

    return render(request, 'quotes/quotes_list.html', context)
