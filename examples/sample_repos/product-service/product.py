import requests

def get_product(product_id):
    response = requests.get(f"http://inventory-service/stock/{product_id}")
    return response.json()
