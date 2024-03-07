from django.db import models
from django.core.files import File
from io import BytesIO
from PIL import Image
from django.contrib.auth.models import User








class Product(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name
    
  

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x240x.jpg'
            

    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'PNG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
    

class Order(models.Model):
    ORDERED = 'ordered'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'

    STATUS_CHOICES = (
        (ORDERED, 'Ordered'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered')
    )

    user = models.ForeignKey(User, related_name='orders', blank=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    state = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    total_cost = models.IntegerField(default=0)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default=ORDERED)

    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return f'{self.user}'
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price =models.IntegerField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.order} - {self.product}'