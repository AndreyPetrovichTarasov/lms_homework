import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(course_name):
    """
    Создает продукт на платформе Stripe для курса.
    """
    product = stripe.Product.create(
        name=course_name,
        description="Курс по Django",  # или описание курса
    )
    return product.id


def create_stripe_price(product_id, amount):
    """
    Создает цену на платформе Stripe для продукта.
    Цена передается в копейках.
    """
    price = stripe.Price.create(
        unit_amount=int(amount * 100),  # Преобразуем цену в копейки
        currency="rub",  # Валюта (например, рубли)
        product=product_id,
    )
    return price.id


def create_stripe_checkout_session(price_id, success_url, cancel_url):
    """
    Создает сессию для оплаты через Stripe Checkout.
    """
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session
