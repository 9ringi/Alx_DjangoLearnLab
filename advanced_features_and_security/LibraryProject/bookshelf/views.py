from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from .models import Book
from django.db.models import Q
from .forms import ExampleForm

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    # Edit book logic here
    pass

@permission_required('bookshelf.can_view', raise_exception=True)
def view_books(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


def search_books(request):
    query = request.GET.get('q')
    results = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    return render(request, 'bookshelf/book_list.html', {'books': results})