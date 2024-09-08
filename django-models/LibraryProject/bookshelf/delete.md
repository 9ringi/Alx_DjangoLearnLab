**Command:** Delete the book you created and confirm the deletion by trying to retrieve all books again.

```python
>>> from bookshelf.models import Book
>>> book = Book.objects.get(id=1)
>>> book.delete()
```

**Expected Output:** 
```python
(1, {'bookshelf.Book': 1})
```
The book with `id=1` is successfully deleted from the database.