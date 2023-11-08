from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct
from collections import OrderedDict


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']
        

class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price']
        


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']
        
        
    def create(self, validated_data):
        
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)

        for i in positions:
            d = dict(i)
            StockProduct.objects.create(
                product = d['product'],
                quantity = d['quantity'],
                price = d['price'],
                stock = stock
                )

        return stock

    def update(self, instance, validated_data):

        position = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        
        for i in position:
            product = position.get('product')
            quantity = position.get('quantity')
            price = position.get('price')
            StockProduct.objects.update_or_create(
                product = product,
                stock = stock,
                defaults={'quantity':quantity,
                          'price':price
                }
                )

        return stock
