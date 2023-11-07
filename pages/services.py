import requests

def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    
def get_name(params={}):
    response = generate_request('34.95.42.190:8000/api/products/', params)
    if response:
       product = response.get('Products')[0]
       return product.get('name')

    return ''

def get_price(params={}):
    response = generate_request('34.95.42.190:8000/api/products/', params)
    if response:
       product = response.get('Products')[0]
       return product.get('price')

    return ''

def get_color(params={}):
    response = generate_request('34.95.42.190:8000/api/products/', params)
    if response:
       product = response.get('Products')[0]
       return product.get('color')

    return ''

def get_size(params={}):
    response = generate_request('34.95.42.190:8000/api/products/', params)
    if response:
       product = response.get('Products')[0]
       return product.get('size')

    return ''

def get_description(params={}):
    response = generate_request('34.95.42.190:8000/api/products/', params)
    if response:
       product = response.get('Products')[0]
       return product.get('description')

    return ''

