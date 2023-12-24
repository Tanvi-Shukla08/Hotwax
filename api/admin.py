from django.contrib import admin
from import_export.admin import ExportActionModelAdmin

from api.models import Party, Person, Product, OrderHeader, OrderPart, OrderItem


# Register your models here.
@admin.register(Party)
class PartyAdmin(ExportActionModelAdmin):
    list_filter = ('party_id', 'party_type_enum_id', )
    search_fields = ('party_id', 'party_type_enum_id', )
    list_display = ('party_id', 'party_type_enum_id',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('party_id', 'first_name', 'last_name', 'gender', 'birth_date', 'marital_status_enum_id',
                    'employment_status_enum_id', 'occupation')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'owner_party_id', 'product_name', 'charge_shipping', 'returnable')


@admin.register(OrderHeader)
class OrderHeaderAdmin(admin.ModelAdmin):
    list_display = (
    'order_id', 'order_name', 'placed_date', 'approved_date', 'status_id', 'currency_uom_id', 'product_store_id',
    'sales_channel_enum_id', 'grand_total', 'completed_date', 'credit_card')
    search_fields = ('order_id', 'order_name')


@admin.register(OrderPart)
class OrderPartAdmin(admin.ModelAdmin):
    list_display = (
    'order_id', 'order_part_seq_id', 'part_name', 'status_id', 'vendor_party_id', 'customer_party_id', 'part_total',
    'facility_id', 'shipment_method_enum_id')
    search_fields = ('order_id__order_id', 'part_name')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
    'order_id', 'order_item_seq_id', 'order_part_seq_id', 'product_id', 'item_description', 'quantity', 'unit_amount',
    'item_type_enum_id', 'parent_item_seq_id')
    search_fields = ('order_id__order_id', 'item_description')


