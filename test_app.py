import pytest
from uuid import uuid4
import os
os.environ["FLASK_ENV"] = "testing"
import app
os.environ["FLASK_ENV"] = ""

# Start with empty database
app.orders_ref.set({})
app.inventory_ref.set({})

# Test client for Flask
@pytest.fixture
def client():
    with app.app.test_client() as client:
        yield client

def test_get_orders_empty(client):
    # Try getting orders when the database is empty
    response = client.get("/")
    # Check for OK html response
    assert response.status_code == 200

def test_get_inventory_empty(client):
    # Try getting inventory when the database is empty
    response = client.get("/inventory")
    # Check for OK html response
    assert response.status_code == 200

def test_create_order_valid_input(client):
    # Simulate a POST request to the '/create_order' route with valid form data
    response = client.post('/create_order', data={
        'name': 'John Doe',  # Valid: only letters and spaces
        'drug': 'H2O',  # Valid: selected option
        'qty': '5'  # Valid: positive number
    })

    # Check that the response redirects (302 for a successful redirect)
    assert response.status_code == 302
    assert response.location == '/'  # Assuming the redirect is to the index page

def test_create_order_invalid_name(client):
    # Simulate a POST request to the '/create_order' route with invalid name
    response = client.post('/create_order', data={
        'name': 'John123',  # Invalid: contains numbers
        'drug': 'H2O',
        'qty': '5'
    })

    # Check for a 400 Bad Request status
    assert response.status_code == 400
    assert b"Name must only contain letters and spaces." in response.data

def test_create_order_invalid_drug(client):
    # Simulate a POST request to the '/create_order' route with no input selected for drug
    response = client.post('/create_order', data={
        'name': 'John Doe',
        'drug': '',  # Invalid: no option selected
        'qty': '5'
    })

    # Check that the form rejects this with a 400 status code
    assert response.status_code == 400  
    assert b"Drug must be selected." in response.data

def test_create_order_invalid_quantity(client):
    # Simulate a POST request to the '/create_order' route with a negative quantity
    response = client.post('/create_order', data={
        'name': 'John Doe',
        'drug': 'H2O',
        'qty': '-5'  # Invalid: negative number
    })

    # Check for a 400 Bad Request status
    assert response.status_code == 400
    assert b"Please enter a positive number." in response.data

def test_app_loads(client):
    #Check that our app runs properly
    response = client.get('/')
    res = response.get_data(as_text=True)

    assert '<html lang="en">' in res

def test_inventory_loads(client):
    #Check that our inventory loads properly
    app.inventory_ref.set({"H2O": {"name": "H2O", "qty": 1000000, "expires" : "N/A"},
                           "KCN": {"name": "KCN", "qty": 100, "expires" : "N/A"}})
    response = client.get('/inventory')
    res = response.get_data(as_text=True)

    # Check that all inventory contents are displayed
    assert 'H2O' in res
    assert 'KCN' in res
    assert '1000000' in res
    assert '100' in res

def test_inventory_search(client):
    response = client.post('/inventory', data={
        "search_query": "H2O"
    })
    res = response.get_data(as_text=True)

    # Make sure only matching search shows up
    assert "H2O" in res
    assert "KCN" not in res
    assert response.status_code == 200

def test_inventory_qty_sort(client):
    #test that we can sort ordering by qty
    response = client.get('/inventory?sort=qty')
    res = response.get_data(as_text=True)

    assert res.find('100') < res.find('1000000')

def test_inventory_name_sort(client):
    #test that we can sort ordering by name
    response = client.get('/inventory?sort=name')
    res = response.get_data(as_text=True)

    assert res.find('H2O') < res.find('KCN')
        
def test_orders_loads(client):
    id1 = str(uuid4())
    id2 = str(uuid4())
    app.orders_ref.set({id1:{"name": "Charlie", "drug": "H2O", "qty": 1, "date": "09/30/24", "id":id1},
                       id2:{"name": "Aleyssu", "drug": "KCN", "qty": 2, "date": "10/30/24", "id":id2}})
    response = client.get('/')
    # Ensure all orders are displayed
    res = response.get_data(as_text=True)
    assert 'Charlie' in res
    assert 'Aleyssu' in res
    assert 'H2O' in res
    assert 'KCN' in res
    assert '1' in res
    assert '2' in res
    assert '09/30/24' in res
    assert '10/30/24' in res
    # Ensure client recieves OK html response
    assert response.status_code == 200

