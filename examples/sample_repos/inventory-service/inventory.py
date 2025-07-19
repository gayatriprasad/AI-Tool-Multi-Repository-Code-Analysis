stock = {"item-1": 100, "item-2": 45}

def get_stock(item_id):
    return {"stock": stock.get(item_id, 0)}
 