from django.shortcuts import render, get_object_or_404, redirect

from .models import Product, Order, OrderItem
from payment.models import Payment
from django.conf import settings
from cart.cart import Cart
from .forms import AddToCartForm, OrderForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required



          


def product(request, slug):
    cart = Cart(request)
    product = get_object_or_404(Product, slug=slug)

    form = AddToCartForm()

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart.add(product_id=product.id, quantity=quantity, update_quantity=False)
            messages.success(request, 'The product has been added to cart')

        return redirect('product', slug=slug)

    return render(request, 'product/product.html', {'product':product, 'form': form})

@login_required
def start_order(request):
    cart = Cart(request)
    orderItem = []
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            user = request.user
            total_cost = 0
            

            for item in cart:
                product_in_cart = item['product']
                quantity_in_cart = item['quantity']

                product_instance = get_object_or_404(Product, pk=product_in_cart.id)

                order = form.save(commit=False)
                order.user = user
                order.total_cost = product_instance.price * quantity_in_cart

                total_cost += order.total_cost
                order.total_cost = total_cost
                order.save()

                orderItem = OrderItem.objects.create(order=order, 
                                                    product=product_instance, 
                                                    price=product_instance.price * quantity_in_cart, 
                                                    quantity=quantity_in_cart
                                                    )
            payment = Payment.objects.create(amount=total_cost, email=user.email, user=user)
            payment.save()
            pub_key = settings.PAYSTACK_PUBLISHABLE
            
            
            context = {
                'order': order,
                'total_cost': total_cost,
                'orderitem': orderItem,
                'payment': payment,
                'paystack_pub_key': pub_key,
                'amount': payment.amount_value()
            }
            return render(request, 'product/make_payment.html', context)
        else:
            form_errors = form.errors.as_text()
            messages.warning(request, f'Error: Invalid Data. Details: {form_errors}')
            return redirect('start_order')
        

    form = OrderForm()
    context = {'form': form}
    return render(request, 'cart/checkout.html', context)
