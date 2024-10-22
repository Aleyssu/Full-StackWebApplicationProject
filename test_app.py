import pytest

def test_app_loads(client):
    #Check that our app runs properly
    response = client.get('/inventory')
    res = response.get_data(as_text=True)

    assert '<html lang="en">' in res
    



      




  