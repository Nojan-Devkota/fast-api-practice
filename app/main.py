from datetime import datetime, timezone
from uuid import uuid4
from fastapi import FastAPI, HTTPException, Query, Path
from services.products import get_all_products
from schema.product_schema import Product
from typing import Literal
from services.products import add_product

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI"}


@app.get("/allproducts")
def get_products():
    return get_all_products()


@app.get("/products")
def list_product(
    name: str = Query(
        min_length=1,
        max_length=50,
        description="Search by product name",
        examples="Xiaomi",
    ),
    sort_by_price: bool = Query(
        default=False, description="Sort by price", example=True
    ),
    order_of_sort: Literal["asc", "desc"] = Query(
        default="asc",
        description="Order of sort",
    ),
    limit: int = Query(
        default=10, ge=1, le=100, description="Limit the number of products", example=10
    ),
):
    products = get_all_products()

    if name:
        name = name.strip().lower()
        products = [p for p in products if name in p.get("name", "").lower()]

    if not products:
        raise HTTPException(status_code=404, detail="Product not found")

    if sort_by_price:
        products.sort(
            key=lambda x: x.get("price", 0),
            reverse=True if order_of_sort == "desc" else False,
        )

    products = products[:limit]
    total = len(products)

    return {"total": total, "limit": limit, "items": products}


@app.get("/products/{product_id}")
def get_product_by_id(
    product_id: str = Path(
        min_length=36,
        max_length=36,
        description="UUID of the product",
        examples="0005a4ea-ce3f-4dd7-bee0-f4ccc70fea6a",
    ),
):
    products = get_all_products()

    for product in products:
        if product.get("id") == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


@app.post("/products", status_code=201)
def create_product(product: Product):
    product.id = uuid4()
    
    product.created_at = datetime.now(timezone.utc)
    
    try:
        product_dict = product.model_dump(mode="json")
        add_product(product_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "Product created successfully", "product": product}