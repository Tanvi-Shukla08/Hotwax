from django.db import models
from django.utils.crypto import get_random_string


class Party(models.Model):
    party_id = models.CharField(max_length=40, primary_key=True)
    party_type_enum_id = models.CharField(max_length=40, blank=True, null=True, default=None)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.party_id}'


class Person(models.Model):
    party_id = models.OneToOneField(Party, on_delete=models.CASCADE, primary_key=True, related_name='person')
    salutation = models.CharField(max_length=255, blank=True, null=True, default=None)
    first_name = models.CharField(max_length=255, blank=True, null=True, default=None)
    middle_name = models.CharField(max_length=255, blank=True, null=True, default=None)
    last_name = models.CharField(max_length=255, blank=True, null=True, default=None)
    gender = models.CharField(max_length=1, blank=True, null=True, default=None)
    birth_date = models.DateField(blank=True, null=True, default=None)
    marital_status_enum_id = models.CharField(max_length=40, blank=True, null=True, default=None)
    employment_status_enum_id = models.CharField(max_length=40, blank=True, null=True, default=None)
    occupation = models.CharField(max_length=255, blank=True, null=True, default=None)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.party_id} - {self.first_name}'


class Product(models.Model):
    product_id = models.CharField(max_length=40, primary_key=True)
    owner_party_id = models.ForeignKey(Party, on_delete=models.SET_NULL, blank=True, null=True, default=None, related_name='products')
    product_name = models.CharField(max_length=255, blank=True, null=True, default=None)
    description = models.CharField(max_length=4095, blank=True, null=True, default=None)
    charge_shipping = models.CharField(max_length=1, blank=True, null=True, default=None)
    returnable = models.CharField(max_length=1, blank=True, null=True, default=None)
    product_type_enum_id = models.CharField(max_length=40, blank=True, null=True, default=None)
    asset_type_enum_id = models.CharField(max_length=40, blank=True, null=True, default=None)
    asset_class_enum_id = models.CharField(max_length=40, blank=True, null=True, default=None)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product_id} - {self.product_name}'


class OrderHeader(models.Model):
    order_id = models.CharField(max_length=40, primary_key=True)
    order_name = models.CharField(max_length=255, blank=True, null=True, default=None)
    placed_date = models.DateTimeField(null=True, blank=True, default=None)
    approved_date = models.DateTimeField(blank=True, null=True, default=None)
    status_id = models.CharField(max_length=40, blank=True, null=True, default=None)
    currency_uom_id = models.CharField(max_length=40, blank=True, null=True, default=None)
    product_store_id = models.CharField(max_length=40, blank=True, null=True, default=None)
    sales_channel_enum_id = models.CharField(max_length=40, blank=True, null=True, default=None)
    grand_total = models.DecimalField(max_digits=24, decimal_places=4, blank=True, null=True, default=None)
    completed_date = models.DateTimeField(null=True, blank=True, default=None)
    credit_card = models.CharField(max_length=255, blank=True, null=True, default=None)


    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = get_random_string(length=6)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.order_id} - {self.order_name}'


class OrderPart(models.Model):
    order_id = models.ForeignKey(OrderHeader, on_delete=models.CASCADE, related_name='order_parts')
    order_part_seq_id = models.CharField(max_length=40, blank=True, null=True, default=None)
    part_name = models.CharField(max_length=255, blank=True, null=True, default=None)
    status_id = models.CharField(max_length=40, blank=True, null=True, default=None)
    vendor_party_id = models.CharField(max_length=40, blank=True, null=True, default=None)
    customer_party_id = models.ForeignKey(Party, on_delete=models.SET_NULL, blank=True, null=True, default=None, related_name='party_order_parts')
    part_total = models.DecimalField(max_digits=24, decimal_places=4, blank=True, null=True, default=None)
    facility_id = models.CharField(max_length=40, blank=True, null=True, default=None)
    shipment_method_enum_id = models.CharField(max_length=40, blank=True, null=True, default=None)

    class Meta:
        unique_together = (('order_id', 'order_part_seq_id'),)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.order_id} - {self.order_part_seq_id}'


class OrderItem(models.Model):
    order_id = models.CharField(max_length=40, db_column='order_id_column')
    order_item_seq_id = models.CharField(max_length=40, db_column='order_item_seq_id_column',blank=True, null=True, default=None)
    order_part_seq_id = models.CharField(max_length=40, blank=True, null=True, default=None,
                                         db_column='order_part_seq_id_column')
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, default=None,
                                   db_column='product_id_column', related_name='product_orders')
    item_description = models.CharField(max_length=255, blank=True, null=True, default=None)
    quantity = models.DecimalField(max_digits=26, decimal_places=6, blank=True, null=True, default=None)
    unit_amount = models.DecimalField(max_digits=25, decimal_places=5, blank=True, null=True, default=None)
    item_type_enum_id = models.CharField(max_length=40, blank=True, null=True, default=None)
    parent_item_seq_id = models.CharField(max_length=40, blank=True, null=True, default=None)

    class Meta:
        unique_together = ('order_id', 'order_item_seq_id')
        db_table = 'order_item'

    def __str__(self):
        return f"{self.order_id} - {self.order_item_seq_id}"
