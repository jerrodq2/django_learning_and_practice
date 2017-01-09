from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import Product

def index(request):
    products = Product.PManager.all()
    return render(request, 'semi/index.html', {'products': products})

def new(request):
    return render(request, 'semi/new.html')

def create(request):
    if request.method != 'POST':
        return redirect(reverse('semi:index'))
    product = Product.PManager.createProduct(request.POST)
    if product:
        for i in product['errors']:
            messages.info(request, i)
        return redirect(reverse('semi:new'))
    return redirect(reverse('semi:index'))

def show(request, id):
    product = Product.PManager.filter(pk=id)
    if len(product) == 0:
        return redirect(reverse('semi:index'))
    return render(request, 'semi/show.html', {'product': product[0]})

def edit(request, id):
    product = Product.PManager.filter(pk=id)
    if len(product) == 0:
        return redirect(reverse('semi:index'))
    return render(request, 'semi/edit.html', {'product': product[0]})

def update(request, id):
    if request.method != 'POST':
        return redirect(reverse('semi:index'))
    product = Product.PManager.updateProduct(request.POST, id)
    if product:
        for i in product['errors']:
            messages.info(request, i)
        return redirect(reverse('semi:edit', kwargs={'id': id}))
    return redirect(reverse('semi:edit', kwargs={'id': id}))

def destroy(request, id):
    product = Product.PManager.destroyProduct(id)
    return redirect(reverse('semi:index'))
