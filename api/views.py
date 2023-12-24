from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.models import Person, OrderHeader, OrderPart
from api.serializers import PersonSerializer, OrderHeaderSerializer, OrderPartCreateSerializer\
    , OrderHeaderListSerializer, OrderPartSerializer, OrderHeaderGetSerializer


class PersonViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        try:
            person = get_object_or_404(Person, party_id=kwargs.get('pk'))
            serializer = self.serializer_class(person)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Error Occurred', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(self.queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Error Occurred', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Error Occurred', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            person = get_object_or_404(Person, party_id=kwargs.get('pk'))
            serializer = self.serializer_class(person, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Error Occurred', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OrderViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = OrderHeader.objects.all()
    serializer_class = OrderHeaderSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        try:
            order_name = request.data.get('orderName')
            placed_date = request.data.get('placedDate')
            approved_date = request.data.get('approvedDate')
            status_id = request.data.get('statusId', 'OrderPlaced')
            currency_uom_id = request.data.get('currencyUomId', 'USD')
            product_store_id = request.data.get('productStoreId')
            sales_channel_enum_id = request.data.get('salesChannelEnumId')
            grand_total = request.data.get('grandTotal')
            completed_date = request.data.get('completedDate')
            credit_card = request.data.get('creditCard')
            if not order_name or not placed_date:
                return Response({'message': 'Error Occurred', 'error': 'Order Name and Placed Date are mandatory'},
                                status=status.HTTP_400_BAD_REQUEST)
            order_header = OrderHeader.objects.create(
                order_name=order_name,
                placed_date=placed_date,
                approved_date=approved_date,
                status_id=status_id,
                currency_uom_id=currency_uom_id,
                product_store_id=product_store_id,
                sales_channel_enum_id=sales_channel_enum_id,
                grand_total=grand_total,
                completed_date=completed_date,
                credit_card=credit_card
            )
            return Response({'order_id': order_header.order_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': 'Error Occurred', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='order_items')
    def order_items(self, request):
        try:
            serializer = OrderPartCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'order_id': serializer.validated_data.get('order_id'),
                                 'order_part_seq_id': serializer.validated_data.get('order_part_seq_id')},
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Error Occurred', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        try:
            order_header = OrderHeader.objects.all()
            serializer = OrderHeaderListSerializer(order_header, many=True)
            return Response({'orders': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Error Occurred', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            orderHeader = get_object_or_404(OrderHeader, order_id=kwargs.get('pk'))
            serializer = OrderPartSerializer(OrderPart.objects.get(order_id=orderHeader))
            return Response({'orders': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Error Occurred', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            order_id = kwargs.get('pk')
            order_name = request.data.get('orderName')
            orderHeader = get_object_or_404(OrderHeader, order_id=order_id)
            orderHeader.order_name = order_name
            orderHeader.save()
            serializer = OrderHeaderGetSerializer(orderHeader)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Error Occurred', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
