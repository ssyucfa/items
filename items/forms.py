from django import forms

from items.models import Order, Item
from items.services import add_random_discount, add_random_tax


class CreateOrderForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(required=True, queryset=Item.objects.all())

    class Meta:
        model = Order
        exclude = ("total_price", )

    def save(self, commit=True):
        order = super().save(commit=False)

        total_price = sum(item.price for item in self.cleaned_data["items"])

        order.set_total_price(total_price, commit=False)

        # Creating order in db
        order.save()
        self._save_m2m()

        add_random_discount(order)
        add_random_tax(order)

        return order
