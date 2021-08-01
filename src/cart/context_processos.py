from .models import Cart, CartItems
from .views import _cart_id
from django.core.exceptions import ObjectDoesNotExist

def counter(request):
    cart_count = 0      # var coz counter number on  cart
    if 'admin' in request.path:            # request path if admin can you though data to return see anything
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = CartItems.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_item = 0
    return dict(cart_count=cart_count)

def CartView(request, total=0, quantity=0, tax=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItems.objects.filter(cart=cart)
        for cart_item in cart_items:
            total += (cart_item.product.PRDPrice * cart_item.quantity)
            quantity += cart_item.quantity
            tax += (total) * (cart_item.product.tax)
        total_tex = (total + tax)

    except ObjectDoesNotExist:
        total_tex = (total + tax)

    context = {
        'cart_items': cart_items,
        'quantity': quantity,
        'total': total,
        'tax': tax,
        'total_tex': total_tex,

    }
    return dict (context)
