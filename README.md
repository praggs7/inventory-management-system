# StockFlow — Inventory / Product Management System

## Project Title
Inventory / Product Management System

## Brief Description
StockFlow is a full-stack web application for managing product inventory. It allows users to add, search, update stock quantity and price, and delete product records. The dashboard also displays total products, total units, inventory value, and low-stock alerts.

## Technologies / Tools Used
- HTML5
- CSS3
- JavaScript (Fetch API)
- Python 3
- Flask
- SQLite
- REST API / JSON
- Git & GitHub

## Features
- Add product records
- View all products
- Search by Product ID, name, or category
- Update quantity and price
- Delete products
- Unique Product ID validation
- Non-negative quantity and price validation
- Low-stock alerts for quantity <= 5
- Dynamic updates without page reload
- Dashboard statistics

## Project Structure
```text
inventory-management/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## How to Run

### 1. Install Python
Make sure Python 3 is installed.

### 2. Open the project folder
```bash
cd inventory-management
```

### 3. Create and activate a virtual environment (recommended)
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Start the application
```bash
python app.py
```

### 6. Open in your browser
Go to:
```text
http://127.0.0.1:5000
```

The SQLite database is created automatically when the application starts.

## API Endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/products` | List/search products |
| POST | `/api/products` | Add a product |
| PUT | `/api/products/<id>` | Update quantity/price |
| DELETE | `/api/products/<id>` | Delete a product |
| GET | `/api/stats` | Dashboard statistics |

## Validation / Edge Cases
- Duplicate Product IDs are rejected.
- Quantity cannot be negative.
- Price cannot be negative.
- Required fields cannot be empty.
- Deleting a non-existent product returns an error.
- Searching for unavailable products returns an empty result rather than crashing.

## Assessment Alignment
The application implements the requirements of Aim 6: adding, searching, updating stock, deleting product records, SQLite storage, Flask REST endpoints, JSON/HTTP communication, validation, dynamic Fetch API rendering, and low-stock alerts.
