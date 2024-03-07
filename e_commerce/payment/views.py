from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Payment
from product.models import Order

from django.http import JsonResponse
from cart.cart import Cart


def verify_payment(request, ref):
    
    try:
        cart = Cart(request)
        payment = Payment.objects.get(ref=ref)
        verified = payment.verify_payment()

        if verified:
            last_order = Order.objects.latest('created_at')
            
            if last_order:
                order = get_object_or_404(Order, pk=last_order.id)
                order.paid = True
                order.save()


                order_info = {
                    'id': order.id,
                    'total_cost': order.total_cost
                }

                context = {
                    'placed_order': order_info,
                    'payment': payment
                }
                cart.clear()
                return render(request, 'core/thankyou.html', context)
            else:
                messages.warning(request, 'Order ID not found')
                return JsonResponse({'error_message': 'Order ID not found'})
        else:
            messages.warning(request, 'Oops, your order was not processed, please contact support.')
            return redirect('/')
    except Payment.DoesNotExist:
        messages.warning(request, 'Payment not found for this ref.')
        return JsonResponse({'error_message': 'Payment not found.'})
