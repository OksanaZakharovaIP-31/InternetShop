from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .card import Card
from .forms import CardAddProductForm
from coupons.forms import CouponApplyForm

# Create your views here.


@require_POST
def card_add(request, product_id):
    card = Card(request)
    product = get_object_or_404(Product, id=product_id)
    form = CardAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        card.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('card:card_detail')


@require_POST
def card_remove(request, product_id):
    card = Card(request)
    product = get_object_or_404(Product, id=product_id)
    card.remove(product)
    return redirect('card:card_detail')


def card_detail(request):
    card = Card(request)
    for item in card:
        item['update_quantity_form'] = CardAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    coupon_apply_form = CouponApplyForm()
    return render(request, 'card/detail.html',
                  {'card': card,
                   'coupon_apply_form': coupon_apply_form})
