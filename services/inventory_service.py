from typing import List

from sqlalchemy.orm import Session

from models import Inventory, InventoryLog, Product
from schemas import ChangeType, InventoryUpdate


class InventoryService:
    def __init__(self, db: Session):
        self.db = db

    def update_inventory(
        self, inventory_id: int, update_data: InventoryUpdate
    ) -> Inventory:
        inventory = (
            self.db.query(Inventory).filter(Inventory.id == inventory_id).first()
        )
        if not inventory:
            raise ValueError("Inventory not found")

        previous_quantity = inventory.quantity

        if update_data.change_type == ChangeType.STOCK_IN:
            new_quantity = previous_quantity + update_data.quantity_change
        elif update_data.change_type == ChangeType.STOCK_OUT:
            new_quantity = max(0, previous_quantity - update_data.quantity_change)
        else:
            new_quantity = max(0, previous_quantity + update_data.quantity_change)

        inventory.quantity = new_quantity

        log_entry = InventoryLog(
            inventory_id=inventory_id,
            change_type=update_data.change_type.value,
            quantity_change=update_data.quantity_change,
            previous_quantity=previous_quantity,
            new_quantity=new_quantity,
            reason=update_data.reason,
        )

        self.db.add(log_entry)
        self.db.commit()
        self.db.refresh(inventory)

        return inventory

    def get_low_stock_items(self) -> List[Inventory]:
        return (
            self.db.query(Inventory)
            .join(Product)
            .filter(
                Inventory.quantity <= Inventory.low_stock_threshold,
                Product.is_active == True,
            )
            .all()
        )
