from enum import StrEnum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Noor Foods Order API")


class OrderStatus(StrEnum):
    PENDING = "pending"
    DELIVERED = "delivered"


class NewOrder(BaseModel):
    customer: str = Field(min_length=2, max_length=120)
    total: int = Field(gt=0)


class Order(BaseModel):
    id: str
    customer: str
    total: int
    status: OrderStatus


ORDERS = {
    "A101": Order(
        id="A101",
        customer="Noor Foods",
        total=4500,
        status=OrderStatus.PENDING,
    ),
    "A102": Order(
        id="A102",
        customer="Bilal Traders",
        total=12800,
        status=OrderStatus.DELIVERED,
    ),
    "A103": Order(
        id="A103",
        customer="Karachi Crafts",
        total=2300,
        status=OrderStatus.PENDING,
    ),
}


@app.get("/")
def read_root() -> dict[str, str]:
    return {"app": "Noor Foods Orders API", "docs": "/docs"}


@app.get("/orders")
def list_orders(
    status: OrderStatus | None = None, limit: int = 10
) -> list[Order]:
    orders = []
    for order in ORDERS.values():
        if status is None or order.status == status:
            orders.append(order)
    return orders[:limit]


@app.get("/orders/{order_id}")
def get_order(order_id: str) -> Order:
    if order_id not in ORDERS:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    return ORDERS[order_id]

@app.post("/orders", status_code=201)
def create_order(new_order: NewOrder) -> Order:
    order_id = f"A{101 + len(ORDERS)}"
    order = Order(
        id=order_id,
        customer=new_order.customer,
        total=new_order.total,
        status=OrderStatus.PENDING,
    )
    ORDERS[order_id] = order
    return order
