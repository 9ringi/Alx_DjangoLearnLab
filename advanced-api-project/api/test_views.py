from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Book, Author
from django.contrib.auth.models import User

class BookAPITests(APITestCase):

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='password')

        # Create an Author instance
        self.author = Author.objects.create(name='Author One')

        # Create some Book instances for testing, linking to the author
        self.book1 = Book.objects.create(title='Book One', publication_year=2000, author=self.author)
        self.book2 = Book.objects.create(title='Book Two', publication_year=2010, author=self.author)

        # Define the URL for the book list endpoint
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})

    # Test to retrieve the list of books
    def test_get_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # Test to retrieve a single book by ID
    def test_get_single_book(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    # Test to create a new book (requires authentication)
    def test_create_book(self):
        self.client.login(username='testuser', password='password')
        data = {'title': 'Book Three', 'publication_year': 2022, 'author': self.author.id}
        create_url = reverse('book-create')
        response = self.client.post(create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    # Test to update a book (requires authentication)
    def test_update_book(self):
        self.client.login(username='testuser', password='password')
        data = {'title': 'Updated Book One', 'publication_year': 2022, 'author': self.author.id}
        update_url = reverse('book-update', kwargs={'pk': self.book1.pk})
        response = self.client.put(update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book One')

    # Test to delete a book (requires authentication)
    def test_delete_book(self):
        self.client.login(username='testuser', password='password')
        delete_url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # Test filtering by publication year
    def test_filter_books_by_publication_year(self):
        response = self.client.get(f"{self.list_url}?publication_year=2000")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book One')

    # Test searching by title
    def test_search_books_by_title(self):
        response = self.client.get(f"{self.list_url}?search=Book One")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book One')

    # Test ordering by publication year
    def test_order_books_by_publication_year(self):
        response = self.client.get(f"{self.list_url}?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Book One')  # Older book first
