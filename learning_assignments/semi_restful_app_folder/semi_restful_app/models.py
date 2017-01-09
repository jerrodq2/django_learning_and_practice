from __future__ import unicode_literals

from django.db import models

class PManager(models.Manager):
    def createProduct(self, data):
        errors = []
        if len(data['name']) == 0:
            errors.append('Name cannot be blank')
        if len(data['description']) == 0:
            errors.append('Description cannot be blank')
        if len(data['price']) == 0:
            errors.append('Price cannot be blank')
        try:
            float(data['price'])
        except:
            errors.append('Price must be a number')
        if errors:
            return {'errors': errors}
        prod = Product.PManager.create(name=data['name'], description=data['description'], price=data['price'])
        try:
            prod.save()
        except:
            return {'errors': ['There was an error']}
        return

    def updateProduct(self, data, id):
        errors = []
        if len(data['name']) == 0:
            errors.append('Name cannot be blank')
        if len(data['description']) == 0:
            errors.append('Description cannot be blank')
        if len(data['price']) == 0:
            errors.append('Price cannot be blank')
        try:
            float(data['price'])
        except:
            errors.append('Price must be a number')
        if errors:
            return {'errors': errors}
        try:
            product = Product.PManager.get(pk=id)
        except:
            return {'errors': ['Product not found']}
        product.name = data['name']
        product.description = data['description']
        product.price = data['price']
        try:
            product.save()
        except:
            return {'errors': ['There was an error']}
        return

    def destroyProduct(self, id):
        try:
            product = Product.PManager.get(pk=id)
        except:
            return 'Product not found'
        product.delete()
        return

class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    PManager = PManager()
