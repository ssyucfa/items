import random

import stripe
from django.conf import settings

from items.models import Discount, Order, Tax

RANDOM_TAX_PERCENTAGE = [1, 2, 3, 4, 5, 6]
RANDOM_DISCOUNT_PERCENTAGE = [0, 2, 3, 4, 5, 6]

stripe.api_key = settings.STRIPE_API_KEY


def add_random_tax(order: Order) -> Tax:
    tax = Tax.objects.create(order=order, percentage=random.choice(RANDOM_TAX_PERCENTAGE))
    order.add_tax()

    return tax


def add_random_discount(order: Order) -> Discount:
    discount = Discount.objects.create(order=order, percentage=random.choice(RANDOM_DISCOUNT_PERCENTAGE))
    order.add_discount()

    return discount


def create_stripe_session(order: Order) -> int:
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": order.currency,
                    "unit_amount": int(order.total_price * 100),
                    "product_data": {
                        "name": f"Order {order.id}",
                    },
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
    )
    return session.id
