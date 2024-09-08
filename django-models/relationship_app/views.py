from django.shortcuts import render
from .models import Library 
from .models import Book
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.decorators import permission_required


def user_is_admin(user):
    return user.userprofile.role == 'admin'

def user_is_librarian(user):
    return user.userprofile.role == 'librarian'

def user_is_member(user):
    return user.userprofile.role == 'member'

@user_passes_test(user_is_admin)
def admin_view(request):
    context = {'message': 'Welcome to the Admin Dashboard'}
    return render(request, 'relationship_app/admin_view.html', context)

@user_passes_test(user_is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(user_is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')


def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Library.objects.all()
        return context
    

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('some_view_name')
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})



@login_required
@permission_required('relationship_app.can_add_book')
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        book = Book(title=title, author_id=author_id)  
        book.save()
        return redirect('book_list') 
    else:
        return render(request, 'relationship_app/add_book.html')

@login_required
@permission_required('relationship_app.can_change_book')
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.save()
        return redirect('book_detail', pk=book.pk)
    else:
        context = {'book': book}
        return render(request, 'relationship_app/edit_book.html', context)

@login_required
@permission_required('relationship_app.can_delete_book')
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('book_list') 