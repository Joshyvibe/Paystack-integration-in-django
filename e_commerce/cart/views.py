from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .cart import Cart

from product.models import Product

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return redirect('shop')

def cart(request):
    return render(request, 'cart/cart.html')



def update_cart(request, product_id):
    cart = Cart(request)
    action = request.GET.get('action')
    quantity = int(request.GET.get('quantity', 1))

    if action == 'increment':
        cart.add(product_id, quantity, True)
        
        return redirect('cart')
    elif action == 'decrement':
        cart.add(product_id, -quantity, True)
        
        return redirect('cart')
    elif action == 'remove':
        cart.remove(product_id)
        
        return redirect('cart')
    
    product = Product.objects.get(pk=product_id)
    quantity = cart.get_item(product_id)
    
    if quantity:
        quantity = quantity['quantity']

        item = {
            'product': {
                'id': product.id,
                'name': product.name,
                'image': product.image,
                'get_thumbnail': product.get_thumbnail(),
                'price': product.price,
            },
            'total_price': (quantity * product.price),
            'quantity': quantity,
        }
    else:
        item = None

    response = render(request, 'cart/components/cart_item.html', {'item': item})
   

    return response