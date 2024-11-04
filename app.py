from datetime import datetime
from flask import Flask, render_template, request, redirect
from uuid import uuid4
import sys
import re

app = Flask(__name__)

# Fake order data
orders = [
    {"name": "Charlie", "drug": "H2O", "qty": 1, "date": "09/30/24", "id":str(uuid4())},
    {"name": "Alice", "drug": "Dihydrogen Monoxide", "qty": 10000, "date": "09/19/24", "id":str(uuid4())},
    {"name": "Bob", "drug": "Hydrogen Hydroxide", "qty": 42, "date": "09/24/24", "id":str(uuid4())}
]

# Fake inventory
drug_inventory = [
    {"name": "H2O", "qty": 1000000, "expires" : "N/A"},
    {"name": "Hydrogen Hydroxide", "qty": 200, "expires" : "N/A"},
    {"name": "Dihydrogen Monoxide", "qty": 800000, "expires" : "N/A"}
]

# Returns the dictionary of a drug's information from the inventory given a name
def get_drug(name):
    drug = [d for d in drug_inventory if d['name'] == name]
    if len(drug) < 1:
        return None
    else:
        return drug[0]
       
# Returns an order given its id
def get_order(id):
    order = [o for o in orders if o['id'] == id]
    if len(order) < 1:
        return None
    else:
        return order[0]

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        return render_template('index.html', user_input=user_input)
    return render_template('index.html', user_input=None)

@app.route('/', methods=["GET", "POST"])
def get_orders():

    search_result = []
    if request.method == "POST":
        # Get search query from the form
        query = request.form.get("search_query", "").lower()
        # Search in the array
        search_result = [item for item in orders if query in item["name"].lower()]
    else:
        # For GET requests, get the search query from the URL (for sort persistence)
        query = request.args.get("search_query", "").lower()
        if query:
            search_result = [item for item in orders if query in item["name"].lower()]

    # Default to sorting by date
    sort_key = request.args.get('sort', 'date')

    # Get orders searched for if none exist show all orders
    if search_result != []:
        sorted_orders = sorted(search_result, key=lambda x: x[sort_key])
    else:
        sorted_orders = sorted(orders, key=lambda x: x[sort_key])
    

    return render_template('orders.html', orders=sorted_orders, sort_key=sort_key, search_query=query)

@app.route('/create_order', methods=["GET", "POST"])
def create_order():
    # Get inputs
    name = request.form.get('name')
    drug = request.form.get('drug')
    qty = request.form.get('qty')

    if not re.match(r'^[A-Za-z\s]+$', name):
        return "Name must only contain letters and spaces.", 400
    
    if not drug:
        return "Drug must be selected.", 400
    
    if float(qty) <= 0:
        return "Please enter a positive number.", 400

    # Get date
    dateNow = datetime.now()
    date = str(dateNow.month) + "/" + str(dateNow.day) + "/" + str(dateNow.year)
    # Add inputs to temporary data
    orders.append({"name": name, "drug": drug, "qty": int(qty), "date": date, "id": str(uuid4())})
    
    # Redirect back to the home page
    return redirect('/')
    
@app.route('/complete_order/<order_id>', methods=["POST"])
def complete_order(order_id):
    order = get_order(order_id)
    qty_removed = order["qty"]
    drug_name = order["drug"]
    
    drug_entry = get_drug(drug_name)
    drug_entry["qty"] -= qty_removed
    
    orders.remove(order)
    
    # Redirect back to the home page or a success page
    return redirect('/')
    
@app.route('/inventory', methods=["GET", "POST"])
def get_inventory():

    search_result = []
    if request.method == "POST":
        # Get search query from the form
        query = request.form.get("search_query", "").lower()
        # Search in the array
        search_result = [item for item in drug_inventory if query in item["name"].lower()]
    else:
        # For GET requests, get the search query from the URL (for sort persistence)
        query = request.args.get("search_query", "").lower()
        if query:
            search_result = [item for item in drug_inventory if query in item["name"].lower()]

    # Default to sorting by name
    sort_key = request.args.get('sort', 'name')

    # Get orders searched for if none exist show all orders
    if search_result != []:
        sorted_inventory = sorted(search_result, key=lambda x: x[sort_key])
    else:
        sorted_inventory = sorted(drug_inventory, key=lambda x: x[sort_key])
    
    reversed_inventory=sorted_inventory[::-1]
    return render_template('inventory.html', drug_inventory=sorted_inventory, drug_inventory_reversed=reversed_inventory, sort_key=sort_key, search_query=query)

if __name__ == '__main__':
    app.run(debug=True)