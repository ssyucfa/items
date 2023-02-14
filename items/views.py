import stripe
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from items.forms import CreateOrderForm
from items.models import Order
from items.services import create_stripe_session


class CreateOrderView(CreateView):
    form_class = CreateOrderForm
    template_name = "items/create_order.html"

    def get_success_url(self):
        return reverse_lazy("order-detail", args=[self.object.pk])


class CreateDetailView(DetailView):
    model = Order
    template_name = "items/detail_order.html"


def buy_order(request, pk):
    order = get_object_or_404(Order, pk=pk)

    try:
        session_id = create_stripe_session(order)
    except stripe.error.StripeError as e:
        return JsonResponse({"error": str(e)})

    return JsonResponse({"session_id": session_id})
