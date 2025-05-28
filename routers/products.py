from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models import Category, Inventory, Product
from schemas import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product with initial inventory."""
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    product_data = product.dict()
    initial_stock = product_data.pop("initial_stock")
    low_stock_threshold = product_data.pop("low_stock_threshold")

    db_product = Product(**product_data)
    db.add(db_product)
    db.flush()

    db_inventory = Inventory(
        product_id=db_product.id,
        quantity=initial_stock,
        low_stock_threshold=low_stock_threshold,
    )
    db.add(db_inventory)

    try:
        db.commit()
        db.refresh(db_product)

        product_with_relations = (
            db.query(Product)
            .options(joinedload(Product.category), joinedload(Product.inventory))
            .filter(Product.id == db_product.id)
            .first()
        )

        response_data = ProductResponse.model_validate(product_with_relations)
        response_data.current_stock = (
            product_with_relations.inventory.quantity
            if product_with_relations.inventory
            else 0
        )
        response_data.is_low_stock = (
            product_with_relations.inventory.is_low_stock
            if product_with_relations.inventory
            else False
        )

        return response_data
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="SKU already exists")


@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = Query(None),
    is_active: Optional[bool] = Query(None),
    low_stock_only: Optional[bool] = Query(False),
    db: Session = Depends(get_db),
):
    """Get products with filtering options."""
    query = db.query(Product).options(
        joinedload(Product.category), joinedload(Product.inventory)
    )

    if category_id:
        query = query.filter(Product.category_id == category_id)

    if is_active is not None:
        query = query.filter(Product.is_active == is_active)

    if low_stock_only:
        query = query.join(Inventory).filter(
            Inventory.quantity <= Inventory.low_stock_threshold
        )

    products = query.offset(skip).limit(limit).all()

    response_products = []
    for product in products:
        response_data = ProductResponse.model_validate(product)
        response_data.current_stock = (
            product.inventory.quantity if product.inventory else 0
        )
        response_data.is_low_stock = (
            product.inventory.is_low_stock if product.inventory else False
        )
        response_products.append(response_data)

    return response_products


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)
):
    """Update a product."""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_update.dict(exclude_unset=True)

    if "category_id" in update_data:
        category = (
            db.query(Category).filter(Category.id == update_data["category_id"]).first()
        )
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

    for field, value in update_data.items():
        setattr(db_product, field, value)

    try:
        db.commit()
        db.refresh(db_product)

        product_with_relations = (
            db.query(Product)
            .options(joinedload(Product.category), joinedload(Product.inventory))
            .filter(Product.id == product_id)
            .first()
        )

        response_data = ProductResponse.model_validate(product_with_relations)
        response_data.current_stock = (
            product_with_relations.inventory.quantity
            if product_with_relations.inventory
            else 0
        )
        response_data.is_low_stock = (
            product_with_relations.inventory.is_low_stock
            if product_with_relations.inventory
            else False
        )

        return response_data
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Update failed")
