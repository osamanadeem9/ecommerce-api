def seed_database():
    """Populate database with demo data for Amazon & Walmart products."""
    import random
    from datetime import datetime, timedelta
    from decimal import Decimal

    from database import SessionLocal
    from models import Category, Inventory, Product, Sale

    db = SessionLocal()

    try:
        from database import engine
        from models import Base, Category, Inventory, Product, Sale

        Base.metadata.create_all(bind=engine)

        db.query(Sale).delete()
        db.query(Inventory).delete()
        db.query(Product).delete()
        db.query(Category).delete()
        db.commit()

        categories_data = [
            {
                "name": "Electronics",
                "description": "Electronic devices and accessories",
            },
            {
                "name": "Home & Garden",
                "description": "Home improvement and garden supplies",
            },
            {
                "name": "Clothing & Accessories",
                "description": "Fashion and personal accessories",
            },
            {
                "name": "Health & Beauty",
                "description": "Health care and beauty products",
            },
            {
                "name": "Sports & Outdoors",
                "description": "Sports equipment and outdoor gear",
            },
            {
                "name": "Books & Media",
                "description": "Books, movies, and digital media",
            },
            {
                "name": "Automotive",
                "description": "Car parts and automotive accessories",
            },
            {"name": "Toys & Games", "description": "Children's toys and board games"},
        ]

        categories = []
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.add(category)
            categories.append(category)

        db.flush()

        products_data = [
            {
                "name": "Wireless Bluetooth Headphones",
                "sku": "WBH-001",
                "price": Decimal("79.99"),
                "cost": Decimal("35.00"),
                "category_id": categories[0].id,
            },
            {
                "name": "Smart Phone Charger Cable",
                "sku": "SPC-002",
                "price": Decimal("15.99"),
                "cost": Decimal("4.50"),
                "category_id": categories[0].id,
            },
            {
                "name": "Portable Power Bank 10000mAh",
                "sku": "PPB-003",
                "price": Decimal("29.99"),
                "cost": Decimal("12.00"),
                "category_id": categories[0].id,
            },
            {
                "name": "LED Desk Lamp with USB Port",
                "sku": "LDL-004",
                "price": Decimal("45.99"),
                "cost": Decimal("18.00"),
                "category_id": categories[0].id,
            },
            {
                "name": "Wireless Mouse",
                "sku": "WM-005",
                "price": Decimal("24.99"),
                "cost": Decimal("8.50"),
                "category_id": categories[0].id,
            },
            {
                "name": "Stainless Steel Kitchen Knife Set",
                "sku": "KNS-006",
                "price": Decimal("89.99"),
                "cost": Decimal("35.00"),
                "category_id": categories[1].id,
            },
            {
                "name": "Indoor Plant Pot Set",
                "sku": "IPS-007",
                "price": Decimal("34.99"),
                "cost": Decimal("12.00"),
                "category_id": categories[1].id,
            },
            {
                "name": "Memory Foam Pillow",
                "sku": "MFP-008",
                "price": Decimal("39.99"),
                "cost": Decimal("15.00"),
                "category_id": categories[1].id,
            },
            {
                "name": "Garden Hose 50ft",
                "sku": "GH-009",
                "price": Decimal("49.99"),
                "cost": Decimal("20.00"),
                "category_id": categories[1].id,
            },
            {
                "name": "Cotton T-Shirt Pack (3-Pack)",
                "sku": "CTS-010",
                "price": Decimal("24.99"),
                "cost": Decimal("8.00"),
                "category_id": categories[2].id,
            },
            {
                "name": "Leather Wallet",
                "sku": "LW-011",
                "price": Decimal("59.99"),
                "cost": Decimal("22.00"),
                "category_id": categories[2].id,
            },
            {
                "name": "Baseball Cap",
                "sku": "BC-012",
                "price": Decimal("19.99"),
                "cost": Decimal("6.50"),
                "category_id": categories[2].id,
            },
            {
                "name": "Winter Gloves",
                "sku": "WG-013",
                "price": Decimal("16.99"),
                "cost": Decimal("5.50"),
                "category_id": categories[2].id,
            },
            {
                "name": "Electric Toothbrush",
                "sku": "ET-014",
                "price": Decimal("69.99"),
                "cost": Decimal("28.00"),
                "category_id": categories[3].id,
            },
            {
                "name": "Vitamin D3 Supplements",
                "sku": "VD3-015",
                "price": Decimal("19.99"),
                "cost": Decimal("6.00"),
                "category_id": categories[3].id,
            },
            {
                "name": "Face Moisturizer SPF 30",
                "sku": "FM-016",
                "price": Decimal("32.99"),
                "cost": Decimal("12.50"),
                "category_id": categories[3].id,
            },
            {
                "name": "Hair Styling Gel",
                "sku": "HSG-017",
                "price": Decimal("12.99"),
                "cost": Decimal("4.00"),
                "category_id": categories[3].id,
            },
            {
                "name": "Yoga Mat Premium",
                "sku": "YM-018",
                "price": Decimal("44.99"),
                "cost": Decimal("18.00"),
                "category_id": categories[4].id,
            },
            {
                "name": "Water Bottle Insulated 32oz",
                "sku": "WB-019",
                "price": Decimal("28.99"),
                "cost": Decimal("10.00"),
                "category_id": categories[4].id,
            },
            {
                "name": "Resistance Bands Set",
                "sku": "RBS-020",
                "price": Decimal("19.99"),
                "cost": Decimal("7.50"),
                "category_id": categories[4].id,
            },
            {
                "name": "Camping Flashlight LED",
                "sku": "CFL-021",
                "price": Decimal("22.99"),
                "cost": Decimal("8.00"),
                "category_id": categories[4].id,
            },
            {
                "name": "Bestseller Novel Collection",
                "sku": "BNC-022",
                "price": Decimal("14.99"),
                "cost": Decimal("4.50"),
                "category_id": categories[5].id,
            },
            {
                "name": "Educational Science Kit",
                "sku": "ESK-023",
                "price": Decimal("39.99"),
                "cost": Decimal("16.00"),
                "category_id": categories[5].id,
            },
            {
                "name": "Puzzle 1000 Pieces",
                "sku": "P1000-024",
                "price": Decimal("18.99"),
                "cost": Decimal("6.50"),
                "category_id": categories[5].id,
            },
            {
                "name": "Car Phone Mount",
                "sku": "CPM-025",
                "price": Decimal("21.99"),
                "cost": Decimal("7.50"),
                "category_id": categories[6].id,
            },
            {
                "name": "Emergency Car Kit",
                "sku": "ECK-026",
                "price": Decimal("54.99"),
                "cost": Decimal("22.00"),
                "category_id": categories[6].id,
            },
            {
                "name": "Car Air Freshener Pack",
                "sku": "CAF-027",
                "price": Decimal("8.99"),
                "cost": Decimal("2.50"),
                "category_id": categories[6].id,
            },
            {
                "name": "Building Blocks Set 500pc",
                "sku": "BBS-028",
                "price": Decimal("49.99"),
                "cost": Decimal("18.00"),
                "category_id": categories[7].id,
            },
            {
                "name": "Board Game Strategy",
                "sku": "BGS-029",
                "price": Decimal("34.99"),
                "cost": Decimal("14.00"),
                "category_id": categories[7].id,
            },
            {
                "name": "Remote Control Car",
                "sku": "RCC-030",
                "price": Decimal("79.99"),
                "cost": Decimal("32.00"),
                "category_id": categories[7].id,
            },
        ]

        products = []
        for prod_data in products_data:
            product = Product(**prod_data)
            db.add(product)
            products.append(product)

        db.flush()

        inventories = []
        for product in products:
            inventory = Inventory(
                product_id=product.id,
                quantity=random.randint(10, 500),
                low_stock_threshold=random.randint(5, 25),
            )
            db.add(inventory)
            inventories.append(inventory)

        db.flush()

        platforms = ["Amazon", "Walmart"]
        customer_emails = [
            "customer1@email.com",
            "customer2@email.com",
            "customer3@email.com",
            "customer4@email.com",
            "customer5@email.com",
            "customer6@email.com",
            "customer7@email.com",
            "customer8@email.com",
            "customer9@email.com",
            "customer10@email.com",
        ]

        start_date = datetime.utcnow() - timedelta(days=365)
        sales_data = []

        for day_offset in range(365):
            current_date = start_date + timedelta(days=day_offset)

            daily_sales_count = random.randint(2, 15)
            if current_date.weekday() >= 5:  # Weekend
                daily_sales_count = int(daily_sales_count * 1.5)

            for _ in range(daily_sales_count):
                product = random.choice(products)
                quantity = random.randint(1, 5)

                price_variation = 1 + (random.random() - 0.5) * 0.4
                unit_price = product.price * Decimal(str(price_variation))
                unit_price = unit_price.quantize(Decimal("0.01"))

                sale = Sale(
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_amount=unit_price * quantity,
                    customer_email=random.choice(customer_emails)
                    if random.random() > 0.3
                    else None,
                    platform=random.choice(platforms),
                    order_id=f"ORD-{random.randint(100000, 999999)}",
                    sale_date=current_date
                    + timedelta(
                        hours=random.randint(0, 23), minutes=random.randint(0, 59)
                    ),
                )
                sales_data.append(sale)

        for i in range(0, len(sales_data), 1000):
            batch = sales_data[i : i + 1000]
            db.add_all(batch)
            db.flush()

        db.commit()

        print(f"Database seeded successfully!")
        print(f"Created {len(categories)} categories")
        print(f"Created {len(products)} products")
        print(f"Created {len(inventories)} inventory records")
        print(f"Created {len(sales_data)} sales records")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()
