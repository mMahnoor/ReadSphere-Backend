# 📚 Readsphere – Library Management System (DRF)

Readsphere is a **Library Management System** built with **Django Rest Framework (DRF)**.
It provides a robust API backend for managing books, authors, categories, and library transactions like borrowing, returning, reserving, and reviewing books.

---

## 🚀 Features

- **User Management**

  - Register/login users
  - Manage user profiles and roles (admin, member)

- **Books, Authors & Categories**

  - CRUD operations for books
  - Each book linked to an author and a category
  - Browse by category or author

- **Borrow & Return**

  - Users can borrow available books
  - Return books once finished
  - Track borrowed books with status and due dates

- **Reservation System**

  - Reserve books when unavailable
  - Auto-notify when reserved copy is available

- **Rating & Reviews**

  - Users can rate and review books
  - Average rating visible for each book

- **Admin Dashboard**

  - Admins can manage books, categories, authors, and reservations
  - Full control over user permissions

---

## 🛠️ Tech Stack

- **Backend**: Django 5, Django Rest Framework
- **Database**: PostgreSQL (or SQLite for development)
- **Authentication**: JWT (SimpleJWT)
- **Documentation**: DRF browsable API / Swagger

---

## 📂 Project Structure

```
Readsphere/
│── api/               #Centralized urls
│── users/             # User authentication & profiles
│── book/             # Books, authors, categories
│── borrow/            # Borrow & return logic
│── reservation/      # Book reservation system
│── reviews/           # Ratings & reviews
│── readsphere/            # Main project settings
│── requirements.txt
│── manage.py
```

---

## ⚡ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/mMahnoor/ReadSphere-Backend.git
   cd ReadSphere-Backend
   ```

2. **Create & activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**

   - Copy `.env.example` to `.env`
   - Update values as per your configuration

   ```bash
   cp .env.example .env
   ```

   **`.env.example`**

   ```
   DEBUG=True
   SECRET_KEY=your-secret-key

   DATABASE_NAME=readsphere_db
   DATABASE_USER=your_db_user
   DATABASE_PASSWORD=your_db_password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432

   ```

5. **Run migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**

   ```bash
   python manage.py runserver
   ```

---

## 🔑 API Endpoints (Sample)

### Authentication

- `POST /api/v1/auth/register/` – Register user
- `POST /api/v1/auth/login/` – Login & get JWT token

### Books

- `GET /api/v1/books/` – List all books
- `POST /api/v1/books/` – Add new book (admin)
- `GET /api/v1/books/{id}/` – Book details

### Borrow & Return

- `POST /api/v1/borrow/` – Borrow a book
- `POST /api/v1/borrow/{id}/return/` – Return a book

### Reservation

- `POST /api/v1/reservations/make` – Reserve a book
- `GET /api/v1/reservations/` – View reservations

### Reviews

- `POST /api/v1/reviews/` – Add a review
- `GET /api/v1/reviews/{book_id}/` – List book reviews

---

## 🌐 Live Links

- **Backend Deployment**:
- **Swagger Documentation**:

---

## 🧪 Testing

Run tests with:

```bash
python manage.py test
```

---

## 📌 Roadmap

- [ ] Add email notifications for reservations
- [ ] Implement book availability tracking with copies
- [ ] Improve admin dashboard with analytics

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

Developed by **Mahnur Akther**
