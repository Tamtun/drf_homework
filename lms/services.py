import stripe
from django.conf import settings
from lms.models import Course

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product(course):
    product = stripe.Product.create(name=course.title)
    course.stripe_product_id = product.id
    course.save()
    return product.id

def create_stripe_price(course):
    price = stripe.Price.create(
        product=course.stripe_product_id,
        unit_amount=int(course.price * 100),
        currency='usd'
    )
    course.stripe_price_id = price.id
    course.save()
    return price.id

def create_checkout_session(course):
    if not course.stripe_product_id:
        create_stripe_product(course)
    if not course.stripe_price_id:
        create_stripe_price(course)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{'price': course.stripe_price_id, 'quantity': 1}],
        mode='payment',
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:8000/cancel',
    )
    return session.url
