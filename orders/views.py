from urllib.parse import quote

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Order

PLAN_PRICES = {
    "classic": 45000,
    "family": 95000,
    "premium": 65000,
}

PLAN_LABELS = {
    "classic": "Clásica",
    "family": "Familiar",
    "premium": "Premium",
}


@login_required
def plans_view(request):
    return render(request, "orders/plans.html", {"plan_prices": PLAN_PRICES})


@login_required
def create_order_view(request, plan):
    if plan not in PLAN_PRICES:
        return redirect("orders:plans")
    order = Order.objects.create(user=request.user, plan=plan, amount=PLAN_PRICES[plan])
    return redirect("orders:checkout", order_id=order.id)


@login_required
def checkout_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.payment_status == "paid":
        return redirect("orders:confirmation", order_id=order.id)

    message = (
        f"Hola, quiero confirmar el pago de mi placa IDPetScan.\n"
        f"Plan: {order.get_plan_display()}\n"
        f"Valor: ${order.amount}\n"
        f"Código de orden: {order.reference}\n"
        f"Usuario: {request.user.username}"
    )
    whatsapp_url = f"https://wa.me/{settings.WHATSAPP_BUSINESS_NUMBER}?text={quote(message)}"

    return render(request, "orders/checkout.html", {"order": order, "whatsapp_url": whatsapp_url})


@login_required
def confirmation_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/confirmation.html", {"order": order})