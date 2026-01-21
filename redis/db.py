FAKE_DB = [
    {"id": 1 , "name": "iphone", "price": 70000},
    {"id":2, "name": "MacBook", "price": 120000}
]

def get_all_products():
    return FAKE_DB

def add_product(product: dict):
    FAKE_DB.append(product)