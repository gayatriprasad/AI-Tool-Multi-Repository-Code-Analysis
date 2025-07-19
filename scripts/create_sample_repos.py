import os

BASE = "examples/sample_repos"
os.makedirs(BASE, exist_ok=True)

repos = {
    "user-service": {
        "app.py": 'from flask import Flask\napp = Flask(__name__)\n@app.route("/login", methods=["POST"])\ndef login():\n    return {"token": "abc"}\n'
    },
    "product-service": {
        "product.py": 'import requests\ndef get_product(id):\n    return requests.get(f"http://inventory/{id}").json()'
    },
    "inventory-service": {
        "inventory.py": 'stock = {"item-1": 10}\ndef get_stock(id): return stock.get(id, 0)'
    }
}

for repo, files in repos.items():
    path = os.path.join(BASE, repo)
    os.makedirs(path, exist_ok=True)
    for fname, content in files.items():
        with open(os.path.join(path, fname), "w") as f:
            f.write(content)

print("✅ Sample repos created.")
