from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ChangeType(str, Enum):
    STOCK_IN = "stock_in"
    STOCK_OUT = "stock_out"
    ADJUSTMENT = "adjustment"


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    sku: str = Field(..., min_length=1, max_length=50)
    price: Decimal = Field(..., gt=0)
    cost: Decimal = Field(..., gt=0)
    category_id: int
    is_active: bool = True


class ProductCreate(ProductBase):
    initial_stock: int = Field(default=0, ge=0)
    low_stock_threshold: int = Field(default=10, ge=0)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0)
    cost: Optional[Decimal] = Field(None, gt=0)
    category_id: Optional[int] = None
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: CategoryResponse
    current_stock: Optional[int] = None
    is_low_stock: Optional[bool] = None


class InventoryUpdate(BaseModel):
    change_type: ChangeType
    quantity_change: int
    reason: Optional[str] = Field(None, max_length=200)


class InventoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    low_stock_threshold: int
    is_low_stock: bool
    last_updated: datetime
    product: ProductResponse


class SaleCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., gt=0)
    customer_email: Optional[str] = Field(None, max_length=100)
    platform: Optional[str] = Field(None, max_length=50)
    order_id: Optional[str] = Field(None, max_length=100)
    sale_date: Optional[datetime] = None


class SaleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    total_amount: Decimal
    customer_email: Optional[str] = None
    platform: Optional[str] = None
    order_id: Optional[str] = None
    sale_date: datetime
    product: ProductResponse


class SalesAnalytics(BaseModel):
    total_revenue: Decimal
    total_orders: int
    total_quantity_sold: int
    average_order_value: Decimal
    period_start: datetime
    period_end: datetime


class RevenueComparison(BaseModel):
    current_period: SalesAnalytics
    previous_period: SalesAnalytics
    growth_rate: float
    growth_amount: Decimal
