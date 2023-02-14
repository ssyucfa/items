import decimal

from django.core.exceptions import ValidationError
from django.db import models

MIN_PRICE = 1


def validate_min(value):
    if value < MIN_PRICE:
        raise ValidationError(
            f"%(value)s is less than {MIN_PRICE}",
            params={"value": value},
        )


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_min])

    def __str__(self):
        return self.name


class Order(models.Model):
    class CurrencyChoices(models.TextChoices):
        USD = "usd", "USD"
        RUB = "cad", "CAD"

    items = models.ManyToManyField(Item)
    total_price = models.DecimalField(max_digits=11, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CurrencyChoices.choices, default=CurrencyChoices.RUB)

    def set_total_price(self, total_price: decimal.Decimal, *, commit: bool = True) -> None:
        self.total_price = total_price

        if commit:
            self.save(update_fields=["total_price"])

    def add_tax(self, *, commit: bool = True) -> None:
        if self.tax is None:
            return

        total_price = self.total_price + self.total_price / 100 * self.tax.percentage
        self.set_total_price(total_price, commit=commit)

    def add_discount(self, *, commit: bool = True) -> None:
        if self.discount is None:
            return

        total_price = self.total_price - self.total_price / 100 * self.discount.percentage
        self.set_total_price(total_price, commit=commit)

    def __str__(self):
        return f"Order: {self.total_price}"


class Discount(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Order discount: {self.order_id}"


class Tax(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Order tax: {self.order_id}"
