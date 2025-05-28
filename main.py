from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models import Base
from routers import categories, health, inventory, products, sales

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Forsit E-Commerce Admin API",
    description="API for e-commerce admin with sales, inventory and low stock management",
)

# Just allowing all origins for debug environment. Must update it if this is to be deployed to prod.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Using routers for better organization of APIs
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(sales.router)
app.include_router(inventory.router)
app.include_router(health.router)
