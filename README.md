# 🎬 WatchList & Review API  

A RESTful API built with **Django REST Framework (DRF)** for managing movies (watchlist) and reviews.  
It provides CRUD operations, user reviews, authentication, pagination, and search functionality.  

---

## 🚀 Features
- List all movies (APIView & GenericView examples)  
- Retrieve movie details  
- Add reviews for movies  
- Get all reviews for a movie  
- Get all reviews by a specific user  
- Retrieve or update review details  
- Authentication & Permissions (only authenticated users can add/update/delete)  
- Pagination, Filtering & Search  

---

## 📌 API Endpoints

### 🎬 Watchlist
| Method | Endpoint       | Description                  |
|--------|----------------|------------------------------|
| GET    | `watch/list/`       | Get all movies (APIView)     |
| GET    | `watch/list2/`      | Get all movies (GenericView) |
| GET    | `watch/{id}/`       | Get details of a movie       |

---

### 📝 Reviews
| Method | Endpoint                   | Description                          |
|--------|-----------------------------|--------------------------------------|
| POST   | `watch/{id}/review-create/`      | Add a review for a movie             |
| GET    | `watch/{id}/reviews/`            | Get all reviews for a movie          |
| GET    | `watch/review/{id}/`             | Get details of a single review       |

---

### 👤 User Reviews
| Method | Endpoint   | Description                          |
|--------|-----------|--------------------------------------|
| GET    | `watch/user/`  | Get all reviews written by a user     |

---

### 🔗 Router-based Endpoints
- `/` → Automatically generated endpoints (via `include(router.urls)`)  

---

### 🔑 Authentication
| Endpoint       | Description                             |
|----------------|-----------------------------------------|
| `/api-auth/`   | Browsable API login/logout (DRF built-in) |

---
