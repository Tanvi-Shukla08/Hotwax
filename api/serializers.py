from rest_framework import serializers

from api.models import Person, OrderHeader, OrderPart, OrderItem, Party, Product


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class OrderHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHeader
        exclude = ('order_id',)


class OrderItemCreateSerializer(serializers.Serializer):
    orderId = serializers.CharField(source='order_id', required=False)
    orderItemSeqId = serializers.CharField(source='order_item_seq_id', required=False)
    orderPartSeqId = serializers.CharField(source='order_part_seq_id', required=False)
    productId = serializers.CharField(source='product_id')
    itemDescription = serializers.CharField(source='item_description', required=False)
    quantity = serializers.DecimalField(max_digits=26, decimal_places=6)
    unitAmount = serializers.DecimalField(source='unit_amount', max_digits=25, decimal_places=5)
    itemTypeEnumId = serializers.CharField(source='item_type_enum_id', required=False)
    parentItemSeqId = serializers.CharField(source='parent_item_seq_id', required=False)




class OrderPartCreateSerializer(serializers.Serializer):
    orderId = serializers.CharField(source='order_id', required=False)
    partName = serializers.CharField(source='part_name', required=False)
    orderPartSeqId = serializers.CharField(source='order_part_seq_id', required=False)
    statusId = serializers.CharField(source='status_id', required=False)
    vendorPartyId = serializers.CharField(source='vendor_party_id', required=False)
    customerPartyId = serializers.CharField(source='customer_party_id', required=False)
    partTotal = serializers.DecimalField(source='part_total', max_digits=24, decimal_places=4, required=False)
    facilityId = serializers.CharField(source='facility_id', required=False)
    shipmentMethodEnumId = serializers.CharField(source='shipment_method_enum_id', required=False,
                                                 default='ShMthGround')
    item_details = OrderItemCreateSerializer(many=True, required=True)

    def create(self, validated_data):
        item_details_data = validated_data.pop('item_details', [])
        
        order_id = validated_data.get('order_id')
        
        order_header_instance = OrderHeader.objects.get(order_id=order_id)
        validated_data.pop('order_id')
        customer_party_id = validated_data.get('customer_party_id')
        party_instance = Party.objects.get(party_id=customer_party_id)
        validated_data.pop('customer_party_id')
        
        order_part = OrderPart.objects.create(
            order_id=order_header_instance,
            customer_party_id=party_instance,
            **validated_data
        )
        for item_data in item_details_data:
            product_id = item_data.get('product_id')
            product_instance = Product.objects.get(product_id=product_id)
            item_data.pop('product_id')
            OrderItem.objects.create(order_id=order_header_instance, product_id=product_instance, **item_data)

        return order_part


class PersonGetSerializer(serializers.ModelSerializer):
    customerPartyId = serializers.CharField(source='party_id')
    firstName = serializers.CharField(source='first_name')
    middleName = serializers.CharField(source='middle_name')
    lastName = serializers.CharField(source='last_name')

    class Meta:
        model = Person
        fields = ('customerPartyId', 'firstName', 'middleName', 'lastName')


class OrderItemGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('order_item_seq_id', 'product_id', 'item_description', 'quantity', 'unit_amount')


class OrderPartGetSerializer(serializers.ModelSerializer):
    item_details = serializers.SerializerMethodField()

    class Meta:
        model = OrderPart
        fields = ('order_part_seq_id', 'part_name', 'facility_id', 'shipment_method_enum_id', 'status_id', 'part_total',
                  'item_details')

    def get_item_details(self, obj):
        return OrderItemGetSerializer(OrderItem.objects.filter(order_id=obj.order_id), many=True).data


class OrderHeaderListSerializer(serializers.ModelSerializer):
    order_parts = serializers.SerializerMethodField()
    customer_details = serializers.SerializerMethodField()

    class Meta:
        model = OrderHeader
        fields = (
            'order_id', 'order_name', 'currency_uom_id', 'sales_channel_enum_id', 'status_id', 'placed_date',
            'grand_total', 'customer_details', 'order_parts')

    def get_customer_details(self, obj):
        if obj.order_parts.first():
            return PersonGetSerializer(Person.objects.get(party_id=obj.order_parts.first().customer_party_id)).data
        return None

    def get_order_parts(self, obj):
        return OrderPartGetSerializer(OrderPart.objects.filter(order_id=obj.order_id), many=True).data


class OrderPartSerializer(serializers.ModelSerializer):
    item_details = serializers.SerializerMethodField()

    class Meta:
        model = OrderPart
        fields = ('order_id', 'part_name', 'facility_id', 'shipment_method_enum_id', 'customer_party_id', 'item_details')

    def get_item_details(self, obj):
        return OrderItemGetSerializer(OrderItem.objects.filter(order_id=obj.order_id), many=True).data


class OrderHeaderGetSerializer(serializers.ModelSerializer):
    approved_date=serializers.SerializerMethodField()
    placed_date=serializers.SerializerMethodField()
    class Meta:
        model = OrderHeader
        fields = ('order_id', 'order_name', 'currency_uom_id', 'sales_channel_enum_id', 'status_id', 'product_store_id',
                  'placed_date', 'approved_date', 'grand_total')
    def get_approved_date(self,obj):
        return obj.approved_date.date() if obj.approved_date else None
    def get_placed_date(self,obj):
        return obj.placed_date.date() if obj.placed_date else None