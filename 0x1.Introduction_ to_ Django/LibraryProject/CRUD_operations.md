# CRUD Operations in Django Shell

This document outlines the steps to perform Create, Read, Update, and Delete (CRUD) operations using the Django shell.

## Create

***Command:*** Create a Book instance with the title "1984," author "George Orwell," and publication year 1949.

```python
>>> from bookshelf.models import Book
>>> book1 = Book(title="1984", author="George Orwell", publication_year=1949)
>>> book1.save()
```

***Expected Output:*** 
```plaintext
A new book titled "1984" by George Orwell, published in 1949, is successfully created in the database.
```

## Read

***Command:*** Retrieve and display all attributes of the book you just created.

```python
>>> book = Book.objects.get(title="1984")
>>> print(f"Title: {book.title}, Author: {book.author}, Publication Year: {book.publication_year}")
```

***Expected Output:*** 
```
Title: 1984, Author: George Orwell, Publication Year: 1949
```
*The details of the book "1984" by George Orwell, published in 1949, are displayed.*

## Update

***Command:*** Update the title of "1984" to "Nineteen Eighty-Four" and save the changes.

```python
>>> book = Book.objects.get(title="1984")
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()
```

***Expected Output:*** 
```plaintext
The book's title is successfully updated to "Nineteen Eighty-Four" and saved in the database.
```

## Delete

***Command:*** Delete the book you created and confirm the deletion by trying to retrieve all books again.

```python
>>> book = Book.objects.get(title="Nineteen Eighty-Four")
>>> book.delete()
>>> all_books = Book.objects.all()
>>> print(all_books)
```

***Expected Output:*** 
```plaintext
[]
```
*This output confirms that the book has been successfully deleted, as the list of all books is now empty.*
