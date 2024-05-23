from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField('Title', max_length=120)
    description = models.TextField('Description')
    price = models.FloatField('Price')
    image = models.ImageField('Project image', upload_to='product_images')

    def __str__(self):
        return f'{self.title} - ${self.price}'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_ids = models.TextField('Product IDs')

    def __str__(self):
        return f'{self.user.username} cart'

    @property
    def get_full_price(self):
        product_ids = self.product_ids.split()
        products = [Product.objects.get(id=id) for id in product_ids]
        return sum([p.price for p in products])

    @property
    def get_quantity(self):
        return len(self.product_ids.split())


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    company_name = models.CharField('Company', max_length=120)
    country = models.CharField('Country', max_length=120)
    address = models.CharField('Address', max_length=120)
    town = models.CharField('Town', max_length=120)
    zip_code = models.CharField('ZIP Code', max_length=120)
    phone = models.CharField('Phone', max_length=120)
    comment = models.TextField('Comment')

    def __str__(self):
        return f'Order by {self.cart.user.username}'
