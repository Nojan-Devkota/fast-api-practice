import json
from pathlib import Path
from typing import List, Dict

DATA_FILE = Path(
    "C:/Nojan/OneDrive - Texas State University/Fast Api Tut/FastApi-ecommerce/app/data/products.json"
)


def load_products() -> List[Dict]:
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_all_products() -> List[Dict]:
    return load_products()


def save_products(products: list[Dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(products, file, indent=4, ensure_ascii=False)


def add_product(product: Dict) -> Dict:
    products = get_all_products()

    if any(p.get("sku") == product.get("sku") for p in products):
        raise ValueError("Product already exists")

    products.append(product)
    save_products(products)

    return product


def delete_product(id: str) -> Dict:
    products = get_all_products()

    for idx, p in enumerate(products):
        if p.get("id") == id:
            del products[idx]
            save_products(products)
            return {"message": "Product deleted successfully"}

    raise ValueError("Product not found")


def update_product(id: str, updated_data: dict) -> dict:
    products = get_all_products()

    for idx, p in enumerate(products):
        if p.get("id") == id:
            p.update(updated_data)
            save_products(products)
            return {"message": "Product updated successfully", "product": p}

    raise ValueError("Product not found")
