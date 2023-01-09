from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Collection, Product
from .serializers import CollectionSerializer, ProductSerializer


class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()

    # def get_serializer_class(self):
    #     return ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    # def get(self, request):
    #     queryset = Product.objects.select_related('collection').all()
    #     serializer = ProductSerializer(
    #         queryset, many=True, context={'request': request})
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = ProductSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, pk):
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    # def get(self, request):
    #     queryset = Collection.objects.annotate(
    #         products_count=Count('products')).all()
    #     serializer = CollectionSerializer(queryset, many=True)
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = CollectionSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
