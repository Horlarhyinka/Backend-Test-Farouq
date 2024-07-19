from rest_framework import serializers
from .models import User, Category, Product, Order, OrderItem

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'cover']

class ProductSerializer(serializers.ModelSerializer):
    categoryId = serializers.IntegerField(write_only=True, source='category.id')
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['name', 'price', 'categoryId', 'category', 'id']

    def create(self, validated_data):
        category_id = validated_data.pop('category')['id']
        category = Category.objects.get(id=category_id)
        product = Product.objects.create(category=category, **validated_data)
        return product
    def update(self, instance, validated_data):
            category_id = validated_data.pop('category')['id']
            category = Category.objects.get(id=category_id)
            instance.name = validated_data.get('name', instance.name)
            instance.price = validated_data.get('price', instance.price)
            instance.category = category
            instance.save()
            return instance
    
class OrderItemSerializer(serializers.ModelSerializer):
    productId = serializers.IntegerField(write_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['productId', 'product', 'quantity']

    def create(self, validated_data):
        product_id = validated_data.pop('productId')
        product = Product.objects.get(id=product_id)
        validated_data['product'] = product
        validated_data['price'] = validated_data['quantity'] * product.price
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'items', "status"]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            item_data['order'] = order
            OrderItemSerializer().create(item_data)
        return order