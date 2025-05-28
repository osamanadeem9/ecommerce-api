from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models import Inventory, Product, Sale
from schemas import RevenueComparison, SaleCreate, SaleResponse, SalesAnalytics
from services.sales_service import SalesService

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.post("/", response_model=SaleResponse)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    """Record a new sale."""
    product = db.query(Product).filter(Product.id == sale.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_amount = sale.quantity * sale.unit_price

    sale_data = sale.dict()
    if not sale_data.get("sale_date"):
        sale_data["sale_date"] = datetime.utcnow()

    db_sale = Sale(**sale_data, total_amount=total_amount)
    db.add(db_sale)

    inventory = (
        db.query(Inventory).filter(Inventory.product_id == sale.product_id).first()
    )
    if inventory:
        inventory.quantity = max(0, inventory.quantity - sale.quantity)

    try:
        db.commit()
        db.refresh(db_sale)

        sale_with_product = (
            db.query(Sale)
            .options(joinedload(Sale.product).joinedload(Product.category))
            .filter(Sale.id == db_sale.id)
            .first()
        )

        return sale_with_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to create sale")


@router.get("/", response_model=List[SaleResponse])
def get_sales(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    product_id: Optional[int] = Query(None),
    platform: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Get sales with filtering options."""
    query = db.query(Sale).options(
        joinedload(Sale.product).joinedload(Product.category)
    )

    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    if product_id:
        query = query.filter(Sale.product_id == product_id)
    if platform:
        query = query.filter(Sale.platform == platform)

    sales = query.order_by(Sale.sale_date.desc()).offset(skip).limit(limit).all()
    return sales


@router.get("/analytics", response_model=SalesAnalytics, tags=["Sales Analytics"])
def get_sales_analytics(
    period: str = Query(..., regex="^(daily|weekly|monthly|annual)$"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    product_id: Optional[int] = Query(None),
    category_id: Optional[int] = Query(None),
    platform: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Get sales analytics for specified period."""
    if not start_date or not end_date:
        end_date = datetime.utcnow()
        if period == "daily":
            start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "weekly":
            start_date = end_date - timedelta(days=7)
        elif period == "monthly":
            start_date = end_date - timedelta(days=30)
        else:
            start_date = end_date - timedelta(days=365)

    sales_service = SalesService(db)
    return sales_service.get_sales_analytics(
        start_date=start_date,
        end_date=end_date,
        product_id=product_id,
        category_id=category_id,
        platform=platform,
    )


@router.get(
    "/revenue-comparison", response_model=RevenueComparison, tags=["Sales Analytics"]
)
def get_revenue_comparison(
    period: str = Query(..., regex="^(daily|weekly|monthly|annual)$"),
    db: Session = Depends(get_db),
):
    """Compare revenue between current and previous periods."""
    end_date = datetime.utcnow()

    if period == "daily":
        current_start = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
        previous_start = current_start - timedelta(days=1)
        previous_end = current_start
    elif period == "weekly":
        current_start = end_date - timedelta(days=7)
        previous_start = current_start - timedelta(days=7)
        previous_end = current_start
    elif period == "monthly":
        current_start = end_date - timedelta(days=30)
        previous_start = current_start - timedelta(days=30)
        previous_end = current_start
    else:
        current_start = end_date - timedelta(days=365)
        previous_start = current_start - timedelta(days=365)
        previous_end = current_start

    sales_service = SalesService(db)
    return sales_service.get_revenue_comparison(
        current_start=current_start,
        current_end=end_date,
        previous_start=previous_start,
        previous_end=previous_end,
    )
