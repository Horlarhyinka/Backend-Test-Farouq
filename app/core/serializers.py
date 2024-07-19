from rest_framework import serializers
from .models import User, Category, Product

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = '__all__'
# from rest_framework import serializers
# from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    categoryId = serializers.IntegerField(write_only=True, source='category.id')
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['name', 'price', 'categoryId', 'category']

    def create(self, validated_data):
        category_id = validated_data.pop('category')['id']
        category = Category.objects.get(id=category_id)
        product = Product.objects.create(category=category, **validated_data)
        return product