def test_orders_search(client):
    response = client.post('/', data={
        "search_query": "Charlie"
    })
    res = response.get_data(as_text=True)

    # Make sure only matching search shows up
    assert "Charlie" in res
    assert "Aleyssu" not in res
    assert response.status_code == 200

def test_orders_name_sort(client):
    # Check orders sorting by name
    response = client.get('/?sort=name').get_data(as_text=True)
    assert response.find('Aleyssu') < response.find('Charlie')

def test_orders_date_sort(client):
    # Check orders sorting by date
    response = client.get('/?sort=date').get_data(as_text=True)
    assert response.find('09/30/24') < response.find('10/30/24')

def test_orders_drug_sort(client):
    # Check orders sorting by drug name
    response = client.get('/?sort=drug').get_data(as_text=True)
    assert response.find('H2O') < response.find('KCN')
    
def test_complete_order(client):
    # Try completing every order in the database
    for order in app.get_orders():
        drug = order["drug"]
        prev_qty = app.get_drug(drug)['qty']
        order_id = order['id']
        
        response = client.post('/complete_order/' + order_id)
        # Ensure inventory drug qty is updated appropriately
        assert app.get_drug(drug)['qty'] == prev_qty - order['qty']
        # Ensure order has been removed from database
        assert app.get_order(order_id) is None
        # Ensure successful redirect
        assert response.status_code == 302

def test_modify_order(client):
    id = str(uuid4())
    app.orders_ref.set({id:{"name": "Charlie", "drug": "H2O", "qty": 1, "date": "09/30/24", "id":id}})
    response = client.post("/modify_order/" + id, data={
        'name': 'Aleyssu',
        'qty': 3,
        'drug': 'Hydrogen Hydroxide',
        'action': 'modify'
    })
    order = app.get_order(id)
    assert order['name'] == 'Aleyssu'
    assert order['qty'] == 3
    assert order['drug'] == 'Hydrogen Hydroxide'
    assert response.status_code == 302

def test_delete_order(client):
    id = str(uuid4())
    app.orders_ref.set({id:{"name": "Charlie", "drug": "H2O", "qty": 1, "date": "09/30/24", "id":id}})
    response = client.post("/modify_order/" + id, data={
        'name': 'Aleyssu',
        'qty': 3,
        'drug': 'Hydrogen Hydroxide',
        'action': 'delete'
    })
    assert app.get_order(id) is None
    assert response.status_code == 302

def test_modify_inventory_new(client):
    response = client.post('/inventory/modify_inventory', data={
        'name': 'New Drug',
        'qty': 50,
        'mode': 'change'
    })
    # Make sure new drug shows up in database
    assert app.get_drug("New Drug") is not None
    # 302 successful redirect
    assert response.status_code == 302

def test_modify_inventory_add(client):
    response = client.post('/inventory/modify_inventory', data={
        'name': 'New Drug',
        'qty': 50,
        'mode': 'add'
    })
    # 302 successful redirect
    assert app.get_drug("New Drug")['qty'] == 100
    assert response.status_code == 302

def test_modify_inventory_subtract(client):
    response = client.post('/inventory/modify_inventory', data={
        'name': 'New Drug',
        'qty': 10,
        'mode': 'subtract'
    })
    # 302 successful redirect
    assert app.get_drug("New Drug")['qty'] == 90
    assert response.status_code == 302

def test_inventory_delete(client):
    client.post('/inventory/modify_inventory', data={
        'name': 'New Drug 2',
        'qty': 10,
        'mode': 'set'
    })

    response = client.post('/inventory/modify_inventory', data={
        'name': 'New Drug 2',
        'qty': 10,
        'mode': 'delete'
    })

    inventory = app.get_drug_list()
    assert "New Drug 2" not in inventory
    assert response.status_code == 302

