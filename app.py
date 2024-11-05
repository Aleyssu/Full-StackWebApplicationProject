from datetime import datetime
from flask import Flask, render_template, request, redirect
from uuid import uuid4
import re
import firebase_admin
from firebase_admin import credentials, db
import os

# Ensure Firebase app is initialized only once
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(
            cred, {'databaseURL': 'https://cisc327-project-eb026-default-rtdb.firebaseio.com/'})

if os.getenv("FLASK_ENV") == "testing":
    print("Starting in testing mode")
    orders_ref = db.reference("testing/orders")
    inventory_ref = db.reference("testing/inventory")
else:
    print("Starting in production mode")
    orders_ref = db.reference("orders")
    inventory_ref = db.reference("inventory")

app = Flask(__name__)

# Returns the dictionary of a drug's information from the inventory given a name
def get_drug(name):
    return inventory_ref.child(name).get()

# Returns an order given its id
def get_order(id):
    return orders_ref.child(id).get()

# Returns list of all orders in the database
def get_orders():
    dict = orders_ref.get()
    return list(dict.values()) if dict else []

# Returns list of all drugs in the inventory
def get_inventory():
    dict = inventory_ref.get()
    return list(dict.values()) if dict else []

# Returns a list of strings of all drug names in the inventory
def get_drug_list():
    dict = inventory_ref.get()
    return list(dict.keys()) if dict else []

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        return render_template('index.html', user_input=user_input)
    return render_template('index.html', user_input=None)

@app.route('/', methods=["GET", "POST"])
def get_orders_sorted():
    orders = get_orders()
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
    
    return render_template('orders.html', orders=sorted_orders, sort_key=sort_key, 
                           drugs=get_drug_list(), search_query=query)

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
    # Add inputs to database as an order
    id = str(uuid4())
    orders_ref.update({id : {"name": name, "drug": drug, "qty": int(qty), "date": date, "id": id}})
    # Redirect back to the home page
    return redirect('/')
    
@app.route('/complete_order/<order_id>', methods=["POST"])
def complete_order(order_id):
    order = get_order(order_id)
    drug = order["drug"]
    # Remove order from database
    orders_ref.child(order_id).delete()
    # Update inventory qty
    inventory_ref.child(drug).update({'qty' : get_drug(drug)['qty'] - order["qty"]})
    # Redirect back to the home page or a success page
    return redirect('/')

@app.route('/modify_order/<order_id>', methods=["POST"])
def modify_order(order_id):
    action = request.form.get("action")
    if action == "delete":
        orders_ref.child(order_id).delete()
    else:
        name = request.form.get('name')
        drug = request.form.get('drug')
        qty = int(request.form.get('qty'))
        order_ref = orders_ref.child(order_id)
        order_ref.update({"name": name, "drug": drug, "qty": qty})

    return redirect("/")
    
@app.route('/inventory', methods=["GET", "POST"])
def get_inventory_sorted():
    drug_inventory = get_inventory()
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

@app.route('/inventory/modify_inventory', methods=["POST"])
def modify_inventory():
    drug = request.form.get('name')
    qty = int(request.form.get('qty'))
    mode = request.form.get('mode')
    if mode == "set" or inventory_ref.child(drug).get() is None:
        inventory_ref.update({drug: {"name": drug, "qty": qty, "expires": "N/A"}})
    elif mode == "delete":
         inventory_ref.child(drug).delete()
    elif mode == "add":
        drug_ref = inventory_ref.child(drug)
        drug_ref.update({"qty": drug_ref.child("qty").get() + qty})
    else:
        drug_ref = inventory_ref.child(drug)
        if drug_ref.child("qty").get() < qty:
            return redirect("/inventory")
        drug_ref.update({"qty": drug_ref.child("qty").get() - qty})

    return redirect("/inventory")

if __name__ == '__main__':
    app.run(debug=True)