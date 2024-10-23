from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Llave secreta para la sesión

# Ruta principal
@app.route('/')
def index():
    if 'products' not in session:
        session['products'] = []  # Inicializar la lista de productos en la sesión
    
    return render_template('index.html', products=session['products'])

# Agregar un nuevo producto
@app.route('/add', methods=['POST'])
def add_product():
    id = len(session['products']) + 1
    name = request.form['name']
    quantity = request.form['quantity']
    price = request.form['price']
    expiration_date = request.form['expiration_date']
    category = request.form['category']
    
    # Crear un nuevo producto como diccionario
    new_product = {
        'id': id,
        'name': name,
        'quantity': quantity,
        'price': price,
        'expiration_date': expiration_date,
        'category': category
    }
    
    session['products'].append(new_product)  # Añadir a la lista de productos
    session.modified = True  # Marcar la sesión como modificada
    
    return redirect(url_for('index'))

# Eliminar producto
@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    products = session['products']
    session['products'] = [product for product in products if product['id'] != product_id]
    session.modified = True
    return redirect(url_for('index'))

# Editar producto
@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if request.method == 'POST':
        products = session['products']
        for product in products:
            if product['id'] == product_id:
                product['name'] = request.form['name']
                product['quantity'] = request.form['quantity']
                product['price'] = request.form['price']
                product['expiration_date'] = request.form['expiration_date']
                product['category'] = request.form['category']
                break
        session.modified = True
        return redirect(url_for('index'))
    
    product = next((p for p in session['products'] if p['id'] == product_id), None)
    return render_template('edit.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)