@pytest.mark.integration
def test_inventory_modifications():
    with app.app.test_client() as client:

        app.inventory_ref.set({})

        inventory = app.get_inventory()
        assert len(inventory) == 0

        #check new entry can be created
        response = client.post('/inventory/modify_inventory', data={
            'name': 'Newest Drug',
            'qty': 1000,
            'mode': 'add'
        })  

        assert app.get_drug("Newest Drug")['qty'] == 1000

        #check add function works
        response = client.post('/inventory/modify_inventory', data={
            'name': 'Newest Drug',
            'qty': 1,
            'mode': 'add'
        })  

        assert app.get_drug("Newest Drug")['qty'] == 1001

        #ensure system can handle strange inputs
        response = client.post('/inventory/modify_inventory', data={
            'name': 'Newest Drug',
            'qty': -1,
            'mode': 'add'
        })  

        assert app.get_drug("Newest Drug")['qty'] == 1000

        #check set function works
        response = client.post('/inventory/modify_inventory', data={
            'name': 'Newest Drug',
            'qty': 500,
            'mode': 'set'
        })  

        assert app.get_drug("Newest Drug")['qty'] == 500

        #check subtract function works
        response = client.post('/inventory/modify_inventory', data={
            'name': 'Newest Drug',
            'qty': 20,
            'mode': 'remove'
        })  

        assert app.get_drug("Newest Drug")['qty'] == 480

        #check we inventory functions with a second drug
        response = client.post('/inventory/modify_inventory', data={
            'name': 'Newest Drug 2',
            'qty': 100,
            'mode': 'set'
        })  

        assert app.get_drug("Newest Drug")['qty'] == 480
        assert app.get_drug("Newest Drug 2")['qty'] == 100

        #check we can remove drugs from inventory
        response = client.post('/inventory/modify_inventory', data={
            'name': 'Newest Drug',
            'qty': 0,
            'mode': 'delete'
        }) 

        inventory = app.get_inventory()
        assert len(inventory) == 1

        #Check inventory stays on refresh
        response = client.get("/inventory")

        inventory = app.get_inventory()
        assert len(inventory) == 1

        response = client.post('/inventory/modify_inventory', data={
            'name': 'Newest Drug 2',
            'qty': 0,
            'mode': 'delete'
        }) 

        inventory = app.get_inventory()
        assert len(inventory) == 0

        #reset
        app.inventory_ref.set({})

@pytest.mark.integration
def test_create_and_complete_order():
    with app.app.test_client() as client:
        # set db
        app.orders_ref.set({})
        app.inventory_ref.set({"H2O": {"name": "H2O", "qty": 1000000, "expires" : "N/A"}})
        orders = app.orders_ref.get()
        number_of_orders = 0
        if orders:
            number_of_orders = len(orders)
        # get main page
        response = client.get("/")
        assert response.status_code == 200
        # submit valid order
        response = client.post('/create_order', data={
            'name': 'John Doe', 
            'drug': 'H2O',  
            'qty': '5'  
        })
        assert response.status_code == 302
        assert response.location == '/' 
        # check order now exists
        orders = app.orders_ref.get()
        orders_dict = orders.to_dict() if hasattr(orders, 'to_dict') else orders
        assert len(orders_dict) == number_of_orders + 1
        order_id, order_details = list(orders_dict.items())[-1]
        name = order_details["name"]
        drug = order_details["drug"]
        qty = order_details["qty"]
        id = order_details["id"]
        assert name == "John Doe"
        assert drug == "H2O"
        assert qty == 5  
        assert "date" in order_details  # date field exists
        assert id == order_id  # order ID matches
        # complete order
        prev_qty = app.get_drug(drug)['qty'] 
        response = client.post('/complete_order/' + id)
        assert app.get_drug(drug)['qty'] == prev_qty - qty 
        assert app.get_order(order_id) is None
        assert response.status_code == 302

        #reset database
        app.orders_ref.set({})
        app.inventory_ref.set({})

@pytest.mark.integration
# Test adding a drug to the inventory, creating an order with it, then completing the order
def test_add_drug_and_create_order(client):
    # Set db to empty
    app.orders_ref.set({})
    app.inventory_ref.set({})
    # Get inventory page to make sure it's accessible
    response = client.get("/inventory")
    assert response.status_code == 200
    # Add drug to inventory
    response = client.post('/inventory/modify_inventory', data={
        'name': 'Test Drug', 
        'qty': 100,  
        'mode': '5'  
    })
    assert response.status_code == 302
    assert response.location == '/inventory' 
    # Check drug now exists
    assert len(app.inventory_ref.get()) == 1
    drug_ref = app.inventory_ref.child('Test Drug')
    assert drug_ref.get() is not None
    # Navigate to orders page
    response = client.get('/')
    assert response.status_code == 200
    # Create order with newly added drug
    response = client.post('/create_order', data={
        'name': 'Aleyssu',
        'drug': 'Test Drug', 
        'qty': 11
    })
    assert response.status_code == 302
    assert response.location == '/'
    orders = app.orders_ref.get()
    assert len(orders) == 1
    drug_id = orders.popitem()[0]
    # Complete order
    response = client.post('/complete_order/' + drug_id)
    assert response.status_code == 302
    assert response.location == '/'
    assert len(app.get_orders()) == 0
    assert drug_ref.child('qty').get() == 89
