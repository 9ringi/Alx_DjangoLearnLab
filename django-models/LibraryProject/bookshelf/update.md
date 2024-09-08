***Command:*** Update the title of "1984" to "Nineteen Eighty-Four" and save the changes.

```python
>>> book = Book.objects.get(title="1984")
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()
```

***Expected Output:*** The book's title is successfully updated to "Nineteen Eighty-Four" and saved in the database.
