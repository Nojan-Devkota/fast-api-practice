from datetime import datetime
from pydantic import (
    BaseModel,
    Field,
    AnyUrl,
    field_validator,
    model_validator,
    computed_field,
    EmailStr,
)
from typing import Annotated, Literal, List, Optional
from uuid import UUID


class Seller(BaseModel):
    """Seller Schema"""

    seller_id: UUID
    name: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
            title="Seller Name",
            description="Name of the seller",
            examples=["Xiaomi", "Samsung"],
        ),
    ]
    email: EmailStr
    website: AnyUrl

    @field_validator("email", mode="after")
    @classmethod
    def validate_email(cls, value: EmailStr) -> EmailStr:
        allowed_domains = [
            "mistore.in",
            "realmeofficial.in",
            "samsungindia.in",
            "lenovostore.in",
        ]
        domain = str(value).split("@")[-1]

        if domain not in allowed_domains:
            raise ValueError("Invalid email domain")

        return value


class Dimensions(BaseModel):
    """Dimensions Schema"""

    length: Annotated[
        float,
        Field(
            gt=1,
            strict=True,
            title="Length",
            description="Length of the product",
            examples=[10.00, 20.5],
        ),
    ]
    width: Annotated[
        float,
        Field(
            gt=1,
            strict=True,
            title="Width",
            description="Width of the product",
            examples=[10.00, 20.5],
        ),
    ]
    height: Annotated[
        float,
        Field(
            gt=1,
            strict=True,
            title="Height",
            description="Height of the product",
            examples=[10.00, 20.5],
        ),
    ]


class Product(BaseModel):
    """Product Schema"""

    id: UUID
    sku: Annotated[
        str,
        Field(
            min_length=6,
            max_length=36,
            title="SKU",
            description="Stock Keeping Unit",
            examples=["123-abc-456", "ads-456-fgh"],
        ),
    ]
    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=200,
            title="Product Name",
            description="Name of the product",
            examples=["Xiaomi Model Pro", "Samsung S25 Ultra"],
        ),
    ]

    description: Annotated[
        str,
        Field(
            title="Product Description",
            max_length=200,
            description="Description of the product",
        ),
    ]

    category: Annotated[
        str,
        Field(
            title="Category",
            min_length=1,
            max_length=100,
            description="Category of the product",
            examples=["mobiles", "laptops"],
        ),
    ]

    brand: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
            title="Brand",
            description="Brand of the product",
            examples=["Xiaomi", "Samsung"],
        ),
    ]
    price: Annotated[
        float,
        Field(
            gt=1,
            strict=True,
            title="Price",
            description="Price of the product",
            examples=[500.00, 1000.20],
        ),
    ]

    currency: Literal["NPR", "USD", "EUR"] = "NPR"

    discount_percent: Annotated[
        float,
        Field(
            ge=0,
            strict=True,
            title="Discount Percent",
            description="Discount percent of the product (in %)",
            examples=[10.00, 20.5],
        ),
    ]

    stock: Annotated[
        int,
        Field(
            ge=0,
            title="Stock",
            description="Stock of the product",
            examples=[10, 20, 30],
        ),
    ]

    is_active: Annotated[
        bool,
        Field(
            default=True, title="Active", description="Whether the product is active"
        ),
    ]
    rating: Annotated[
        float,
        Field(
            ge=0,
            le=5,
            title="Rating",
            description="Rating of the product",
            examples=[4.5, 5.0],
            strict=True,
        ),
    ]

    tags: Annotated[
        Optional[List[str]],
        Field(
            title="Tags",
            default=None,
            max_length=10,
            description="Tags of the product up to 10 tags",
            examples=[["charger", "amoled", "tablet"]],
        ),
    ]

    image_urls: Annotated[
        List[AnyUrl],
        Field(
            min_length=1,
            title="Image URLs",
            description="List of image URLs",
            examples=[
                [
                    "https://cdn.example.com/xiaomi/front.png",
                    "https://cdn.example.com/xiaomi/back.png",
                ]
            ],
        ),
    ]

    dimensions_cm: Annotated[
        Dimensions,
        Field(title="Dimensions", description="Dimensions of the product"),
    ]
    seller: Annotated[
        Seller,
        Field(title="Seller", description="Seller of the product"),
    ]

    created_at: Annotated[
        datetime,
        Field(
            title="Created At",
            description="When the product was created",
            examples=["2022-01-01T00:00:00Z"],
        ),
    ]

    @field_validator("sku", mode="after")
    @classmethod
    def validate_sku(cls, value: str):

        if "-" not in value:
            raise ValueError("SKU must be in the format of XXX-XXX-XXX")

        last = value.split("-")[-1]

        if not (len(last) == 3 and last.isdigit()):
            raise ValueError("SKU must be in the format of XXX-XXX-XXX")
        return value

    @model_validator(mode="after")
    @classmethod
    def validate_business_rules(cls, model: "Product") -> "Product":
        if model.stock == 0 and model.is_active:
            raise ValueError("If stock is 0, product should be inactive")

        if model.discount_percent > 0 and model.rating == 0:
            raise ValueError(
                "If discount percent is greater than 0, product should have a rating"
            )
        return model

    @computed_field
    def selling_price(self) -> float:
        return self.price * (1 - self.discount_percent / 100)


