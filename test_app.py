import pytest

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