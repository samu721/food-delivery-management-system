from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from cart import cart_router
from checkout import checkout_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cart_router, prefix="/cart")
app.include_router(checkout_router, prefix="/checkout")
