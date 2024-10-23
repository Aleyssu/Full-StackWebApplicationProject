import pytest
import app

# Test client for Flask
@pytest.fixture
def client():
    with app.app.test_client() as client:
        yield client
        
def test_create_order_valid_input(client):
    # Simulate a POST request to the '/create_order' route with valid form data
    response = client.post('/create_order', data={
        'name': 'John Doe',  # Valid: only letters and spaces
        'drug': 'H20',  # Valid: selected option
        'qty': '5'  # Valid: positive number
    })

    # Check that the response redirects (302 for a successful redirect)
    assert response.status_code == 302
    assert response.location == '/'  # Assuming the redirect is to the index page

def test_create_order_invalid_name(client):
    # Simulate a POST request to the '/create_order' route with invalid name
    response = client.post('/create_order', data={
        'name': 'John123',  # Invalid: contains numbers
        'drug': 'H20',
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
        'drug': 'H20',
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
    #Check that our app runs properly
    response = client.get('/inventory')
    res = response.get_data(as_text=True)

    assert '<div class="row list1" style="display: flex;">' in res

def test_different_sort(client):
    response = client.get('/inventory?sort=quantity')
    res = response.get_data(as_text=True)

    assert '800000' in res
    assert '200' in res
        
def test_get_orders(client):
    response = client.get('/')
    html = response.get_data(as_text=True)
    # Ensure client recieves OK html response
    assert response.status_code == 200
    
def test_complete_order(client):
    # Try completing every order in the database
    for order in app.orders:
        drug = app.get_drug(order["drug"])
        prev_qty = app.get_drug(drug['name'])['qty']
        removed_qty = order['qty']
        order_id = order['id']
        
        response = client.post('/complete_order/' + order_id)
        # Ensure inventory drug qty is updated appropriately
        assert drug['qty'] == prev_qty - removed_qty
        # Ensure order has been removed from database
        assert app.get_order(order_id) is None
        # Ensure successful redirect
        assert response.status_code == 302