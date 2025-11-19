from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    # Check if the product ID (as a string) exists in the cart keys
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False

@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
    # Directly get the value using the string version of the product ID
    # If not found, return 0
    return cart.get(str(product.id), 0)

@register.filter(name='price_total')
def price_total(product, cart):
    return product.price * cart_quantity(product, cart)

@register.filter(name='total_cart_price')
def total_cart_price(products, cart):
    sum = 0
    for p in products:
        sum += price_total(p, cart)
    return sum

@register.filter(name='multiply')
def multiply(number, number1):
    return number * number1