class SellerUpdate(BaseModel):
    """Seller Schema"""

    seller_id: UUID
    name: Annotated[
        Optional[str],
        Field(
            min_length=1,
            max_length=100,
            title="Seller Name",
            description="Name of the seller",
            examples=["Xiaomi", "Samsung"],
        ),
    ] = None
    email: Optional[EmailStr] = None
    website: Optional[AnyUrl] = None

    @field_validator("email", mode="after")
    @classmethod
    def validate_email(cls, value: EmailStr) -> EmailStr:
        allowed_domains = [
            "mistore.in",
            "realmeofficial.in",
            "samsungindia.in",
            "lenovostore.in",
        ]
        domain = str(value).split("@")[-1]

        if domain not in allowed_domains:
            raise ValueError("Invalid email domain")

        return value


class DimensionsUpdate(BaseModel):
    """Dimensions Schema"""

    length: Annotated[
        Optional[float],
        Field(
            gt=1,
            strict=True,
            title="Length",
            description="Length of the product",
            examples=[10.00, 20.5],
        ),
    ] = None
    width: Annotated[
        Optional[float],
        Field(
            gt=1,
            strict=True,
            title="Width",
            description="Width of the product",
            examples=[10.00, 20.5],
        ),
    ] = None
    height: Annotated[
        Optional[float],
        Field(
            gt=1,
            strict=True,
            title="Height",
            description="Height of the product",
            examples=[10.00, 20.5],
        ),
    ] = None


class ProductUpdate(BaseModel):
    """Product Schema"""

    id: Optional[UUID] = None
    sku: Annotated[
        Optional[str],
        Field(
            min_length=6,
            max_length=36,
            title="SKU",
            description="Stock Keeping Unit",
            examples=["123-abc-456", "ads-456-fgh"],
        ),
    ] = None
    name: Annotated[
        Optional[str],
        Field(
            min_length=3,
            max_length=200,
            title="Product Name",
            description="Name of the product",
            examples=["Xiaomi Model Pro", "Samsung S25 Ultra"],
        ),
    ] = None

    description: Annotated[
        Optional[str],
        Field(
            title="Product Description",
            max_length=200,
            description="Description of the product",
        ),
    ] = None

    category: Annotated[
        Optional[str],
        Field(
            title="Category",
            min_length=1,
            max_length=100,
            description="Category of the product",
            examples=["mobiles", "laptops"],
        ),
    ] = None

    brand: Annotated[
        Optional[str],
        Field(
            min_length=1,
            max_length=100,
            title="Brand",
            description="Brand of the product",
            examples=["Xiaomi", "Samsung"],
        ),
    ] = None
    price: Annotated[
        Optional[float],
        Field(
            gt=1,
            strict=True,
            title="Price",
            description="Price of the product",
            examples=[500.00, 1000.20],
        ),
    ] = None

    currency: Optional[Literal["NPR", "USD", "EUR"]] = None

    discount_percent: Annotated[
        Optional[float],
        Field(
            ge=0,
            strict=True,
            title="Discount Percent",
            description="Discount percent of the product (in %)",
            examples=[10.00, 20.5],
        ),
    ] = None

    stock: Annotated[
        Optional[int],
        Field(
            ge=0,
            title="Stock",
            description="Stock of the product",
            examples=[10, 20, 30],
        ),
    ] = None

    is_active: Annotated[
        Optional[bool],
        Field(
            default=True, title="Active", description="Whether the product is active"
        ),
    ] = None
    rating: Annotated[
        Optional[float],
        Field(
            ge=0,
            le=5,
            title="Rating",
            description="Rating of the product",
            examples=[4.5, 5.0],
            strict=True,
        ),
    ] = None

    tags: Annotated[
        Optional[List[str]],
        Field(
            title="Tags",
            default=None,
            max_length=10,
            description="Tags of the product up to 10 tags",
            examples=[["charger", "amoled", "tablet"]],
        ),
    ] = None

    image_urls: Annotated[
        Optional[List[AnyUrl]],
        Field(
            min_length=1,
            title="Image URLs",
            description="List of image URLs",
            examples=[
                [
                    "https://cdn.example.com/xiaomi/front.png",
                    "https://cdn.example.com/xiaomi/back.png",
                ]
            ],
        ),
    ] = None

    dimensions_cm: Annotated[
        Optional[DimensionsUpdate],
        Field(title="Dimensions", description="Dimensions of the product"),
    ] = None
    seller: Annotated[
        Optional[SellerUpdate],
        Field(title="Seller", description="Seller of the product"),
    ] = None

    created_at: Annotated[
        Optional[datetime],
        Field(
            title="Created At",
            description="When the product was created",
            examples=["2022-01-01T00:00:00Z"],
        ),
    ] = None

    @field_validator("sku", mode="after")
    @classmethod
    def validate_sku(cls, value: str):

        if "-" not in value:
            raise ValueError("SKU must be in the format of XXX-XXX-XXX")

        last = value.split("-")[-1]

        if not (len(last) == 3 and last.isdigit()):
            raise ValueError("SKU must be in the format of XXX-XXX-XXX")
        return value

    @model_validator(mode="after")
    @classmethod
    def validate_business_rules(cls, model: "ProductUpdate") -> "ProductUpdate":
        if model.stock is not None and model.is_active is not None:
            if model.stock == 0 and model.is_active:
                raise ValueError("If stock is 0, product should be inactive")

        if model.discount_percent is not None and model.rating is not None:
            if model.discount_percent > 0 and model.rating == 0:
                raise ValueError(
                    "If discount percent is greater than 0, product should have a rating"
                )
        return model

    @computed_field
    def selling_price(self) -> Optional[float]:
        if self.price is not None and self.discount_percent is not None:
            return self.price * (1 - self.discount_percent / 100)
        return None
