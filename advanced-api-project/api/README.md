# Advanced API Project

## API Endpoints

### Books
- **GET** `/books/` - Retrieve all books.
- **GET** `/books/<id>/` - Retrieve a specific book by ID.
- **POST** `/books/create/` - Create a new book (requires authentication).
- **PUT** `/books/<id>/update/` - Update an existing book (requires authentication).
- **DELETE** `/books/<id>/delete/` - Delete a book (requires authentication).

### Authentication
For creating, updating, and deleting books, you must be an authenticated user. You can obtain an authentication token by logging in.

## Testing
You can test these endpoints using Postman or curl by sending requests to the server.

## API Query Features

### Filtering:
- Filter books by `title`, `author`, or `publication_year` using query parameters:
  - `/books/?title=some_title`
  - `/books/?author=1`
  - `/books/?publication_year=2020`

### Searching:
- Search books by `title` or `author` using the `?search=` parameter:
  - `/books/?search=Harry`

### Ordering:
- Order books by `title` or `publication_year` using the `?ordering=` parameter:
  - `/books/?ordering=publication_year`
