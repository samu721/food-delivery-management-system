from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Cart, Order, OrderItem, Menu
from database import get_db

checkout_router = APIRouter()

@checkout_router.post("/checkout/{user_id}")
async def checkout(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cart).filter(Cart.user_id == user_id))
    cart_items = result.scalars().all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_price = sum(item.quantity * item.item.price for item in cart_items)

    new_order = Order(user_id=user_id, total_price=total_price)
    db.add(new_order)
    await db.commit()

    for item in cart_items:
        order_item = OrderItem(order_id=new_order.id, item_id=item.item_id, quantity=item.quantity)
        db.add(order_item)
        await db.delete(item)

    await db.commit()
    return {"message": "Order placed successfully", "order_id": new_order.id}
