from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from models import Product, Sale
from schemas import RevenueComparison, SalesAnalytics


class SalesService:
    def __init__(self, db: Session):
        self.db = db

    def get_sales_analytics(
        self,
        start_date: datetime,
        end_date: datetime,
        product_id: Optional[int] = None,
        category_id: Optional[int] = None,
        platform: Optional[str] = None,
    ) -> SalesAnalytics:
        query = self.db.query(
            func.sum(Sale.total_amount).label("total_revenue"),
            func.count(Sale.id).label("total_orders"),
            func.sum(Sale.quantity).label("total_quantity_sold"),
            func.avg(Sale.total_amount).label("average_order_value"),
        ).filter(and_(Sale.sale_date >= start_date, Sale.sale_date <= end_date))

        if product_id:
            query = query.filter(Sale.product_id == product_id)

        if category_id:
            query = query.join(Product).filter(Product.category_id == category_id)

        if platform:
            query = query.filter(Sale.platform == platform)

        result = query.first()

        return SalesAnalytics(
            total_revenue=result.total_revenue or Decimal("0"),
            total_orders=result.total_orders or 0,
            total_quantity_sold=result.total_quantity_sold or 0,
            average_order_value=result.average_order_value or Decimal("0"),
            period_start=start_date,
            period_end=end_date,
        )

    def get_revenue_comparison(
        self,
        current_start: datetime,
        current_end: datetime,
        previous_start: datetime,
        previous_end: datetime,
        **filters
    ) -> RevenueComparison:
        current_analytics = self.get_sales_analytics(
            current_start, current_end, **filters
        )
        previous_analytics = self.get_sales_analytics(
            previous_start, previous_end, **filters
        )

        growth_amount = (
            current_analytics.total_revenue - previous_analytics.total_revenue
        )
        growth_rate = float(
            (growth_amount / previous_analytics.total_revenue * 100)
            if previous_analytics.total_revenue > 0
            else 0
        )

        return RevenueComparison(
            current_period=current_analytics,
            previous_period=previous_analytics,
            growth_rate=growth_rate,
            growth_amount=growth_amount,
        )
