import pytest

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
    
    
    



      




  