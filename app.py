from datetime import datetime
from flask import Flask, render_template, request, redirect
from uuid import uuid4
import sys

app = Flask(__name__)

# Fake order data
orders = [
    {"name": "Charlie", "drug": "H2O", "qty": 1, "date": "09/30/24", "id":uuid4().hex},
    {"name": "Alice", "drug": "Dihydrogen Monoxide", "qty": 10000, "date": "09/19/24", "id":uuid4().hex},
    {"name": "Bob", "drug": "Hydrogen Hydroxide", "qty": 42, "date": "09/24/24", "id":uuid4().hex}
]

# Fake inventory
drug_inventory = [
    {"name": "H2O", "qty": 1000000, "expires" : "N/A"},
    {"name": "Hydrogen Hydroxide", "qty": 200, "expires" : "N/A"},
    {"name": "Dihydrogen Monoxide", "qty": 800000, "expires" : "N/A"}
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
    print(orders, flush=True)
    sort_key = request.args.get('sort', 'date')
    sorted_orders = sorted(orders, key=lambda x: x[sort_key])
    return render_template('orders.html', orders=sorted_orders, sort_key=sort_key)

@app.route('/create_order', methods=["POST"])
def create_order():
    #Create Order popup
    name = request.form.get('name')
    drug = request.form.get('drug')
    qty = request.form.get('qty')

    # Do something with the inputs (e.g., save them to a database, process data, etc.)
    dateNow = datetime.now()
    date = str(dateNow.month) + "/" + str(dateNow.day) + "/" + str(dateNow.year)
    orders.append({"name": name, "drug": drug, "qty": qty, "date": date, "id": uuid4().hex})
    
    # Redirect back to the home page or a success page
    return redirect('/')
    
@app.route('/complete_order/<order_id>', methods=["POST"])
def complete_order(order_id):
    
    print("Order id: ", order_id, flush=True)
    
    for o in orders:
        print(o["id"], flush=True)
    order = [o for o in orders if o['id'] == order_id][0]
    qty_removed = int(order["qty"])
    drug_name = order["drug"]
    
    drug_entry = [drug for drug in drug_inventory if drug["name"] == drug_name][0]
    drug_entry["qty"] -= qty_removed
    
    orders.remove(order)
    
    # Redirect back to the home page or a success page
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
