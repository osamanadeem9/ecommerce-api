from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models import Inventory, Product
from schemas import InventoryResponse, InventoryUpdate
from services.inventory_service import InventoryService

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("/", response_model=List[InventoryResponse])
def get_inventory(
    skip: int = 0,
    limit: int = 100,
    low_stock_only: Optional[bool] = Query(False),
    db: Session = Depends(get_db),
):
    """Get inventory status with filtering options."""
    query = db.query(Inventory).options(
        joinedload(Inventory.product).joinedload(Product.category)
    )

    if low_stock_only:
        query = query.filter(Inventory.quantity <= Inventory.low_stock_threshold)

    inventory_items = query.offset(skip).limit(limit).all()
    return inventory_items


@router.put("/{inventory_id}", response_model=InventoryResponse)
def update_inventory(
    inventory_id: int, update_data: InventoryUpdate, db: Session = Depends(get_db)
):
    """Update inventory levels with logging."""
    inventory_service = InventoryService(db)

    try:
        updated_inventory = inventory_service.update_inventory(
            inventory_id, update_data
        )

        inventory_with_product = (
            db.query(Inventory)
            .options(joinedload(Inventory.product).joinedload(Product.category))
            .filter(Inventory.id == inventory_id)
            .first()
        )

        return inventory_with_product
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to update inventory")


@router.get("/low-stock", response_model=List[InventoryResponse])
def get_low_stock_alerts(db: Session = Depends(get_db)):
    """Get all products with low stock levels."""
    inventory_service = InventoryService(db)
    low_stock_items = inventory_service.get_low_stock_items()
    return low_stock_items
