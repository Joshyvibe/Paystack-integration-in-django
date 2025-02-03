from django.conf import settings

from product.models import Product

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart
        # It first checks if there's an existing cart in the session.
        # If not, it creates an empty cart in the session. 
        # The cart is stored in the self.cart attribute for further use.
    
    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)
        
        for item in self.cart.values():
            item['total_price'] = int(item['product'].price * item['quantity'])

            yield item
        #This method makes the Cart class iterable, meaning you can loop through the items in the cart using a for loop.
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
        # This method returns the total number of items in the cart.
    
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
        #  This method saves the cart back to the user's session after making changes.
    def add(self, product_id, quantity=1, update_quantity=False):
        # This method is used to add products to the cart.
        product_id = str(product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'id': product_id}
        
        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)

            if self.cart[product_id]['quantity'] == 0:
                self.remove(product_id)
            
        self.save()
    
    def remove(self, product_id):
        product_id = str(product_id)  # Ensure data type compatibility
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()  # Ensure cart data is saved to the session

        #  This method removes a product from the cart based on its product_id.
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
        # This method clears the entire cart by deleting it from the session.
    
    def get_total_cost(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

        return int(sum(item['product'].price * item['quantity'] for item in self.cart.values()))
    # This method calculates the total cost of all items in the cart.
    
    def get_item(self, product_id):
        if str(product_id) in self.cart:
            return self.cart[str(product_id)]
        else:
            return None
    # This method retrieves an item from the cart based on its product_id and returns it
