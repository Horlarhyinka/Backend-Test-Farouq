"""Manage admin page for main app."""

from django.contrib import admin
from .models import User, Product, Category
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
