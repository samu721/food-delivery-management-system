from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import Cart, Menu

cart_router = APIRouter()

@cart_router.post("/add-to-cart/{user_id}/{item_id}")
async def add_to_cart(user_id: int, item_id: int, quantity: int = 1, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Menu).filter(Menu.id == item_id))
    menu_item = result.scalars().first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Item not found")

    cart_item = Cart(user_id=user_id, item_id=item_id, quantity=quantity)
    db.add(cart_item)
    await db.commit()
    return {"message": "Item added to cart"}

@cart_router.get("/cart/{user_id}")
async def get_cart(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cart).filter(Cart.user_id == user_id))
    cart_items = result.scalars().all()
    return cart_items

@cart_router.delete("/cart/remove/{cart_id}")
async def remove_from_cart(cart_id: int, db: AsyncSession = Depends(get_db)):
    cart_item = await db.get(Cart, cart_id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not in cart")
    
    await db.delete(cart_item)
    await db.commit()
    return {"message": "Item removed from cart"}
