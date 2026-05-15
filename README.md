# 🛒 FastAPI E-Commerce Backend

A fully functional e-commerce REST API built with **FastAPI** and **Pydantic**, featuring complete CRUD operations, advanced data validation, and a live **Streamlit** dashboard frontend.

## 🌐 Live Demo

| Service | URL |
|---------|-----|
| 🖥️ **Frontend (Streamlit)** | [fast-api-practice.streamlit.app](https://fast-api-practice.streamlit.app/) |
| ⚡ **Backend API (FastAPI)** | [fast-api-practice-ecommerce.onrender.com](https://fast-api-practice-ecommerce.onrender.com/) |
| 📄 **API Docs (Swagger)** | [Swagger UI](https://fast-api-practice-ecommerce.onrender.com/docs) |

> **Note:** The backend is hosted on Render's free tier and may take ~30 seconds to wake up on first visit.

---

## ✨ Features

- **Full CRUD Operations** — Create, Read, Update, and Delete products
- **Advanced Pydantic Validation** — Strict type checking, business rules, computed fields, and custom validators
- **Search & Filter** — Search products by name with sorting and pagination
- **Partial Updates** — `PUT` endpoint supports partial updates using `exclude_unset`
- **HTTP Middleware** — Request logging middleware for monitoring
- **Response Models** — Validated outbound data with Pydantic schemas
- **Streamlit Dashboard** — Interactive frontend connected to the API via HTTP requests

---

## 🏗️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| **FastAPI** | Backend REST API framework |
| **Pydantic v2** | Data validation and schema enforcement |
| **Uvicorn** | ASGI server |
| **Streamlit** | Frontend dashboard |
| **Render** | Backend deployment |
| **Streamlit Cloud** | Frontend deployment |

---

## 📁 Project Structure

```
FastApi-ecommerce/
├── app/
│   ├── data/
│   │   └── products.json        # Product data storage
│   ├── schema/
│   │   └── product_schema.py    # Pydantic models & validators
│   ├── services/
│   │   └── products.py          # Business logic & data persistence
│   ├── main.py                  # FastAPI routes & middleware
│   ├── frontend.py              # Streamlit dashboard
│   └── requirements.txt         # Python dependencies
└── README.md
```

---

## 🚀 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Welcome message |
| `GET` | `/allproducts` | Get all products |
| `GET` | `/products?name=...` | Search products by name with sorting & limit |
| `GET` | `/products/{product_id}` | Get a single product by UUID |
| `POST` | `/products` | Create a new product |
| `PUT` | `/products/{product_id}` | Update a product (partial updates supported) |
| `DELETE` | `/products/{product_id}` | Delete a product |

---

## 🛠️ Local Development

### Prerequisites

- Python 3.10+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/Nojan-Devkota/fast-api-practice.git
cd fast-api-practice

# Install dependencies
pip install -r app/requirements.txt
```

### Running Locally

You need **two terminals** running simultaneously:

**Terminal 1 — Backend:**
```bash
cd app
uvicorn main:app --reload
```

**Terminal 2 — Frontend:**
```bash
cd app
python -m streamlit run frontend.py
```

Then open:
- Backend API: http://127.0.0.1:8000
- Swagger Docs: http://127.0.0.1:8000/docs
- Frontend Dashboard: http://localhost:8501

---

## 📦 Pydantic Schemas

The project uses strict Pydantic v2 schemas with:

- **`Product`** — Full product schema with required fields and validation
- **`ProductUpdate`** — All fields optional for partial updates
- **`Seller`** / **`SellerUpdate`** — Seller info with email domain validation
- **`Dimensions`** / **`DimensionsUpdate`** — Product dimensions with `gt=0` constraints
- **Computed Fields** — `selling_price` auto-calculated from price and discount
- **Business Rules** — Active products must have stock > 0

---

## 🔗 Frontend ↔ Backend Connection

The Streamlit frontend communicates with FastAPI using the Python `requests` library:

```python
import requests

API_URL = "https://fast-api-practice-ecommerce.onrender.com"

# GET all products
response = requests.get(f"{API_URL}/allproducts")
products = response.json()

# POST a new product
response = requests.post(f"{API_URL}/products", json=product_data)

# PUT to update
response = requests.put(f"{API_URL}/products/{product_id}", json=update_data)

# DELETE a product
response = requests.delete(f"{API_URL}/products/{product_id}")
```

---

## 👤 Author

**Nojan Devkota**

---
