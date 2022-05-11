import json

from django.http import JsonResponse
from django.shortcuts import render
from store.models import Product, Order, OrderItem


def store(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False)
        cart_items = order.get_order_quantity
    else:
        order = {'get_order_quantity': 0, 'get_order_sum': 0}
        cart_items = order['get_order_quantity']

    context = {"products": products,
               'cart_items': cart_items}
    return render(request, 'store/store.html', context)


def checkout(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_order_quantity

    else:
        items = []
        order = {'get_order_sum': 0, 'get_order_quantity': 0, 'shipping': False}
        cart_items = order['get_order_quantity']

    context = {'items': items,
               'order': order,
               'cart_items': cart_items}
    return render(request, 'store/checkout.html', context)


def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_order_quantity
    else:
        items = []
        order = {"get_order_sum": 0, "get_order_quantity": 0}
        cart_items = order['get_order_quantity']
    context = {"items": items,
               "order": order,
               "cart_items": cart_items}
    return render(request, 'store/cart.html', context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = OrderItem.objects.get_or_create(order_id=order, product=product)

    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse("Item was added", safe=False)
