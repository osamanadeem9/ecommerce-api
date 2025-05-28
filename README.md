# E-commerce Admin API Project



## Setup Instructions



**Using docker compose:**

```bash

git clone https://github.com/osamanadeem9/ecommerce-api
cd ecommerce-api

docker-compose up -d --build
```






## API Endpoints Overview



### Sales Analytics

-  `GET /sales/analytics?period=daily|weekly|monthly|annual` - Get sales analytics of current day/week/month/year

-  `GET /sales/revenue-comparison?period=daily|weekly|monthly|annual` - Compare revenue periods against the prev day or week etc.

-  `GET /sales/?platform=Walmart` - Get sales with different filters like start_date, end_date, platform or product_id.

-  `POST /sales/` - Create a new sale object



### Inventory Management

-  `GET /inventory/` - Get all the items available in inventory
-  `GET /inventory/low-stock` - Get inventory items which are low on stock
-  `PUT /inventory/{id}` - Update inventory level of any item.



### Product Management

-  `GET /products/` - Get list of all products
-  `GET /products/?low_stock_only=true&category_id=1` - Filter products based on different params like category_id, is_active or low_stock_only


-  `POST /products/` - Create a new product

-  `PUT /products/{id}` - Update a product detail



### Categories

-  `GET /categories/` - Get all categories of products

-  `POST /categories/` - Create a new category



## Key Features



1.  **Advanced Database Design:**

- Proper indexing for optimized queries

- Normalized schema preventing redundancy

- Audit logging for inventory changes



2.  **Senior-Level Code Architecture:**

- Service layer pattern

- Dependency injection

- Comprehensive error handling

- Type hints throughout



3.  **Production-Ready Features:**

- Database connection pooling

- Environment-based configuration

- Comprehensive test suite

- Docker containerization

- Proper logging and monitoring



4.  **Performance Optimizations:**

- Efficient database queries with joins

- Proper indexing strategy

- Batch operations for large datasets

- Query result pagination



<!-- ## Testing



```bash

# Run tests

pytest tests/ -v



# Run with coverage

pytest tests/ --cov=. --cov-report=html

``` -->



## API Usage Examples



### Create a new product:

```python

import requests

product_data = {

"name": "Apple Airpods",

"sku": "AIR-001",

"price": 99.99,

"cost": 55.00,

"category_id": 1,

"initial_stock": 100,

"low_stock_threshold": 15

}



response = requests.post("http://localhost:8000/products/", json=product_data)

```



### Get Sales Analytics:

```python

response = requests.get("http://localhost:8000/sales/analytics?period=monthly")

analytics = response.json()

print(f"Monthly revenue: ${analytics['total_revenue']}")

```



### Update Inventory:

```python

inventory_update = {

"change_type": "stock_in",

"quantity_change": 50,

"reason": "New stock"

}



response = requests.put("http://localhost:8000/inventory/1", json=inventory_update)

```



## Database Schema



The database consists of the following main entities:

-  **Categories**: Product categorization
-  **Products**: Details about the products
- **Inventory**: Stores the inventory levels and stock thresholds
-  **Sales**: Details about sales records for analytics
