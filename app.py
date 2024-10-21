from datetime import datetime
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Fake order data
orders = [
    {"name": "Charlie", "drug": "H2O", "qty": "1", "date": "09/30/24"},
    {"name": "Alice", "drug": "Dihydrogen monoxide", "qty": "10000", "date": "09/19/24"},
    {"name": "Bob", "drug": "Hydrogen hydroxide", "qty": "42", "date": "09/24/24"},
    {"name": "Charlie", "drug": "H2O", "qty": "1", "date": "09/30/24"},
    {"name": "Charlie", "drug": "H2O", "qty": "1", "date": "09/30/24"},
    {"name": "Charlie", "drug": "H2O", "qty": "1", "date": "09/30/24"},
    {"name": "Charlie", "drug": "H2O", "qty": "1", "date": "09/30/24"}
]

# Fake inventory
drug_inventory = [
    {"name": "H2O", "quantity": 1000000, "expires" : "N/A"},
    {"name": "Hydrogen Hydroxide", "quantity": 200, "expires" : "N/A"},
    {"name": "Dihydrogen Monoxide", "quantity": 800000, "expires" : "N/A"}
]

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        return render_template('index.html', user_input=user_input)
    return render_template('index.html', user_input=None)

@app.route('/')
def get_orders():
    # Default to sorting by date
    sort_key = request.args.get('sort', 'date')
    sorted_orders = sorted(orders, key=lambda x: x[sort_key])
    return render_template('orders.html', orders=sorted_orders, sort_key=sort_key)

@app.route('/create_order', methods=["POST"])
def create_order():
    # Get inputs
    name = request.form.get('name')
    drug = request.form.get('drug')
    qty = request.form.get('qty')

    # Get date
    dateNow = datetime.now()
    date = str(dateNow.month) + "/" + str(dateNow.day) + "/" + str(dateNow.year)
    # Add inputs to temporary data
    orders.append({"name": name, "drug": drug, "qty": qty, "date": date})
    
    # Redirect back to the home page
    return redirect('/')
    
@app.route('/inventory')
def get_inventory():
    # Default to sorting by name
    sort_key = request.args.get('sort', 'name')
    sorted_inventory = sorted(drug_inventory, key=lambda x: x[sort_key])
    reversed_inventory=sorted_inventory[::-1]
    return render_template('inventory.html', drug_inventory=sorted_inventory, drug_inventory_reversed=reversed_inventory, sort_key=sort_key)

if __name__ == '__main__':
    app.run(debug=True)
