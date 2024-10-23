import pytest
import app

# Test client for Flask
@pytest.fixture
def client():
    with app.app.test_client() as client:
        yield client
        
def test_get_orders(client):
    response = client.get('/')
    html = response.get_data(as_text=True)
    # Ensure client recieves OK html response
    assert response.status_code == 200
    
def test_create_order(client):
    test_orders = []
    # Test entering every drug in the mock database
    for drug in app.drug_inventory:
        test_orders.append({'name': "a", 'drug':drug["name"], "qty":1})
    for order in test_orders:
        response = client.post('/create_order', data=order)
        # Ensure new order shows up in database exactly once
        assert len([o for o in app.orders if ((o['name'] == order['name']) and (o['drug'] == order['drug']) and (o['qty'] == order['qty']))]) == 1
    # Ensure successful redirect
    assert response.status_code == 302
    
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