***Command:*** Retrieve and display all attributes of the book you just created.

```python
>>> book = Book.objects.get(title="1984")
>>> print(f"Title: {book.title}, Author: {book.author}, Publication Year: {book.publication_year}")
```

***Expected Output:*** The details of the book "1984" by George Orwell, published in 1949, are displayed.

```
Title: 1984, Author: George Orwell, Publication Year: 1949
```
