# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from core.models import User, Category, Product, Order, OrderItem

# class OrderTests(APITestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(email='user@example.com', password='password123')
#         self.staff_user = User.objects.create_user(email='staff@example.com', password='password123', is_staff=True)
#         self.category = Category.objects.create(name='TestCategory')
#         self.product1 = Product.objects.create(name='Product1', price=10.00, category=self.category)
#         self.product2 = Product.objects.create(name='Product2', price=20.00, category=self.category)
#         self.order = Order.objects.create(user=self.user)
#         self.order_item1 = OrderItem.objects.create(order=self.order, product=self.product1, quantity=1, price=10.00)
#         self.order_item2 = OrderItem.objects.create(order=self.order, product=self.product2, quantity=2, price=40.00)

#     def authenticate_user(self):
#         self.client.login(email='user@example.com', password='password123')

#     def authenticate_staff_user(self):
#         self.client.login(email='staff@example.com', password='password123')

#     def test_create_order(self):
#         self.authenticate_user()
#         url = reverse('orders')
#         data = {
#             "items": [
#                 {"productId": self.product1.id, "quantity": 2},
#                 {"productId": self.product2.id, "quantity": 1}
#             ]
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Order.objects.count(), 2)
#         self.assertEqual(OrderItem.objects.count(), 4)

#     def test_list_orders_as_staff(self):
#         self.authenticate_staff_user()
#         url = reverse('orders')
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)

#     def test_list_orders_as_user(self):
#         self.authenticate_user()
#         url = reverse('orders')
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)

#     def test_retrieve_order(self):
#         self.authenticate_user()
#         url = reverse('order', args=[self.order.id])
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['id'], self.order.id)

#     def test_update_order(self):
#         self.authenticate_user()
#         url = reverse('order', args=[self.order.id])
#         data = {
#             "items": [
#                 {"productId": self.product1.id, "quantity": 3}
#             ]
#         }
#         response = self.client.put(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.order.refresh_from_db()
#         self.assertEqual(self.order.items.first().quantity, 3)

#     def test_delete_order(self):
#         self.authenticate_user()
#         url = reverse('order', args=[self.order.id])
#         response = self.client.delete(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Order.objects.filter(id=self.order.id).exists())
