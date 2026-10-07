from flask import Flask, request, jsonify, render_template
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB = Path(__file__).with_name('inventory.db')


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        quantity INTEGER NOT NULL CHECK(quantity >= 0),
        price REAL NOT NULL CHECK(price >= 0)
    )''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/api/products')
def get_products():
    q = request.args.get('q', '').strip()
    conn = get_db()
    if q:
        rows = conn.execute('''SELECT * FROM products
            WHERE product_id LIKE ? OR name LIKE ? OR category LIKE ?
            ORDER BY id DESC''', (f'%{q}%', f'%{q}%', f'%{q}%')).fetchall()
    else:
        rows = conn.execute('SELECT * FROM products ORDER BY id DESC').fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.post('/api/products')
def add_product():
    data = request.get_json() or {}
    required = ['product_id', 'name', 'category', 'quantity', 'price']
    if any(str(data.get(k, '')).strip() == '' for k in required):
        return jsonify(error='All fields are required.'), 400
    try:
        quantity = int(data['quantity'])
        price = float(data['price'])
        if quantity < 0 or price < 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify(error='Quantity and price must be non-negative numbers.'), 400

    conn = get_db()
    try:
        conn.execute('INSERT INTO products(product_id,name,category,quantity,price) VALUES(?,?,?,?,?)',
                     (data['product_id'].strip(), data['name'].strip(), data['category'].strip(), quantity, price))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify(error='Product ID already exists.'), 409
    conn.close()
    return jsonify(message='Product added successfully.'), 201


@app.put('/api/products/<int:pid>')
def update_product(pid):
    data = request.get_json() or {}
    try:
        quantity = int(data['quantity'])
        price = float(data['price'])
        if quantity < 0 or price < 0:
            raise ValueError
    except (KeyError, ValueError, TypeError):
        return jsonify(error='Quantity and price must be non-negative numbers.'), 400

    conn = get_db()
    cur = conn.execute('UPDATE products SET quantity=?, price=? WHERE id=?', (quantity, price, pid))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        return jsonify(error='Product not found.'), 404
    return jsonify(message='Product updated successfully.')


@app.delete('/api/products/<int:pid>')
def delete_product(pid):
    conn = get_db()
    cur = conn.execute('DELETE FROM products WHERE id=?', (pid,))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        return jsonify(error='Product not found.'), 404
    return jsonify(message='Product deleted successfully.')


@app.get('/api/stats')
def stats():
    conn = get_db()
    row = conn.execute('''SELECT COUNT(*) products,
        COALESCE(SUM(quantity),0) units,
        COALESCE(SUM(quantity * price),0) value,
        COALESCE(SUM(CASE WHEN quantity <= 5 THEN 1 ELSE 0 END),0) low_stock
        FROM products''').fetchone()
    conn.close()
    return jsonify(dict(row))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
