from django.db import models
from django.utils.translation import gettext_lazy as _

class CartItem(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(_('quantity'))
    subtotal = models.DecimalField(_('Subtotal'), max_digits=10, decimal_places=2)  # ✅ To‘g‘rilandi

    def __str__(self):
        return f"User ID: {self.user.id}| Product ID: {self.product.id}"

class Card(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='cards')
    name_on_card = models.CharField(_("Name on card"), max_length=120)
    card_number = models.CharField(_("Card number"), max_length=16)
    cvv = models.CharField(_("CVV"), max_length=3)
    expiration_date = models.DateField(_("Expiration date"))

    def __str__(self):
        return f"User ID: {str(self.user.id)}| Card Number: {self.card_number}"

class Discount(models.Model):
    code = models.CharField(_("Code"), max_length=60)
    max_limit_price = models.FloatField(_("Max limit price"))
    percentage = models.FloatField(_("Percentage"))
    start_date = models.DateTimeField(_("Start date"))
    end_date = models.DateTimeField(_("End date"))
    is_active = models.BooleanField(_("Is active"))

    def __str__(self):
        return f"Code: {self.code}| Max limit price: {self.max_limit_price}"

class Branch(models.Model):
    name = models.CharField(_("Name"), max_length=120)
    regions = models.ForeignKey('common.Region', on_delete=models.CASCADE, related_name='branches')
    zip_code = models.CharField(_("Zip code"), max_length=10)
    street = models.CharField(_("Street"), max_length=120)
    address = models.CharField(_("Address"), max_length=120)
    longitude = models.FloatField(_("Longitude"))
    latitude = models.FloatField(_("Latitude"))

    def __str__(self):
        return f"Name: {self.name}| Region: {self.regions}"

class DeleveryTarif(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='delevery_tarifs')
    high = models.FloatField(_("High"))
    width = models.FloatField(_("Width"))
    weight = models.FloatField(_("Weight"))
    price = models.FloatField(_("Price"))
    regions = models.ForeignKey('common.Region', on_delete=models.CASCADE, related_name='delevery_tarifs')
    delivery_time = models.TimeField(_("Delivery time"))

    def __str__(self):
        return f"Branch: {self.branch}| Price: {self.price}"

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        CREATED = 'created', _('Created')
        IN_PROGRESS = 'in_progress', _('In progress')
        DELIVERED = 'delivered', _('Delivered')
        CANCELLED = 'cancelled', _('Cancelled')
        FINISHED = 'finished', _('Finished')

    class PaymentStatus(models.TextChoices):
        CREATED = 'created', _('Created')
        PENDING = 'pending', _('Pending')
        PAID = 'paid', _('Paid')
        CANCELLED = 'cancelled', _('Cancelled')

    class PaymentMethod(models.TextChoices):
        CASH = 'cash', _('Cash')
        PAYME = 'payme', _('Payme')
        CLICK = 'click', _('Click')

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(_("Status"), max_length=60, choices=OrderStatus.choices)
    items = models.ManyToManyField(CartItem, related_name='orders')
    total_price = models.FloatField(_("Total price"))
    address = models.ForeignKey('accounts.UserAddress', on_delete=models.CASCADE, related_name='orders')
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    payment_status = models.CharField(_("Payment status"), max_length=60, choices=PaymentStatus.choices)
    payment_method = models.CharField(_("Payment method"), max_length=60, choices=PaymentMethod.choices)
    delevery_tarif = models.ForeignKey(DeleveryTarif, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')

    def __str__(self):
        return f"User ID: {self.user.id}| Status: {self.status}"